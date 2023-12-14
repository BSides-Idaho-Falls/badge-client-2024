
default_registration_key = "ded764bc-fd7a-470e-9df2-27bd3b05117a"

def init_db():
    try:
        f = open("db.json", "r")
    except OSError:
        pass

