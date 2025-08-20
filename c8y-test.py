# c8y-test.py

from c8y_api import CumulocityApi
from dotenv import load_dotenv
import os

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
else:
    print("Cumulocity API initialized OK")
