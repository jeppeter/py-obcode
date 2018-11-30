echo off
set filename=%~f0
for %%F in ("%filename%") do set script_dir=%%~dpF
echo %script_dir%


if -%1- == -OB_PATCH- (
	call :dump_patch_file_out main.obj
	call :dump_patch_file_out main2.obj
	call :dump_patch_file_out main.exe
	call :dump_patch_file_out main2.exe
	call :dump_patch_file_out callc.obj
) else (
	call :dump_file_out main.obj
	call :dump_file_out main2.obj
	call :dump_file_out main.exe
	call :dump_file_out main2.exe
	call :dump_file_out callc.obj
)


goto :end

:dump_file_out
set _bin_file=%1
set _out_txt=z:\%1.dumpbin.txt
goto :dump_out_func

:dump_patch_file_out
set _bin_file=%1
set _out_txt=z:\%1.patch.dumpbin.txt
goto :dump_out_func


:dump_out_func
echo "_bin_file [%_bin_file%]"
echo "_out_txt [%_out_txt%]"
dumpbin /nologo /DISASM /out:%_out_txt% %_bin_file%
exit /b %errorlevel%
REM exit /b 0

:end
echo on