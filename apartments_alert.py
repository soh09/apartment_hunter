import time
from requests_html import HTMLSession
from twilio.rest import Client
from datetime import datetime
import json
import sys

def get_html(url):
    """
    This function gets the html content of the target url.
    Input:
        the target url
    Return:
        The 'p' tag html elements from the url
    """
    session = HTMLSession()
    req = session.get(url)
    paragraphs = req.html.find('p')
    paragraphs = paragraphs[:-3]

    return paragraphs

def make_dict(ps):
    """
    This function parses the results of get_html() and makes a dictionary.\n
    For example, if paragraphs (return value of get_html()) looked like this

    [
        <Element 'p' class=('floor_plan_name',)>,
        <Element 'p' class=('floor_plan_size',)>,
        <Element 'p' class=('floor_plan_name',)>,
        <Element 'p' class=('floor_plan_size',)>,
        <Element 'p' class=('floor_plan_name',)>,
        <Element 'p' class=('floor_plan_size',)>
    ]

    then, this function makes a dictionary, where floor_plan_name is the key, and
    floor_plan_size are the values.

    For this specific example, this function would return the following dictionary.

    {
        'Lease Add-On': ['Room w/ shared bath, 500 Sq. Ft.'],
        'Escape 1A 1 Bed/1 Ba': ['1 bed, 1 bath, 874 Sq. Ft.'],
        'Panorama 2B 2 Bed/2 Ba': ['2 bed, 2 bath, 1154 Sq. Ft.']
    }

    'Lease Add-On' represents the the content of the first '<Element 'p' class=('floor_plan_name',)>'
    and '['Room w/ shared bath, 500 Sq. Ft.']' represents the content of the first 
    '<Element 'p' class=('floor_plan_size',)>'.

    Input:
        ps: the 'p' tags from the apartment url (this is the return value of the get_html() function)
    Return:
        the ps in the form of a dictionary
    """
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
    """
    This function takes in the name of the apartment, the url of the apartment leasing website,
    and two dictionaries to compare: d_before and d_current.
    d_before represents the dictionary created from the webpage a minute before, and d_current
    represents the dictionary that was made from the webpage at this time.
    This function is only called when the lengths of the dictionary keys are different; this function
    figures out if a listing was removed, or a listing was added, and builds a different message for
    those two cases. 

    It returns a message which will be passed to the send_message function.

    For example, if name was 'Sky Heights', url was 'url.com', the d_before was:
    {
        'Lease Add-On': ['Room w/ shared bath, 500 Sq. Ft.'],
        'Escape 1A 1 Bed/1 Ba': ['1 bed, 1 bath, 874 Sq. Ft.'],
        'Panorama 2B 2 Bed/2 Ba': ['2 bed, 2 bath, 1154 Sq. Ft.']
    }
    and d_crurrent was:
    {
        'Escape 1A 1 Bed/1 Ba': ['1 bed, 1 bath, 874 Sq. Ft.'],
        'Panorama 2B 2 Bed/2 Ba': ['2 bed, 2 bath, 1154 Sq. Ft.']
    }
    d_current has a shorter key length, which means that a listing was taken off. Therefore, the 
    message returned will be 
    '[Sky Heights] Listing removed update: Lease Add-On'.

    If a new listing was added, the url will also be a part of the message, so that the person who
    recieved the text can apply ASAP.

    Inputs:
        name: name of the apartment
        d_before: dictionary built from the url a minute ago
        d_current: dictionary built from the url right now
        url: the url where the html elements are fetched from
    Returns:
        The update message.
    """
    message = ""
    if (len(d_before)) > len(d_current):
        taken = ", ".join(d_before.keys() - d_current.keys())
        message = "[" + name + "] " + "Listing removed update: " + taken
    else:
        added = ", ".join(d_current.keys() - d_before.keys())
        message = "[" + name + "] " + "New listing update: " + added + " [Website]: " + url

    return message

def send_message(message, account_sid, token, service_sid, number):
    """
    This function sends 'message' to the specified number using the twilio credentials provided.\n
    Inputs:
        message: the content of the text message
        account_sid: twillio account sid
        token: twillio auth token
        service_sid: twillio messaging service sid
        number: number to send the message to
    """
    client = Client(account_sid, token)
    message = client.messages.create(messaging_service_sid = service_sid, body = message, to = number)


# reads in the json file as a dictionary
with open(sys.path[0] + '/input.json', 'r') as j:
    inputs = json.load(j)

# makes a dictionary, which has the names of the building as keys, and the result of make_dict() for that building as the values
old_listings_dicts = {name: make_dict(get_html(link)) for (name, link) in zip(inputs['names'], inputs['links'])}
# makes a dictionary, which has the name of the buiilding as the key, and the link for that building as the value
name_link_d = {name: link for (name, link) in zip(inputs['names'], inputs['links'])}


while (True):

    # putting the entire thing in a try except prevents the program from termintating abruptly, like when the internet goes out.
    try:
        new_listings_dicts = {name: make_dict(get_html(link)) for (name, link) in zip(inputs['names'], inputs['links'])}

        # iterates through the key of new_listing_dicts, which are the building names
        for key in new_listings_dicts.keys():
            # if there is difference in the length of the dictionary
            if len(old_listings_dicts[key]) != len(new_listings_dicts[key]):
                # passes the name, the old dict, new dict, and the url of the building, and constructs a message
                message = get_difference(key, old_listings_dicts[key], new_listings_dicts[key], name_link_d[key])
                # sets the old dict to new dict, since new dict is now the old dict
                old_listings_dicts[key] = new_listings_dicts[key]
                print("sending update: " + message)
                # if lenth of inputs["numbers"] is 0, that indicates that the user customzied who gets notifications for specific buildings
                if len(inputs["numbers"]) == 0:
                    # sending messages to the numbers signed up for this specific building
                    for number in inputs["{}_numbers".format(key)]:
                        send_message(message, inputs["account_sid"], inputs["auth_token"], inputs["service_sid"], number)
                # in the case that the user did not customize, we just send out notifications to every number in inputs["numbers"]
                else:
                    for number in inputs["numbers"]:
                        send_message(message, inputs["account_sid"], inputs["auth_token"], inputs["service_sid"], number)

        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        
        # prints a status message 
        print("--------------------------------------")
        print("Current status at " + dt_string+ ": \n")
        for key in new_listings_dicts.keys():
            print(key + ": " + " ".join(new_listings_dicts[key].keys()))
        print("--------------------------------------")
        # loop runs every inputs["frequency"] seconds.
        time.sleep(inputs["frequency"])
    except Exception as e:
        print(e)

