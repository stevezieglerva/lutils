# lutil_download_url

## Description
Downloads a web page and saves the latest copy and historical copy of the html in a S3 bucket. The download is a basic curl-style download without the execution of any client-side JS. 


## Triggering Event
The Lambda is triggered by SNS messages published to the lutil_s3_text_lines_output topic. That topic is feed messages by the [lutil_s3_text_lines_to_sns](../lutil_s3_text_lines_to_sns) lambda as it reads newly added text files. Each line in the source text file should contain a fully qualified url:

```
https://www.cnn.com
https://news.google.com
https://msn.com
```

The SNS topic messages will look like:

```
{
    "line_number": 1,
    "line": "https://www.cnn.com",
    "source": "lutil_s3_text_lines_to_sns/lutil_s3_text_lines_output/list_of_news_urls.txt",
    "date": "2020-01-01T10:15:23",
}
```

In order to group the downloaded pages, it might be useful to use additional folder prefixes in the key name of the URL text file.



## Output
The Lambda will generate two files:

* s3://lutils-processingbucket-mlzuepg0mol2/lutil-download-url/**latest**/\<website domain name\>/\<escaped url\> - this location in the "latest" folder stores the last downloaded file

* s3://lutils-processingbucket-mlzuepg0mol2/lutil-download-url/\<website domain name\>/\<escaped url **with timestamp suffix**\> - this location will store a timestamped version of the file in the same location as previouis downloads

The example above will store the following names:
* lutil-download-url/**latest**/www.cnn.com/https___www.cnn.com
* lutil-download-url/www.cnn.com/https___www.cnn.com.**2020-07-17T17:59:15.905054**


## Environment Variables

* s3_bucket - Bucket name of the output files set during deployment. Changing to a differnt bucket will require additional bucket policy permissions for the Lambda.

* use_quids_for_filenames - [yes|no] - Saves the files names as an MD5 hash of the URL instead of the escaped URL filename to help with long URL names and special characters
