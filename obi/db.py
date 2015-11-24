from peewee import *
import datetime
import jsonpatch
from obi.upload import upload_file
# Registering expressions with peewee
# ''' GLOBALS '''
# db = MySQLDatabase('openbraininitative', user='wolfv', password='abcde')
from playhouse.postgres_ext import *
from uuid import uuid4, UUID
import base64
import json

ext_db = PostgresqlExtDatabase('obi', user='wolfv')

# Dataset types:
# - Textual
#   - Multiple tags
#   - Pointer
# - Image
#   - Single tag / multi tag


def setupDB():
    ext_db.connect()
    # setup tables here
    # Example: MyModel.create_table(True)
    User.create_table(True)
    DataBucket.create_table(True)
    ChangeSet.create_table(True)
    Data.create_table(True)
    ext_db.close()

class DBModel(Model):
    """A base model that will use our Mysql database"""
    class Meta:
        database = ext_db

class User(DBModel):
    name = CharField()

class DataBucket(DBModel):
    name = CharField()
    uuid = UUIDField(default=uuid4)
    created_by = ForeignKeyField(User, default=1)
    created_date = DateTimeField(default=datetime.datetime.now)
    data_type = CharField()
    current_head = UUIDField(default=UUID(int=0))

    def apply_changeset(self, changeset):
        if 'modify' in changeset.changeset:
            cs = changeset.changeset['modify']
            for key in cs:
                try:
                    data_item = self.data.where(Data.uuid == key).get()
                    data_item.apply_changes(cs[key])
                    data_item.save()
                except Data.DoesNotExist:
                    print("There was an error with nonexistent data")

        if 'create' in changeset.changeset:
            cs = changeset.changeset['create']
            for cs_item in cs:
                data_item = Data()
                data_item.bucket = self
                data_item.json_store = {}
                data_item.current_head = changeset.uuid
                data_item.apply_changes(cs_item)
                data_item.save()

        if 'delete' in changeset.changeset:
            print("Not implemented")

        self.current_head = changeset.uuid
        self.save()

    def as_json(self):
        ret_dict = {}
        for d in self.data:
            ret_dict[str(d.uuid)] = d.json_store

        return json.dumps(ret_dict)

class FileObject(DBModel):
    path = CharField()
    name = CharField()

    uuid = UUIDField()
    created_by = ForeignKeyField(User)
    created_date = DateTimeField(default=datetime.datetime.now)
    data_bucket = ForeignKeyField(DataBucket)

    def upload(self, databucket, file_flask):
        upload_file(databucket, file_flask)


class ChangeSet(DBModel):
    uuid = UUIDField(default=uuid4)
    user = ForeignKeyField(User, related_name='changesets')
    bucket = ForeignKeyField(DataBucket)

    created_date = DateTimeField(default=datetime.datetime.now)

    previous_changeset = ForeignKeyField('self', related_name='next_changeset', null=True)
    changeset = JSONField(null=False)

    def __getitem__(self, item):
        return self.changeset[item]

    def check_and_upload(self, cs):
        if cs:
            for op in cs:
                if op['path'] == '/data' and 'file' in op['value']:
                    file_data = base64.b64decode(op['value']['file']['contents'])
                    mime = op['value']['file']['mime']
                    fn = upload_file(self.bucket, file_data)
                    del op['value']['file']['contents']
                    op['value']['file']['uri'] = 'obi://' + fn

    def set_changeset(self, changeset_json):
        # replaces all files in changeset with uploaded uri
        changeset_object = json.loads(changeset_json)

        if 'modify' in changeset_object:
            cs = changeset_object['modify']
            for key in cs:
                self.check_and_upload(cs[key])

        if 'create' in changeset_object:
            cs = changeset_object['create']
            for el in cs:
                self.check_and_upload(el)

        self.changeset = changeset_object


class Data(DBModel):
    bucket = ForeignKeyField(DataBucket, related_name='data')
    uuid = UUIDField(default=uuid4)

    current_head = UUIDField(default=UUID(int=0))
    json_store = JSONField()

    def apply_changes(self, patch):
        print(self)
        print(self.uuid)
        print(self.current_head)
        current_val = self.json_store
        print(current_val)
        if patch:
            new_val = jsonpatch.apply_patch(current_val, patch)
            print(current_val, new_val)
            self.json_store = new_val
        self.save()


class Annotation(DBModel):
    name = CharField()
    description = CharField()
    user = ForeignKeyField(User, related_name='annotations')
    data = ForeignKeyField(Data, related_name='annotations')
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    coordinates = CharField()


class ImageData(DBModel):
    path = CharField()

class TextData(DBModel):
    data = ForeignKeyField(Data, related_name='parent')
    data = TextField()


if __name__ == '__main__':
    import sys, os
    sys.path.insert(1, os.path.dirname(os.getcwd()))

    setupDB()
