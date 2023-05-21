import pytest
from app.utils.graph import *
from app.utils.graph import _get_graph_token

@pytest.fixture
def dummy_settings():
    class DummySettings():
        tenant_id: str = "1d2acae1-1a04-4995-95f5-97c38b0c0213"
        app_id: str = "e9c81d56-fc50-44a1-8739-a569a9a6e13a"
        client_secret: str = "DummySecret"
    settings = DummySettings()
    return settings

@pytest.fixture
def dummy_token():
    class DummyToken():
        token: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6IjY1OTg4MGM1YWY5Y2Y1Y2M3MjkxNGYyMjUzM2VlY2U1In0.eyJhdWQiOiJhcGk6Ly9lOWM4MWQ1Ni1mYzUwLTQ0YTEtODczOS1hNTY5YTlhNmUxM2EiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8xZDJhY2FlMS0xYTA0LTQ5OTUtOTVmNS05N2MzOGIwYzAyMTMvIiwiaWF0IjoxNjg0NTgxMDA2LCJuYmYiOjE2ODQ1ODEwMDYsImV4cCI6MTY4NDU4NTQzMCwiYWNyIjoiMSIsImFpbyI6IkFhUUFXLzhUQUFBQU5wMFBLWS9zd2FoWEVNQ2J6UjUzRzlYV09wNDc5Um9UM2FqSU8vYWowbUN5UXZLbzdBMCtva2dpZUpxRk1MTXZHNmtKeExzOFNZZ1U4SXM0Qm1Ba0w2c1NBQjNSZytOekxMdm5uaU1QNVJFRmliSVBIbU93SXFoL054dDFxbWJJRVExTkJHRU1hS0FVWmhMVUJQdTZnOExDbWF1VmpaVVV6bGpaUGo0QTdueVdQSHdOTk9IaE1OUGJBRGtUajRudEJndmlyRzJGUFdiZDlDOVg4NHhlQWc9PSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwaWQiOiJlOWM4MWQ1Ni1mYzUwLTQ0YTEtODczOS1hNTY5YTlhNmUxM2EiLCJhcHBpZGFjciI6IjEiLCJlbWFpbCI6ImR1bW15X3VzZXJAaG90bWFpbC5jb20iLCJmYW1pbHlfbmFtZSI6IkR1bW15IiwiZ2l2ZW5fbmFtZSI6IlVzZXIiLCJpZHAiOiJsaXZlLmNvbSIsImlwYWRkciI6IjI0LjEzMi4yMzguNCIsIm5hbWUiOiJEdW1teSBVc2VyIiwib2lkIjoiY2FmN2ZhMmMtYTJjYS00Y2VmLTg0YWMtMjAyMGMzZmNlMGExIiwicmgiOiIwLkFYd0FDSlZzeFluXzBFeVY5S28teF9zRmItV0hJclZRaHQxRHQyQkppQkJ4RUhaOEFFWS4iLCJyb2xlcyI6WyJub3JtYWwtcm9sZSJdLCJzY3AiOiJkdW1teV9zY29wZSIsInN1YiI6ImlTNy0xcHVJUWs0RFFIRTNlZk5KNUxVdjc2MF9ydmZGdkRMTUZWUkZZQ0UiLCJ0aWQiOiJjNTZjOTUwOC1mZjg5LTRjZDAtOTVmNC1hYTNlYzdmYjA1NmYiLCJ1bmlxdWVfbmFtZSI6ImR1bW15X3VzZXJAaG90bWFpbC5jb20iLCJ1dGkiOiJEVFFSTTN2bDJrMlVjZkFIRlk0TkFBIiwidmVyIjoiMS4wIn0.LaBc1qN2p_Y5lW1qnBQj58Vj_gPWP_vBRJ3PHYFHWRIWIeJH3ZBExmEkBmIVnsoqNXEf39uYxSDRvaPx4yq-Rw"
        expires_on: str = 1684671181
    token = DummyToken()
    return token

