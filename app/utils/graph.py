from app.utils.config import settings
import logging
from azure.identity import ClientSecretCredential

logger = logging.getLogger(__name__)

client_id = settings.app_id
client_secret = settings.client_secret
authority = f'https://login.microsoftonline.com/{settings.tenant_id}'
scope = 'https://graph.microsoft.com/.default'

credential = ClientSecretCredential(tenant_id=settings.tenant_id, client_id=client_id, client_secret=client_secret)

def check_graph_connection():
    get_graph_token()

def get_graph_token():
    access_token = credential.get_token(scope)
    return access_token