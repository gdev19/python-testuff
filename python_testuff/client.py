import requests
from requests.auth import HTTPBasicAuth
from .models import Test, User, Project, Suite, Run, Lab, Requirement, Defect

API = "api/v0"

class TestuffClient:
    def __init__(self, email, password, base_url="https://service2.testuff.com"):
        self.auth = HTTPBasicAuth(email, password)
        self.base_url = base_url
        self.login = email
        self.password = password
        self.headers = {
            "Accept": "application/json"
        }

    #  Public methods
    def get_token(self):
        endpoint = "login"  
        url = f"{self.base_url}/{API}/{endpoint}/"
        params = {"login":self.login, "password":self.password}
        response = requests.post(url, headers=self.headers, json=params)
        response.raise_for_status()
        data = response.json()
        return data.get("token")
        
    def get_by_id(self, model_cls, id):
        endpoint = model_cls.API_ENDPOINT  
        url = f"{self.base_url}/{API}/{endpoint}/{id}/"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        if response.status_code == 200:
            obj = response.json()
            if isinstance(obj, dict):
                return model_cls.from_dict(obj)
        return None
        
    def get(self, model_cls, **params):
        endpoint = model_cls.API_ENDPOINT  
        url = f"{self.base_url}/{API}/{endpoint}/"
        attrs = {}
        if params:
            attrs = {k: v for k, v in params.items() if k in getattr(model_cls, "ALLOWED_PARAMS", set())}
                
        mapping = getattr(model_cls, "_param_mapping", set())
        attrs = {mapping.get(k) or k:v for k, v in attrs.items()} 
        while url:
            response = requests.get(url, headers=self.headers, auth=self.auth, params=attrs)
            response.raise_for_status()
            response_data = response.json()
            if isinstance(response_data, dict) and "meta" in response_data and "objects" in response_data:
                for obj in response_data["objects"]:
                    yield model_cls.from_dict(obj)
                attrs = None
                next = response_data["meta"]["next"]
                if next:
                    url = f"{self.base_url}{next}"
                else:
                    url = None
                    break
            else:
                url = None
                break
        
    def add(self, model_cls, **params):
        if model_cls is None:
            return
        endpoint = model_cls.API_ENDPOINT  
        url = f"{self.base_url}/{API}/{endpoint}/"
        
        response = requests.post(url, headers=self.headers, auth=self.auth, json=params)
        response.raise_for_status()
        return model_cls.from_dict(response.json())

    def add_automation(self, token, **params):
        endpoint = "testone"
        url = f"{self.base_url}/{API}/{endpoint}/?token={token}"
        # check post params:
        POST_FIELDS_REQUIRED = ['branch_id', 'name', 'status'] 
        POST_FIELDS_OPTIONAL = ['lab_name', 'seconds', 'comment', 'automation_id'] 
        fields = POST_FIELDS_REQUIRED + POST_FIELDS_OPTIONAL

        attrs = {}
        if params:
            attrs = {k: v for k, v in params.items() if k in fields}

        for field in POST_FIELDS_REQUIRED:
            if field not in params:
                print(f"Missing field: {field}")
                print(f"\nThese fields are required:")
                print(f"{', '.join(POST_FIELDS_REQUIRED)}")
                print(f"\nThese fields are optional:")
                print(f"{', '.join(POST_FIELDS_OPTIONAL)}")
                return None

        response = requests.post(url, headers=self.headers, json=attrs)
        response.raise_for_status()
        return Run.from_dict(response.json())

    def save(self, model_cls, id, **params):
        if model_cls is None:
            return
        endpoint = model_cls.API_ENDPOINT  
        url = f"{self.base_url}/{API}/{endpoint}/{id}/"
        
        response = requests.put(url, headers=self.headers, auth=self.auth, json=params)
        response.raise_for_status()
        return model_cls.from_dict(response.json())

    def delete(self, model_cls, id):
        if model_cls is None:
            return
        endpoint = model_cls.API_ENDPOINT  
        url = f"{self.base_url}/{API}/{endpoint}/{id}/"
        response = requests.delete(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.status_code == 204

