import time
from requests_html import HTMLSession
from twilio.rest import Client
from datetime import datetime


lux = 'https://www.on-site.com/web/online_app/choose_unit?goal=6&attr=x20&property_id=225322&lease_id=0&unit_id=0&required='
three_60 = 'https://www.on-site.com/web/online_app/choose_unit?goal=6&attr=x20&property_id=191247&lease_id=0&unit_id=0&required='
cv = 'https://www.on-site.com/web/online_app/choose_unit?goal=6&attr=x20&property_id=1166&lease_id=0&unit_id=0&required='

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

def get_difference(name, d_before, d_current, url):
    message = ""
    if (len(d_before)) > len(d_current):
        taken = ", ".join(d_before.keys() - d_current.keys())
        message = "[" + name + "] " + "Listing removed update: " + taken
    else:
        added = ", ".join(d_current.keys() - d_before.keys())
        message = "[" + name + "] " + "New listing update: " + added + " [Website]: " + url

    return message

def send_so_sms(message):
    account_sid = 'ACb89be4618d01504371ee5a71581e0a4d' 
    auth_token = '257e09038f86713f5d78f6e025a0ebdb' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create(messaging_service_sid='MG9b262dfc07ca251f557ea5206000f0cc', body = message, to='16502914624')

def send_zack_sms(message):
    account_sid = 'ACb89be4618d01504371ee5a71581e0a4d' 
    auth_token = '257e09038f86713f5d78f6e025a0ebdb' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create(messaging_service_sid='MG9b262dfc07ca251f557ea5206000f0cc', body=message, to='17605045501')

def send_peter_sms(message):
    account_sid = 'ACb89be4618d01504371ee5a71581e0a4d' 
    auth_token = '257e09038f86713f5d78f6e025a0ebdb' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create(messaging_service_sid='MG9b262dfc07ca251f557ea5206000f0cc', body=message, to='16193175276')

def send_sam_sms(message):
    account_sid = 'ACb89be4618d01504371ee5a71581e0a4d' 
    auth_token = '257e09038f86713f5d78f6e025a0ebdb'
    client = Client(account_sid, auth_token) 
    message = client.messages.create(messaging_service_sid='MG9b262dfc07ca251f557ea5206000f0cc', body=message, to='16266861588')

def send_adrian_sms(message):
    account_sid = 'ACb89be4618d01504371ee5a71581e0a4d' 
    auth_token = '257e09038f86713f5d78f6e025a0ebdb'
    client = Client(account_sid, auth_token)
    message = client.messages.create(messaging_service_sid='MG9b262dfc07ca251f557ea5206000f0cc', body=message, to='18476248866')

def send_dang_sms(message):
    account_sid = 'ACb89be4618d01504371ee5a71581e0a4d' 
    auth_token = '257e09038f86713f5d78f6e025a0ebdb'
    client = Client(account_sid, auth_token)
    message = client.messages.create(messaging_service_sid='MG9b262dfc07ca251f557ea5206000f0cc', body=message, to='16692437630') 

  

minute_before_lux_d = make_dict(get_html(lux))
minute_before_three_60_d = make_dict(get_html(three_60))
minute_before_cv_d = make_dict(get_html(cv))


while (True):
    three_60_d = make_dict(get_html(three_60))
    lux_d = make_dict(get_html(lux))
    cv_d = make_dict(get_html(cv))

    if len(minute_before_lux_d) != len(lux_d):
        message = get_difference("Lux UTC", minute_before_lux_d, lux_d, lux)
        minute_before_lux_d = lux_d
        print("sending update: " + message)
        send_so_sms(message)
        send_zack_sms(message)
        # send_sam_sms(message, lux)
        send_peter_sms(message)
        send_adrian_sms(message)

    if len(minute_before_three_60_d) != len(three_60_d):
        message = get_difference("360", minute_before_three_60_d, three_60_d, three_60)
        minute_before_three_60_d = three_60_d
        print("sending update: " + message)
        send_so_sms(message)
        send_zack_sms(message)
        # send_sam_sms(message, lux)
        send_peter_sms(message)
        send_adrian_sms(message)
    
    if len(minute_before_cv_d) != len(cv_d):
        message = get_difference("Costa Verde", minute_before_cv_d, cv_d, cv)
        minute_before_cv_d = cv_d
        print("sending update: " + message)
        send_so_sms(message)
        send_zack_sms(message)
        # send_sam_sms(message, lux)
        send_peter_sms(message)
        send_adrian_sms(message)
        send_dang_sms(message)

    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    
    print("--------------------------------------")
    print("Current status at " + dt_string+ ": ")
    print("Lux UTC: " + ", ".join(lux_d.keys()))
    print("360: " + ", ".join(three_60_d.keys()))
    print("Costa Verde Villages: " + ", ".join(cv_d.keys()))
    print("--------------------------------------")
    time.sleep(60)

