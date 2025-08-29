import os
from c8y_api import CumulocityApi
from dotenv import load_dotenv
from collections import OrderedDict

# =============================================================================

def listSerialNumbers(serial_numbers):
  sns = serial_numbers
  num = len(sns)
  col_width = 14

  for i in range(0, num, 5):
    row = sns[i:i+5]
    print("".join(word.ljust(col_width) for word in row))
  
# =============================================================================

print("\nS/Ns of UPS by country")

# Load c8y login credentials from .env file
load_dotenv()
BASE_URL = os.getenv('C8Y_BASE_URL')
TENANT_ID = os.getenv('C8Y_TENANT_ID')
USERNAME = os.getenv('C8Y_USERNAME')
PASSWORD = os.getenv('C8Y_PASSWORD')

# Login to c8y
c8y = CumulocityApi(base_url=BASE_URL, tenant_id=TENANT_ID, username=USERNAME, password=PASSWORD)

if c8y == None:
    print("Cannot instantiate the Cumulocity API")
    quit()

num_ups = 0
num_no_ups = 0
ups_by_country = {}

print("Getting all devices from Cumulocity...")
devices = c8y.device_inventory.get_all()

print("Analyzing devices info...")
for device in devices:
  if device.type != "UPS_Device":  
    num_no_ups += 1
  else:
    num_ups += 1
    try:
        country = device.fragments['Country']
    except KeyError:
        country = '<Country not Defined>'
    try:
      serial_number = device.fragments['c8y_Hardware']['serialNumber']
    except KeyError:
      serial_number = "* Not Defined *"

    if not country in ups_by_country:
      ups_by_country[country] = []

    ups_by_country[country].append(serial_number)

print("Sorting the results by country...")
sorted_ups_by_country = OrderedDict(sorted(ups_by_country.items()))

for country in sorted_ups_by_country:
  print(f"{country}")
  listSerialNumbers(sorted_ups_by_country[country])
  print()

print(f"{num_ups} UPS in total, {num_no_ups} non-UPS devices")
print("Report completed")