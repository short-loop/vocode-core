# import asyncio
# import os
# import logging
#
# from dotenv import load_dotenv
# from livekit.agents import (
#     AutoSubscribe,
#     JobContext,
#     JobProcess,
#     JobRequest,
#     WorkerOptions,
#     cli,
#     llm,
# )
# from livekit.agents.voice_assistant import VoiceAssistant
# from livekit.plugins import openai, deepgram, silero
#
# from vocode.logging import configure_pretty_logging
# from vocode.streaming.action.end_conversation import EndConversationVocodeActionConfig
# from vocode.streaming.agent import ChatGPTAgent
# from vocode.streaming.livekit.livekit_conversation import LiveKitConversation
# from vocode.streaming.models.actions import PhraseBasedActionTrigger, PhraseBasedActionTriggerConfig, PhraseTrigger
# from vocode.streaming.models.agent import ChatGPTAgentConfig
# from vocode.streaming.models.message import BaseMessage
# from vocode.streaming.models.synthesizer import AzureSynthesizerConfig, ElevenLabsSynthesizerConfig
# from vocode.streaming.models.transcriber import DeepgramTranscriberConfig, PunctuationEndpointingConfig
# from vocode.streaming.output_device.livekit_output_device import LiveKitOutputDevice
# from vocode.streaming.synthesizer.azure_synthesizer import AzureSynthesizer
# from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizer
# from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
#
# load_dotenv(dotenv_path=".env")
# sandbox = os.getenv("LIVEKIT_SANDBOX_ID")
# logger = logging.getLogger("voice-assistant")
#
# async def wait_for_termination(conversation: LiveKitConversation, ctx: JobContext):
#     await conversation.wait_for_termination()
#     await conversation.terminate()
#     await ctx.room.disconnect()
#
# def prewarm(proc: JobProcess):
#     proc.userdata["vad"] = silero.VAD.load()
#
#
# async def entrypoint(ctx: JobContext):
#     # initial_ctx = llm.ChatContext().append(
#     #     role="system",
#     #     text=(
#     #         "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
#     #         "You should use short and concise responses, and avoiding usage of unpronouncable punctuation. "
#     #         "You were created as a demo to showcase the capabilities of LiveKit's agents framework, "
#     #         "as well as the ease of development of realtime AI prototypes. You are currently running in a "
#     #         "LiveKit Sandbox, which is an environment that allows developers to instantly deploy prototypes "
#     #         "of their realtime AI applications to share with others."
#     #     ),
#     # )
#
#
#     # logger.info(f"connecting to room {ctx.room.name}")
#     # await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
#     await ctx.connect()
#
#     configure_pretty_logging()
#     output_device = LiveKitOutputDevice(
#         sampling_rate=16000
#     )
#     conversation = LiveKitConversation(
#         output_device=output_device,
#         transcriber=DeepgramTranscriber(
#             DeepgramTranscriberConfig.from_livekit_input_device(
#                 endpointing_config=PunctuationEndpointingConfig(),
#                 api_key=os.getenv("DEEPGRAM_API_KEY"),
#             ),
#         ),
#         agent=ChatGPTAgent(
#             ChatGPTAgentConfig(
#                 openai_api_key=os.getenv("OPENAI_API_KEY"),
#                 initial_message=BaseMessage(text="What up"),
#                 prompt_preamble="""The AI is having a pleasant conversation about life""",
#                 actions=[
#                     EndConversationVocodeActionConfig(
#                         action_trigger=PhraseBasedActionTrigger(
#                             config=PhraseBasedActionTriggerConfig(
#                                 phrase_triggers=[
#                                     PhraseTrigger(
#                                         phrase="goodbye",
#                                         conditions=["phrase_condition_type_contains"],
#                                     )
#                                 ]
#                             )
#                         )
#                     )
#                 ],
#             )
#         ),
#         synthesizer=ElevenLabsSynthesizer(
#             synthesizer_config=ElevenLabsSynthesizerConfig.from_output_device(
#                 output_device=output_device
#             )
#         )
#     )
#
#     # Wait for the first participant to connect
#     # participant = await ctx.wait_for_participant()
#     # logger.info(f"starting voice assistant for participant {participant.identity}")
#
#     await conversation.start_room(ctx.room)
#
#     await asyncio.create_task(wait_for_termination(conversation, ctx))
#
#
# # The agent can be configured to only accept jobs from specific rooms
# async def request(ctx: JobRequest):
#     # In this case, when running in a sandbox we only want to join rooms
#     # associated with that sandbox.
#     # if sandbox is not None:
#     #     hash = sandbox.split("-")[-1]
#     #     if ctx.room.name.startswith(f"sbx-{hash}"):
#     #         return await ctx.accept()
#     #     return await ctx.reject()
#     return await ctx.accept()
#
#
# if __name__ == "__main__":
#     cli.run_app(
#         WorkerOptions(
#             entrypoint_fnc=entrypoint,
#             prewarm_fnc=prewarm,
#             request_fnc=request,
#         ),
#     )