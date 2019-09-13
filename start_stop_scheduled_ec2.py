import json
import boto3
import os
import datetime
from botocore.exceptions import ClientError

weekdays_list=[]
weekends_list=[]
alldays_list=[]


def lambda_handler(event, context):
    today = datetime.datetime.now()
    now=str(today.strftime("%a"))+' '+str(today.strftime("%d"))+' '+str(today.strftime("%B"))+','+str(today.strftime("%Y"))
    #print(now)
# def list_instances_by_tag_value(AutoOffweekend, 'True'):
    ec2client = boto3.client('ec2')
    #print(ec2client)
    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:AutoOffweekend',
                'Values': ['True']
            }
        ]
    )
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            for name in instance["Tags"]:
                if(name['Key']=="Name"):
                    #print(name['Value'])
                    weekdays_list.append(name['Value'])
    #return weekdays_list
    #print("----------------------------Instance which are start at 9 AM and stop at 9 PM from Monday-Friday ------------------------------")
    # for i in weekdays_list:
    #     print(i)
        
    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:AutoOn',
                'Values': ['True']
            }
           
        ]
    )
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            for name in instance["Tags"]:
                if(name['Key']=="Name"):
                    #print(name['Value'])
                    weekends_list.append(name['Value'])
    #return weekends_list
    #print("----------------------------Instance which are start and stop at 9 AM and stop at 9 PM from Monday-Sunday----------------------")
    # for w_list in weekends_list:
    #     print(w_list)    
    
   
    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:AutoOn',
                'Values': ['False']
            }
           
        ]
    )
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            for name in instance["Tags"]:
                if(name['Key']=="Name"):
                    #print(name['Value'])
                    alldays_list.append(name['Value'])
    #return weekends_list
    #print("Instance which are running 24/7 :")
    # for a_list in alldays_list:
    #     print(a_list)
        
    data=now+"\n"
    data=data+"==========Instance which are start at 9 AM and stop at 9 PM from Monday-Friday==========\n"
    for i in weekdays_list:
        data=data+"* "+i+"\n"
    data=data+"==========Instance which are start at 9 AM and stop at 9 PM from Monday-Sunday==========\n"
    for i in weekends_list:
        data=data+"* "+i+"\n"
    data=data+"==========Instance which are running 24/7==========\n"
    for i in alldays_list:
        data=data+"* "+i+"\n"
    
    #print(data)
    
############Email notification
    
    SENDER = "MS-Team1 <aniket.pradhane@blazeclan.com>"
    RECIPIENT = "shashi.prakash@adityabirlacapital.com"
    #CC = "msteam1@blazeclan.com"
    CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "us-east-1"
    SUBJECT = "ABFSSL-Money Tool schedule start/stop report"
    BODY_TEXT = (""
                )
    BODY_HTML = """<html>
                <head></head>
                <body>
                <h1>Patching Update on Server</h1>
                </body>
                </html>
                """            
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    alldata = data

# Try to send the email.
    try:
    #Provide the contents of the email.
           response = client.send_email(
               Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                    
                    'CcAddresses': [
                        'msteam1@blazeclan.com',
                    ],    
               },
               Message={
                   'Body': {
#                       'Html': {
#                           'Charset': CHARSET,
#                           'Data': alldata,
 #                      },
                       'Text': {
                           'Charset': CHARSET,
                           'Data': alldata,
                       },
                    },
                    'Subject': {
                         'Charset': CHARSET,
                         'Data': SUBJECT,
                    },
               },
               Source=SENDER,
            )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])