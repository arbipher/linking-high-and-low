import json
from pathlib import Path
import itertools
import subprocess
import re
from collections import defaultdict

# Modes
lib_modes = ["default", "at_exe", "at_loader", "at_rpath"]
bin_modes = ["default", "at_exe", "at_loader", "at_rpath"]

# To confirm
# @executable: center to App bundle's binary. Absolute position.
#    Agreeing on using @executable in rpath, the libraries are almost owned by the binary
# @loader: center to entry library. Relative position
#    Agreeing on using @loader in rpath, the rest libraries are owned by the entry library
# @rpath: Multiple spines
#       Multi-to-multi

# Platform-aware build root
platform = "macos"
build_root = Path("build") / platform
libadd_dir = build_root / "libadd"
libsum_dir = build_root / "libsum"
bin_dir = build_root / "bin"
libadd_dir.mkdir(parents=True, exist_ok=True)
libsum_dir.mkdir(parents=True, exist_ok=True)
bin_dir.mkdir(parents=True, exist_ok=True)

results_path = build_root / "results.json"

# Install name settings with full relative paths for libadd
add_install_names = {
    "default": "",
    "at_exe": f"-install_name @executable_path/../{libadd_dir.name}/libadd_at_exe.dylib",
    "at_loader": f"-install_name @loader_path/../{libadd_dir.name}/libadd_at_loader.dylib",
    "at_rpath": "-install_name @rpath/libadd_at_rpath.dylib",
}

# Function to generate libsum install_name dynamically
def get_sum_install_name(sum_mode: str, sum_out_path: Path):
    if sum_mode == "default":
        return ""
    elif sum_mode == "at_exe":
        return f"-install_name @executable_path/../{libsum_dir.name}/{sum_out_path.name}"
    elif sum_mode == "at_loader":
        return f"-install_name @loader_path/../{libsum_dir.name}/{sum_out_path.name}"
    elif sum_mode == "at_rpath":
        return f"-install_name @rpath/{sum_out_path.name}"
    else:
        raise ValueError(f"Unknown sum_mode: {sum_mode}")

# Bin rpath settings
bin_rpaths = {
    "default": "",
    "at_exe": f"-Wl,-rpath,@executable_path/../{libsum_dir.name}",
    "at_loader": f"-Wl,-rpath,@loader_path/../{libsum_dir.name}",
    "at_rpath": "-Wl,-rpath,@rpath",
}

# Function to convert libsum*.dylib to correct -l flag
def dylib_to_libname(name: str) -> str:
    assert name.startswith("lib") and name.endswith(".dylib")
    return name[3:-6]

# Simplify reason for missing library
def simplify_reason(lib: str) -> str:
    if "libadd" in lib:
        return "@rpath/libadd...dylib"
    elif "libsum" in lib:
        return "@rpath/libsum...dylib"
    return lib

if results_path.exists():
    print("📦 Using cached results from previous run.")
    with open(results_path) as f:
        results = json.load(f)
