import os

from dotenv import load_dotenv

from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.telephony import PlivoConfig, TwilioConfig

load_dotenv()

from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall

BASE_URL = os.environ["BASE_URL"]


async def main():
    config_manager = InMemoryConfigManager()

    outbound_call = OutboundCall(
        base_url=BASE_URL,
        to_phone="+918669145213",
        from_phone="+14152639423",
        config_manager=config_manager,
        agent_config=ChatGPTAgentConfig(
            initial_message=BaseMessage(text="What up"),
            prompt_preamble="Have a pleasant conversation about life",
            generate_responses=True,
        ),
        telephony_config=PlivoConfig(
            auth_id=os.environ["PLIVO_AUTH_ID"],
            auth_token=os.environ["PLIVO_AUTH_TOKEN"],
        ),
    )

    input("Press enter to start call...")
    await outbound_call.start()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
