# alarms-by-id-fiole.py

from c8y_api import CumulocityApi
from collections import OrderedDict
from datetime import date, timedelta, datetime
from dotenv import load_dotenv
import sys
import os


def getIDsFromCmdline():
    result = set()
    if len(sys.argv) == 0:
        print("No arguments provided")
        return result
    for i in range(1, len(sys.argv)):
        result.add(sys.argv[i])
#        print(sys.argv[i])
    return result

def getIDsFromFile():
    result = set()
    if len(sys.argv) == 2:
        fname = sys.argv[1]
        try:
            fl = open(fname, "r")
        except OSError:
            print(f"File '{fname}' can not be opened. Quit.")
            exit(1)
        for line in fl:
            ids = line.split()
            for id in ids:
                result.add(id)
        return result 
    else:
        print(f"Usage: {argv[0]} <FILE_WITH_IDS>")
        exit(0)
            
def getIDs():
    return getIDsFromCmdline()
#    return getIDsFromFile()
#
# =============================================================================
#
load_dotenv()   # load c8y credential from .env file
BASE_URL = os.getenv('C8Y_BASE_URL')
TENANT_ID = os.getenv('C8Y_TENANT_ID')
USERNAME = os.getenv('C8Y_USERNAME')
PASSWORD = os.getenv('C8Y_PASSWORD')


c8y = CumulocityApi(base_url=BASE_URL, tenant_id=TENANT_ID, username=USERNAME, password=PASSWORD)


print("\nalarms-by-id-file.py")

if c8y == None:
    print("Cannot instantiate the Cumulocity API")
    quit()

ids = getIDs()
if len(ids) == 0:
    print("No ID(s) provided. Quit.")
    quit()

print("Alarms for selected device IDs")
print(f"{ids}")

num_ups = 0
num_files = 0
for id in ids:
    num_ups += 1
    ups = c8y.device_inventory.get(id)
    sn = ups.fragments['c8y_Hardware']['serialNumber']
    end_date = date.today()
    start_date = end_date - timedelta(days=60)

    print("==================================================================================================")
    print(f"#{id} from {start_date} to {end_date}")
    data_alarms = c8y.alarms.get_all(source=id, after=start_date, before=end_date)

    if len(data_alarms) == 0:
      print("No alarms registered")
    else:
      filename = sn + '-' + id + ".json"
      print(f"Alarms log is written to '{filename}'")

      outf = open(filename, "w")
      num_files += 1
      #print("\nALARMS:\n")
      for alarm in data_alarms:
        #print(alarm.to_json())
        outf.write(str(alarm.to_json()))
        outf.write("\n\n")
      outf.close() 
      
print("==================================================================================================")
print(f"{num_ups} UPS analyzed, {num_files} JSON file(s) created")
print("Completed")
    
