FOR /F "tokens=*" %%G IN ('DIR /B /S *.png') DO python lmtpng2normalpng.py i g "%%G" "%%G_out.png"
pause
