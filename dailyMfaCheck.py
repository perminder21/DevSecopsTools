### Python Version 3.7 Used
import boto3
import logging
import os
import json
from urllib.request import Request, urlopen, URLError, HTTPError

# Setting up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(context,event):
   
    client                  = boto3.client('iam')
    response                = client.list_users()
    userVirtualMfa          = client.list_virtual_mfa_devices()
    mfaNotEnabled           = []
    virtualEnabled          = []
    physicalString          = ''
    notusers = ("jenkins" <<<<<Add the Users which are not required in the slack message, add as tuple)
    
    # loop through users to find users MFA Status.
    for user in response['Users']:
        userMfa  = client.list_mfa_devices(UserName=user['UserName'])
        # If the Users don't have MFA enabled, then it will be appended in the list
        if len(userMfa['MFADevices']) == 0:
            if user['UserName'] not in virtualEnabled:
                if not user['UserName'].startswith(notusers):
                    mfaNotEnabled.append(user['UserName'])
     
    if len(mfaNotEnabled) > 0:
        physicalString = 'Physical & Virtual MFA is not enabled for the following users: \n\n' + '\n'.join(mfaNotEnabled)
    else:
        physicalString = 'All Users have Physical and Virtual MFA enabled'
    

    slack_message = {
      "channel": "<<CHANNEL NAME>>",
      "text": physicalString,
      "username": "AWS - MFA Device not enabled for following accounts"
    }
    logger.info(str(slack_message))
    
    req = Request(
        "<<WEBHOOK for SLACK >>",
      data=json.dumps(slack_message).encode("utf-8"),
     headers={"content-type": "application/json"}
    )
    try:
      response = urlopen(req)
      response.read()
      logger.info("Message posted to: %s", slack_message['channel'])
    except HTTPError as e:
       logger.error("Request failed : %d %s", e.code, e.reason)
    except URLError as e:
       logger.error("Server connection failed: %s", e.reason)
    
    return mfaNotEnabled
