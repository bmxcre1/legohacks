import os
import glob
import re

def GetDataModel():

    def get_latest_log_file(logs_folder):
        log_files = glob.glob(os.path.join(logs_folder, '*.log'))
        if not log_files:
            return None
        latest_log_file = max(log_files, key=os.path.getmtime)
        return latest_log_file

    roblox_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox')
    logs_folder = os.path.join(roblox_path, 'Logs')

    def scan_datamodel(log_file):
        pattern = re.compile(r'dataModel\(([0-9a-fA-F]+)\)')
        memory_addresses = []
        with open(log_file, 'r', encoding='utf-8') as file:
            for line in file:
                match = pattern.search(line)
                if match:
                    memory_addresses.append(match.group(1))
        return memory_addresses

    if not (os.path.exists(roblox_path) and os.path.exists(logs_folder)):
        print("Error fetching DataModel ERR:01")
        return False

    latest_log_file = get_latest_log_file(logs_folder)
    if latest_log_file is None:
        print("Error fetching DataModel ERR:02")
        return False

    datamodel_addresses = scan_datamodel(latest_log_file)
    if not datamodel_addresses:
        print("Error fetching DataModel ERR:03")
        return False

    return datamodel_addresses[0]


