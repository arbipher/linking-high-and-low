Examples of Linking Scenarios
===============

# Script

```shell
$python3 matrix.py
```

# Result Table

| Id  | Add       | Sum       | BinMode   | Status          | Reason                |
| --- | --------- | --------- | --------- | --------------- | --------------------- |
| 00  | default   | default   | default   | ✅ success       |                       |
| 01  | default   | default   | at_exe    | ✅ success       |                       |
| 02  | default   | default   | at_loader | ✅ success       |                       |
| 03  | default   | default   | at_rpath  | ✅ success       |                       |
| 04  | default   | at_exe    | default   | ✅ success       |                       |
| 05  | default   | at_exe    | at_exe    | ✅ success       |                       |
| 06  | default   | at_exe    | at_loader | ✅ success       |                       |
| 07  | default   | at_exe    | at_rpath  | ✅ success       |                       |
| 08  | default   | at_loader | default   | ✅ success       |                       |
| 09  | default   | at_loader | at_exe    | ✅ success       |                       |
| 10  | default   | at_loader | at_loader | ✅ success       |                       |
| 11  | default   | at_loader | at_rpath  | ✅ success       |                       |
| 12  | default   | at_rpath  | default   | ❌ loading_error | @rpath/libsum...dylib |
| 12  | default   | at_rpath  | default   | ✅ success       |                       |
| 13  | default   | at_rpath  | at_exe    | ❌ loading_error | @rpath/libsum...dylib |
| 13  | default   | at_rpath  | at_exe    | ✅ success       |                       |
| 14  | default   | at_rpath  | at_loader | ❌ loading_error | @rpath/libsum...dylib |
| 14  | default   | at_rpath  | at_loader | ✅ success       |                       |
| 15  | default   | at_rpath  | at_rpath  | ❌ loading_error | @rpath/libsum...dylib |
| 15  | default   | at_rpath  | at_rpath  | ✅ success       |                       |
| 16  | at_exe    | default   | default   | ✅ success       |                       |
| 17  | at_exe    | default   | at_exe    | ✅ success       |                       |
| 18  | at_exe    | default   | at_loader | ✅ success       |                       |
| 19  | at_exe    | default   | at_rpath  | ✅ success       |                       |
| 20  | at_exe    | at_exe    | default   | ✅ success       |                       |
| 21  | at_exe    | at_exe    | at_exe    | ✅ success       |                       |
| 22  | at_exe    | at_exe    | at_loader | ✅ success       |                       |
| 23  | at_exe    | at_exe    | at_rpath  | ✅ success       |                       |
| 24  | at_exe    | at_loader | default   | ✅ success       |                       |
| 25  | at_exe    | at_loader | at_exe    | ✅ success       |                       |
| 26  | at_exe    | at_loader | at_loader | ✅ success       |                       |
| 27  | at_exe    | at_loader | at_rpath  | ✅ success       |                       |
| 28  | at_exe    | at_rpath  | default   | ❌ loading_error | @rpath/libsum...dylib |
| 28  | at_exe    | at_rpath  | default   | ✅ success       |                       |
| 29  | at_exe    | at_rpath  | at_exe    | ❌ loading_error | @rpath/libsum...dylib |
| 29  | at_exe    | at_rpath  | at_exe    | ✅ success       |                       |
| 30  | at_exe    | at_rpath  | at_loader | ❌ loading_error | @rpath/libsum...dylib |
| 30  | at_exe    | at_rpath  | at_loader | ✅ success       |                       |
| 31  | at_exe    | at_rpath  | at_rpath  | ❌ loading_error | @rpath/libsum...dylib |
| 31  | at_exe    | at_rpath  | at_rpath  | ✅ success       |                       |
| 32  | at_loader | default   | default   | ✅ success       |                       |
| 33  | at_loader | default   | at_exe    | ✅ success       |                       |
| 34  | at_loader | default   | at_loader | ✅ success       |                       |
| 35  | at_loader | default   | at_rpath  | ✅ success       |                       |
| 36  | at_loader | at_exe    | default   | ✅ success       |                       |
| 37  | at_loader | at_exe    | at_exe    | ✅ success       |                       |
| 38  | at_loader | at_exe    | at_loader | ✅ success       |                       |
| 39  | at_loader | at_exe    | at_rpath  | ✅ success       |                       |
| 40  | at_loader | at_loader | default   | ✅ success       |                       |
| 41  | at_loader | at_loader | at_exe    | ✅ success       |                       |
| 42  | at_loader | at_loader | at_loader | ✅ success       |                       |
| 43  | at_loader | at_loader | at_rpath  | ✅ success       |                       |
| 44  | at_loader | at_rpath  | default   | ❌ loading_error | @rpath/libsum...dylib |
| 44  | at_loader | at_rpath  | default   | ✅ success       |                       |
| 45  | at_loader | at_rpath  | at_exe    | ❌ loading_error | @rpath/libsum...dylib |
| 45  | at_loader | at_rpath  | at_exe    | ✅ success       |                       |
| 46  | at_loader | at_rpath  | at_loader | ❌ loading_error | @rpath/libsum...dylib |
| 46  | at_loader | at_rpath  | at_loader | ✅ success       |                       |
| 47  | at_loader | at_rpath  | at_rpath  | ❌ loading_error | @rpath/libsum...dylib |
| 47  | at_loader | at_rpath  | at_rpath  | ✅ success       |                       |
| 48  | at_rpath  | default   | default   | ❌ loading_error | @rpath/libadd...dylib |
| 48  | at_rpath  | default   | default   | ✅ success       |                       |
| 49  | at_rpath  | default   | at_exe    | ❌ loading_error | @rpath/libadd...dylib |
| 49  | at_rpath  | default   | at_exe    | ✅ success       |                       |
| 50  | at_rpath  | default   | at_loader | ❌ loading_error | @rpath/libadd...dylib |
| 50  | at_rpath  | default   | at_loader | ✅ success       |                       |
| 51  | at_rpath  | default   | at_rpath  | ❌ loading_error | @rpath/libadd...dylib |
| 51  | at_rpath  | default   | at_rpath  | ✅ success       |                       |
| 52  | at_rpath  | at_exe    | default   | ❌ loading_error | @rpath/libadd...dylib |
| 52  | at_rpath  | at_exe    | default   | ✅ success       |                       |
| 53  | at_rpath  | at_exe    | at_exe    | ❌ loading_error | @rpath/libadd...dylib |
| 53  | at_rpath  | at_exe    | at_exe    | ✅ success       |                       |
| 54  | at_rpath  | at_exe    | at_loader | ❌ loading_error | @rpath/libadd...dylib |
| 54  | at_rpath  | at_exe    | at_loader | ✅ success       |                       |
| 55  | at_rpath  | at_exe    | at_rpath  | ❌ loading_error | @rpath/libadd...dylib |
| 55  | at_rpath  | at_exe    | at_rpath  | ✅ success       |                       |
| 56  | at_rpath  | at_loader | default   | ❌ loading_error | @rpath/libadd...dylib |
| 56  | at_rpath  | at_loader | default   | ✅ success       |                       |
| 57  | at_rpath  | at_loader | at_exe    | ❌ loading_error | @rpath/libadd...dylib |
| 57  | at_rpath  | at_loader | at_exe    | ✅ success       |                       |
| 58  | at_rpath  | at_loader | at_loader | ❌ loading_error | @rpath/libadd...dylib |
| 58  | at_rpath  | at_loader | at_loader | ✅ success       |                       |
| 59  | at_rpath  | at_loader | at_rpath  | ❌ loading_error | @rpath/libadd...dylib |
| 59  | at_rpath  | at_loader | at_rpath  | ✅ success       |                       |
| 60  | at_rpath  | at_rpath  | default   | ❌ loading_error | @rpath/libsum...dylib |
| 60  | at_rpath  | at_rpath  | default   | ❌ loading_error | @rpath/libadd...dylib |
| 60  | at_rpath  | at_rpath  | default   | ✅ success       |                       |
| 61  | at_rpath  | at_rpath  | at_exe    | ❌ loading_error | @rpath/libsum...dylib |
| 61  | at_rpath  | at_rpath  | at_exe    | ❌ loading_error | @rpath/libadd...dylib |
| 61  | at_rpath  | at_rpath  | at_exe    | ✅ success       |                       |
| 62  | at_rpath  | at_rpath  | at_loader | ❌ loading_error | @rpath/libsum...dylib |
| 62  | at_rpath  | at_rpath  | at_loader | ❌ loading_error | @rpath/libadd...dylib |
| 62  | at_rpath  | at_rpath  | at_loader | ✅ success       |                       |
| 63  | at_rpath  | at_rpath  | at_rpath  | ❌ loading_error | @rpath/libsum...dylib |
| 63  | at_rpath  | at_rpath  | at_rpath  | ❌ loading_error | @rpath/libadd...dylib |
| 63  | at_rpath  | at_rpath  | at_rpath  | ✅ success       |                       |


