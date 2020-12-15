# zip -r myDeploymentPackage.zip netaddr* lambda_function.py
# aws lambda update-function-code --function-name aws-ip-tracker-service-check --zip-file fileb://myDeploymentPackage.zip

import json
import urllib.request
from netaddr import IPNetwork, IPAddress

def lambda_handler(event, context):

    CIDR = []
    REGION = []
    SERVICE = []
    IP_ADDRESSES = []
    IP_ADD_AMZ_REGION = []
    exists = False
    error = False

    event_json = json.dumps(event)
    loaded_event_json = json.loads(event_json)
    body_payload = json.loads(loaded_event_json['body'])
    IP_ADDRESSES_LIST = list(set(body_payload['ip_addresses']))


    # if len(IP_ADDRESSES_LIST) > 12:
    #     return {
    #         "statusCode": 400,
    #         "headers": {
    #                 "Access-Control-Allow-Origin": "*"
    #         },
    #         "body": 'Max number of lines exceeded.(Max 12)'
    #     }

    with urllib.request.urlopen("https://ip-ranges.amazonaws.com/ip-ranges.json") as url:
        data = json.loads(url.read().decode())
        # data = data['prefixes']

    for ip in IP_ADDRESSES_LIST:
        for x in reversed(data['prefixes']):
           
            if error is False:
                try:
                    if IPAddress(str(ip)) in IPNetwork(x['ip_prefix']):

                        if x['service'] != 'AMAZON' and str(ip) not in IP_ADDRESSES:
                            CIDR.append(x['ip_prefix'])
                            REGION.append(x['region'])
                            SERVICE.append(x['service'])
                            IP_ADDRESSES.append(ip)
                            exists = True

                        if x['service'] == 'AMAZON' and str(ip) not in IP_ADDRESSES:
                            CIDR.append(x['ip_prefix'])
                            REGION.append(x['region'])
                            SERVICE.append(x['service'])
                            IP_ADDRESSES.append(ip)
                            exists = True     
                    
                except:
                    error = True
                    IP_ADDRESSES.append(ip)
                    SERVICE.append('Error most likely due to invalid IP')
                    CIDR.append('/')
                    REGION.append('/')
                    print(error)
                    break


 
        if exists is False and error is False:
            IP_ADDRESSES.append(ip)
            SERVICE.append('This IP does not seem to belong to AWS')
            CIDR.append('/')
            REGION.append('/')    
        
        exists = False  
        error = False

  
    body = {
        'cidr': CIDR,
        'region': REGION,
        'service': SERVICE,
        'ip_addresses': IP_ADDRESSES
    }


    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }