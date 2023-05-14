import msal
from app.utils.config import settings
import logging
from azure.identity import DefaultAzureCredential, ClientSecretCredential

logger = logging.getLogger(__name__)

# Enter the details of your AAD app registration
client_id = settings.app_id
client_secret = settings.client_secret
authority = f'https://login.microsoftonline.com/{settings.tenant_id}'
scope = ['https://graph.microsoft.com/.default']

# Create an MSAL instance providing the client_id, authority and client_credential parameters
# client: msal.ConfidentialClientApplication = None
# logger.info("I am here in graph.py")
# client = msal.ConfidentialClientApplication(client_id=client_id, authority=authority, client_credential=client_secret)

# # First, try to lookup an access token in cache
# token_result = client.acquire_token_silent(scope, account=None)

# # If the token is available in cache, save it to a variable
# if token_result:
#   access_token = 'Bearer ' + token_result['access_token']
#   print('Access token was loaded from cache')

# # If the token is not available in cache, acquire a new one from Azure AD and save it to a variable
# if not token_result:
#   token_result = client.acquire_token_for_client(scopes=scope)
#   print(token_result)
#   access_token = 'Bearer ' + token_result['access_token']
#   print('New access token was acquired from Azure AD')

default_credential = ClientSecretCredential(tenant_id=settings.tenant_id, client_id=client_id, client_secret=client_secret)
access_token = default_credential.get_token("https://graph.microsoft.com/.default")


def test_graph():
    print(access_token)