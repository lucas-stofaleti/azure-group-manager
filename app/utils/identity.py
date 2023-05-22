import httpx
import logging
from httpx import Response
from fastapi import Request
from functools import wraps
from jose import jwt
from fastapi.templating import Jinja2Templates
import msal
from .config import settings

templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

def initialize():
    logger.info("Initalizing Azure Identity...")
    global tenant_id, client_id
    tenant_id = settings.tenant_id
    client_id = settings.app_id
    logger.info("Azure Identity initialized!")

msal_client = msal.ConfidentialClientApplication(
        settings.app_id, authority=f"https://login.microsoftonline.com/{settings.tenant_id}",
        client_credential=settings.client_secret)

class AuthError(Exception):
    def __init__(self, error_msg:str, status_code:int):
        super().__init__(error_msg)

        self.error_msg = error_msg
        self.status_code = status_code

def get_token_auth_cookie(request: Request):
    auth = request.cookies.get("token", None)
    if not auth:
        raise AuthError("Authentication is required", 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError("Authentication error: Authorization header must start with ' Bearer'", 401)
    elif len(parts) == 1:
        raise AuthError("Authentication error: Token not found", 401)
    elif len(parts) > 2:
        raise AuthError("Authentication error: Authorization header must be 'Bearer <token>'", 401)

    token = parts[1]
    return token

def get_token_claims(request: Request):
    token = get_token_auth_cookie(request)
    unverified_claims = jwt.get_unverified_claims(token)
    return unverified_claims 

def validate_scope(required_scope:str, request: Request):
    has_valid_scope = False
    token = get_token_auth_cookie(request)
    unverified_claims = jwt.get_unverified_claims(token)
    ## check to ensure that either a valid scope or a role is present in the token
    if unverified_claims.get("scp") is None and unverified_claims.get("roles") is None:
        raise AuthError("IDW10201: No scope or app permission (role) claim was found in the bearer token", 403)

    is_app_permission = True if unverified_claims.get("roles") is not None else False

    if is_app_permission:
        if unverified_claims.get("roles"):
            # the roles claim is an array
            for scope in unverified_claims["roles"]:
                if scope.lower() == required_scope.lower():
                    has_valid_scope = True
        else:
            raise AuthError("IDW10201: No app permissions (role) claim was found in the bearer token", 403)
    else:
        if unverified_claims.get("scp"):
            # the scp claim is a space delimited string
            token_scopes = unverified_claims["scp"].split()
            for token_scope in token_scopes:
                if token_scope.lower() == required_scope.lower():
                    has_valid_scope = True
        else:
            raise AuthError("IDW10201: No scope claim was found in the bearer token", 403)
   
        
    if is_app_permission and not has_valid_scope:
        raise AuthError(f'IDW10203: The "role" claim does not contain role {required_scope} or was not found', 403)
    elif not has_valid_scope:
        raise AuthError(f'IDW10203: The "scope" or "scp" claim does not contain scopes {required_scope} or was not found', 403) 

async def function():
    try:
        token = get_token_auth_cookie(kwargs["request"])
        url = f'https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys'
        
        async with httpx.AsyncClient() as client:
            resp: Response = await client.get(url)
            if resp.status_code != 200:
                raise AuthError("Problem with Azure AD discovery URL", status_code=404)

            jwks = resp.json()
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
    except AuthError as auth_err:
        client = msal_client.initiate_auth_code_flow(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
        url = client["auth_uri"]
        response = templates.TemplateResponse(
            "pages/login.html", {"request": kwargs["request"], "url": url, "error": auth_err}, status_code=401
        )
        response.set_cookie(key="code_flow", value=client, httponly=True)
        return response

    except Exception as ex:
        client = msal_client.initiate_auth_code_flow(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
        url = client["auth_uri"]
        response = templates.TemplateResponse(
            "pages/login.html", {"request": kwargs["request"], "url": url, "error": ex}, status_code=401
        )
        response.set_cookie(key="code_flow", value=client, httponly=True)
        return response
    if rsa_key:
        try :
            token_version = __get_token_version(token)
            __decode_JWT(token_version, token, rsa_key)
            return f(*args, **kwargs)
        except AuthError as auth_err:
            client = msal_client.initiate_auth_code_flow(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
            url = client["auth_uri"]
            response = templates.TemplateResponse(
                "pages/login.html", {"request": kwargs["request"], "url": url, "error": auth_err}, status_code=401
            )
            response.set_cookie(key="code_flow", value=client, httponly=True)
            return response
    client = msal_client.initiate_auth_code_flow(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
    url = client["auth_uri"]
    response = templates.TemplateResponse(
        "pages/login.html", {"request": kwargs["request"], "url": url, "error": auth_err}, status_code=401
    )
    response.set_cookie(key="code_flow", value=client, httponly=True)
    return response
    pass

def requires_auth(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            token = get_token_auth_cookie(kwargs["request"])
            url = f'https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys'
            
            async with httpx.AsyncClient() as client:
                resp: Response = await client.get(url)
                if resp.status_code != 200:
                    raise AuthError("Problem with Azure AD discovery URL", status_code=404)

                jwks = resp.json()
                unverified_header = jwt.get_unverified_header(token)
                rsa_key = {}
                for key in jwks["keys"]:
                    if key["kid"] == unverified_header["kid"]:
                        rsa_key = {
                            "kty": key["kty"],
                            "kid": key["kid"],
                            "use": key["use"],
                            "n": key["n"],
                            "e": key["e"]
                        }
        except AuthError as auth_err:
            client = msal_client.initiate_auth_code_flow(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
            url = client["auth_uri"]
            response = templates.TemplateResponse(
                "pages/login.html", {"request": kwargs["request"], "url": url, "error": auth_err}, status_code=401
            )
            response.set_cookie(key="code_flow", value=client, httponly=True)
            return response

        except Exception as ex:
            client = msal_client.initiate_auth_code_flow(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
            url = client["auth_uri"]
            response = templates.TemplateResponse(
                "pages/login.html", {"request": kwargs["request"], "url": url, "error": ex}, status_code=401
            )
            response.set_cookie(key="code_flow", value=client, httponly=True)
            return response
        if rsa_key:
            try :
                token_version = __get_token_version(token)
                __decode_JWT(token_version, token, rsa_key)
                return f(*args, **kwargs)
            except AuthError as auth_err:
                client = msal_client.initiate_auth_code_flow(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
                url = client["auth_uri"]
                response = templates.TemplateResponse(
                    "pages/login.html", {"request": kwargs["request"], "url": url, "error": auth_err}, status_code=401
                )
                response.set_cookie(key="code_flow", value=client, httponly=True)
                return response
        client = msal_client.initiate_auth_code_flow(scopes=[settings.scope], redirect_uri=f"{settings.domain}/auth/callback")
        url = client["auth_uri"]
        response = templates.TemplateResponse(
            "pages/login.html", {"request": kwargs["request"], "url": url, "error": auth_err}, status_code=401
        )
        response.set_cookie(key="code_flow", value=client, httponly=True)
        return response
    return decorated

def __decode_JWT(token_version, token, rsa_key):
    if token_version == "1.0":
        _issuer = f'https://sts.windows.net/{tenant_id}/'
        _audience=f'api://{client_id}'
    else:
        _issuer = f'https://login.microsoftonline.com/{tenant_id}/v2.0'
        _audience=f'{client_id}'
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=_audience,
            issuer=_issuer
        )
    except jwt.ExpiredSignatureError:
        raise AuthError("Token error: The token has expired", 401)
    except jwt.JWTClaimsError:
        raise AuthError("Token error: Please check the audience and issuer", 401)
    except Exception as e:
        raise AuthError(f"Token error: Unable to parse authentication: {e}", 401)

def __get_token_version(token):
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("ver"):
        return unverified_claims["ver"]   
    else:
        raise AuthError("Missing version claim from token. Unable to validate", 403)