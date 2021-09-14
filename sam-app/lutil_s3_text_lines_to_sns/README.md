# lutil_s3_text_lines_to_sns

## Description
Reads a newly created S3 file and publishes each line in the file to an SNS topic for processing by topic subscribers.



## Triggering Event
The Lambda is triggered by S3 creation events in the lutils-processingbucket bucket when text files are created with a specified prefix.

The triggering input event must match some criteria:

### Input S3 prefix

"lutil_s3_text_lines_to_sns/\<sns-topic-name\>/\<folder-prefixes\>/\<text-file-name.txt\>"

\<sns-topic-name\> refers to the destination SNS topic that will publish the messages.

\<folder-prefixes\> refers to any number of prefix folders that might be useful for organization for SNS subscribers. lutil_download_url uses prefix folders to help organize the downloaded files. 

### Input file
\<text-file-name.txt\> refers to a text file with a single record, per row. There is no required format for this Lambda since it just publishes messages to the SNS topic.

```
Apex,NC => Fairfax,VA
Durham,NC => Miami,FL
```

```
3938309|Smith|Developer
2929103|Johnson|Manager
```




## Output
For example, if an input file at this location contained a list of origin and destintion cities for a distance calculator Lambda:

```
s3://lutil_s3_text_lines_to_sns/distance_calculator_topic/list_of_cities.txt
```

```
Apex,NC => Fairfax,VA
Durham,NC => Miami,FL
```

the following messages would be published to the distance_calculator_topic SNS topic:

```
 {
    "line_number": 1,
    "line": "Apex,NC => Fairfax,VA",
    "source": "lutil_s3_text_lines_to_sns/distance_calculator_topic/list_of_cities.txt",
    "date": "2020-01-01T10:15:23",
}
```
and 
```
{
    "line_number": 2,
    "line": "Durham,NC => Miami,FL",
    "source": "lutil_s3_text_lines_to_sns/distance_calculator_topic/list_of_cities.txt",
    "date": "2020-01-01T10:15:23",
}
```





## Environment Variables
Variables for the current region and account are created during the deployment process. While these could be retrieved at run-time through sts.get-caller-identify, they are created at deployment-time to save the time of a separate API call. The variables are used to create the appropriate SNS ARN for message publication


