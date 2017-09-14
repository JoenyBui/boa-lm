:: Deployment Build for application.  Only for Windows.
call startup.bat
@RD /S /Q "build"
@RD /S /Q "dist"
::pyinstaller --noconsole --hidden-import=h5py.defs --hidden-import=h5py.utils --hidden-import=h5py.h5ac --hidden-import=h5py._proxy boalm/app.py
::pyinstaller --debug --log-level=DEBUG "boalm/client.py" --specpath="build" --path="boalm" --upx-dir="D:\App\upx391w\upx.exe"
pyinstaller --debug --log-level=DEBUG "boalm/client.py" --specpath="build" --path="boalm"
::pyinstaller --debug --log-level=DEBUG "boalm/app.py" --specpath="build" --path="boalm"
:: Exit
