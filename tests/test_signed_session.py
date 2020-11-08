import pytest

from xbox.webapi.common.signed_session import SignedSession

from tests.common import get_response


@pytest.mark.asyncio
async def test_sending_signed_request(aresponses):
    aresponses.add("xsts.auth.xboxlive.com", response=get_response("auth_xsts_token"))

    signed_session = SignedSession()

    async with signed_session:
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

    aresponses.assert_plan_strictly_followed()
    assert resp.request_info.headers.get("Signature") is not None
