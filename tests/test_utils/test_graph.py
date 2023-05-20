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

def test_check_graph_connection(mocker, dummy_token):
    mocker.patch(
        'app.utils.graph._get_graph_token',
        return_value = dummy_token
    )
    check_graph_connection()

def test_get_graph_token(mocker, dummy_settings, dummy_token):
    mocker.patch(
        'app.utils.graph.settings',
        dummy_settings
    )
    mocker.patch(
        'app.utils.graph.ClientSecretCredential.get_token',
        return_value = dummy_token
    )
    azure_token = _get_graph_token()
    assert azure_token.token == dummy_token.token
    assert azure_token.expires_on == dummy_token.expires_on