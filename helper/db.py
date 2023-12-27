import requests, json
from helper.config import GH_TOKEN

GIST_ID = "9cc9852a7a78c168f1a4242d91a5c0ff"

def get_json() -> list[str]:
    response = requests.get(f"https://api.github.com/gists/{GIST_ID}")
    return json.loads(response.json()["files"]["ph.json"]["content"])

def set_json(data: list[str]):
    requests.patch(
        f"https://api.github.com/gists/{GIST_ID}",
        headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {GH_TOKEN}"},
        json={"files": {"ph.json": {"content": json.dumps(data.sort(), indent=2)}}}
    )