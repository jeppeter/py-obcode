echo off
set filename=%~f0
for %%F in ("%filename%") do set script_dir=%%~dpF
echo %script_dir%

if -%PYTHON%- == -- (
	set PYTHON=python
)

echo "PYTHON [%PYTHON%]"

del /Q /F %script_dir%obcode.py.touched 2>NUL
del /Q /F %script_dir%obcode.py 2>NUL
del /Q /F %script_dir%obpatch.py.touched 2>NUL
del /Q /F %script_dir%obpatch.py 2>NUL
del /Q /F %script_dir%obmak.py.touched 2>NUL
del /Q /F %script_dir%obmak.py 2>NUL
rmdir /Q /S %script_dir%__pycache__ 2>NUL

%PYTHON% -m insertcode -p %%C_CODE_CRC32CALC%% -i %script_dir%src\chkval.py.tmpl pythonc %script_dir%src\crc32calc.c | %PYTHON% -m insertcode -p %%C_CODE_MD5CALC%% pythonc %script_dir%src\md5calc.c | %PYTHON% -m insertcode -p %%C_CODE_SHA256CALC%% pythonc %script_dir%src\sha256calc.c | %PYTHON% -m insertcode -p %%C_CODE_SHA3CALC%% pythonc %script_dir%src\sha3calc.c | %PYTHON% -m insertcode -p %%C_CODE_CHKVALDEF%% pythonc %script_dir%src\chkvaldef.c | %PYTHON% -m insertcode -p %%C_CODE_CHKVAL%% -o %script_dir%src\chkval.py pythonc %script_dir%src\chkval.c

if not errorlevel 0 (
	echo "can not insert code" >&2
	goto :fail
)


%PYTHON% %script_dir%src\obcode_debug.py --release
call :check_file %script_dir%obcode.py.touched

%PYTHON% %script_dir%src\obmak_debug.py --release
call :check_file %script_dir%obmak.py.touched

%PYTHON% %script_dir%src\obpatch_debug.py --release
call :check_file %script_dir%obpatch.py.touched

%PYTHON% -m insertcode -p %%OBMAK_CODE%% -i  %script_dir%src\obcode.mak.tmpl   bz2base64mak %script_dir%obmak.py  | %PYTHON% -m insertcode -p %%OBPATCH_CODE%% -o %script_dir%obcode.mak bz2base64mak %script_dir%obpatch.py

if not errorlevel 0 (
	echo "can not insert code" >&2
	goto :fail
)

goto :end

:check_file

set _waitf=%1
set _maxtime=100
set _cnt=0
set _checked=0
if x%_waitf% == x (
	goto :check_file_end
)

:check_file_again
if %_maxtime% LSS %_cnt% (
	echo "can not wait (%_waitf%) in (%_maxtime%)"
	exit /b 3
)

if exist %_waitf% (
	%PYTHON% -c "import time;time.sleep(0.1)"
	set /A _checked=%_checked%+1
	if %_checked% GTR 3 (
		del /F /Q %_waitf%
		goto :check_file_end
	)
    echo "will check (%_checked%) %_waitf%"
) else (
	set _checked=0
)

set /A _cnt=%_cnt%+1
%PYTHON% -c "import time;time.sleep(0.1)"
goto :check_file_again

:check_file_end
exit /b 0

:fail
goto :end


:end
echo on