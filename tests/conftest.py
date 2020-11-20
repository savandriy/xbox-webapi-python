from datetime import datetime, timedelta
import json
import os

from aiohttp import ClientSession
from ecdsa.keys import SigningKey, VerifyingKey
import pytest

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import (
    OAuth2TokenResponse,
    XAUResponse,
    XSTSDisplayClaims,
    XSTSResponse,
)
from xbox.webapi.common.request_signer import RequestSigner

from tests.common import get_response

collect_ignore = ["setup.py"]


@pytest.fixture(scope="function")
async def auth_mgr(event_loop):
    mgr = AuthenticationManager(
        ClientSession(loop=event_loop), "abc", "123", "http://localhost"
    )
    mgr.oauth = OAuth2TokenResponse.parse_raw(get_response("auth_oauth2_token"))
    mgr.user_token = XAUResponse.parse_raw(get_response("auth_user_token"))
    mgr.xsts_token = XSTSResponse.parse_raw(get_response("auth_xsts_token"))
    return mgr


@pytest.fixture(scope="function")
def xbl_client(auth_mgr):
    return XboxLiveClient(auth_mgr)


@pytest.fixture(scope="session")
def ecdsa_signing_key_str() -> str:
    with open("tests/data/test_signing_key.pem") as f:
        return f.read()


@pytest.fixture(scope="session")
def ecdsa_signing_key(ecdsa_signing_key_str: str) -> SigningKey:
    return SigningKey.from_pem(ecdsa_signing_key_str)


@pytest.fixture(scope="session")
def ecdsa_verifying_key() -> VerifyingKey:
    with open("tests/data/test/verifying_key.pem") as f:
        key = f.read()
    return VerifyingKey.from_pem(key)


@pytest.fixture(scope="session")
def synthetic_request_signer(ecdsa_signing_key) -> RequestSigner:
    return RequestSigner(ecdsa_signing_key)


@pytest.fixture(scope="session")
def synthetic_timestamp() -> datetime:
    return datetime.utcfromtimestamp(1586999965)
