title Sync

:loop
call echo %time% input
call aws s3 sync .\input s3://svz-aws-download-webpages/input
call echo %time% output
call aws s3 sync s3://svz-aws-download-webpages/output .\output
call echo %time% firehose 
call aws s3 sync s3://svz-aws-download-webpages/firehose .\firehose
call echo %time% url_files 
call aws s3 sync s3://svz-aws-download-webpages/url_files .\url_files


timeout 10
goto loop

