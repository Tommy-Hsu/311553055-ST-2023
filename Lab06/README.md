# 311553055 許博濟 Lab06
## 環境, 編譯器及版本

Ubuntu 22.04.2 LTS ( aarch64 版本並安裝在 docker) <br>
gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0
## Lab 6

|  | Valgrind | ASan |
| :--------: | :--------: | :--------: |
| Heap out-of-bounds | 能 | 能 |
| Stack out-of-bounds | 不能 | 能|
| Global out-of-bounds | 不能 | 能 |
| Use-after-free | 能     | 能    |
| Use-after-return | 能 | 能 |
| cross Redzone | N/A| 不能 |


### Heap out-of-bounds
```c=
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(){
	char *str = malloc(4);
	str[4] = 'a';
	printf("%c\n", str[4]);
	free(str);

	return 0;
}

```
```sh=
=================================================================
==4306==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xffffb7c007b4 at pc 0xaaaac9fa0b38 bp 0xfffffd588b50 sp 0xfffffd50
WRITE of size 1 at 0xffffb7c007b4 thread T0
    #0 0xaaaac9fa0b34 in main (/home/software_testing/lab06/t2+0xb34)
    #1 0xffffbbce73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffffbbce74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaac9fa09ec in _start (/home/software_testing/lab06/t2+0x9ec)

0xffffb7c007b4 is located 0 bytes to the right of 4-byte region [0xffffb7c007b0,0xffffb7c007b4)
allocated by thread T0 here:
    #0 0xffffbbf1a2f4 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0xaaaac9fa0ae0 in main (/home/software_testing/lab06/t2+0xae0)
    #2 0xffffbbce73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #3 0xffffbbce74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #4 0xaaaac9fa09ec in _start (/home/software_testing/lab06/t2+0x9ec)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/software_testing/lab06/t2+0xb34) in main
Shadow bytes around the buggy address:
  0x200ff6f800a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff6f800b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff6f800c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff6f800d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff6f800e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x200ff6f800f0: fa fa fa fa fa fa[04]fa fa fa fa fa fa fa fa fa
  0x200ff6f80100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff6f80110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff6f80120: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff6f80130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff6f80140: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==4306==ABORTING
```
```sh=
==4424== Memcheck, a memory error detector
==4424== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==4424== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==4424== Command: ./t2
==4424==
==4424== Invalid write of size 1
==4424==    at 0x108834: main (in /home/software_testing/lab06/t2)
==4424==  Address 0x4a3a044 is 0 bytes after a block of size 4 alloc'd
==4424==    at 0x4865058: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==4424==    by 0x108823: main (in /home/software_testing/lab06/t2)
==4424==
==4424== Invalid read of size 1
==4424==    at 0x108840: main (in /home/software_testing/lab06/t2)
==4424==  Address 0x4a3a044 is 0 bytes after a block of size 4 alloc'd
==4424==    at 0x4865058: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==4424==    by 0x108823: main (in /home/software_testing/lab06/t2)
==4424==
a
==4424==
==4424== HEAP SUMMARY:
==4424==     in use at exit: 0 bytes in 0 blocks
==4424==   total heap usage: 2 allocs, 2 frees, 1,028 bytes allocated
==4424==
==4424== All heap blocks were freed -- no leaks are possible
==4424==
==4424== For lists of detected and suppressed errors, rerun with: -s
==4424== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
```
` ASan 能, Valgrind 能 `

