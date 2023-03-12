import json

with open("./etc/secrets/config.json") as f:
    data = json.load(f)
    print(data["private_key_id"])