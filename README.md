# python-testuff

Python SDK for the [Testuff API](https://app.testuff.com/api/index.html).

## Features

- Easy integration with Testuff API using Python
- Handles authentication via Basic Authentication
- Simple access methods for API rest requests

## Contributions

This repository does not accept direct code contributions.  
Please report bugs and feature requests using the GitHub Issues tab.

## Installation

pip install git+https://github.com/TestuffAPI/python-testuff.git

## Quick Start

After installing the package, run this script to verify installation and basic functionality:

```python
from python_testuff.client import TestuffClient
from python_testuff.models import Test

# Initialize client (replace with actual parameters)
client = TestuffClient(email="LOGIN", password="PASSWORD", base_url="https://service2.testuff.com")

# Example: fetch Test instance (adjust per your API)
tests = client.get(Test)
try:
    first_test = next(tests)
except StopIteration:
    print("No tests found")
else:
    print("At least one test found")
    print(first_test)
```

## Public Methods for each Model
- get_token(self) 
- get_by_id(self, model_cls, id)
- get(self, model_cls, **params)
- add(self, model_cls, **params)
- add_automation(self, **params)
- save(self, model_cls, id, **params)
- delete(self, model_cls, id)
- model_cls.get_help()

## Public Objects in TestuffClient
- Test: Test script details
- Run: Test execution instance
- Defect: Defect details
- Project: Project detals
- Branch: Branch details
- Suite: Suite details
- Requirement: Requrement details
- Lab: Lab details

## Hierarchy for test collections
- Project: Includes list of Branches
- Branch: Includes list of Suites, Labs, Requirements
- Suite: Includes list of Tests
- Requirement: Includes list of Tests
- Lab: Includes list of Runs

### Using `get_help()` Method

Each model class in this SDK provides a class method named `get_help()` that prints a summary of valid fields for initialization and allowed query parameters. This method is useful to explore model properties without browsing external documentation.

Example usage:
```python
#This method helps in interactive exploration and debugging of data classes.
from pythontestuff.models import Test

Test.get_help()
```

Expected output:
```
Test

Valid fields for Query:
id, suite_id, branch_id, lab_id

Valid fields for initialization:
  suite_id (required) : str
  summary (required) : str
  id (optional) : str
  automation_id (optional) : str
  version (optional) : int
  priority (optional) : int
  softlink_of_test_id (optional) : str
  preconditions (optional) : str
  stage (optional) : str
  category (optional) : str
  steps (optional) : List
  attachments (optional) : List
  labels (optional) : List
```

---



