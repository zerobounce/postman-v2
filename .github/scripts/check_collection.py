"""CI check for the Postman collection: valid v2.1 JSON, and no API key in it."""
import json
import re
import sys

PATH = "ZeroBounce_ API_ v2.postman_collection.json"
KEY_VARIABLES = {"api_key", "warmup_api_key"}
errors = []

with open(PATH, encoding="utf-8") as handle:
    collection = json.load(handle)

schema = collection.get("info", {}).get("schema", "")
if "v2.1.0" not in schema:
    errors.append(f"expected a Postman v2.1.0 collection, got schema {schema!r}")

variables = {v.get("key"): v.get("value", "") for v in collection.get("variable", [])}
for name in sorted(KEY_VARIABLES):
    if name not in variables:
        errors.append(f"collection variable {name!r} is missing")
    elif variables[name]:
        errors.append(f"collection variable {name!r} has a value; leave it empty")


def requests(items, trail=()):
    for item in items:
        if "item" in item:
            yield from requests(item["item"], trail + (item.get("name", "?"),))
        elif "request" in item:
            yield " / ".join(trail + (item.get("name", "?"),)), item["request"]


count = 0
for name, request in requests(collection.get("item", [])):
    count += 1
    text = json.dumps(request)
    # Any api_key / API-Key value must be a {{variable}}, never a literal.
    for match in re.finditer(r'"(?:key)":\s*"(api_key|API-Key)",\s*"value":\s*"([^"]*)"', text):
        if not re.fullmatch(r"\{\{\w+\}\}", match.group(2)):
            errors.append(f"{name}: {match.group(1)} is a literal value, not a variable")
    for match in re.finditer(r"api_key=([^&\"\s]+)", text):
        if not re.fullmatch(r"\{\{\w+\}\}", match.group(1)):
            errors.append(f"{name}: the URL carries a literal api_key")

if count == 0:
    errors.append("the collection has no requests")
for error in errors:
    print(f"error: {error}")
print(f"checked {count} requests")
sys.exit(1 if errors else 0)
