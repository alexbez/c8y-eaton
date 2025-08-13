# This script connects to Eaton tenancy in Cumulocity
# and fetches info about Connectivity Cards:
# their models and HW revisions

from c8y_api import CumulocityApi
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv
import sys
import os


def normalize_model(model): 
    if "Eaton X-Slot Industrial Gateway Card" in model:
        return "INDGW-X2"
    if "Eaton Gigabit Network Card 3" in model:
        return "NM3"
    if "Eaton Industrial Gateway Card" in model:
        return "INDGW-M2"
    if "Gigabit Network Card" in model:
        return "NM2"
    return model

def country_and_model():
    country = None
    model = None

    if len(sys.argv) == 3:
        country = sys.argv[1]
        model = sys.argv[2]
    else:
        print("Usage: python3 conn-cards-per-country-and-model.py <COUNTRY>|'*' <CARD_MODEL>")
        print("CARD_MODEL: NM2, NM3, INDGW-X2, INDGW-M2")
        exit(1)
    return country, model


set_country, set_model = country_and_model()

print("Connectivity Cards in Cumulocity per country and card model")
print(f"Country:    {set_country}")
print(f"Card model: {set_model}")

load_dotenv()   # load c8y credential from .env file
BASE_URL = os.getenv('C8Y_BASE_URL')
TENANT_ID = os.getenv('C8Y_TENANT_ID')
USERNAME = os.getenv('C8Y_USERNAME')
PASSWORD = os.getenv('C8Y_PASSWORD')

c8y = CumulocityApi(base_url=BASE_URL, tenant_id=TENANT_ID, username=USERNAME, password=PASSWORD)


if c8y == None:
    print("Cannot instantiate the Cumulocity API")
    quit()

num_cc = 0
cc_sn_list = []

print("Wait, it will take some time...")

for d in c8y.device_inventory.select():
    #print(f"{count} #{d.id} '{d.name}' {d.type}, owned by {d.owner}")

    try:
        ups_serial_number = d.fragments['c8y_Hardware']['serialNumber']
    except KeyError:
        ups_serial_number = "<No S/N>"

    try:
        country = d.fragments['Country']
    except KeyError:
        country = '<No country>'

    if (set_country != "*") and (not country == set_country):
        continue

    if d.child_devices != None:
        for cd in d.child_devices:
            #print(dir(cd))
            if cd.name == 'Connectivity Card':
                cc = c8y.inventory.get(cd.id)
                
                try:
                    model = cc.fragments['c8y_Firmware']['name']
                except KeyError:
                    model = cc.fragments['c8y_Hardware']['model']

                model = normalize_model(model)

                try:
                    revision = cc.fragments['c8y_Hardware']['revision']
                except KeyError:
                    revision = ''
                if model == set_model:
                    cc_sn_list.append(country + " " + ups_serial_number)
                    num_cc += 1
print()

cc_sn_list.sort()

print("Checking connectivity cards completed")
print(f"Number of Connectivity Cards of type {set_model}: {num_cc}")
for sn in cc_sn_list:
    print(f"     {sn}")

print(f"Completed on {datetime.now()}")
print(f"(c) Eaton 2025")
