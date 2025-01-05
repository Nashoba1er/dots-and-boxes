# tests/test_fonctions_de_jeu.py

import unittest

from dots_and_boxes.fonctions_de_jeu import carre, test_danger


class TestFonctionsDeJeu(unittest.TestCase):

    def test_carre(self):
        [H, V, C] = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0], [0, 0]],
        ]
        self.assertEqual(carre([H, C, V], (0, 0, 255)), False)
        [H, V, C] = [
            [[1, 1, 0], [1, 0, 0], [0, 0, 0]],
            [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0], [0, 0]],
        ]
        self.assertEqual(carre([H, C, V], (0, 0, 255)), True)

    def test_test_danger(self):
        [H, V, C] = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0], [0, 0]],
        ]
        self.assertEqual(test_danger((0, 0, 0), [H, C, V], False))
        [H, V, C] = [
            [[1, 1, 0], [1, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0], [0, 0]],
        ]
        self.assertEqual(test_danger((1, 0, 0), [H, C, V], True))


if __name__ == "__main__":
    unittest.main()