def dummy_get_token(scope:str):
    class DummyToken():
        token: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6IjY1OTg4MGM1YWY5Y2Y1Y2M3MjkxNGYyMjUzM2VlY2U1In0.eyJhdWQiOiJhcGk6Ly9lOWM4MWQ1Ni1mYzUwLTQ0YTEtODczOS1hNTY5YTlhNmUxM2EiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8xZDJhY2FlMS0xYTA0LTQ5OTUtOTVmNS05N2MzOGIwYzAyMTMvIiwiaWF0IjoxNjg0NTgxMDA2LCJuYmYiOjE2ODQ1ODEwMDYsImV4cCI6MTY4NDU4NTQzMCwiYWNyIjoiMSIsImFpbyI6IkFhUUFXLzhUQUFBQU5wMFBLWS9zd2FoWEVNQ2J6UjUzRzlYV09wNDc5Um9UM2FqSU8vYWowbUN5UXZLbzdBMCtva2dpZUpxRk1MTXZHNmtKeExzOFNZZ1U4SXM0Qm1Ba0w2c1NBQjNSZytOekxMdm5uaU1QNVJFRmliSVBIbU93SXFoL054dDFxbWJJRVExTkJHRU1hS0FVWmhMVUJQdTZnOExDbWF1VmpaVVV6bGpaUGo0QTdueVdQSHdOTk9IaE1OUGJBRGtUajRudEJndmlyRzJGUFdiZDlDOVg4NHhlQWc9PSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwaWQiOiJlOWM4MWQ1Ni1mYzUwLTQ0YTEtODczOS1hNTY5YTlhNmUxM2EiLCJhcHBpZGFjciI6IjEiLCJlbWFpbCI6ImR1bW15X3VzZXJAaG90bWFpbC5jb20iLCJmYW1pbHlfbmFtZSI6IkR1bW15IiwiZ2l2ZW5fbmFtZSI6IlVzZXIiLCJpZHAiOiJsaXZlLmNvbSIsImlwYWRkciI6IjI0LjEzMi4yMzguNCIsIm5hbWUiOiJEdW1teSBVc2VyIiwib2lkIjoiY2FmN2ZhMmMtYTJjYS00Y2VmLTg0YWMtMjAyMGMzZmNlMGExIiwicmgiOiIwLkFYd0FDSlZzeFluXzBFeVY5S28teF9zRmItV0hJclZRaHQxRHQyQkppQkJ4RUhaOEFFWS4iLCJyb2xlcyI6WyJub3JtYWwtcm9sZSJdLCJzY3AiOiJkdW1teV9zY29wZSIsInN1YiI6ImlTNy0xcHVJUWs0RFFIRTNlZk5KNUxVdjc2MF9ydmZGdkRMTUZWUkZZQ0UiLCJ0aWQiOiJjNTZjOTUwOC1mZjg5LTRjZDAtOTVmNC1hYTNlYzdmYjA1NmYiLCJ1bmlxdWVfbmFtZSI6ImR1bW15X3VzZXJAaG90bWFpbC5jb20iLCJ1dGkiOiJEVFFSTTN2bDJrMlVjZkFIRlk0TkFBIiwidmVyIjoiMS4wIn0.LaBc1qN2p_Y5lW1qnBQj58Vj_gPWP_vBRJ3PHYFHWRIWIeJH3ZBExmEkBmIVnsoqNXEf39uYxSDRvaPx4yq-Rw"
        expires_on: str = 1684671181
    if "https://graph.microsoft.com/" in scope:
        token = DummyToken()
        return token
    else:
        raise Exception(f"Scope invalid for Microsoft Graph {scope}")

def test_check_graph_connection(mocker, dummy_token):
    mocker.patch(
        'app.utils.graph._get_graph_token',
        return_value = dummy_token
    )
    check_graph_connection()

def test_get_graph_token(mocker, dummy_settings):
    mocker.patch(
        'app.utils.graph.settings',
        return_value = dummy_settings
    )
    mocker.patch(
        'app.utils.graph.ClientSecretCredential.get_token',
        side_effect = dummy_get_token
    )
    dummy_token = dummy_get_token("https://graph.microsoft.com/.default")
    azure_token = _get_graph_token()
    assert azure_token.token == dummy_token.token
    assert azure_token.expires_on == dummy_token.expires_on

# def test_check(mocker, dummy_token):
#     mocker.patch(
#         'app.utils.graph._get_graph_token',
#         return_value = dummy_token
#     )
#     with pytest.raises(Exception, match=f"Unexpected error while searching for user 17ef72f8-ff58-4279-aa87-667941e69fc4 in Microsoft Graph. Returned response from Microsoft: {UNEXPECTED_ERROR}"):
#         user = get_graph_user("17ef72f8-ff58-4279-aa87-667941e69fc4")
    # print(user.json())
    # print(user.status_code)
    # assert user.json() == "123"


## CORRECT USER
EXISTENT_USER = {
    '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users/$entity',
    'businessPhones': [],
    'displayName': 'test', 
    'givenName': None, 
    'jobTitle': None, 
    'mail': None, 
    'mobilePhone': None, 
    'officeLocation': None, 
    'preferredLanguage': None, 
    'surname': None, 
    'userPrincipalName': 
    'test@test.com', 
    'id': 'f35ef496-4935-4269-bd9b-0b329471aa94'
}

## WRONG USER ID
NON_EXISTENT_USER = {
    'error': {
        'code': 'Request_ResourceNotFound', 
        'message': "Resource '79390e24-95ca-4a0e-a87f-bbeca8e710b6' does not exist or one of its queried reference-property objects are not present.", 
        'innerError': {'date': '2023-05-21T10:15:14', 'request-id': 'db8fc38f-e06b-4263-971b-ea9fd9198f42', 'client-request-id': 'db8fc38f-e06b-4263-971b-ea9fd9198f42'}
    }
}

UNEXPECTED_ERROR = {
    'error': {
        'code': 'InvalidAuthenticationToken', 
        'message': 'Invalid signing algorithm.', 
        'innerError': {'date': '2023-05-21T10:57:04', 'request-id': '26c4d63f-e124-4f88-aac1-4ca100cecf12', 'client-request-id': '26c4d63f-e124-4f88-aac1-4ca100cecf12'}
    }
}

def test_get_graph_user(mocker, requests_mock, dummy_token):
    mocker.patch(
        'app.utils.graph._get_graph_token',
        return_value = dummy_token
    )
    requests_mock.get(
        'https://graph.microsoft.com/v1.0/users/f35ef496-4935-4269-bd9b-0b329471aa94',
        request_headers={"Authorization":dummy_token.token},
        json=EXISTENT_USER,
        status_code=200
    )
    requests_mock.get(
        'https://graph.microsoft.com/v1.0/users/79390e24-95ca-4a0e-a87f-bbeca8e710b6',
        request_headers={"Authorization":dummy_token.token},
        json=NON_EXISTENT_USER,
        status_code=404
    )
    requests_mock.get(
        'https://graph.microsoft.com/v1.0/users/17ef72f8-ff58-4279-aa87-667941e69fc4',
        request_headers={"Authorization":dummy_token.token},
        json=UNEXPECTED_ERROR,
        status_code=401
    )
    existent_user = get_graph_user("f35ef496-4935-4269-bd9b-0b329471aa94")
    assert existent_user == EXISTENT_USER, f"{existent_user} should be {EXISTENT_USER}. Because this is a valid user."
    non_existent_user = get_graph_user("79390e24-95ca-4a0e-a87f-bbeca8e710b6")
    assert non_existent_user == None, f"{non_existent_user} should be {None}. Because user f35ef496-4935-4269-bd9b-0b329471aa94 doesn't exist."
    with pytest.raises(Exception, match=rf'{UNEXPECTED_ERROR}'):
        user = get_graph_user("17ef72f8-ff58-4279-aa87-667941e69fc4")
    

