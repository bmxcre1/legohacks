import ctypes
from ctypes import wintypes

class MemoryAPI:
    def __init__(self, process_name="RobloxPlayerBeta.exe"):
        self.kernel32 = ctypes.WinDLL('kernel32')
        self.psapi = ctypes.WinDLL('Psapi.dll')
        self.process_name = process_name
        self.process = self.open_process()

    def get_process_list(self):
        arr = (wintypes.DWORD * 256)()
        pids = ctypes.sizeof(arr)
        self.psapi.EnumProcesses(ctypes.byref(arr), ctypes.sizeof(arr), ctypes.byref(pids))
        return [i for i in arr if i != 0]

    def open_process(self, desired_access=wintypes.DWORD(0x0010 | 0x0020 | 0x0008)):
        for pid in self.get_process_list():
            process = self.kernel32.OpenProcess(desired_access, False, pid)
            if process:
                exe_name = ctypes.create_unicode_buffer(512)
                self.psapi.GetModuleBaseNameW(process, None, exe_name, 512)
                if exe_name.value == self.process_name:
                    return process
                self.kernel32.CloseHandle(process)
        raise Exception(f"Process '{self.process_name}' not found")

    def read_memory(self, address, num_bytes):
        buffer = (ctypes.c_char * num_bytes)()
        bytesRead = wintypes.SIZE_T()
        if not self.kernel32.ReadProcessMemory(self.process, ctypes.c_void_p(address), buffer, num_bytes, ctypes.byref(bytesRead)):
            raise Exception("Failed to read memory at address: 0x{:X}".format(address))
        return buffer.raw

    def write_memory(self, address, data_bytes):
        num_bytes = len(data_bytes)
        buffer = (ctypes.c_char * num_bytes).from_buffer_copy(data_bytes)
        bytesWritten = wintypes.SIZE_T()
        if not self.kernel32.WriteProcessMemory(self.process, ctypes.c_void_p(address), buffer, num_bytes, ctypes.byref(bytesWritten)):
            raise Exception("Failed to write memory at address: 0x{:X}".format(address))

    def __del__(self):
        if self.process:
            self.kernel32.CloseHandle(self.process)
