import unittest

from nhlstats.models import Player


class TestModelPlayer(unittest.TestCase):
      def test_height_na(self):
            p = Player()
            self.assertEqual(p.height, None)
            self.assertEqual(p.height_imperial, 'N/A')
            self.assertEqual(p.height_metric, 'N/A')

            p = Player(height=0)
            self.assertEqual(p.height, 0)
            self.assertEqual(p.height_imperial, 'N/A')
            self.assertEqual(p.height_metric, 'N/A')

      def test_weight_na(self):
            p = Player()
            self.assertEqual(p.weight, None)
            self.assertEqual(p.weight_imperial, 'N/A')
            self.assertEqual(p.weight_metric, 'N/A')

            p = Player(weight=0)
            self.assertEqual(p.weight, 0)
            self.assertEqual(p.weight_imperial, 'N/A')
            self.assertEqual(p.weight_metric, 'N/A')

      def test_height_imperial(self):
            p = Player(height=72)
            self.assertEqual(p.height_imperial, '6\'0"')
            p = Player(height=71)
            self.assertEqual(p.height_imperial, '5\'11"')

      def height_metric(self):
            p = Player(height=72)
            self.assertEqual(p.height_metric, '144cm')

      def test_weight_imperial(self):
            p = Player(weight=175)
            self.assertEqual(p.weight_imperial, '175lbs')

      def test_weight_metric(self):
            p = Player(weight=175)
            self.assertEqual(p.weight_metric, '79.0kg')
