from obi import app

# allow running from the command line
if __name__ == '__main__':
    print([rule for rule in app.url_map.iter_rules()])
    app.run()
