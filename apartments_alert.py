from time import time
import numpy as np
from requests_html import HTMLSession
from twilio.rest import Client

lux = 'https://www.on-site.com/web/online_app/choose_unit?goal=6&attr=x20&property_id=225322&lease_id=0&unit_id=0&required='
three_60 = 'https://www.on-site.com/web/online_app/choose_unit?goal=6&attr=x20&property_id=191247&lease_id=0&unit_id=0&required='

def get_html(url):
    session = HTMLSession()
    req = session.get(url)
    paragraphs = req.html.find('p')
    paragraphs = paragraphs[:-3]

    return paragraphs

def make_dict(ps):
    current_plan = ""
    d = {}
    for p in ps:
        if (p.attrs['class'][0] == 'floor_plan_name') & (p.text not in d):
            d[p.text] = []
            current_plan = p.text
        else:
            d[current_plan].append(p.text)
    return d

def get_difference(d_before, d_current):
    message = ""
    if (len(d_before)) > len(d_current):
        taken = ", ".join(d_before.keys() - d_current.keys())
        message = "Listing removed update: " + taken
    else:
        added = ", ".join(d_current.keys() - d_before.keys())
        message = "New listing update: " + added

    return message

def send_sms(message):
    account_sid = 'ACb89be4618d01504371ee5a71581e0a4d' 
    auth_token = '257e09038f86713f5d78f6e025a0ebdb' 
    client = Client(account_sid, auth_token) 
    
    # sending to so
    message = client.messages.create(messaging_service_sid='MG9b262dfc07ca251f557ea5206000f0cc', body=message, to='+16502914624') 
    # sending to zack
    message = client.messages.create(messaging_service_sid='MG9b262dfc07ca251f557ea5206000f0cc', body=message, to='+17605045501') 
    # sending to peter
    message = client.messages.create(messaging_service_sid='MG9b262dfc07ca251f557ea5206000f0cc', body=message, to='+16193175276') 
    

minute_before_lux_d = make_dict(get_html(three_60))
minute_before_three_60_d = make_dict(get_html(lux))


while (True):
    three_60_d = make_dict(get_html(three_60))
    lux_d = make_dict(get_html(lux))

    if len(minute_before_lux_d) != len(lux_d):
        message = get_difference(minute_before_lux_d, lux_d)
        minute_before_lux_d = lux_d
        send_sms(message)

    if len(minute_before_three_60_d) != len(three_60_d):
        message = get_difference(minute_before_three_60_d, three_60_d)
        minute_before_three_60_d = three_60_d
        send_sms(message)
    
    print("Current status: ")
    print("Lux UTC: " + ", ".join(lux_d.keys()))
    print("360 Luxury: " + ", ".join(three_60_d.keys()))
    time.sleep(60)





