from agents import (
    Agent,
    WebSearchTool,
    Runner,
    RunConfig
)
from typing import cast
from ingredients_guardrails import ingredients_guardrail
import chainlit as cl
from setup_config import config



@cl.on_chat_start
async def start():

    cl.user_session.set("config", config)
    cl.user_session.set("chat_history", [])

    agent=Agent(
        name="Recipe Generator",
        instructions="Generate a recipe based on the ingredients.The Ingredients used should be halal.",
        input_guardrails=[ingredients_guardrail],
        tools=[WebSearchTool()]
    )
    cl.user_session.set("agent", agent)

    await cl.Message(content="👋 Welcome to Smart Recipe Generator! How can I help you today?").send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses with emojis and friendly formatting."""
    msg = cl.Message(content="⏳ Thinking... Please wait while I whip up something delicious!")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=history,
            run_config=config
        )

        thinking_removed = False
        chef_prefix = "👨‍🍳 "
        async for event in result.stream_events():
            if hasattr(event, "type") and event.type == "raw_response_event":
                data = getattr(event, "data", None)
                if getattr(data, "type", None) == "response.output_text.delta":
                    token = getattr(data, "delta", "")
                    if token:
                        if not thinking_removed:
                            await msg.remove()
                            msg = cl.Message(content=chef_prefix)
                            await msg.send()
                            thinking_removed = True
                        await msg.stream_token(token)

        msg.content = chef_prefix + (result.final_output or "")
        await msg.update()
        cl.user_session.set("chat_history", result.to_input_list())

    except Exception as e:
        # If the error is a guardrail tripwire, show a warning emoji and the reason
        if hasattr(e, "guardrail_result") and hasattr(e.guardrail_result.output, "output_info"):
            reason = getattr(e.guardrail_result.output.output_info, "reason", "Unknown reason")
            msg.content = f"⚠️ Sorry, I can't use those ingredients: {reason}"
        else:
            msg.content = f"❌ Error: {str(e)}"
        await msg.update()


