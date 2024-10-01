import logging
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import os
import uvicorn

from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.telephony import PlivoConfig
from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall

from typing import Optional

from vocode.streaming.telephony.server.base import TelephonyServer, PlivoInboundCallConfig

config_manager = InMemoryConfigManager()

app = FastAPI(docs_url=None)
templates = Jinja2Templates(directory="templates")

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BASE_URL = os.getenv("BASE_URL")

PLIVO_CONFIG = PlivoConfig(
  auth_id=os.getenv("PLIVO_AUTH_ID") or "<your twilio account sid>",
  auth_token=os.getenv("PLIVO_AUTH_TOKEN") or "<your twilio auth token>",
)

CONFIG_MANAGER = config_manager  #RedisConfigManager()

AGENT_CONFIG = ChatGPTAgentConfig(
  initial_message=BaseMessage(text="Hello?"),
  prompt_preamble="Have a pleasant conversation about life",
  generate_responses=True,
)

telephony_server = TelephonyServer(
  base_url=BASE_URL,
  config_manager=CONFIG_MANAGER,
  inbound_call_configs=[
    PlivoInboundCallConfig(url="/inbound_call",
                      agent_config=AGENT_CONFIG,
                      plivo_config=PLIVO_CONFIG)
  ],
)
app.include_router(telephony_server.get_router())


async def start_outbound_call(to_phone: Optional[str]):
  if to_phone:
    outbound_call = OutboundCall(base_url=BASE_URL,
                                 to_phone=to_phone,
                                 from_phone="+14152639423",
                                 config_manager=CONFIG_MANAGER,
                                 agent_config=AGENT_CONFIG,
                                 telephony_config=PLIVO_CONFIG)
    await outbound_call.start()


@app.post("/start_outbound_call")
async def api_start_outbound_call():
  await start_outbound_call("+918669145213")
  return {"status": "success"}


uvicorn.run(app, host="0.0.0.0", port=3000)
