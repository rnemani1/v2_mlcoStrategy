from twilio.rest import Client
from datetime import datetime

account_sid = 'ACae3c6bf7c3b06eb335b1f06a5e3c4d74'
auth_token = 'cf32a22a4fadddabf6506d3f5361913d'
client = Client(account_sid, auth_token)

numbers = ['+19806225619', '+19806216434']
#numbers = ['+19806225619', '+19806216434', '+14845056035']

def text(case, league, fTeam, fmLine):

    for number in numbers:

        body = f'{league}: Cash-{case} {fTeam} @{fmLine}'

        client.messages.create(
            body = body,
            from_ = '+13252465980',
            to = number
        )
    
    print(f'{league}: Cash-{case} {fTeam} @{fmLine}')