import sys, os
sys.path.insert(1, os.getcwd())

import json
from obi.db import *
from uuid import uuid4

patch_1 = {}
patch_1['items_to_create'] = [
    {"op": "add", "path": "/test", "value": ["a new item, cool"]}
]

def create_records():
    user = User.get()
    bucket = DataBucket.get(id=1)
    print(bucket, bucket.data)
    data = bucket.data.select()
    print(data[0].json_store)
    print(user, bucket, data)
    changeset = ChangeSet()
    changeset.bucket = bucket
    changeset.user = user

    patch_1[str(data[0].uuid)] = [
        {"op": "add", "path": "/hello", "value": ["world"]},
        {"op": "add", "path": "/news", "value": ["value"]},
    ]

    changeset.changeset = patch_1
    changeset.save()

    bucket.apply_changeset(changeset)

if __name__ == '__main__':
    create_records()