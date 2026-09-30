import asyncio
import os
import time
from typing import Any, cast

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


async def main():
    api_key = os.getenv("NEBIUS_API_KEY")
    base_url = os.getenv("TOKEN_FACTORY_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
    client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    model = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
    print(f"\n--- S2: Reasoning behavior for {model} ---")

    start = time.time()
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Think step by step and tell me what is 123 * 456"}
            ],
            max_tokens=500,
        )
        print("Response received in", round(time.time() - start, 2), "s")
        print("Content:")
        print(resp.choices[0].message.content)

        # In python library, reasoning content is often not exposed or it's in the text. Let's check model dump
        print("\nMessage dump:")
        print(resp.choices[0].message.model_dump())
    except Exception as e:
        print("Error:", e)

    # Tool calling test
    print(f"\n--- S2: Tool calling for {model} ---")
    tools = [
        {
            "type": "function",
            "function": {
                "name": "multiply",
                "description": "Multiplies two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
                    "required": ["a", "b"],
                },
            },
        }
    ]

    try:
        resp2 = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "What is 123 * 456?"}],
            tools=cast("Any", tools),
            max_tokens=500,
        )
        print("Tool calls:")
        print(resp2.choices[0].message.tool_calls)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())
