import sys, os
sys.path.insert(1, os.getcwd())
print(sys.path)
import uuid
from obi.db import *
import json

jsonstring = """{"test": "cool"}"""

def create_records():
    user = User()
    user.name = 'Wolf Vollprecht'
    user.save()

    databucket = DataBucket()
    databucket.name = 'TestBucket'
    databucket.created_by = user
    databucket.data_type = 'image'
    databucket.save()

    changeset1 = ChangeSet()
    changeset1.changeset = '{create: ...}'
    changeset1.user = user
    changeset1.bucket = databucket
    changeset1.save()

    data = Data()
    data.bucket = databucket
    data.json_store = json.loads(jsonstring)
    print(data.json_store)
    data.current_head = uuid.UUID(int=0)

    data.save()


if __name__ == '__main__':
    create_records()