### Stack out-of-bounds
```c=
#include <stdio.h>

int main(){
    int i = 0;
    int v[10];
    for( i = 0; i <= 20; i++){
        v[i] = 4;
    }
    printf("%d\n", v[11]);
    return 0;
}
```
```c=
=================================================================
==6412==ERROR: AddressSanitizer: stack-buffer-overflow on address 0xffffc400c188 at pc 0xaaaabf460ca8 bp 0xffffc400c0d0 sp 0xffffc40
WRITE of size 4 at 0xffffc400c188 thread T0
    #0 0xaaaabf460ca4 in main (/home/software_testing/lab06/t2+0xca4)
    #1 0xffffad1573f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffffad1574c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaabf460aac in _start (/home/software_testing/lab06/t2+0xaac)

Address 0xffffc400c188 is located in stack of thread T0 at offset 88 in frame
    #0 0xaaaabf460ba0 in main (/home/software_testing/lab06/t2+0xba0)

  This frame has 1 object(s):
    [48, 88) 'v' (line 5) <== Memory access at offset 88 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (/home/software_testing/lab06/t2+0xca4) in main
Shadow bytes around the buggy address:
  0x200ff88017e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff88017f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8801800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8801810: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8801820: 00 00 00 00 00 00 f1 f1 f1 f1 f1 f1 00 00 00 00
=>0x200ff8801830: 00[f3]f3 f3 f3 f3 00 00 00 00 00 00 00 00 00 00
  0x200ff8801840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8801850: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8801860: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8801870: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8801880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==6412==ABORTING
```
```c=
==6436== Memcheck, a memory error detector
==6436== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==6436== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==6436== Command: ./stack
==6436==
4
*** stack smashing detected ***: terminated
==6436==
==6436== Process terminating with default action of signal 6 (SIGABRT)
==6436==    at 0x490F200: __pthread_kill_implementation (pthread_kill.c:44)
==6436==    by 0x48CA67B: raise (raise.c:26)
==6436==    by 0x48B712F: abort (abort.c:79)
==6436==    by 0x4903307: __libc_message (libc_fatal.c:155)
==6436==    by 0x4985897: __fortify_fail (fortify_fail.c:26)
==6436==    by 0x4985863: __stack_chk_fail (stack_chk_fail.c:24)
==6436==    by 0x1088E3: main (stack.c:11)
==6436==
==6436== HEAP SUMMARY:
==6436==     in use at exit: 1,024 bytes in 1 blocks
==6436==   total heap usage: 1 allocs, 0 frees, 1,024 bytes allocated
==6436==
==6436== LEAK SUMMARY:
==6436==    definitely lost: 0 bytes in 0 blocks
==6436==    indirectly lost: 0 bytes in 0 blocks
==6436==      possibly lost: 0 bytes in 0 blocks
==6436==    still reachable: 1,024 bytes in 1 blocks
==6436==         suppressed: 0 bytes in 0 blocks
==6436== Rerun with --leak-check=full to see details of leaked memory
==6436==
==6436== For lists of detected and suppressed errors, rerun with: -s
==6436== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
Aborted
```
`ASan 能, Valgrind 不能`
### Global out-of-bounds
```c=
#include <stdio.h>

int arr[3];

int main() {
    arr[3] = 4; // 这里会访问数组 arr 之外的内存
    printf("%d", arr[3]);
    return 0;
}
```
```c=
=================================================================
==6944==ERROR: AddressSanitizer: global-buffer-overflow on address 0xaaaadc2210cc at pc 0xaaaadc210ab0 bp 0xffffc7738d90 sp 0xffffc0
WRITE of size 4 at 0xaaaadc2210cc thread T0
    #0 0xaaaadc210aac in main (/home/software_testing/lab06/t2+0xaac)
    #1 0xffffa63f73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffffa63f74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaadc21096c in _start (/home/software_testing/lab06/t2+0x96c)

0xaaaadc2210cc is located 0 bytes to the right of global variable 'arr' defined in 'global.c:3:5' (0xaaaadc2210c0) of size 12
SUMMARY: AddressSanitizer: global-buffer-overflow (/home/software_testing/lab06/t2+0xaac) in main
Shadow bytes around the buggy address:
  0x15655b8441c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x15655b8441d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x15655b8441e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x15655b8441f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x15655b844200: 00 00 00 00 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
=>0x15655b844210: f9 f9 f9 f9 00 00 00 00 00[04]f9 f9 f9 f9 f9 f9
  0x15655b844220: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x15655b844230: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x15655b844240: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x15655b844250: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x15655b844260: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==6944==ABORTING
```
```c=
==6998== Memcheck, a memory error detector
==6998== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==6998== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==6998== Command: ./global
==6998==
4==6998==
==6998== HEAP SUMMARY:
==6998==     in use at exit: 0 bytes in 0 blocks
==6998==   total heap usage: 1 allocs, 1 frees, 1,024 bytes allocated
==6998==
==6998== All heap blocks were freed -- no leaks are possible
==6998==
==6998== For lists of detected and suppressed errors, rerun with: -s
==6998== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
`ASan 能, Valgrind 不能`
### Use-after-free
```c=
#include <stdio.h>
#include <stdlib.h>

int main() {
    int* ptr = malloc(sizeof(int));
    *ptr = 5;  
    free(ptr); 
    *ptr = 7; 
    int val = *ptr;

    printf("%d\n", val);
    return 0;
}
```
```c=
=================================================================
==7507==ERROR: AddressSanitizer: heap-use-after-free on address 0xffff86b007b0 at pc 0xaaaacf060b1c bp 0xffffc200c840 sp 0xffffc2000
WRITE of size 4 at 0xffff86b007b0 thread T0
    #0 0xaaaacf060b18 in main (/home/software_testing/lab06/usefree+0xb18)
    #1 0xffff8abc73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffff8abc74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaacf06096c in _start (/home/software_testing/lab06/usefree+0x96c)

0xffff86b007b0 is located 0 bytes inside of 4-byte region [0xffff86b007b0,0xffff86b007b4)
freed by thread T0 here:
    #0 0xffff8adf9fe8 in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:127
    #1 0xaaaacf060ac8 in main (/home/software_testing/lab06/usefree+0xac8)
    #2 0xffff8abc73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #3 0xffff8abc74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #4 0xaaaacf06096c in _start (/home/software_testing/lab06/usefree+0x96c)

