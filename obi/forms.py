from flask_wtf import Form
from wtforms import *

class DataBucketForm(Form):
	name = TextField('Name')
	data_type = SelectField("Data Type", choices=[('Image', 'IMAGE'), ('Text', 'TEXT')])

class ImageDataForm(Form):
	pass