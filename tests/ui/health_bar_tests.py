import unittest

from src.ui.health_bar import HealthBarView


class HealthBarTests(unittest.TestCase):

    def test_full_bar(self):
        view = HealthBarView().get_view(100, 100)
        expected = "■■■■■■■■■■"
        self.assertEqual(view, expected)

    def test_empty_bar(self):
        view = HealthBarView().get_view(0, 100)
        expected = "⧄⧄⧄⧄⧄⧄⧄⧄⧄⧄"
        self.assertEqual(view, expected)

    def test_partial_bar(self):
        view = HealthBarView().get_view(56, 100)
        expected = "■■■■■◩⧄⧄⧄⧄"
        self.assertEqual(view, expected)

    def test_round_up_bar(self):
        view = HealthBarView().get_view(78, 100)
        expected = "■■■■■■■■⧄⧄"
        self.assertEqual(view, expected)

    def test_round_down_bar(self):
        view = HealthBarView().get_view(81, 100)
        expected = "■■■■■■■■⧄⧄"
        self.assertEqual(expected, view)