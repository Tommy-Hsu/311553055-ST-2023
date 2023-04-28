# 311553055 許博濟 Lab07
## PoC: the file that can trigger the vulnerability
![](https://i.imgur.com/ZYEzfiJ.png)

## The commands (steps) that you used in this lab
### Build & fuzz with AFL
移動到目標目錄下
```bash
cd Lab07
```
將環境變數 CC 也就是預設編譯器改為 AFL 的編譯器
```bash
export CC=~/AFL/afl-gcc
```
將環境變數 AFL_USE_ASAN 設定為 true
```bash
export AFL_USE_ASAN=1
```
將我們的目標程式碼，編譯成為執行檔
注意 Makefile 需要寫成 CC?=gcc 
```bash
make
```
![](https://i.imgur.com/zvzhGj6.png)

加入 in 目錄用來放置 testing inputs
```bash
mkdir in
```
將測試的 bmp 放入 in 目錄
```bash
cp test.bmp in/
```
執行 AFL fuzz
```bash 
~/AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
```
![](https://i.imgur.com/21yprwl.png)
## Screenshot of AFL running (with triggered crash)
![](https://i.imgur.com/zSSyddf.png)

## Screenshot of crash detail (with ASAN error report)
bmpgrayscale 這個執行檔需要兩個參數，第一個是 input，第二個是 output，
所以第一個檔案就是 crashes 內的檔案，也就是 input file
```bash=
./bmpgrayscale out/crashes/id:000000* a.bmp
```
![](https://i.imgur.com/sxr9oq4.png)

![](https://i.imgur.com/cGGRr05.png)

