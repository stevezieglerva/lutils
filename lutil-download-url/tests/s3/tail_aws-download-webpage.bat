echo off
title CloudWatch Tail - aws-download-webpage
color 17


set log=aws-download-webpage

:repeat
echo *** %date% %time%
echo *** %date% %time% >> log_%log%.txt
call awslogs get /aws/lambda/%log% --start="1m" > results_%log%.txt
type results_%log%.txt
type results_%log%.txt >> log_%log%.txt

REM Silent wait
CHOICE /C:AB /d:A /T:10 >NUL

goto repeat

