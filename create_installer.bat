pyinstaller -w qesend.py
DEL C:\Users\tedla\prj\qesend\dist\qesend\PyQt6\Qt6\bin\opengl32sw.dll
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup_script.iss
rmdir /s /q build
rmdir /s /q dist
DEL qesend.spec