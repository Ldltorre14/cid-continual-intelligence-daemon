
import psutil 
import platform
import cpuinfo
import GPUtil
from pydantic import BaseModel
from typing import Any

class CpuSnapshot(BaseModel):
    physical_cores  :  int          = psutil.cpu_count(logical=False)
    logical_cores   :  int          = psutil.cpu_count(logical=True)
    cpu_freq_mhz    :  float        = psutil.cpu_freq().current
    cpu_times       :  Any          = psutil.cpu_times()
    cpu_times_perct :  list[float]  = psutil.cpu_times_percent(percpu=True)
    cpu_utilization :  list[float]  = psutil.cpu_percent(percpu=True)
    cpu_stats       :  Any          = psutil.cpu_stats()  


class CPUInfo(BaseModel):
    pass


class GPUInfo(BaseModel):
    name: str 
    load: float 


class MemoryInfo(BaseModel):
    pass



class SystemHardware(BaseModel):
    cpu          :   CPUInfo
    gpu          :   GPUInfo
    memory       :   MemoryInfo





def get_formatted_cpu_data():

    snapshot = CpuSnapshot()

    cpu_data = f"""
    --- CPU Snapshot ---
    Physical Cores : {snapshot.physical_cores}
    Logical Cores  : {snapshot.logical_cores}
    Current Freq   : {snapshot.cpu_freq_mhz} MHz
    Utilization %  : {snapshot.cpu_utilization} (per core)
    Stats          : {snapshot.cpu_stats}
    --------------------
    """

    return cpu_data



print(get_formatted_cpu_data())