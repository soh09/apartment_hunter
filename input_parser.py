import json
import sys
from time import sleep
from requests_html import HTMLSession

inputs = {
    'links': [],
    'names': [],
    'account_sid': '',
    'auth_token': '',
    'service_sid': '',
    'numbers': [],
    'frequency': 60
}

print("This program will ensure that your inputs are valid, so the alert program runs properly.\n")

print("First, input the links for the apartment application portals that you want to scrape, and the name of the apartment.")
print("Note that this program currently only works for sites with links that start with \"https://www.on-site.com\"")
print("Once you are done inputting the links, type \"done\".\n")

counter = 1
link = ''

# constructs the link list
link = input("Link #{}: ".format(counter))
while (link != 'done'):
    link = link.replace(" ", "")
    # checking if the input link is a valid on-site website link
    if (link[:51] != "https://www.on-site.com/web/online_app/choose_unit?"):
        print("<Invalid Link> This link doesn't start with \n\"https://www.on-site.com/web/online_app/choose_unit?\"\n which means the alerts probably won't work.")
        print("If you have different links, feel free to try those out.")
    elif (link in inputs["links"]):
        print("<Duplicate Link> You can't have duplicate links. Input another one, or type \"done\".")
    else:
        try:
            session = HTMLSession()
            req = session.get(link)
        except Exception:
            print("<Fetch Error> There was an error fetching that link. Check for typos, or try another one.")
            continue
        if (req.status_code != 200):
            print("<Fetch Error> There was an error fetching that link. Check for typos, or try another one.")
        else:
            name = input("What do you want to call this building? (You can input the name of the building, or a different unique identifier)\n")
            if (name.strip() == ""):
               print("<Invalid Name> Name must not be all spaces.")
            elif (name in inputs['names']):
                print("<Duplicate Name> Name for building must be unique.")
            else:
                inputs['links'].append(link)
                inputs['names'].append(name)
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
print("\nNext, input all the numbers you'd like to send the text alerts to.")
print("Please follow this format: the number '012-345-6789' would be `country code` + '0123456789'.")
print("For example, if this is a US number, then the number would be inputted as '10123456789'.\n")

print("You can customize who recieves notifications about which building. This helps you save Twilio credits, because it'll prevent sending unnecessary notifications.\n")
customize = input("Would you like to customize? Type \"y\" for yes, type anything else for no.\n").lower()

if customize == 'y':
    # code for customizing, a for loop that goes through each building name
    for name in inputs["names"]:
        inputs["{}_numbers".format(name)] = []
        counter = 1
        print("\nOnce you're done inputting numbers for {}, type \"done\".".format(name))
        number = input("Phone number {} for \"{}\": ".format(counter, name))
        while (number != "done"):
            if (number.isdigit() == False):
                print("<Invalid Number> Input is not a phone number, or is not formatted correctly. You may only input numbers.")
            elif (len(number) <= 10):
                print("<Invalid Number> The length of the phone number is short. Did you forget to add the country code?")
            elif (number in inputs["numbers"]):
                print("<Duplicate Numbers> This number is already registered for {}. Type \"done\" when done.".format(name))
            else:
                inputs["{}_numbers".format(name)].append(number)
                counter += 1
            number = input("Phone number {} for \"{}\": ".format(counter, name))
else:
    print("Once you're done inputting numbers, type \"done\".")
    counter = 1
    number = input("Phone number {}: ".format(counter))
    while (number != "done"):
        if (number.isdigit() == False):
            print("<Invalid Number> Input is not a phone number, or is not formatted correctly. You may only input numbers.")
        elif (len(number) <= 10):
            print("<Invalid Number> The length of the phone number is short. Did you forget to add the country code?")

        else:
            inputs["numbers"].append(number)
            counter += 1
        number = input("Phone number {}: ".format(counter))

print("\nFinally, you can change the update frequncy of the prorgram.")
print("By default, the program will visit the urls every 60 seconds and checks for updates.")
print("I do not recommend updating more than once every minute, but you may change this interval if you'd like.")
change_frequency = input("Type \"y\" if you would like to change the frequency. Type any other character to skip this step.\n")

if (change_frequency.lower() == 'y'):
    valid = False
    while(valid == False):
        interval = input("Type the new update frequency as whole numbers in seconds: ")
        if (interval.isdigit()):
            valid = True
            if (int(interval) < 60):
                print("Beware that this program hasn't been tested for update frequencies less than 60 seconds. The program may error.")
            inputs["frequency"] = int(interval)
        else:
            print("<Invalid Input> Make sure that your input is formatted like \"60\", or \"121\".\n")


print("Generating input.json file.")
# sys.path ensures that the json files are stored in the same directory as apartments_alert.py
with open(sys.path[0] + '/input.json', 'w') as f:
    json.dump(inputs, f)
sleep(3)
print("Exiting program.")