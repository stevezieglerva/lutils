title Delete Output

call del /q .\output\*.*
call del /q .\firehose\*.*
call del /q .\url_files\*.*

call echo %time% output
call aws s3 sync .\output s3://svz-aws-download-webpages/output --delete
call echo %time% firehose 
call aws s3 sync .\firehose s3://svz-aws-download-webpages/firehose --delete
call echo %time% url_files
call aws s3 sync .\url_files s3://svz-aws-download-webpages/url_files --delete



