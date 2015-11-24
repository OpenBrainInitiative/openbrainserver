sudo -u postgres dropdb obi
sudo -u postgres createdb obi
sudo -u postgres psql obi -c 'create extension hstore'
python db.py
python tests/setup_database.py
