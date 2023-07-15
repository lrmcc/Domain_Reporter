import tkinter.messagebox as tkmsg
import datetime
import json

def create_entry(domain, domain_status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"timestamp": timestamp, "domain": domain, "status": domain_status}

def append_entry(entry, file_path):
    data = get_file_data(file_path)
    data.append(entry)
    write_file(data, file_path)

def get_last_entry(file_path):
    data = get_file_data(file_path)
    if data:
        return data[-1]
    else:
        return None
        
def get_file_data(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def write_file(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        print(f"Status appended to {file_path}")

