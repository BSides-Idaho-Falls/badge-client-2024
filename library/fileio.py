import json


def get_local_data():
    default_registration_key = "ded764bc-fd7a-470e-9df2-27bd3b05117a"
    try:
        f = open("db.json", "r")
        data = json.loads(f.read())
        f.close()
        return data
    except Exception:
        print("Returning fresh database")
        return {
            "registration_token": default_registration_key
        }


def write_local_data(data):
    if isinstance(data, dict):
        data = json.dumps(data)
    f = open("db.json", 'w')
    f.write(data)
    f.close()
    return True
