import json
import boto3
import os
import datetime


bucket = '<bucket-name>'
prefix = 'ips-json/'

def pullDataFromS3(service, date1, date2):
    ips = []
    ips2 = []
    ipsv6 = []
    ipsv6_2 = []
    regions = []
    regions_removed = []
    regionsv6 = []
    regionsv6_removed = []
    flag_regions = None
    flag_regions_removed = None
    flag_regionsv6 = None
    flag_regionsv6_removed = None

    s3 = boto3.resource('s3')
    
    try:

        s3.meta.client.download_file(bucket, prefix+date2+'.json', '/tmp/'+date2+'.json')
        
        # Opens the files and stores them into their corresponding variables 
        file2 = open('/tmp/'+date2+'.json', 'r')
        file2_loaded = json.load(file2)
        
        json_ips_date2 = file2_loaded['prefixes']
        json_ipsv6_date2 = file2_loaded['ipv6_prefixes']
       
        # Iterates through the objects and it appens to the ips2 list based on the service specified - IPv4
        i = 0
        for x in json_ips_date2:
            if json_ips_date2[i]['service'] == service:
                ips2.append(json_ips_date2[i]['ip_prefix'])
                
            i += 1
        
        # Iterates through the objects and it appens to the ips2 list based on the service specified - IPv6
        i = 0
        for x in json_ipsv6_date2:
            if json_ipsv6_date2[i]['service'] == service:
                ipsv6_2.append(json_ipsv6_date2[i]['ipv6_prefix'])
            i += 1
        
        # Downloads the objects for the specified dates and stores them into the /tmp
        try:
            s3.meta.client.download_file(bucket, prefix+date1+'.json', '/tmp/'+date1+'.json')
            file1 = open('/tmp/'+date1+'.json', 'r')
            file1_loaded = json.load(file1)
            json_ips_date1 = file1_loaded['prefixes']
            json_ipsv6_date1 = file1_loaded['ipv6_prefixes']

             # Iterates through the objects and it appens to the ips list based on the service specified - IPv4
            i = 0
            for x in json_ips_date1:
                if json_ips_date1[i]['service'] == service:
                    ips.append(json_ips_date1[i]['ip_prefix'])
                i += 1
            
            # Iterates through the objects and it appens to the ips list based on the service specified - IPv6
            i = 0
            for x in json_ipsv6_date1:
                if json_ipsv6_date1[i]['service'] == service:
                    ipsv6.append(json_ipsv6_date1[i]['ipv6_prefix'])
                i += 1
            
        except:
            ips.append(" ")
            ipsv6.append(" ")

            i = 0
            for x in json_ips_date2:
                if json_ips_date2[i]['service'] == service:
                    regions.append(json_ips_date2[i]['region'])
                    
                i += 1
            
            # Iterates through the objects and it appens to the ips2 list based on the service specified - IPv6
            i = 0
            for x in json_ipsv6_date2:
                if json_ipsv6_date2[i]['service'] == service:
                    regionsv6.append(json_ipsv6_date2[i]['region'])
                i += 1
            
            body = {
                'diff': '',
                'diffv6': '',
                'ips1': '',
                'ips2': ips2,
                'ipv6': '',
                'ipv6_2': ipsv6_2,
                'regions': regions,
                'regionsv6': regionsv6
            }

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(body)
            }
      
        # Calculates the difference between the two lists - IPv4
        diff = list(set(ips2) - set(ips))
        diff_removed = list(set(ips) - set(ips2))
        
        # Calculates the difference between the two lists - IPv6
        diffv6 = list(set(ipsv6_2) - set(ipsv6))
        diffv6_removed = list(set(ipsv6) - set(ipsv6_2))
            
        # Finds the regions of the new ip addresses in list "diff" by iterating through 
        # "json_ips_date2" and comparing prefixes
        i = 0
        j = 0
        for ip in diff:
            for x in json_ips_date2:
                if flag_regions == None:
                    if x['service'] == service and x['ip_prefix'] == ip:
                        i += 1
                        regions.append(x['region'])
                        
                        # This flag indicates that the number of regions found is the same as the number of ips in diff.
                        # Therefore, the iteration can be stopped
                        if i == len(diff):
                            flag_regions = True
                            break
                        
        # Finds the regions of the removed ip addresses in list "diff_removed" by iterating through 
        # "json_ips_date1" and comparing prefixes                
        i = 0
        for ip in diff_removed:
            for x in json_ips_date1:
                if flag_regions_removed == None:
                    if x['service'] == service and x['ip_prefix'] == ip:
                        i += 1
                        regions_removed.append(x['region'])
                        print(regions_removed)
                        # This flag indicates that the number of regions found is the same as the number of ips in diff.
                        # Therefore, the iteration can be stopped
                        if i == len(diff_removed):
                            flag_regions_removed = True
                            break
        
        # Finds the regions of the new ipv6 addresses in list "diffv6" by iterating through 
        # "json_ipsv6_date2" and comparing prefixes                 
        i = 0
        for ipv6 in diffv6:
            for x in json_ipsv6_date2:
                if flag_regionsv6 == None:
                    if x['service'] == service and x['ipv6_prefix'] == ipv6:
                        i += 1
                        regionsv6.append(x['region'])
                        
                        # This flag indicates that the number of regions found is the same as the number of ips in diff.
                        # Therefore, the iteration can be stopped
                        if i == len(diffv6):
                            flag_regionsv6 = True
        
        # Finds the regions of the removed ipv6 addresses in list "diffv6_removed" by iterating through 
        # "json_ipsv6_date1" and comparing prefixes                      
        i = 0
        for ipv6 in diffv6_removed:
            for x in json_ipsv6_date1:
                if flag_regionsv6_removed == None:
                    if x['service'] == service and x['ipv6_prefix'] == ipv6:
                        i += 1
                        regionsv6_removed.append(x['region'])
                        
                        # This flag indicates that the number of regions found is the same as the number of ips in diff.
                        # Therefore, the iteration can be stopped
                        if i == len(diffv6_removed):
                            flag_regionsv6_removed = True

        
        body = {
            'diff': diff,
            'diff_removed': diff_removed,
            'diffv6': diffv6,
            'diffv6_removed': diffv6_removed,
            'ips1': ips,
            'ips2': ips2,
            'ipv6': ipsv6,
            'ipv6_2': ipsv6_2,
            'regions': regions,
            'regions_removed': regions_removed,
            'regionsv6': regionsv6,
            'regionsv6_removed': regionsv6_removed
        }
            
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(body)
        }
        
    except Exception as e:
        print('Exception occured :' + str(e))
        raise e
        
    
        
