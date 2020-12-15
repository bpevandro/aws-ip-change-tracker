import json
import urllib.request
import boto3
import datetime

bucket = '<bucket-name>'
prefix = 'ips-json/'
max_retries = 3

def lambda_handler(event, context):
    
    
    with urllib.request.urlopen("https://ip-ranges.amazonaws.com/ip-ranges.json") as url:
        data = json.loads(url.read().decode())

    s3 = boto3.client('s3')
    
    date_of_release = data['createDate']
    
    date_of_release = date_of_release.split('-')
    obj_name = date_of_release[0]+'-'+date_of_release[1]+'-'+date_of_release[2]

    
    # Deprecated for now
    # now = datetime.datetime.now()
    # obj_name = now.strftime('%Y-%m-%d')
    
    
    for _ in range(max_retries):
        try:
            r = s3.put_object(
                Bucket = bucket,
                Key = prefix+obj_name+'.json',
                Body = json.dumps(data),
                ContentType = 'application/json'
            )
            break
    
        except Exception as e:
            print('Exception occured :' + str(e))
            raise e
        
