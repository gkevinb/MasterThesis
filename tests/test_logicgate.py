import unittest
from modules import logicgate

HIGH = 'HIGH'
LOW = 'LOW'


class KNVotingGateTestCase(unittest.TestCase):

    def setUp(self):
        self.slice_ = [LOW, HIGH, LOW, HIGH, LOW]
        self.s1 = [1, 4]
        self.s2 = [3, 5, 6, 8, 9]
        self.s3 = [2, 7]
        self.streams = [self.s1, self.s2, self.s3]

    def test_IsAtLeastKDown(self):
        self.assertTrue(logicgate._is_at_least_k_down(self.slice_, 1))
        self.assertTrue(logicgate._is_at_least_k_down(self.slice_, 2))
        self.assertTrue(logicgate._is_at_least_k_down(self.slice_, 3))
        self.assertFalse(logicgate._is_at_least_k_down(self.slice_, 4))
        self.assertFalse(logicgate._is_at_least_k_down(self.slice_, 5))

    def test_EvaluateSliceKVoting(self):
        self.assertEqual(logicgate._k_voting_evaluate_slice(self.slice_, 1), LOW)
        self.assertEqual(logicgate._k_voting_evaluate_slice(self.slice_, 2), LOW)
        self.assertEqual(logicgate._k_voting_evaluate_slice(self.slice_, 3), LOW)
        self.assertEqual(logicgate._k_voting_evaluate_slice(self.slice_, 4), HIGH)
        self.assertEqual(logicgate._k_voting_evaluate_slice(self.slice_, 5), HIGH)

    def test_Evaluate(self):
        self.assertEqual(logicgate.evaluate(2, self.streams), [2, 5, 6, 7])


class AndGateTestCase(unittest.TestCase):

    def setUp(self):
        x = [8.618904143724958, 18.760026889953128]
        y = [9.754214745654227, 16.54121097802728]
        self.data_streams = [x, y]

    def test_Evaluate(self):
        self.assertEqual(logicgate.evaluate('AND', self.data_streams), [8.618904143724958, 18.760026889953128])


if __name__ == '__main__':
    unittest.main()
