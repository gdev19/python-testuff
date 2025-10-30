POST_FIELDS_REQUIRED = ['branch_id', 'name', 'status'] 
POST_FIELDS_OPTIONAL = ['lab_name', 'seconds', 'comment', 'automation_id'] 

fields = POST_FIELDS_REQUIRED + POST_FIELDS_OPTIONAL
print fields
