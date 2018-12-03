
echo off
set filename=%~f0
for %%F in ("%filename%") do set script_dir=%%~dpF


del /Q /F %script_dir%obcode.py.touched 2>NUL
del /Q /F %script_dir%obcode.py 2>NUL
rmdir /Q /S %script_dir%__pycache__ 2>NUL
rmdir /Q /S %script_dir%src\__pycache__ 2>NUL
del /Q /F %script_dir%obcode.mak 2>NUL
del /Q /F %script_dir%obmak.py 2>NUL
del /Q /F %script_dir%obpatch.py 2>NUL
