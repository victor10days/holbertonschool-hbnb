from flask import current_app

def facade():
    return current_app.config["FACADE"]
