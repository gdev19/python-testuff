import dataclasses
from dataclasses import dataclass
from typing import Optional, List, Dict, Union, Any, get_origin, get_args

class BaseModel:
    ALLOWED_PARAMS: List[str] = []
    FIELDS_READ_ONLY: List[str] = []
    _field_mapping = {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        field_values = {}
        for field, field_type in cls.__annotations__.items():
            json_key = cls._field_mapping.get(field, field)
            value = data.get(json_key)

            origin = get_origin(field_type)
            args = get_args(field_type)

            if origin is Union and type(None) in args:
                non_none_args = [arg for arg in args if arg is not type(None)]
                if len(non_none_args) == 1:
                    inner_type = non_none_args[0]
                    inner_origin = get_origin(inner_type)
                    inner_args = get_args(inner_type)

                    if inner_origin in (list, List):
                        list_inner_type = inner_args[0]
                        if value is not None and isinstance(value, list):
                            # ONLY call from_dict if inner type is not 'dict'
                            if list_inner_type is dict:
                                # Keep list of dict as is
                                pass
                            elif hasattr(list_inner_type, "from_dict"):
                                value = [list_inner_type.from_dict(item) for item in value]
                    elif hasattr(inner_type, "from_dict") and value is not None:
                        value = inner_type.from_dict(value)

            else:
                if origin in (list, List):
                    list_inner_type = args[0]
                    if value is not None and isinstance(value, list):
                        if list_inner_type is dict:
                            # Keep list of dict as is
                            pass
                        elif hasattr(list_inner_type, "from_dict"):
                            value = [list_inner_type.from_dict(item) for item in value]

                elif hasattr(field_type, "from_dict") and value is not None:
                    value = field_type.from_dict(value)

            field_values[field] = value
        return cls(**field_values)

    @classmethod
    def print_help(cls):
        print(f"{cls.__name__}")
        print(f"\nValid fields for Query:")
        print(f"{', '.join(cls.ALLOWED_PARAMS)}")
        print(f"\nValid fields for initialization:")
        for name, annotation in cls.__annotations__.items():
            origin = get_origin(annotation)
            args = get_args(annotation)
            required = True
            if origin is Union and type(None) in args:
                required = False
                inner_types = [arg for arg in args if arg is not type(None)]
                if len(inner_types) == 1:
                    typ = inner_types[0]
                else:
                    typ = inner_types
            else:
                typ = annotation

            # Get readable type name if possible
            if hasattr(typ, "__name__"):
                type_str = typ.__name__
            else:
                type_str = str(typ).replace("typing.", "")

            if name not in getattr(cls, "FIELDS_READ_ONLY", []):
                print(f"  {name} ({'required' if required else 'optional'}) : {type_str}")


@dataclass
class Test(BaseModel):
    # Mandatory: no default
    suite_id: str
    summary: str
    # Optional: with default
    id: Optional[str] = None
    automation_id: Optional[str] = None
    version: Optional[int] = 0
    priority: Optional[int] = 2
    softlink_of_test_id: Optional[str] = None
    preconditions: Optional[str] = None
    stage: Optional[str] = None
    category: Optional[str] = None
    steps: Optional[List[Dict[str, Any]]] = None  # Raw list of dicts with limited keys
    attachments: Optional[List[Dict[str, Any]]] = None  # Raw list of dicts with limited keys
    labels: Optional[List[str]] = None            # List of label names
    # ReadOnly: with defauls 
    suite_name: Optional[str] = None
    branch_id: Optional[str] = None
    project_id: Optional[str] = None
    comments: Optional[int] = 0
    last_run_status: Optional[str] = None
    create_date: Optional[str] = None
    create_user_id: Optional[str] = None
    create_user_name: Optional[str] = None
    update_date: Optional[str] = None
    update_user_id: Optional[str] = None
    update_user_name: Optional[str] = None

    API_ENDPOINT = "test"
    FIELDS_READ_ONLY = ['suite_name', 'branch_id', 'project_id', 'comments', 'last_run_status', 'create_date',
                                'create_user_id', 'create_user_name', 'update_date' , 'update_user_id', 'update_user_name']
    ALLOWED_PARAMS = ["id", "suite_id", "branch_id", "lab_id"]
    _field_mapping = {
        "stage": "status",
        "category": "test_category"
    }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        obj = super().from_dict(data)

        # Process steps to list of dicts with selected keys
        if obj.attachments:
            obj.attachments = [
                {k: attach.get(k) for k in ("filename", "url")}
                for attach in obj.attachments
            ]

        # Process steps to list of dicts with selected keys
        if obj.steps:
            obj.steps = [
                {k: step.get(k) for k in ("position", "description", "expected")}
                for step in obj.steps
            ]

        # Process labels to list of names
        labels_data = data.get("labels")
        if labels_data and isinstance(labels_data, list):
            obj.labels = [label.get("name") for label in labels_data]
        else:
            obj.labels = []

        return obj

@dataclass
class Project(BaseModel):
    # Mandatory: no default
    id: int
    name: str
    # Optional: with default
    description: Optional[str] = None
    branchs: Optional[List[Dict[str, Any]]] = None 
        
    API_ENDPOINT = "project"
    ALLOWED_PARAMS = ["name", "name_icontains"]
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        obj = super().from_dict(data)
        # Process steps to list of dicts with selected keys
        if obj.branchs:
            obj.branchs = [
                {k: branch.get(k) for k in ("id", "name")}
                for branch in obj.branchs
            ]
        return obj
        
@dataclass
class User(BaseModel):
    # Mandatory: no default
    id: int
    name: str
    email: str
    # Optional: with default
        
    API_ENDPOINT = "user"
    ALLOWED_PARAMS = ["name", "email"]
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        obj = super().from_dict(data)
        return obj
        
@dataclass
class Branch(BaseModel):
    # Mandatory: no default
    id: int
    name: str
    project_id: str
    # Optional: with default
    description: Optional[str] = None
        
    API_ENDPOINT = "branch"
    ALLOWED_PARAMS = ["name", "project_id"]

@dataclass
class Suite(BaseModel):
    id: int
    name: str
    branch_id: int
    # Optional: with default
    preconditions: Optional[str] = None
    parent_id: Optional[str] = None

    API_ENDPOINT = "suite"
    ALLOWED_PARAMS = ["id", "name", "branch_id", "parent_id"]

@dataclass
class Run(BaseModel):
    id: Optional[str]
    test_id: Optional[str]
    # Optional with defaults
    status: Optional[str] = "not run"
    automation: Optional[str] = "not run"
    lab_id: Optional[str] = None
    user_id: Optional[str] = None
    steps: Optional[List[Dict[str, Any]]] = None  # Raw list of dicts with limited keys
    attachments: Optional[List[Dict[str, Any]]] = None  # Raw list of dicts with limited keys
    labels: Optional[List[str]] = None            # List of label names
    # ReadOnly: with defauls 
    summary: Optional[str] = None
    priority: Optional[int] = 2
    preconditions: Optional[str] = None
    project_id: Optional[str] = None
    branch_id: Optional[str] = None
    user_name: Optional[str] = None
    comment: Optional[int] = 0
    automation_id: Optional[str] = None
    conf_name: Optional[str] = None
    estimated_time: Optional[str] = None 
    actual_time: Optional[str] = None 
    product_version: Optional[str] = None 
    test_category: Optional[str] = None 
    suite_name: Optional[str] = None
    run_date: Optional[str] = None
    numbering: Optional[str] = None

    API_ENDPOINT = "run"
    FIELDS_READ_ONLY = ['priority', 'preconditions', 'project_id', 'branch_id', 'user_name', 'comment', 'automation_id', 'summary',
                'conf_name', 'estimated_time', 'actual_time', 'product_version', 'test_category', 'suite_name', 'run_date', 'numbering']
    ALLOWED_PARAMS = ["id", "summary", "summary_icontains", "project_id", "branch_id", "lab_id", "user_id", "test_id", "automation", "comments", "comments_gte", "status", "conf_name", "priority", "defects", "defects_gt", "run_date", "run_date_gt", "run_date_lt"]
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        obj = super().from_dict(data)
        # Process steps to list of dicts with selected keys
        if obj.attachments:
            obj.attachments = [
                {k: attach.get(k) for k in ("filename", "url")}
                for attach in obj.attachments
            ]

        # Process steps to list of dicts with selected keys
        if obj.steps:
            obj.steps = [
                {k: step.get(k) for k in ("position", "description", "expected", "status", "comments")}
                for step in obj.steps
            ]

        # Process labels to list of names
        labels_data = data.get("labels")
        if labels_data and isinstance(labels_data, list):
            obj.labels = [label.get("name") for label in labels_data]
        else:
            obj.labels = []

        return obj

@dataclass
class Lab(BaseModel):
    id: int
    name: str
    branch_id: int
    # Optional: with default
    instructions: Optional[str] = None
    notes: Optional[str] = None
    parent_id: Optional[str] = None
    due_date: Optional[str] = None
    product_version: Optional[str] = None
    labels: Optional[List[str]] = None            # List of label names
    # ReadOnly: with defauls 
    start_date: Optional[str] = None

    API_ENDPOINT = "suite"
    ALLOWED_PARAMS = ["id", "name", "name_icontains", "branch_id", "parent_id"]
    FIELDS_READ_ONLY = ['start_date']
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        obj = super().from_dict(data)

        # Process labels to list of names
        labels_data = data.get("labels")
        if labels_data and isinstance(labels_data, list):
            obj.labels = [label.get("name") for label in labels_data]
        else:
            obj.labels = []
        return obj

@dataclass
class Requirement(BaseModel):
    id: int
    name: str
    branch_id: int
    # Optional: with default
    description: Optional[str] = None
    risk: Optional[str] = None
    priority: Optional[str] = None
    req_type: Optional[str] = None
    parent_id: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    labels: Optional[List[str]] = None
    bug_tracker_url: Optional[str] = None
    # Readonly
    total: Optional[int] = 0
    passed: Optional[int] = 0
    failed: Optional[int] = 0
    wontdo: Optional[int] = 0
    not_run: Optional[int] = 0
    blocked: Optional[int] = 0
    full_name: Optional[str] = None
    
    API_ENDPOINT = "req"
    ALLOWED_PARAMS = ["id", "name", "name_icontains", "branch_id", "parent_id", "risk", 'priority', 'req_type']
    FIELDS_READ_ONLY = ['total', 'passed', 'failed', 'wontdo', 'not_run', 'blocked', 'full_name', 'bug_tracker_url']
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        obj = super().from_dict(data)
        if obj.attachments:
            obj.attachments = [
                {k: attach.get(k) for k in ("filename", "url")}
                for attach in obj.attachments
            ]

        # Process labels to list of names
        labels_data = data.get("labels")
        if labels_data and isinstance(labels_data, list):
            obj.labels = [label.get("name") for label in labels_data]
        else:
            obj.labels = []
        return obj

@dataclass
class Defect(BaseModel):
    id: str
    branch_id: str
    user_id: str
    summary: str
    # Optional: with default
    lab_id: Optional[str] = None
    run_id: Optional[str] = None
    run_step_position: Optional[int] = 0
    
    severity: Optional[str] = None
    status: Optional[str] = None
    conf_name: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    bug_tracker_url: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    labels: Optional[List[str]] = None
    # Readonly
    test_id: Optional[str] = None

    API_ENDPOINT = "defect"
    ALLOWED_PARAMS = ["id", "summary", "status","state", "project_id", "branch_id", "lab_id", 
                    "run_id", "test_id", "user_id", "report_date_gte", "report_date_lte"]
    FIELDS_READ_ONLY = ["project_id", "branch_id", "test_id"]
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        obj = super().from_dict(data)
        if obj.attachments:
            obj.attachments = [
                {k: attach.get(k) for k in ("filename", "url")}
                for attach in obj.attachments
            ]

        # Process labels to list of names
        labels_data = data.get("labels")
        if labels_data and isinstance(labels_data, list):
            obj.labels = [label.get("name") for label in labels_data]
        else:
            obj.labels = []
        return obj
