import pytest

from xbox.webapi.common.signed_session import SignedSession


@pytest.mark.asyncio
async def test_sending_signed_request():
    signed_session = SignedSession()

    resp = await signed_session.send_signed(
        method="POST",
        url="https://xsts.auth.xboxlive.com/xsts/authorize",
        headers={"x-xbl-contract-version": "1"},
        data={
            "RelyingParty": "http://xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "UserTokens": ["eyJWTblabla"],
                "SandboxId": "RETAIL",
            },
        },
    )

    assert resp.request_info.headers.get("Signature") is not None
