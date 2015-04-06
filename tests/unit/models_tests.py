import unittest

from nhlstats.models import Player


class TestModelPlayer(unittest.TestCase):
      def test_height_na(self):
            p = Player()
            self.assertEqual(p.height_imperial, 'N/A')