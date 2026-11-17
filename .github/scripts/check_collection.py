"""CI check for the Postman collection: valid v2.1 JSON, and no API key in it."""
import json
import re
import sys

PATH = "ZeroBounce_ API_ v2.postman_collection.json"
KEY_VARIABLES = {"api_key", "warmup_api_key"}
KEY_NAMES = {"api_key", "api-key", "x-api-key", "authorization"}
VARIABLE = re.compile(r"\{\{\w+\}\}")
BEARER = re.compile(r"^Bearer \{\{\w+\}\}$")
OMITTED = "the response text was omitted because it contained a credential"


def check(collection):
    errors = []
    schema = collection.get("info", {}).get("schema", "")
    if "v2.1.0" not in schema:
        errors.append(f"expected a Postman v2.1.0 collection, got schema {schema!r}")

    variables = {v.get("key"): v.get("value", "") for v in collection.get("variable", [])}
    for name in sorted(KEY_VARIABLES):
        if name not in variables:
            errors.append(f"collection variable {name!r} is missing")
        elif variables[name]:
            errors.append(f"collection variable {name!r} has a value; leave it empty")

    count = 0
    for name, request in requests(collection.get("item", [])):
        count += 1
        behavior = request.get("protocolProfileBehavior") or {}
        if behavior.get("followRedirects") is not False:
            errors.append(f"{name}: followRedirects is not false")
        walk(request, name, errors)
    if count == 0:
        errors.append("the collection has no requests")

    # Descriptions and other text outside a request can still hold a pasted key.
    walk(collection.get("info", {}), "info", errors)
    return errors, count


def requests(items, trail=()):
    for item in items:
        if "item" in item:
            yield from requests(item["item"], trail + (item.get("name", "?"),))
        elif "request" in item:
            yield " / ".join(trail + (item.get("name", "?"),)), item["request"]


def walk(node, where, errors):
    if isinstance(node, dict):
        key = node.get("key")
        if isinstance(key, str) and key.lower() in KEY_NAMES:
            if not allowed_secret(key, node.get("value")):
                errors.append(f"{where}: {key} is not a collection variable")
        if key is None and "value" in node and "description" in node:
            errors.append(f"{where}: a query field has no name")
        for value in node.values():
            walk(value, where, errors)
    elif isinstance(node, list):
        for value in node:
            walk(value, where, errors)
    elif isinstance(node, str):
        scan_text(node, where, errors)


def allowed_secret(key, value):
    if not isinstance(value, str) or not value:
        return False
    if key.lower() == "authorization":
        return BEARER.fullmatch(value) is not None
    return VARIABLE.fullmatch(value) is not None


def scan_text(text, where, errors):
    if "None=" in text:
        errors.append(f"{where}: the URL contains None=")
    for match in re.finditer(r"api_key=([^&\"\s]*)", text):
        if not VARIABLE.fullmatch(match.group(1) or ""):
            errors.append(f"{where}: the URL carries a literal api_key")
    for match in re.finditer(r'"api_key"\s*:\s*"([^"]*)"', text):
        if not VARIABLE.fullmatch(match.group(1) or ""):
            errors.append(f"{where}: a raw body carries a literal api_key")
    for match in re.finditer(r"Bearer\s+(\S+)", text):
        token = match.group(1).rstrip('",')
        if not VARIABLE.fullmatch(token):
            errors.append(f"{where}: Authorization Bearer is not a collection variable")


def main():
    with open(PATH, encoding="utf-8") as handle:
        collection = json.load(handle)
    errors, count = check(collection)
    for error in errors:
        print(f"error: {error}")
    print(f"checked {count} requests")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
