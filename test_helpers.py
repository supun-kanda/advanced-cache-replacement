import unittest

from collections import OrderedDict
from helpers import remove_values_less_than

class TestFrozenCache(unittest.TestCase):
    def setUp(self):
        self.ordered_dict = OrderedDict([
            [1, [0, 1, 2]],
            [2, [3, 6]],
            [3, [4, 7]],
            [4, [5, 8, 9, 10, 11]]
        ])

    def test_remove_values_less_than_1(self):
        remove_values_less_than(self.ordered_dict, 5)
        self.assertEqual(self.ordered_dict, OrderedDict([
            [2, [6]],
            [3, [7]],
            [4, [5, 8, 9, 10, 11]]
        ]))

    def test_f_score(self):
        futures = OrderedDict([
            (1,[20,25,28]),
            (2,[15,17,18]),
            (3,[10,19]),
            (4,[11,12,22,23]),
            (5,[13]),
            (6,[14,16,21,24]),
            (7,[26,27])
        ])

        f_max = max(futures, key=lambda k: len(futures[k]))
        f_score = {key: len(value)/f_max for key, value in futures.items()}

        self.assertEqual(f_score, {
            1:3/4,
            2:3/4,
            3:2/4,
            4:1,
            5:1/4,
            6:1,
            7:2/4
        })

    def test_i_score(self):
        current_step = 10
        max_step = 28
        r_steps = max_step - current_step
        futures = OrderedDict([
            (1,[20,25,28]),
            (2,[15,17,18]),
            (3,[10,19]),
            (4,[11,12,22,23]),
            (5,[13]),
            (6,[14,16,21,24]),
            (7,[26,27])
        ])

        i_score = {key: (max_step - min(value)) / r_steps for key, value in futures.items()}

        self.assertEqual(i_score, {
            1:8/18,
            2:13/18,
            3:18/18,
            4:17/18,
            5:15/18,
            6:14/18,
            7:2/18
        })

    def test_fi_score(self):
        current_step = 10
        max_step = 28
        r_steps = max_step - current_step
        futures = OrderedDict([
            (1,[20,22,23,25]),
            (2,[15,17,18]),
            (3,[10,19,28]),
            (4,[11,12]),
            (5,[13]),
            (6,[14,16,21,24]),
            (7,[26,27])
        ])

        f_max = max(futures, key=lambda k: len(futures[k]))

        i_score = {key: (max_step - min(value)) / r_steps for key, value in futures.items()}
        f_score = {key: len(value)/r_steps for key, value in futures.items()}

        if_score = {key: i_score[key] + f_score[key] for key in i_score}

        print(if_score)

if __name__ == '__main__':
    unittest.main()