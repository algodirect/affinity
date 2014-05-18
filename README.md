affinity
========
This is to support set/get CPU affinity in python2.

Uagse:-
---------
Note: This package is not required for python 3.*

To set/get process's CPU affinity.

```python
import affinity
affinity.sched_getaffinity(0) # parameter is PID, use 0 for current process
affinity.sched_setaffinity(0, [0,2]) # first parameter is PID, use 0 for current process, second parameter is CPU affinity mask
```

```import affinity``` will install ```sched_setaffinity``` and ```sched_getaffinity``` functions in ```os``` package as well, so that code will be comptible to python3 as well.
Ex:-
```python
import os
import affinity
os.sched_setaffinity(0)  
```

Installation:-
---------
```bash
sudo easy_install cpu_affinity
```
or
```bash
sudo pip install cpu_affinity
```
Demo:-
---------
I did some CPU bound operation and switching the CPU(CORE) after some work.
demo.py
```python
for i_ in xrange(affinity.NO_OF_CPU):
            os.sched_setaffinity(0,[i_])
            for j_ in xrange(2500,6000):
                j_ ** j_
```
CPU profiling of demo.py , different cores are fully utilized after an interval.

![alt tag](https://raw.githubusercontent.com/algodirect/affinity/master/affinity/src/test/demo.png)

