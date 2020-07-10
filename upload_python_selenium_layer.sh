echo "Checking if zip file already in the S3 bucket"
aws s3 ls s3://$S3_ARTIFACTS/python-selenium-simplified.zip > ls_results.txt
cat ls_results.txt
grep python-selenium-simplified.zip ls_results.txt ; greprc=$?
if [ $greprc -eq 0 ];
then
    echo "Zip file already uploaded to $S3_ARTIFACTS"
    exit
fi
echo "Zip file not found in $S3_ARTIFACTS"

echo "Get the Python Selenium Lambda layer file to upload to S3 and add lambda layer"
curl https://svz-public.s3.amazonaws.com/python-selenium-simplified.zip -o python-selenium-simplified.zip 

echo "Upload the zip to the S3 bucket so it can be referenced in the lutils template.yaml"
aws s3 cp python-selenium-simplified.zip s3://$S3_ARTIFACTS #env variable set earliers in buildspec

