from test import test_support
import unittest

class SortTest(unittest.TestCase):

    def test_bug1835099(self):
        a = [21469, 0, 25093, 21992, 26488, 21392, 21998, 22387, 30011, 18382, 23114, 24329, 29505, 24637, 22922, 24258, 19705, 17497, 16693, 20602, 24780, 14618, 18200, 18468, 24491, 20448, 16797, 25276, 27262, 134009, 132609, 135000, 133027, 133957, 134209, 136300, 135505, 137629, 137364, 136698, 136705, 135020, 138258, 136820, 136502, 140408, 140861, 152317, 150993, 144857, 137562, 138705, 138811, 137456, 138393, 138521, 140876, 140271, 141384, 139595, 141839, 141237, 140742, 140514, 141127, 141411, 141501]
        a_set = set(a)
        a_sorted = sorted(a)
        a_sorted_set = set(a_sorted)

        if a_sorted_set != a_set:
            print 'list elements changed during sort:'
            print 'removed', tuple(a_set - a_sorted_set)
            print 'added', tuple(a_sorted_set - a_set)

        assert len(a_set - a_sorted_set) == len(a_sorted_set - a_set) == 0


    def test_bug1767(self):
        'Test bug 1767 sorting when __cmp__ inconsistent with __eq__'
        
        class Tricky:
                
            def __init__(self, pair):
                self.key0, self.key1 = pair
                
            def __cmp__(self, other):
                # Duplicates standard sort for pairs
                if self.key0 != other.key0:
                    return cmp(self.key0, other.key0)
                return cmp(self.key1, other.key1)
                
            def __eq__(self,other):
                # Compare only on second key: inconsistent with __cmp__()==0
                return self.key1 == other.key1

            def __repr__(self):
                return "(%d, %d)" %(self.key0, self.key1)

        def slowSorted(qq) :
            'Reference sort peformed by insertion using only <'
            rr = list()
            for q in qq :
                i = 0
                for i in range(len(rr)) :
                    if q < rr[i] :
                        rr.insert(i,q)
                        break
                else :
                    rr.append(q)
            return rr

        def check(trick, answer):
            'Check list of Tricky matches list of pairs in order'
            assert len(trick)==len(answer)
            for t, a in zip(trick,answer) :
                # print q, a
                assert t.key0==a[0] and t.key1==a[1]

        # Test material
        question = [(2, 5), (1, 3), (3, 0), (2, 3), (1, 1), (2, 3),
                    (3, 5), (1, 0), (2, 0), (2, 1), (1, 4), (2, 5),
                    (1, 1), (3, 5), (2, 5), (1, 0), (3, 2), (1, 1),
                    (2, 2), (2, 2), (1, 0), (2, 3), (2, 1), (3, 2)]
        answer = slowSorted(question)

        # Test library function
        que = [Tricky(p) for p in question]
        que.sort()
        check(que, answer)

        # Test library function in reverse
        que = [Tricky(p) for p in question]
        que.sort(reverse=True)
        check(que, list(reversed(answer)))



def test_main():
    test_support.run_unittest(SortTest)

if __name__ == "__main__":
    test_main()
