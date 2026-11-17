"""The collection check fails when a guard is removed or a key is literal."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))
import check_collection as check


def collection():
    return {
        "info": {"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
        "variable": [
            {"key": "api_key", "value": ""},
            {"key": "warmup_api_key", "value": ""},
        ],
        "item": [
            {
                "name": "Example",
                "request": {
                    "method": "GET",
                    "protocolProfileBehavior": {"followRedirects": False},
                    "url": {
                        "raw": "{{base_url}}/validate?api_key={{api_key}}",
                        "query": [{"key": "api_key", "value": "{{api_key}}"}],
                    },
                },
            }
        ],
    }


class CheckTests(unittest.TestCase):
    def test_clean_collection_passes(self):
        errors, count = check.check(collection())
        self.assertEqual(errors, [])
        self.assertEqual(count, 1)

    def test_literal_query_key_fails(self):
        body = collection()
        body["item"][0]["request"]["url"]["query"][0]["value"] = "secret-value"
        errors, _ = check.check(body)
        self.assertTrue(errors)

    def test_raw_json_key_fails(self):
        body = collection()
        body["item"][0]["request"]["body"] = {"mode": "raw", "raw": '{"api_key":"secret-value"}'}
        errors, _ = check.check(body)
        self.assertTrue(any("raw body" in error for error in errors))

    def test_bearer_literal_fails(self):
        body = collection()
        body["item"][0]["request"]["header"] = [
            {"key": "Authorization", "value": "Bearer secret-value"}
        ]
        errors, _ = check.check(body)
        self.assertTrue(errors)

    def test_redirects_must_be_off(self):
        body = collection()
        del body["item"][0]["request"]["protocolProfileBehavior"]
        errors, _ = check.check(body)
        self.assertTrue(any("followRedirects" in error for error in errors))

    def test_filled_collection_variable_fails(self):
        body = collection()
        body["variable"][0]["value"] = "secret-value"
        errors, _ = check.check(body)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
