import unittest
from eapi.hw import EAModul, DimmbaresEAModul


class DimmbaresEAModulTest(unittest.TestCase):
    def setUp(self):
        self.ea = DimmbaresEAModul()

    def tearDown(self):
        self.ea.cleanup()

    def test_schalte_led(self):
        for farbe in [EAModul.LED_ROT, EAModul.LED_GELB, EAModul.LED_GRUEN]:
            self.ea.schalte_led(farbe, 1)
            self.ea.schalte_led(farbe, 0)

            wert = 0.0
            while wert <= 1.0:
                self.ea.schalte_led(farbe, wert)
                wert += 0.1

        with self.assertRaises(ValueError):
            self.ea.schalte_led(0, 1.1)


class EAModulTest(unittest.TestCase):
    def setUp(self):
        self.ea = EAModul()

    def tearDown(self):
        self.ea.cleanup()

    def test_init(self):
        self.ea = EAModul(29, 31, 33, 35, 37)
        self.assertIsNotNone(self.ea)

        with self.assertRaises(Exception):
            EAModul(1, 2, 3, 4, 5, 6)

    def test_schalte_led(self):
        for farbe in [EAModul.LED_ROT, EAModul.LED_GELB, EAModul.LED_GRUEN]:
            self.ea.schalte_led(farbe, 1)
            self.ea.schalte_led(farbe, 0)

        with self.assertRaises(ValueError):
            self.ea.schalte_led(0, 0.5)

        with self.assertRaises(ValueError):
            self.ea.schalte_led(0, 1.1)
            
    def test_taster_gedrueckt(self):
        for i in [0, 1]:
            b = self.ea.taster_gedrueckt(i)
            self.assertIsInstance(b, bool)

        with self.assertRaises(ValueError):
            self.ea.taster_gedrueckt(2)

    def test_event_registrieren(self):
        def m(p):
            pass

        self.ea.taster_event_registrieren(0, m)
        self.ea.taster_event_registrieren(1, m)


if __name__ == '__main__':
    unittest.main()
