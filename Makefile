define show_needed
	@echo "Shared library dependencies of $(1):"; \
	readelf -d $(1) | grep NEEDED || echo "No NEEDED entries found"
endef

define show_runpath
	@echo "Runpath / Rpath of $(1):"; \
	readelf -d $(1) | grep -E 'RUNPATH|RPATH' || echo "No RUNPATH or RPATH found"
endef

define show_symbols
	@echo "Dynamic symbols in $(1):"; \
	nm -D $(1) || echo "No dynamic symbols found"
endef

libadd.so: libadd/libadd.c
	gcc -shared -fPIC -o libadd/libadd.so libadd/libadd.c

#
# broken libsum
#

err-bin-build:
	gcc -shared -fPIC -o libsum/libsum.so libsum/libsum.c
	$(call show_needed,libsum/libsum.so)
	gcc -o bin/bin bin/main.c
# mold: error: undefined symbol: sum
# >>> referenced by main.c
# >>>               /tmp/ccBlvAs8.o:(main)
# collect2: error: ld returned 1 exit status

err-bin-run:
	gcc -shared -fPIC -o libsum/libsum.so libsum/libsum.c
	$(call show_needed,libsum/libsum.so)
	gcc -o bin/bin bin/main.c \
		-Llibsum -lsum
	./bin/bin 10
# ./bin/bin: error while loading shared libraries: libsum.so: cannot open shared object file: No such file or directory

bin-run:
	gcc -shared -fPIC -o libsum/libsum.so libsum/libsum.c
	$(call show_needed,libsum/libsum.so)
	gcc -o bin/bin bin/main.c \
		-Llibsum -lsum
	LD_LIBRARY_PATH=libadd:libsum ./bin/bin 10
# ./bin/bin: symbol lookup error: libsum/libsum.so: undefined symbol: add

bin-run-fix:
	gcc -shared -fPIC -o libsum/libsum.so libsum/libsum.c
	$(call show_needed,libsum/libsum.so)
	gcc -o bin/bin bin/main.c \
		-Llibsum -lsum
	LD_LIBRARY_PATH=libadd:libsum LD_PRELOAD=./libadd/libadd.so ./bin/bin 10

err-bin-run-2:
	gcc -shared -fPIC -o libsum/libsum.so libsum/libsum.c \
			-Llibadd -ladd
	$(call show_needed,libsum/libsum.so)
	gcc -o bin/bin bin/main.c \
		-Llibsum -lsum
	./bin/bin 10
# ./bin/bin: error while loading shared libraries: libsum.so: cannot open shared object file: No such file or directory

bin-fix-2:
	gcc -shared -fPIC -o libsum/libsum.so libsum/libsum.c \
			-Llibadd -ladd
	$(call show_needed,libsum/libsum.so)
	$(call show_runpath,libsum/libsum.so)
	gcc -o bin/bin bin/main.c \
		-Llibsum -lsum
	LD_LIBRARY_PATH=libadd:libsum ./bin/bin 10

bin-fix-3:
	gcc -shared -fPIC -o libsum/libsum.so libsum/libsum.c \
			-Llibadd -ladd \
			-Wl,-rpath,'$$ORIGIN/..libadd'
	$(call show_needed,libsum/libsum.so)
	$(call show_runpath,libsum/libsum.so)
	gcc -o bin/bin bin/main.c \
		-Llibsum -lsum
	$(call show_needed,bin/bin)
	LD_LIBRARY_PATH=libsum ./bin/bin 10

check-preload:
	@LD_PRELOAD=libadd/libadd.so LD_LIBRARY_PATH=libsum:libadd \
	LD_DEBUG=libs ./bin/bin 10 | grep 'libadd/libadd.so' || \
	(echo "LD_PRELOAD failed!" && false)

all: libadd.so
	gcc -shared -fPIC -o libsum/libsum.so libsum/libsum.c \
    -Llibadd -ladd -Wl,-rpath,'$ORIGIN/../libadd'

	gcc -o bin/bin bin/main.c \
    -Llibsum -lsum -Wl,-rpath,'$ORIGIN/../libsum'

	LD_LIBRARY_PATH=libadd:libsum ./bin/bin 10