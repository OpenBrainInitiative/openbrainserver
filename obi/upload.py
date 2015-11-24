from uuid import uuid4
from fs.osfs import OSFS
import os
upload_fs = OSFS('/home/wolfv/Programs/obi/uploads')

from werkzeug.datastructures import FileStorage

def upload_file(databucket, in_file):
    fn = uuid4()
    path_file = os.path.join(str(databucket.uuid), str(fn))
    print(path_file)
    if not upload_fs.isdir('/' + str(databucket.uuid)):
        upload_fs.makedir('/' + str(databucket.uuid))

    fp = upload_fs.open(str(path_file), 'wb+')
    if isinstance(in_file, FileStorage):
        in_file.save(fp)
    elif hasattr(in_file, 'read'):
        fp.write(in_file.read())
    else:
        fp.write(in_file)
    fp.close()
    return path_file
