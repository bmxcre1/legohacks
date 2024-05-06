import os
import pymem
import re
import glob
import GetDM
import VerifyRoblox
import MemoryAPI
import time

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
 
# VERIFY ROBLOX
print("Verifying Roblox")
Roblox,pm,Bloxstrap,Version = VerifyRoblox.Verify()
if not Roblox or not Bloxstrap or not Version:
    print("Failed Roblox Validation")
    exit(2)
else:
    print("Roblox Validated")

# FETCH DATAMODEL
print("Fetching DataModel...")
DataModel = GetDM.GetDataModel()
if DataModel != False:
    print("Fetched DataModel")
    print(DataModel)
else:
    exit(2)
time.sleep(5)




