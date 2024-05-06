# GETDATAMODEL
import psutil
import pymem
import os
import time

def Verify():
    bs_version = 'version-7d64f40489634ca5'
    bloxstrap = False
    roblox = False
    version = False
    pm = None
    process_found = False
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'RobloxPlayerBeta.exe':
            process_found = True
            pm = pymem.Pymem(process.info['pid'])
            break

    if not process_found:
        print("Please run Roblox before injecting")

    print('Found RobloxPlayerBeta.exe')
    roblox = True
    time.sleep(0.7)

    # BLOXSTRAP CHECK

    bloxstrap_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Bloxstrap')
    version_path = os.path.join(bloxstrap_path, 'Versions', bs_version)
    if not os.path.exists(bloxstrap_path):
        print('Bloxstrap not found')
        bloxstrap = False
    else:
         bloxstrap = True

    if os.path.exists(bloxstrap_path) and os.path.exists(version_path) and bloxstrap == True:
        version = True
    else:
        print('Version mismatch, check Discord for updates')

    return roblox,pm,bloxstrap,version
        