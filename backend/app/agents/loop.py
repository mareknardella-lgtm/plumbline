import json

from backend.app.agents.tools import execute_tool
from backend.app.events.models import LLMCallData


async def run_agent_loop(
    llm,
    sandbox,
    messages: list[dict],
    tools: list[dict],
    max_iterations: int,
    model: str,
    temperature: float,
    event_bus,
) -> dict:
    history = messages.copy()

    for _i in range(max_iterations):
        response = await llm.chat(
            messages=history, tools=tools, model=model, temperature=temperature
        )

        await event_bus.emit(
            "llm.call",
            LLMCallData(
                model=model,
                tier="super",  # Simplified
                tokens_in=response.usage.prompt_tokens if hasattr(response, "usage") else 0,
                tokens_out=response.usage.completion_tokens if hasattr(response, "usage") else 0,
            ),
        )

        message = response.choices[0].message
        history.append(message)

        if not message.get("tool_calls"):
            return {"final_message": message["content"], "history": history}

        for tool_call in message["tool_calls"]:
            name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])

            try:
                result = await execute_tool(name, args, sandbox)
            except Exception as e:
                result = f"Error: {str(e)[-1000:]}"  # Compact observation

            history.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": name,
                    "content": str(result),
                }
            )

    return {"final_message": "Max iterations reached", "history": history}
