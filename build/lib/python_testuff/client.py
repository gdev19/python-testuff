import requests

class TestuffClient:
    """
    Python SDK client for Testuff API.
    """
    def __init__(self, api_key, base_url="https://app.testuff.com/api"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    # Add more methods as needed
