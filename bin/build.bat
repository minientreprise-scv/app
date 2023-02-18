echo "Compiling project files..."
py -m py_compile .\bin\production.py

echo "Moving compiled file to project root..."

for /F "delims=" %%i in ('dir /b /a-d .\bin\__pycache__\prod*') do set file=%%i
move bin\__pycache__\%file% serve.pyc

echo "Finished, execute serve.pyc to run in development mode"