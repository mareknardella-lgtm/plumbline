import os

import requests
from dotenv import load_dotenv

load_dotenv()


def main():
    api_key = os.getenv("NEBIUS_API_KEY")
    base_url = os.getenv("TOKEN_FACTORY_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")

    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(f"{base_url}models?verbose=true", headers=headers)

    if resp.status_code != 200:
        print(f"Error: {resp.status_code} {resp.text}")
        return

    data = resp.json().get("data", [])

    print(f"Found {len(data)} total models. Filtering for 'nemotron'...")
    for model in data:
        model_id = model.get("id", "").lower()
        if "nemotron" in model_id:
            print(f"\nModel ID: {model['id']}")
            print(
                f"Max tokens/context: {model.get('max_tokens', 'N/A')} / {model.get('context_length', 'N/A')}"
            )
            # The verbose=true might put extra info in model
            print(model)


if __name__ == "__main__":
    main()