def lambda_handler(event, context):
    
    event_json = json.dumps(event)
    loaded_event_json = json.loads(event_json)
        
    try:
        http_method = loaded_event_json['httpMethod']
    except:
        http_method = ''
    
    if http_method == 'POST':
        
        if loaded_event_json['queryStringParameters'] != None:
            
            queryStrings = loaded_event_json['queryStringParameters']
            
            service = queryStrings['service'].upper()
            date1 = queryStrings['date1']
            date2 = queryStrings['date2']

            r = pullDataFromS3(service, date1, date2)
        
        else:

            body_payload = json.loads(loaded_event_json['body'])
        
            # Takes the body from the APGW event and stores its values and their corresponding variables
            service = body_payload['service'].upper()
            date1 = body_payload['date1']
            date2 = body_payload['date2']

            r = pullDataFromS3(service, date1, date2)
        
        return r
        
    # Falls under here when the request method is not POST. 
    # The front-end does a GET on page load to retrieve the date
    # in which the objects were create so that it can populate the dropdowns
    else:
        
        dates_dropdown = []
        j = 0
        
        s3 = boto3.client('s3')
        
        r = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            StartAfter='ips-json/'
            )
        
        
        objs = r['Contents']

        for x in objs:
            
            #  DEPRECATED
            # last_modified = objs[j]['LastModified']
            # date_converted = last_modified.strftime('%Y-%m-%d')
            # if not date_converted in dates_dropdown:
            #     dates_dropdown.append(date_converted)
                
            # Takes the object key(e.g ips-json/2018-09-30.json) and turns it into 2018-09-30
            obj_name = objs[j]['Key'].split('/')[1].split('.')[0]
            dates_dropdown.append(obj_name)
            
            j+=1
        

        return {
            "statusCode": 200,
            "headers": { 
                "Access-Control-Allow-Origin": "*"
            },
            "body": dates_dropdown
        }
    