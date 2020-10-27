# DevSecopsTools
Tools for different DevSecOps

1) File name : dailyMfaCheck:
 Description:
    Dailymfacheck is a lambda function to check Daily MFA of Users in any AWS account account.
      a) users can filter the data as well for non-users. 
 Requirements:
      a) Create Cloudwatch Rule to trigger the lambda. 
      b) Slack weebhook and channel name is required to post the message in the channel