else:
    # Build libadd
    for add_mode in lib_modes:
        out_path = libadd_dir / f"libadd_{add_mode}.dylib"
        log_path = out_path.with_suffix(".log")
        if not out_path.exists() or not log_path.exists():
            cmd = f"clang -dynamiclib -fPIC libadd/libadd.c -o {out_path} {add_install_names[add_mode]}"
            with open(log_path, "w") as f:
                subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)
                subprocess.run(f"otool -L {out_path}", shell=True, stdout=f, stderr=subprocess.STDOUT)

    # Build libsum
    for sum_mode, add_mode in itertools.product(lib_modes, lib_modes):
        out_path = libsum_dir / f"libsum_{sum_mode}_with_add_{add_mode}.dylib"
        log_path = out_path.with_suffix(".log")
        if not out_path.exists() or not log_path.exists():
            add_lib = f"-L{libadd_dir} -ladd_{add_mode}"
            install_flag = get_sum_install_name(sum_mode, out_path)
            cmd = f"clang -dynamiclib -fPIC libsum/libsum.c -o {out_path} {add_lib} {install_flag}"
            with open(log_path, "w") as f:
                subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)
                subprocess.run(f"otool -L {out_path}", shell=True, stdout=f, stderr=subprocess.STDOUT)

    # Run bin cases with caching and result tracking
    results = []
    combinations = list(itertools.product(lib_modes, lib_modes, bin_modes))
    for idx, (add_mode, sum_mode, bin_mode) in enumerate(combinations):
        sum_libname = f"libsum_{sum_mode}_with_add_{add_mode}.dylib"
        sum_libpath = libsum_dir / sum_libname
        bin_out = bin_dir / f"{idx:02d}_bin_{bin_mode}_sum_{sum_mode}_add_{add_mode}"
        log_path = bin_out.with_suffix(".log")

        # Try to build
        rpath_flag = bin_rpaths[bin_mode]
        lib_flag = dylib_to_libname(sum_libname)
        cmd = f"clang bin/main.c -o {bin_out} -L{libsum_dir} -l{lib_flag} {rpath_flag}"
        try:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            log_path.write_text(e.stderr.decode())
            results.append({"id": idx, "bin": bin_out.name, "status": "build_error", "error": e.stderr.decode(), "add": add_mode, "sum": sum_mode, "binmode": bin_mode, "reason": ""})
            continue

        # Run with fallback logic based on missing library analysis
        run_success = False
        tried_paths = []
        dyld_env = ""
        for _ in range(3):
            env = {"DYLD_LIBRARY_PATH": dyld_env} if dyld_env else None
            proc = subprocess.run([str(bin_out), "10"], capture_output=True, text=True, env=env)
            log_path.write_text(proc.stdout + proc.stderr)
            if proc.returncode == 0 and "Sum from" in proc.stdout:
                results.append({"id": idx, "bin": bin_out.name, "status": "success", "add": add_mode, "sum": sum_mode, "binmode": bin_mode, "reason": ""})
                run_success = True
                break

            m = re.search(r"Library not loaded: (.*?)\n", proc.stderr)
            reason = m.group(1) if m else ""
            results.append({"id": idx, "bin": bin_out.name, "status": "loading_error", "error": proc.stderr, "add": add_mode, "sum": sum_mode, "binmode": bin_mode, "reason": simplify_reason(reason)})

            if not m:
                break
            missing = m.group(1)
            if "libadd" in missing and str(libadd_dir) not in tried_paths:
                tried_paths.append(str(libadd_dir))
            elif "libsum" in missing and str(libsum_dir) not in tried_paths:
                tried_paths.append(str(libsum_dir))
            else:
                break
            dyld_env = ":".join(tried_paths)

        if not run_success:
            results.append({"id": idx, "bin": bin_out.name, "status": "loading_error", "error": proc.stderr, "add": add_mode, "sum": sum_mode, "binmode": bin_mode, "reason": simplify_reason(reason)})

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📝 Results cached to {results_path}")

# Summary printer
def summarize_results(results):
    print("\n📋 Execution Results:")
    for r in results:
        status = r["status"]
        icon = "✅" if status == "success" else "❌" if status == "loading_error" else "🔨"
        msg = f"{icon} {r['bin']}"
        if status != "success":
            simplified = re.search(r"dyld(?:\[\d+\])?: Library not loaded: (.*?)\n", r.get("error", ""))
            if simplified:
                msg += f" — dyld: {simplified.group(1)}"
            else:
                msg += f" — {r.get('error', '').splitlines()[0] if r.get('error') else ''}"
        print(msg)

    print("\n🧪 Observations:")

    for rpath_count in (1, 2):
        count = sum(1 for r in results if r['status'] == 'loading_error' and [r['add'], r['sum']].count('at_rpath') == rpath_count)
        print(f"❌ {rpath_count} @rpath error(s): {count} cases")

    from collections import defaultdict
    from itertools import combinations

    # Map: (add_mode, sum_mode, binmode) → list of all (status, reason) tuples
    detailed_grouped = defaultdict(list)

    for r in results:
        key = (r["add"], r["sum"], r["binmode"])
        reason = r.get("reason", "") if r["status"] == "loading_error" else ""
        detailed_grouped[key].append((r["status"], simplify_reason(reason)))

    print("\n🔍 Checking if binmode result distributions are equivalent per (add, sum):")

    # Group by just (add, sum)
    dist_grouped = defaultdict(dict)
    for (add, sum_, binmode), result_list in detailed_grouped.items():
        dist_grouped[(add, sum_)][binmode] = result_list

    for (add, sum_), bm_results in dist_grouped.items():
        all_distributions = list(bm_results.items())
        mismatch = False

        for (bm1, r1), (bm2, r2) in combinations(all_distributions, 2):
            if r1 != r2:
                print(f"❌ add={add}, sum={sum_} → {bm1} ≠ {bm2}")
                print(f"    {bm1}: {r1}")
                print(f"    {bm2}: {r2}")
                mismatch = True
                break

        if not mismatch:
            print(f"✅ add={add}, sum={sum_} → same: {all_distributions[0][1]}")


    table_path = build_root / "result_table.md"
    with open(table_path, "w") as f:
        f.write("| Id | Add | Sum | BinMode | Status | Reason |\n")
        f.write("|----|-----|-----|---------|--------|--------|\n")
        for r in results:
            color_status = {
                "success": "✅ success",
                "loading_error": "❌ loading_error",
                "build_error": "🔨 build_error",
            }[r["status"]]
            f.write(f"| {r['id']:02d} | {r['add']} | {r['sum']} | {r['binmode']} | {color_status} | {r.get('reason', '')} |\n")
    print(f"\n📄 Result table written to {table_path}")

summarize_results(results)