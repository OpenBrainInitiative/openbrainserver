import json
import sys
from db import *


def load_changeset(changeset_loc):
    with open(changeset_loc, 'r') as fp:
        changeset_str = fp.read()
    changeset_json = json.loads(changeset_str)
    print("loaded changeset")

    try:
        bucket = DataBucket.get(DataBucket.name == changeset_json['bucket']['name'])
        print("found bucket")

    except DataBucket.DoesNotExist:
        bucket = DataBucket()
        bucket.name = changeset_json['bucket']['name']
        bucket.created_by = User.get() # bs value
        bucket.data_type = 'irrelevant'
        bucket.save()

    print("Bucket %r %s" % (bucket, bucket.uuid))
    changeset = ChangeSet()
    changeset.bucket = bucket
    changeset.user = User.get()
    changeset.set_changeset(changeset_str)
    # changeset.previous_changeset = bucket.current_head
    # changeset.changeset = changeset_json
    changeset.save()
    print(bucket, bucket.id)
    bucket.apply_changeset(changeset)


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print("Usage: add changeset to import")
        sys.exit(1)
    changeset_loc = sys.argv[1]
    print(changeset_loc)

    load_changeset(changeset_loc)