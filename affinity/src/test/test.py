'''
Created on May 18, 2014

@author: ashish
'''

import unittest
import affinity
import os

class TestAffinity(unittest.TestCase):
    def test_set_affinity_and_check(self):
        os.sched_setaffinity(0, [0, 1])
        s_ = os.sched_getaffinity(0)
        self.assertTrue(0 in s_)
        self.assertTrue(1 in s_)
        os.sched_setaffinity(0, [0])
        s_ = os.sched_getaffinity(0)
        self.assertTrue(0 in s_)
        self.assertFalse(1 in s_)
        for i_ in xrange(affinity.NO_OF_CPU):
            os.sched_setaffinity(0, [i_])
            s_ = os.sched_getaffinity(0)
            self.assertTrue(i_ in s_)

        os.sched_setaffinity(0, [0, 1])
        self.assertEqual([0, 1], os.sched_getaffinity(0))

if __name__ == "__main__":
    unittest.main()
