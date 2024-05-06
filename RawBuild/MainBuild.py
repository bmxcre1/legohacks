import os
import psutil
import pymem
import time
import re
import glob
import GetDM
import VerifyRoblox

# GENERAL FUNCTIONS

def plat(aob):
    trueB = bytearray()
    aob = aob.replace(" ", "")
    for i in range(0, len(aob), 2):
        item = aob[i: i + 2]
        trueB.extend(b"." if "?" in item else bytes.fromhex(item))
    return bytes(trueB)

def dechex(dc, UseAuto=None):
    if isinstance(dc, int):
        mask = (2**32 - 1) if UseAuto == 32 else (2**64 - 1)
        return hex(dc & mask).replace('0x', '').upper()
    return dc

def hexle(hex):
    lehex = hex.replace(" ", "").zfill(16 if len(hex) > 8 else 8)
    return ''.join(reversed([lehex[i:i+2] for i in range(0, len(lehex), 2)]))

def hexdec(hex, bit=16):
    return int(hex, bit)

def dereference(pm, address, is64Bit):
    bytes_count = 8 if is64Bit else 4
    return int.from_bytes(pm.read_bytes(address, bytes_count), "little")

def valid_pointer(pm, address, is64Bit):
    try:
        address = hexdec(address) if isinstance(address, str) else address
        pm.read_bytes(dereference(pm, address, is64Bit), 1)
        return True
    except:
        return False

def pattern_scan_all(pm, hex_array, xreturn_multiple=False):
    return pymem.pattern.pattern_scan_all(pm.process_handle, plat(hex_array), return_multiple=xreturn_multiple)

# PROCESS CHECK


def get_latest_log_file(logs_folder):
    log_files = glob.glob(os.path.join(logs_folder, '*.log'))
    if not log_files:
        return None
    latest_log_file = max(log_files, key=os.path.getmtime)
    return latest_log_file

def scan_datamodel(log_file):
    pattern = re.compile(r'dataModel\(([0-9a-fA-F]+)\)')
    memory_addresses = []
    with open(log_file, 'r', encoding='utf-8') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                memory_addresses.append(match.group(1))
    return memory_addresses

# FETCH DATAMODEL
print("Fetching DataModel...")
DataModel = GetDM.GetDataModel()
if DataModel != False:
    print("Fetched DataModel")
else:
    exit()

Roblox,pm,Bloxstrap,Version = VerifyRoblox.Verify()
if not Roblox or not Bloxstrap or not Version:
    print("Failed Roblox Validation")
    exit()
else:
    print("Roblox Validated")

# LOGS CHECK
roblox_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox')
logs_folder = os.path.join(roblox_path, 'Logs')



