from app.utils.config import settings
import requests
import logging
from azure.identity import ClientSecretCredential

logger = logging.getLogger(__name__)

authority = f'https://login.microsoftonline.com/{settings.tenant_id}'
scope = 'https://graph.microsoft.com/.default'
url = "https://graph.microsoft.com/v1.0"

def check_graph_connection():
    logger.info("Checking connection to Microsoft Graph...")
    _get_graph_token()
    logger.info("Connection to Microsoft Graph succeeded!")

def _get_graph_token():
    credential = ClientSecretCredential(tenant_id=settings.tenant_id, client_id=settings.app_id, client_secret=settings.client_secret)
    access_token = credential.get_token(scope)
    return access_token

def get_user(id: str):
    endpoint = f"{url}/users/{id}"
    token = _get_graph_token().token
    headers = {
        "Authorization": token
    }
    r = requests.get(endpoint, headers=headers)
    return r

def list_group_members(id: str):
    endpoint = f"{url}/groups/{id}/members"
    token = _get_graph_token().token
    headers = {
        "Authorization": token
    }
    r = requests.get(endpoint, headers=headers)
    return r

def create_group_graph(name: str, description: str, user_id: str):
    endpoint = f"{url}/groups"
    token = _get_graph_token().token
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "description": description,
        "displayName": name,
        "groupTypes": [
        ],
        "mailEnabled": False,
        "mailNickname": "devops",
        "securityEnabled": True,
        "owners@odata.bind": [
            f"{url}/users/{user_id}"
        ],
        "members@odata.bind": [
            f"{url}/users/{user_id}"
        ]
    }   
    try:
        r = requests.post(endpoint, headers=headers, json=data)
        r.raise_for_status()
    except Exception as e:
        logger.error(f"An error ocurred while trying to create a group: {e}")
        logger.error(f"Response from Microsoft: {r.json()}")
        raise
    return r