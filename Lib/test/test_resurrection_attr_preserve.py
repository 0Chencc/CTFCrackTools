import unittest
import gc
import time
import weakref

class ReferentDummy:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class ResurrectionDummy:
    def __del__(self):
        ResurrectionDummy.resurrected = self.toResurrect

class SelfResurrectionDummy:
    def __del__(self):
        SelfResurrectionDummy.resurrected = self

class GCDetector():
    gcIndex = 0

    def __del__(self):
        GCDetector.gcIndex += 1

maxGCRun = 10

def runGC():
    """
    This is needed for Jython, since theoretically Java gc is not guaranteed to
    run if gc.collect is called; the run is only attempted. This method assures
    that actually a gc run happens.
    """
    currentIndex = GCDetector.gcIndex
    gcCount = 0
    detector = GCDetector()
    del detector
    gc.collect()
    time.sleep(0.2)
    while currentIndex == GCDetector.gcIndex and gcCount < maxGCRun:
        gc.collect()
        gcCount += 1
        time.sleep(0.2)

class GCTests(unittest.TestCase):

    def test_id_after_self_resurrection(self):
        rd = SelfResurrectionDummy()
        savedId = id(rd)
        rd = None
        runGC() #needed for Jython etc, even though no cyclic trash appears
        self.assertEqual(id(SelfResurrectionDummy.resurrected), savedId)
        del SelfResurrectionDummy.resurrected

    def test_id_after_resurrection(self):
        l = ["ab"]
        rd = ResurrectionDummy()
        rd.toResurrect = l
        savedId = id(l)
        l = None
        rd = None
        runGC() #needed for Jython etc, even though no cyclic trash appears
        self.assertEqual(id(ResurrectionDummy.resurrected), savedId)
        del ResurrectionDummy.resurrected

#todo: Check these test regarding to CPython behavior 
#     def test_weakref_consistency_after_self_resurrection(self):
#         #fails in CPython
#         rd = SelfResurrectionDummy()
#         wref = weakref.ref(rd)
#         self.assertIn(wref, weakref.getweakrefs(rd))
#         rd = None
#         runGC() #needed for Jython etc, even though no cyclic trash appears
#         self.asserIn(wref, weakref.getweakrefs(SelfResurrectionDummy.resurrected))
#         for wref2 in weakref.getweakrefs(SelfResurrectionDummy.resurrected):
#             self.assertIs(wref2(), SelfResurrectionDummy.resurrected)
#         del SelfResurrectionDummy.resurrected
# 
#     def test_weakref_consistency_after_resurrection(self):
#         l = ReferentDummy("ab")
#         rd = ResurrectionDummy()
#         rd.toResurrect = l
#         wref = weakref.ref(l)
#         self.assertIn(wref, weakref.getweakrefs(l))
#         l = None
#         rd = None
#         runGC() #needed for Jython etc, even though no cyclic trash appears
#         self.asserIn(wref, weakref.getweakrefs(ResurrectionDummy.resurrected))
#         for wref2 in weakref.getweakrefs(ResurrectionDummy.resurrected):
#             self.assertIs(wref2(), ResurrectionDummy.resurrected)
#         del ResurrectionDummy.resurrected



if __name__ == '__main__':
    unittest.main()
