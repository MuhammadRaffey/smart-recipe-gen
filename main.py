from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIResponsesModel,
    WebSearchTool,
    RunConfig,
    Runner,
    InputGuardrailTripwireTriggered,
)
from ingredients_guardrails import ingredients_guardrail
from dotenv import load_dotenv,find_dotenv
import os
import chainlit as cl
import asyncio

_=load_dotenv(find_dotenv())

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

client=AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.openai.com/v1"
)

model=OpenAIResponsesModel(
    model="gpt-4.1-mini",
    openai_client=client
)

config=RunConfig(
    model=model,
    model_provider=client
)

agent=Agent(
    name="Recipe Generator",
    instructions="Generate a recipe based on the ingredients.The Ingredients used should be halal.",
    input_guardrails=[ingredients_guardrail],
    tools=[WebSearchTool()]
)
@cl.on_chat_start
async def start_chat():
    cl.user_session.set("messages", [])
    await cl.Message("Hello, I am a recipe generator. I can help you generate a recipe based on the ingredients you provide.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    msg = cl.user_session.get("messages", [])
    msg.append({"role": "user", "content": message.content})
    ai_msg = cl.Message(content="")
    try:
        result = Runner.run_streamed(
            agent,
            msg,
            run_config=config,
        )
        guardrail_triggered = False
        streamed_started = False
        async for event in result.stream_events():
            if guardrail_triggered:
                break
            if event.type == "run_item_stream_event":
                item = getattr(event, "item", None)
                if item is not None:
                    if getattr(item, "type", None) == "tool_call_item":
                        await cl.Message("🔧 Tool was called").send()
                    elif getattr(item, "type", None) == "tool_call_output_item":
                        await cl.Message(f"🔧 Tool output: {getattr(item, 'output', '')}").send()
            elif event.type == "raw_response_event":
                if not guardrail_triggered and hasattr(event.data, "delta"):
                    if not streamed_started:
                        await asyncio.sleep(3)
                        streamed_started = True
                    await ai_msg.stream_token(event.data.delta)
                continue
            elif isinstance(event, InputGuardrailTripwireTriggered) or getattr(event, 'type', None) == 'input_guardrail_tripwire_triggered':
                output_info = getattr(event, 'output_info', None)
                if output_info and hasattr(output_info, 'reason'):
                    reason_text = output_info.reason
                else:
                    reason_text = str(output_info) if output_info else "Some ingredients are not halal."
                await cl.Message(f"❌ Guardrail triggered: {reason_text}").send()
                guardrail_triggered = True
                break
        if not guardrail_triggered:
            msg.append({"role": "assistant", "content": result.final_output})
            cl.user_session.set("messages", msg)
    except InputGuardrailTripwireTriggered as e:
        output_info = getattr(e.guardrail_result.output, 'output_info', None)
        if output_info and hasattr(output_info, 'reason'):
            reason_text = output_info.reason
        else:
            reason_text = str(output_info) if output_info else "Some ingredients are not halal."
        await cl.Message(f"❌ Guardrail triggered: {reason_text}").send()
        return









