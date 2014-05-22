@echo off

::Set personal Path to the Apps:
set PythonEXE=C:\Python26\python.exe
set SevenZipEXE="C:\Program Files\7-Zip\7z.exe"
set UpxEXE="d:\Dhole\PtProject\Core\bin\upx.exe"

set DeployDir="d:\amw"

:: Compress=1 - Use CompressFiles
:: Compress=0 - Don't CompressFiles
set Compress=0

if not exist %PythonEXE%        call :FileNotFound %PythonEXE%
if not exist %SevenZipEXE%      call :FileNotFound %SevenZipEXE%
if not exist %UpxEXE%           call :FileNotFound %UpxEXE%

::Compile the Python-Script

%PythonEXE% "%~dpn0_run.py" py2exe
if not "%errorlevel%"=="0" (
        echo Py2EXE Error!
        pause
        goto:eof
)

:: Copy the Py2EXE Results to the SubDirectory and Clean Py2EXE-Results

rd build /s /q
rd %DeployDir% /s /q
md %DeployDir%
xcopy dist\*.* %DeployDir% /s /d /y 
:: xcopy dist\imageformats\*.* "%~dpn0_EXE\imageformats\" /d /y 

rd dist /s /q

if "%Compress%"=="1" call:CompressFiles
echo.
echo.
echo Done: %DeployDir%
echo.
pause
goto:eof

:CompressFiles
        %SevenZipEXE% -aoa x "%DeployDir%\library.zip" -o"%DeployDir%\library\"
        del "%DeployDir%\library.zip"

        cd %DeployDir%\library\
        %SevenZipEXE% a -tzip -mx9 "..\library.zip" -r
        cd..
        rd "%DeployDir%\library" /s /q

        cd %DeployDir%\imageformats\
        %UpxEXE% --best *.*
        cd %DeployDir%\
        %UpxEXE% --best *.*
goto:eof

:FileNotFound
        echo.
        echo Error, File not found:
        echo [%1]
        echo.
        echo Check Path in %~nx0???
        echo.
        pause
        exit
goto:eof