previously allocated by thread T0 here:
    #0 0xffff8adfa2f4 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0xaaaacf060a60 in main (/home/software_testing/lab06/usefree+0xa60)
    #2 0xffff8abc73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #3 0xffff8abc74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #4 0xaaaacf06096c in _start (/home/software_testing/lab06/usefree+0x96c)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/software_testing/lab06/usefree+0xb18) in main
Shadow bytes around the buggy address:
  0x200ff0d600a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0d600b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0d600c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0d600d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0d600e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x200ff0d600f0: fa fa fa fa fa fa[fd]fa fa fa fa fa fa fa fa fa
  0x200ff0d60100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0d60110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0d60120: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0d60130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0d60140: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
```
```c=
==7523== Memcheck, a memory error detector
==7523== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==7523== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==7523== Command: ./usefree
==7523==
==7523== Invalid write of size 4
==7523==    at 0x108844: main (in /home/software_testing/lab06/usefree)
==7523==  Address 0x4a3a040 is 0 bytes inside a block of size 4 free'd
==7523==    at 0x4867AD0: free (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==7523==    by 0x10883B: main (in /home/software_testing/lab06/usefree)
==7523==  Block was alloc'd at
==7523==    at 0x4865058: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==7523==    by 0x108823: main (in /home/software_testing/lab06/usefree)
==7523==
==7523== Invalid read of size 4
==7523==    at 0x10884C: main (in /home/software_testing/lab06/usefree)
==7523==  Address 0x4a3a040 is 0 bytes inside a block of size 4 free'd
==7523==    at 0x4867AD0: free (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==7523==    by 0x10883B: main (in /home/software_testing/lab06/usefree)
==7523==  Block was alloc'd at
==7523==    at 0x4865058: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==7523==    by 0x108823: main (in /home/software_testing/lab06/usefree)
==7523==
7
==7523==
==7523== HEAP SUMMARY:
==7523==     in use at exit: 0 bytes in 0 blocks
==7523==   total heap usage: 2 allocs, 2 frees, 1,028 bytes allocated
==7523==
==7523== All heap blocks were freed -- no leaks are possible
==7523==
==7523== For lists of detected and suppressed errors, rerun with: -s
==7523== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
```
`ASan 能, Valgrind 能`
### Use-after-return
```c=
#include <stdio.h>

int *ptr;
void FunctionThatEscapesLocalObject() {
  int local[100];
  ptr = &local[0];
}

int main(int argc, char **argv) {
  FunctionThatEscapesLocalObject();
  ptr[argc] = 7777;
  return ptr[argc];
}
```
```c=
=================================================================
==177==ERROR: AddressSanitizer: stack-use-after-return on address 0xffff7e84c034 at pc 0xaaaada5e0d40 bp 0xfffff545e380 sp 0xfffff545e390
WRITE of size 4 at 0xffff7e84c034 thread T0
    #0 0xaaaada5e0d3c in main (/home/software_testing/lab06/usereturn+0xd3c)
    #1 0xffff81cb73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffff81cb74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaada5e0aac in _start (/home/software_testing/lab06/usereturn+0xaac)

Address 0xffff7e84c034 is located in stack of thread T0 at offset 52 in frame
    #0 0xaaaada5e0ba0 in FunctionThatEscapesLocalObject (/home/software_testing/lab06/usereturn+0xba0)

  This frame has 1 object(s):
    [48, 448) 'local' (line 5) <== Memory access at offset 52 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return (/home/software_testing/lab06/usereturn+0xd3c) in main
Shadow bytes around the buggy address:
  0x200fefd097b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200fefd097c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200fefd097d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200fefd097e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200fefd097f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x200fefd09800: f5 f5 f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x200fefd09810: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x200fefd09820: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x200fefd09830: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x200fefd09840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200fefd09850: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
```
```c=
==193== Memcheck, a memory error detector
==193== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==193== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright infotect_stack_use_after_return
==193== Command: ./t2
==193==
==193== Invalid write of size 4
==193==    at 0x10889C: main (in /home/software_testing/lab06/t2)
==193==  Address 0x1fff00030c is on thread 1's stack
==193==  404 bytes below stack pointer
==193==
==193== Invalid read of size 4
==193==    at 0x1088B8: main (in /home/software_testing/lab06/t2)
==193==  Address 0x1fff00030c is on thread 1's stack
==193==  404 bytes below stack pointer
==193==
==193==
==193== HEAP SUMMARY:
==193==     in use at exit: 0 bytes in 0 blocks
==193==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==193==
==193== All heap blocks were freed -- no leaks are possible
==193==
==193== For lists of detected and suppressed errors, rerun with: -s
==193== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
```
`ASan 能, Valgrind 能`
### Redzone
```c=
#include<stdio.h>

int main(){

    int a[2] = {0};
    printf("%x\n", a[8]);
    a[9] = 9;
    return 0;
}
```
```sh=
da0af5e0
```

`ASan 無法找出來 Stack buffer overflow 剛好越過 redzone(並沒有對 redzone 做讀寫) 的危險情況`

