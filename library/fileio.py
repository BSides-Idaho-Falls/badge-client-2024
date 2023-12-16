import json


def get_local_data():
    try:
        f = open("db.json", "r")
        data = json.loads(f.read())
        f.close()
        return data
    except Exception:
        print("Returning fresh database")
        return {}


def write_local_data(data):
    if isinstance(data, dict):
        data = json.dumps(data)
    f = open("db.json", 'w')
    f.write(data)
    f.close()
    return True
