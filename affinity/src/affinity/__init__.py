'''
Created on May 18, 2014

@author: ashish
'''


import ctypes.util
import os


NO_OF_CPU = os.sysconf('SC_NPROCESSORS_ONLN')
if NO_OF_CPU < 1:
    raise Exception, 'Unsupported platform'

libc = ctypes.CDLL(ctypes.util.find_library('c'))

SZ_LONG = ctypes.sizeof(ctypes.c_ulong)  # 
CPU_SET_SIZE = 1024  # from sched.h


class cpu_set(ctypes.Structure):
    
    _fields_ = [("bits", ctypes.c_ulong * (CPU_SET_SIZE / SZ_LONG))]  # to represent cpu_set_t from sched.h
    
    def __init__(self, cpus_ = None):
        for i_ in xrange(CPU_SET_SIZE / SZ_LONG):
            self.bits[i_] = 0
        if cpus_:
            for cpu_id_ in cpus_:
                self.enable(cpu_id_)
    
    def enable(self, cpu_id_):
        if cpu_id_ < 0 or cpu_id_ >= NO_OF_CPU:
            raise ValueError, "Invalid CPU id %d, it doesn't exist", cpu_id_
        self.bits[cpu_id_ / SZ_LONG] |= 1 << (cpu_id_ % SZ_LONG)
    
    def is_enabled(self, cpu_id_):
        if cpu_id_ < 0 or cpu_id_ >= NO_OF_CPU:
            raise ValueError, "Invalid CPU id %d, it doesn't exist", cpu_id_
        return ((self.bits[cpu_id_ / SZ_LONG]) & (1 << (cpu_id_ % SZ_LONG))) != 0
    
    def to_list(self):
        return [ i_ for i_ in range(NO_OF_CPU) if self.is_enabled(i_) ]

set_affinity = libc.sched_setaffinity
set_affinity.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(cpu_set)]
set_affinity.restype = ctypes.c_int

get_affinity = libc.sched_getaffinity
get_affinity.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(cpu_set)]
get_affinity.restype = ctypes.c_int

errno_location = libc.__errno_location
errno_location.restype = ctypes.POINTER(ctypes.c_int)

def sched_setaffinity(pid_, cpus_):  # same name as in python3
    cpu_set_ = cpu_set(cpus_)
    result_ = set_affinity(pid_, ctypes.sizeof(cpu_set), cpu_set_)
    if result_ != 0:
        errno_ = errno_location().contents.value;
        raise OSError(errno_, os.strerror(errno_))

def sched_getaffinity(pid_):  # same name as in python3
    cpu_set_ = cpu_set()
    result_ = get_affinity(pid_, ctypes.sizeof(cpu_set), cpu_set_)
    if result_ != 0:
        errno_ = errno_location().contents.value;
        raise OSError(errno_, os.strerror(errno_))
    return cpu_set_.to_list()

import inspect

if (hasattr(os, 'sched_setaffinity') and inspect.isfunction(os.sched_setaffinity)) or (hasattr(os, 'sched_getaffinity') and inspect.isfunction(os.sched_getaffinity)):
    pass
else:
    # installing these functions into os module, so that code can be ported to python 3 easily
    os.sched_setaffinity = sched_setaffinity  
    os.sched_getaffinity = sched_getaffinity 

    


