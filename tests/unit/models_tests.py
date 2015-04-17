import unittest

from nhlstats.models import Player, PlayerSkaterStat, PlayerGoalieStat


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


<<<<<<< HEAD
class TestModelPlayerSkaterStat(unittest.TestCase):

    def test_ptspg(self):
        pks = PlayerSkaterStat(gp=82, pts=41)
        self.assertEqual(pks.ptspgp, '0.50')
        pks = PlayerSkaterStat(gp=82, pts=82)
        self.assertEqual(pks.ptspgp, '1.00')
        pks = PlayerSkaterStat(gp=82, pts=164)
        self.assertEqual(pks.ptspgp, '2.00')

    def test_shotpct(self):
        pks = PlayerSkaterStat(shots=25, g=5)
        self.assertEqual(pks.shotpct, '20.0')
        pks = PlayerSkaterStat(shots=100, g=5)
        self.assertEqual(pks.shotpct, '5.0')
        pks = PlayerSkaterStat(shots=100, g=100)
        self.assertEqual(pks.shotpct, '100.0')


class TestModelPlayerGoalieStat(unittest.TestCase):

    def test_gaa(self):
        pgs = PlayerGoalieStat(ga=1, min=60)
        self.assertEqual(pgs.gaa, '1.00')
        pks = PlayerSkaterStat(gp=82, pts=41)
        self.assertEqual(pks.ptspgp, '0.50')
        pgs = PlayerGoalieStat(ga=100, min=1600)
        self.assertEqual(pgs.gaa, '3.75')

    def test_svpct(self):
        pgs = PlayerGoalieStat(ga=1, sha=100)
        self.assertEqual(pgs.svpct, '0.990')
        pgs = PlayerGoalieStat(ga=75, sha=500)
        self.assertEqual(pgs.svpct, '0.850')
        pgs = PlayerGoalieStat(ga=1, sha=100)
        self.assertEqual(pgs.svpct, '0.990')
=======
class TestModelGame(unittest.TestCase):

    def test_get_active(self):
        raise
>>>>>>> Further refined concept of active games, we now only concern ourselves with games not finished less than 24 hours old, introducing the concept of orphaned games (of which there certainly are some, especially in the pre-season, thanks NHL!)
