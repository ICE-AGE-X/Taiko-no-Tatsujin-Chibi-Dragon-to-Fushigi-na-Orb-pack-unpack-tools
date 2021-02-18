FOR /F "tokens=*" %%G IN ('DIR /B /S *.png') DO python lmtpng2normalpng.py e g "%%G" "%%G"
pause
