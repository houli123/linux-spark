@echo off
setlocal enabledelayedexpansion

:: 设置输出文件的编码为UTF-8
chcp 65001 >nul

set "file_index=001"
for %%f in (*.py) do (
    set "filename=%%~nf"
    echo !filename!.py >> output.txt
    type "%%f" >> output.txt
    echo. >> output.txt
    echo. >> output.txt
    echo --------------------------------------------------------------------------------------- >> output.txt
    set /a file_index+=1
)

endlocal