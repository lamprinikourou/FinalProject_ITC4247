import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/"
LOG_FILE = "security_test_results.json"

HEADERS = {"Content-Type": "application/json"}

# Define extreme inputs for different data types
EXTREME_INPUTS = {
    "string": ["", "a" * 10000, 1234, "<script>alert('XSS')</script>", "' OR 1=1; --", None],
    "integer": [-999999, 0, 9999999999, "text", None],
    "boolean": [True, False, "yes", "no", None, 123],
    "float": [-1.0, 0.0, 1.7976931348623157e+308, "abc", None],
}

# API endpoints with their HTTP methods and payload schema
ENDPOINTS = {
    "users/": {
        "methods": ["POST", "GET", "PUT", "DELETE"],
        "payload": {"username": "string", "email": "string", "is_admin": "boolean"}
    },
    "products/": {
        "methods": ["POST", "GET", "PUT", "DELETE"],
        "payload": {"name": "string", "description": "string", "price": "float"}
    },
    "orders/": {
        "methods": ["POST", "GET", "DELETE"],
        "payload": {"user": "integer", "product": "integer", "quantity": "integer"}
    }
}

results = []


def generate_extreme_payload(payload_schema):
    """
    Generate payloads with extreme inputs for each field in the schema.
    """
    payloads = []

    # Generate extreme inputs for each field
    for field, field_type in payload_schema.items():
        extreme_values = EXTREME_INPUTS.get(field_type, ["valid_value"])
        for value in extreme_values:
            payload = {k: "valid_value" for k in payload_schema.keys()}
            payload[field] = value
            payloads.append(payload)

    return payloads


def test_endpoint(endpoint, method, payload_schema):
    """
    Test the specified endpoint with extreme inputs using the given HTTP method.
    """
    url = BASE_URL + endpoint
    extreme_payloads = generate_extreme_payload(payload_schema)

    for payload in extreme_payloads:
        try:
            if method == "POST":
                response = requests.post(url, headers=HEADERS, json=payload, timeout=5)
            elif method == "PUT":
                response = requests.put(url + "1/", headers=HEADERS, json=payload, timeout=5)  # Update ID 1
            elif method == "DELETE":
                response = requests.delete(url + "1/", headers=HEADERS, timeout=5)  # Delete ID 1
            elif method == "GET":
                response = requests.get(url, headers=HEADERS, timeout=5)
            else:
                print(f"Unsupported method {method} for {endpoint}")
                continue

            log_result(endpoint, method, payload, response)

        except requests.exceptions.RequestException as e:
            log_result(endpoint, method, payload, error=str(e))


def log_result(endpoint, method, payload, response=None, error=None):
    """
    Log results to memory and print the status to the console.
    """
    result = {
        "endpoint": endpoint,
        "method": method,
        "payload": payload,
        "status_code": response.status_code if response else "ERROR",
        "response": response.json() if response and response.content else None,
        "error": error
    }
    results.append(result)

    if response:
        print(f"[{method}] {endpoint} -> Status: {response.status_code} | Payload: {payload}")
    else:
        print(f"[{method}] {endpoint} -> ERROR: {error} | Payload: {payload}")


if __name__ == "__main__":
    print("Starting automated security testing with extreme inputs...\n")

    # Loop through all endpoints and test each method
    for endpoint, config in ENDPOINTS.items():
        methods = config["methods"]
        payload_schema = config["payload"]

        for method in methods:
            print(f"Testing {method} {endpoint}...")
            test_endpoint(endpoint, method, payload_schema)

    # Save test results to a JSON file
    with open(LOG_FILE, "w") as file:
        json.dump(results, file, indent=4)
    print(f"\nTest results saved to '{LOG_FILE}'")
