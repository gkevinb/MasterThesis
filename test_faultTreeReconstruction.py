import unittest
import faultTreeReconstruction as ftr


class GetBasicEventTestCase(unittest.TestCase):

    def setUp(self):
        self.list_of_mcs_4 = [None] * 3
        self.list_of_mcs_4[0] = [[1, 3], [1, 4], [2, 3], [2, 4]]
        self.list_of_mcs_4[1] = ((1, 2), (3,), (4,))
        self.list_of_mcs_4[2] = ((1, 2), (3,), (4,))

        self.list_of_mcs_2 = [None] * 2
        self.list_of_mcs_2[0] = ((1,), (2,))
        self.list_of_mcs_2[1] = ((1, 2),)

    def test_BasicEvent_2(self):
        for mcs in self.list_of_mcs_2:
            self.assertEqual(ftr.get_basic_events(mcs), {1, 2})

    def test_BasicEvent_4(self):
        for mcs in self.list_of_mcs_4:
            self.assertEqual(ftr.get_basic_events(mcs), {1, 2, 3, 4})

    def test_CreateEventMCSDictionary(self):
        basic_events = ftr.get_basic_events(self.list_of_mcs_4[0])
        answer = {(1,): {0, 1}, (2,): {2, 3}, (3,): {0, 2}, (4,): {1, 3}}
        self.assertEqual(ftr.create_event_cut_set_dict(basic_events, self.list_of_mcs_4[0]), answer)


class SetsTestCase(unittest.TestCase):

    def setUp(self):
        self.set1 = {1, 2}
        self.set2 = {1, 2}
        self.set3 = {3, 4}
        self.set4 = {2, 3}

    def test_SetsIdentical(self):
        self.assertTrue(ftr.is_sets_identical(self.set1, self.set2), 'Sets should be identical')

    def test_SetsMutuallyExclusive(self):
        self.assertTrue(ftr.is_sets_mutually_exclusive(self.set1, self.set3), 'Sets should be mutually exclusive')

    def test_NotSetsIdentical(self):
        self.assertFalse(ftr.is_sets_identical(self.set2, self.set3), 'Sets should not be identical')

    def test_NotSetsMutuallyExclusive(self):
        self.assertFalse(ftr.is_sets_mutually_exclusive(self.set3, self.set4), 'Sets should not be mutually exclusive')


if __name__ == '__main__':
    unittest.main()
