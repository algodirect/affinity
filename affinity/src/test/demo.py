'''
Created on May 18, 2014

@author: ashish
'''


import unittest
import affinity
import os

class TestAffinity(unittest.TestCase):
    def test_demo(self):
        for i_ in xrange(affinity.NO_OF_CPU):
            os.sched_setaffinity(0,[i_])
            for j_ in range(2500,6000):
                j_ ** j_

if __name__ == "__main__":
    unittest.main()
