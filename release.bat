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
rmdir /Q /S %script_dir%__pycache__ 2>NUL

%PYTHON% %script_dir%src\obcode_debug.py --release
call :check_file %script_dir%obcode.py.touched

%PYTHON% -m insertcode -p %%PYTHON_OBCODE_STR%% -i %script_dir%src\obcode.mak.tmpl -o %script_dir%obcode.mak makepython %script_dir%obcode.py
if not errorlevel 0 (
	echo "can not insert code" >&2
	goto :fail
)

goto :run_test

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

:run_test

%PYTHON% %script_dir%test\unit\test.py -f
if not errorlevel 0 (
	echo "not run test ok" >&2
	goto :end
)

:end
echo on