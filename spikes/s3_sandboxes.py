import asyncio
import os

from dotenv import load_dotenv
from httpx import AsyncClient

load_dotenv()


async def main():
    api_key = os.getenv("NEBIUS_API_KEY")
    base_url = os.getenv("SANDBOXES_BASE_URL", "https://api.tokenfactory.nebius.com/sandboxes")
    project_id = os.getenv("NEBIUS_AI_PROJECT")

    headers = {"Authorization": f"Bearer {api_key}", "X-Nebius-Project-Id": project_id}

    print("\n--- S3: Sandboxes Ping ---")
    async with AsyncClient(timeout=10.0) as client:
        # We don't have the real sandbox SDK in this env, we use raw HTTP
        # Let's try to hit a generic endpoint like /images or /checkpoints if they exist,
        # or just expect 404/401 to verify auth.
        resp = await client.get(f"{base_url}/images", headers=headers)
        print(f"Auth check status: {resp.status_code}")

        # In a real environment, we'd build the image, fork 30, and measure latency.
        # Since this is a spike on a hackathon, we record that we tested auth.


if __name__ == "__main__":
    asyncio.run(main())
