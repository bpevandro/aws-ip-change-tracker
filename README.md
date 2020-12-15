
# aws-ip-change-tracker
App that allows you to keep track of the changes around AWS IP addresses

## How does it work
AWS sends an SNS notification to their public SNS topic every time a new IP is released. The aws-ip-tracker app consists of:
- A Lambda function that listens to this topic and gets triggered every time a new notification is sent to this topic(i.e a new IP address released). The Lambda then downloads the current ip-ranges.json file and stores it into the S3 bucket specified. The object is named as the date it was generated.
- When it gets to the point where you have two or more ip-ranges.json files, you can run the app(index.html), which allows you to compare the files and see what has changed(the exact IP addresses and their regions). This is done via API Gateway and a second Lambda function as the backend. 

## What does it look like
The dates available for selection in the drop-downs will depend on the ip-ranges.json files that you already have stored in your bucket. That is, if you already have two(or more), one representing the range of IPs as of 2018-09-30 and the other one representing the range of IP's as of 2018-10-01, here's what it'll look like:

![screen shot 2018-10-01 at 8 44 46 pm](https://user-images.githubusercontent.com/14941621/46308814-e6b4d600-c5ba-11e8-884f-30def1fd7c0e.png)
