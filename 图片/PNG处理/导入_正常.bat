FOR /F "tokens=*" %%G IN ('DIR /B /S *.png') DO python lmtpng2normalpng.py i n "%%G" "%%G_out.png"
pause
