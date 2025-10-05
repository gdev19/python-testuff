import unittest
from python_testuff.client import TestuffClient
from python_testuff.models import Test, User, Project, Suite, Branch, Run, Lab, Requirement, Defect
from python_testuff.utils import generate_id

WRONG_ID = "WRONG_ID"

class TestTestuffClient(unittest.TestCase):

    def setUp(self):
        self.client = TestuffClient(email="EMAIL", password="PASSWORD", base_url="https://serviceX.testuff.com")

    def _test_first_obj(self, cls):
        objs = self.client.get(cls)
        try:
            first_obj = next(objs)
        except StopIteration:
            raise AssertionError(f"No {cls} found")
        else:
            self.assertIsInstance(first_obj, cls)
        return first_obj
            
    def _test_get_no_objs(self, cls, **params):
        if not params:
            objs = self.client.get(cls, id=WRONG_ID)
        else:
            objs = self.client.get(cls, **params)
        try:
            first_obj = next(objs)
        except StopIteration:
            # good response
            pass
        else:
            raise AssertionError(f"{cls} found for invalid parameter")
            
    def _test_get_obj_by_id(self, cls):
        objs = self.client.get(cls)
        try:
            first_obj = next(objs)
        except StopIteration:
            raise AssertionError("No tests found")
        else:
            self.assertIsInstance(first_obj, cls)
        obj = self.client.get_by_id(cls, first_obj.id)
        self.assertIsInstance(obj, cls)
        obj = self.client.get_by_id(cls, "aaa")
        self.assertEqual(obj, None)
        
    def _test_create_update_delete_obj(self, cls, **add_params):
        # check by retreiving first obj by it's id , assumng test exists in account
        objs = self.client.get(cls)
        try:
            first_obj = next(objs)
        except StopIteration:
            raise AssertionError(f"No {cls} found")
        else:
            self.assertIsInstance(first_obj, cls)
        # add 
        id = generate_id()
        obj = self.client.add(cls, id=id, **add_params)
        self.assertEqual(obj.id, id)

        # update 
        new_value = "updated name"
        if cls.__name__ in ["Test", "Defect"]:
            updated_obj = self.client.save(cls, id, summary=new_value)
            self.assertEqual(updated_obj.summary, new_value)
        elif cls.__name__=="Run":
            updated_obj = self.client.save(cls, id, conf_name=new_value)
            self.assertEqual(updated_obj.conf_name, new_value)
        else:
            updated_obj = self.client.save(cls, id, name=new_value)
            self.assertEqual(updated_obj.name, new_value)
        
        # delete test and check it was deleted
        self.client.delete(cls, id)        
        obj = self.client.get_by_id(cls, id)
        self.assertEqual(obj, None)

    def test_add_automation(self):
        branch = self._test_first_obj(Branch)
        token = "invalid"
        add_params = {
        "branch_id": branch.id,
        "name": "new test",
        "status": "passed",
        }
        # check invalid token
        try:
            obj = self.client.add_automation(token, **add_params)
        except Exception as e:
            self.assertEqual("Unauthorized" in str(e), True)
        else:
            AssertionError(f"Invalid token that succedded: {token}")
        
        # get the token
        token = self.client.get_token()
        
        # add automation not from test
        add_params["branch_id"]= branch.id
        obj = self.client.add_automation(token, **add_params)
        self.assertEqual(obj.__class__.__name__, "Run")

        # add automation from test by it's automation_id
        test = self._test_first_obj(Test)
        add_params["automation_id"]= test.automation_id
        obj = self.client.add_automation(token, **add_params)
        self.assertEqual(obj.test_id, test.id)
        self.assertEqual(obj.automation_id, test.automation_id)
  

    #~ def test_get_tests(self):
        #~ self._test_first_obj(Test)

    #~ def test_get_no_tests(self):
        #~ self._test_get_no_objs(Test)

    #~ def test_get_test_by_id(self):
        #~ self._test_get_obj_by_id(Test)

    #~ def test_create_update_delete_test(self):
        #~ test = self._test_first_obj(Test)
        #~ self._test_create_update_delete_obj(Test, suite_id=test.suite_id, summary="summary", estimated_time=None)

    #~ def test_get_projects(self):
        #~ self._test_first_obj(Project)

    #~ def test_get_no_projects(self):
        #~ self._test_get_no_objs(Project, name="missing name")

    #~ def test_get_project_by_id(self):
        #~ self._test_get_obj_by_id(Project)

    #~ def test_create_update_delete_project(self):
        #~ self._test_create_update_delete_obj(Project, name="new")
        
    #~ def test_get_branchs(self):
        #~ self._test_first_obj(Branch)

    #~ def test_get_no_branchs(self):
        #~ self._test_get_no_objs(Branch, name="missing name")

    #~ def test_get_branch_by_id(self):
        #~ self._test_get_obj_by_id(Branch)

    #~ def test_create_update_delete_branch(self):
        #~ branch= self._test_first_obj(Branch)
        #~ self._test_create_update_delete_obj(Branch, project_id=branch.project_id, name="new")
        
    #~ def test_get_suites(self):
        #~ self._test_first_obj(Suite)

    #~ def test_get_no_suites(self):
        #~ self._test_get_no_objs(Suite, name="missing name")

    #~ def test_get_suite_by_id(self):
        #~ self._test_get_obj_by_id(Suite)

    #~ def test_create_update_delete_suite(self):
        #~ suite= self._test_first_obj(Suite)
        #~ self._test_create_update_delete_obj(Suite, branch_id=suite.branch_id, name="new")

    #~ def test_get_runs(self):
        #~ run = self._test_first_obj(Run)

    #~ def test_get_no_runs(self):
        #~ self._test_get_no_objs(Run)

    #~ def test_get_run_by_id(self):
        #~ self._test_get_obj_by_id(Run)

    #~ def test_create_update_delete_run(self):
        #~ test = self._test_first_obj(Test)
        #~ self._test_create_update_delete_obj(Run, test_id=test.id, status="new")

    #~ def test_get_labs(self):
        #~ obj = self._test_first_obj(Lab)
  
    #~ def test_get_no_labs(self):
        #~ self._test_get_no_objs(Lab)

    #~ def test_get_lab_by_id(self):
        #~ self._test_get_obj_by_id(Lab)

    #~ def test_create_update_delete_lab(self):
        #~ lab = self._test_first_obj(Lab)
        #~ self._test_create_update_delete_obj(Lab, branch_id=lab.branch_id, name="new")

    #~ def test_get_reqs(self):
        #~ obj = self._test_first_obj(Requirement)

    #~ def test_get_no_reqs(self):
        #~ self._test_get_no_objs(Requirement)

    #~ def test_get_req_by_id(self):
        #~ self._test_get_obj_by_id(Requirement)

    #~ def test_create_update_delete_req(self):
        #~ obj = self._test_first_obj(Requirement)
        #~ self._test_create_update_delete_obj(Lab, branch_id=obj.branch_id, name="new")

    #~ def test_get_defects(self):
        #~ obj = self._test_first_obj(Defect)

    #~ def test_get_no_defects(self):
        #~ self._test_get_no_objs(Defect)

    #~ def test_get_defect_by_id(self):
        #~ self._test_get_obj_by_id(Defect)

    #~ def test_create_update_delete_defect(self):
        #~ obj = self._test_first_obj(Defect)
        #~ self._test_create_update_delete_obj(Defect, branch_id=obj.branch_id, summary="new")

if __name__ == "__main__":
    unittest.main()
