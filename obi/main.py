try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
import MySQLdb
from peewee import *

# Registering expressions with peewee

NOT_LIKE = 'NOT LIKE'

def notLike(lhs, rhs):
    return Expression(lhs, NOT_LIKE, rhs)

MySQLDatabase.register_ops({NOT_LIKE: 'NOT LIKE'})

''' GLOBALS '''
db = MySQLDatabase('my_database', user='my_username')

def setupDB():
  db.connect()
  # setup tables here
  # Example: MyModel.create_table(True)
  db.close()


class SuperModel(Model):
    """A base model that will use our Mysql database"""
    class Meta:
        database = db

''' Example
class MyModel(SuperModel):
	createdAt = DateTimeField('%Y-%m-%d %H:%M:%S')
    updatedAt = DateTimeField('%Y-%m-%d %H:%M:%S')
    name = CharField()
'''


