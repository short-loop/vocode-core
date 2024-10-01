import os
from typing import Dict, Optional

import aiohttp
import plivo
from loguru import logger

from vocode.streaming.models.telephony import PlivoConfig
from vocode.streaming.telephony.client.abstract_telephony_client import AbstractTelephonyClient
from vocode.streaming.utils.async_requester import AsyncRequestor


class PlivoBadRequestException(ValueError):
    pass


class PlivoException(ValueError):
    pass

PLIVO_AUTH_ID = os.environ.get("PLIVO_AUTH_ID")
PLIVO_AUTH_TOKEN = os.environ.get("PLIVO_AUTH_TOKEN")

class PlivoClient(AbstractTelephonyClient):
    def __init__(
        self,
        base_url: str,
        maybe_plivo_config: Optional[PlivoConfig] = None,
    ):
        self.plivo_config = maybe_plivo_config or PlivoConfig(
            auth_id=PLIVO_AUTH_ID,
            auth_token=PLIVO_AUTH_TOKEN,
        )
        self.plivo_client = plivo.RestClient(auth_id=PLIVO_AUTH_ID, auth_token=PLIVO_AUTH_TOKEN)
        self.auth = aiohttp.BasicAuth(
            login=self.plivo_config.auth_id,
            password=self.plivo_config.auth_token,
        )
        super().__init__(base_url=base_url)

    def get_telephony_config(self):
        return self.plivo_config

    async def create_call(
        self,
        conversation_id: str,
        to_phone: str,
        from_phone: str,
        record: bool = False,  # currently no-op
        digits: Optional[str] = None,
        telephony_params: Optional[Dict[str, str]] = None,
    ) -> str:
        config = {
            "from_": f"+{from_phone}",
            "to_": f"+{to_phone}",
            "answer_url": self.get_connection_twiml(conversation_id=conversation_id),
            **(telephony_params or {}),
        }
        
        if digits:
            config["digits"] = digits
        
        call = self.plivo_client.calls.create(**config)

        return call["request_uuid"]

    def get_connection_twiml(self, conversation_id: str):
        return f"https://vapi-mum.shortloop.dev/stream/{conversation_id}"

    async def end_call(self, plivo_sid):
        self.plivo_client.calls.hangup(plivo_sid)
