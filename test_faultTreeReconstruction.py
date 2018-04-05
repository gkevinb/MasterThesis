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


class ChildrenTestCase(unittest.TestCase):

    def setUp(self):
        self.events = [{1, 2, 3, 4}, {1, 2}, {3, 4}, {1}, {2}, {3}, {4}]
        self.parent = {0, 1, 2, 3, 4, 5}
        self.children = [{0, 1, 2}, {0, 3, 4}, {1, 3, 5}, {4, 5, 2}]

    def test_FindChildren(self):
        self.assertEqual(ftr.find_children_indices(0, self.events), [1, 2])
        self.assertEqual(ftr.find_children_indices(1, self.events), [3, 4])
        self.assertEqual(ftr.find_children_indices(2, self.events), [5, 6])
        self.assertEqual(ftr.find_children_indices(3, self.events), [])

    def test_ChildrenIdenticalToParent(self):
        self.assertTrue(ftr.is_children_identical_to_parent({0, 1, 2, 3}, [{0, 1, 2, 3}, {0, 1, 2, 3}]))

    def test_ChildrenMutualExclusiveUnionOfParent(self):
        self.assertTrue(ftr.is_children_mutual_exclusive_union_of_parent({0, 1, 2, 3}, [{0, 2}, {1, 3}]))

    def test_ChildrenNChooseKOfParent(self):
        self.assertTrue(ftr.is_children_n_choose_k_of_parent({0, 1, 2}, [{0, 1}, {0, 2}, {1, 2}]))
        self.assertTrue(ftr.is_children_n_choose_k_of_parent(self.parent, self.children))

    def test_CalculateK(self):
        self.assertEqual(ftr.calculate_k_in_voting_gate({0, 1, 2}, [{0, 1}, {0, 2}, {1, 2}]), 2)


class RelationshipTestCase(unittest.TestCase):

    def setUp(self):
        self.sets = [{0, 1, 2, 3}, {0, 2}, {1, 3}]
        self.sets2 = [{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}]
        self.sets3 = [{0, 1, 2}, {0, 1}, {0, 2}, {1, 2}]

    def test_OR(self):
        self.assertEqual(ftr.find_relationship(0, [1, 2], self.sets), 'OR')

    def test_AND(self):
        self.assertEqual(ftr.find_relationship(0, [1, 2], self.sets2), 'AND')

    def test_VOTING(self):
        self.assertEqual(ftr.find_relationship(0, [1, 2, 3], self.sets3), 2)
        self.assertGreater(ftr.find_relationship(0, [1, 2, 3], self.sets3), 1)


class ConversionTestCase(unittest.TestCase):

    def setUp(self):
        self.sets = [{0, 1}, {0, 2}, {1, 2}]

    def test_ListOfSetsToList(self):
        self.assertEqual(ftr.convert_list_of_sets_to_list(self.sets), [0, 1, 0, 2, 1, 2])


if __name__ == '__main__':
    unittest.main()
