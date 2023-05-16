from app.utils.config import settings
import requests
import logging
from azure.identity import ClientSecretCredential

logger = logging.getLogger(__name__)

client_id = settings.app_id
client_secret = settings.client_secret
authority = f'https://login.microsoftonline.com/{settings.tenant_id}'
scope = 'https://graph.microsoft.com/.default'
url = "https://graph.microsoft.com/v1.0"

credential = ClientSecretCredential(tenant_id=settings.tenant_id, client_id=client_id, client_secret=client_secret)

def check_graph_connection():
    logger.info("Checking connection to Microsoft Graph...")
    _get_graph_token()
    logger.info("Connection to Microsoft Graph succeeded!")

def _get_graph_token():
    access_token = credential.get_token(scope)
    return access_token

def get_user(id: str):
    url = f"{url}/v1.0/users/{id}"
    token = _get_graph_token().token
    headers = {
        "Authorization": token
    }
    r = requests.get(url, headers=headers)
    return r
