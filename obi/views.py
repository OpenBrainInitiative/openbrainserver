import sys
import json
from uuid import uuid4
from obi import app
from flask import redirect, request, url_for, abort, render_template, flash
from obi.db import *

from obi.forms import DataBucketForm, ImageDataForm

print(app)

@app.route('/')
def home():
    return "WeEW"
    return render_template('home.html', message="My flask peewee template app!!!")


@app.route('/myendpoint', methods=['GET', 'POST'])
def getexample():

    if request.method is 'POST':
        # do stuff
        responseObj = dict(message="this was from a post request!")
    elif request.method is 'GET':
        # do other stuff
        responseObj = dict(message="this was from a get request!")
    # json response
    return json.dumps(responseObj)


@app.route('/data/bucket/<bucket_id>/', methods=['GET', 'POST'])
def show_bucket(bucket_id=None):
    if(bucket_id):
        bucket_json = DataBucket.get(DataBucket.uuid == bucket_id).as_json()
        bucket = DataBucket.get(DataBucket.uuid == bucket_id)
    return render_template('databucket.html', bucket=bucket, bucket_json=bucket_json)


@app.route('/data/bucket/new', methods=['GET', 'POST'])
def add_bucket():
    if request.method == 'POST':
        form = DataBucketForm(request.form)
        if form.validate():
            print(request.form)
            databucket = DataBucket(name=request.form['name'],
                                    data_type=request.form['data_type'])
            databucket.save()

            flash('Your entry has been saved')
    else:
        form = DataBucketForm()

    return render_template('databucket_edit.html', form=form)

@app.route('/data/bucket/<bucket_id>/edit_item/<item_id>')
def edit_item(bucket_id, item_id):
    bucket = DataBucket.objects.get(id=bucket_id)
    bucket.find_item(item_id)
    return "OK"

@app.route('/data/bucket/<bucket_id>/add_item', methods=['GET', 'POST'])
def add_item(bucket_id):
    bucket = DataBucket.objects.get(id=bucket_id)
    if request.method == 'POST':
        bucket.add_item({'name': request.form['name']})
        redirect(url_for('show_bucket', bucket_id=bucket_id))
    if bucket.data_type == 'Image':
        return render_template('new_item.html', bucket_id=bucket_id)
        return "IMAGE"
    elif bucket.data_type == 'Text':
        return render_template('new_item.html')
    return 'Noting'


@app.route('/data/buckets')
def buckets():
    buckets = DataBucket.select()
    return render_template('buckets.html', buckets=buckets)


@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        # filename = upload_key + 
        destination = "/".join([app.config['UPLOAD_DIR'], filename])
        # print "Accept incoming file:", filename
        # print "Save it to:", destination
        # upload.save(destination)
        file_db_obj = FileObject()



    new_image = ImageData()
    new_image.path = destination
    bucket = DataBucket.get(DataBucket.id == int(request.form['bucket_id']))
    print("Bucket ID: %s" % request.form['bucket_id'])
    new_image.bucket = bucket
    new_image.save()
    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return "Upload Done"

def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))