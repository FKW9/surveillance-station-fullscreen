call env\Scripts\activate.bat
pyinstaller -F --distpath exe --upx-dir=test\upx-4.0.2-win64 -n fullscreen main2.py
pause