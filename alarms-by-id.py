# alarms-by-id.py
# Fetches all alarms for the last 60 days for the UPS with the given ID
#
# Usage: python3 alarms-by-id.py <ID> [<ID>]...
#
# Format of the .env file in the current directory:
#C8Y_BASE_URL=<URL to access your tenant on Cumulocity IoT Platform>
#C8Y_TENANT_ID=<Your tenant ID on Cumulocity>
#C8Y_USERNAME=<Your username>
#C8Y_PASSWORD=<Your password>
#

from c8y_api import CumulocityApi
from datetime import date, timedelta, datetime
import sys
import os
from dotenv import load_dotenv

# Gets the list of IDs from the command line
def getIDs():
    result = set()
    if len(sys.argv) == 1:
        return result
    for i in range(1, len(sys.argv)):
        result.add(sys.argv[i])
    return result



print("\nalarms-by-id.py")

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

# Get the list of IDs from the command line
ids = getIDs()
if len(ids) == 0:
    print("No ID(s) provided. Quit.")
    quit()

print("Alarms for selected device IDs")
print(f"{ids}")

for id in ids:
    alarms = {}
    end_date = date.today()
    start_date = end_date - timedelta(days=60)

    print("==================================================================================================")
    print(f"#{id} from {start_date} to {end_date}")
    #data_measurements = c8y.measurements.get_all(source=id, after=start_date, before=end_date)
    data_alarms = c8y.alarms.get_all(source=id, after=start_date, before=end_date)

    if len(data_alarms) == 0:
      print("No alarms registered during the given period")
    else:
      print("\nALARMS:\n")
      for alarm in data_alarms:
        print(alarm.to_json())
        print()

    print()
    print(f"Completed on {date.today()}")
    