import json
import sys
from requests_html import HTMLSession

inputs = {
    'links': [],
    'account_sid': '',
    'auth_token': '',
    'service_sid': '',
    'numbers': []
}

print("This program will ensure that your inputs are valid, so the alert program runs properly.\n")

print("First, input the links for the apartment application portals that you want to scrape.")
print("Note that this program currently only works for sites with links that start with \"https://www.on-site.com\"")
print("Once you are done inputting the links, type \"next\".\n")

counter = 1
link = ''

# constructs the link list
link = input("Link #{}: ".format(counter))
while (link != 'next'):
    link = link.replace(" ", "")
    # checking if the input link is a valid on-site website link
    if (link[:51] != "https://www.on-site.com/web/online_app/choose_unit?"):
        print("This link doesn't start with \n\"https://www.on-site.com/web/online_app/choose_unit?\"\n which means the alerts probably won't work.")
        print("If you have different links, feel free to try those out.")
    else:
        try:
            session = HTMLSession()
            req = session.get(link)
        except Exception:
            print("There was an error fetching that link. Check for typos, or try another one.")
            continue
        if (req.status_code != 200):
            print("There was an error fetching that link. Check for typos, or try another one.")
        else:
            inputs['links'].append(link)
            counter += 1
    link = input("Link #{}: ".format(counter))


print("\nAccount sid, auth token, and service sid can't be checked by this program if they are valid.\n")
print("I encourage you to try to send text messages to yourself or friends using these credientials beforehand to make sure that they are working properly.\n")

# fetches the account_sid
print("Next, we'll get your Twilio account sid. This can be found on the console, under \"Project Info\".")
account_sid = input("Account sid: ")
inputs['account_sid'] = account_sid.replace(" ", "")

# fetches the auth_token
print("Next, we'll get your Twilio auth token. This can also be found on the console, under \"Project Info\".")
auth_token = input("Auth Token: ")
inputs['auth_token'] = auth_token.replace(" ", "")

# fetches the service_sid
print("Next, we'll get your Twilio messaging service sid. This can be found by navigating to the \"Develop\" tab on the left, under \"Messaging\", then \"Services\".")
service_sid = input("Service sid: ")
inputs['service_sid'] = service_sid.replace(" ", "")


# fetches numbers
print("Finally, input all the numbers you'd like to send the text alerts to. Once done, type \"done\".")
print("Please follow this format: the number '012-345-6789' would be `country code` + '0123456789'.")
print("For example, if this is a US number, then the number would be inputted as '10123456789'.")

number = ''
counter = 1

number = input("Phone number {}: ".format(counter))
while (number != "done"):
    if (number.isdigit() == False):
        print("Input is not a phone number, or is not formatted correctly. You may only input numbers.")
    elif (len(number) <= 10):
        print("The length of the phone number is short. Did you forget to add the country code?")
    else:
        inputs["numbers"].append(number)
        counter += 1
    number = input("Phone number {}: ".format(counter))


# sys.path ensures that the json files are stored in the same directory as apartments_alert.py
with open(sys.path[0] + '/input.json', 'w') as f:
    json.dump(inputs, f)
