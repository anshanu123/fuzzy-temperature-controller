"""Unit tests for membership functions and fuzzy controller."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.fuzzy_temperature.membership import triangular, trapezoidal
from src.fuzzy_temperature.controller import FuzzyTemperatureController


class MembershipFunctionTests(unittest.TestCase):
    def test_triangle_peak(self):
        self.assertEqual(triangular(2, 0, 2, 4), 1.0)

    def test_triangle_outside_support(self):
        self.assertEqual(triangular(5, 0, 2, 4), 0.0)

    def test_trapezoid_plateau(self):
        self.assertEqual(trapezoidal(3, 0, 1, 4, 5), 1.0)


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.controller = FuzzyTemperatureController()

    def test_output_is_bounded(self):
        for error in (-20, -10, -3, 0, 2, 7, 10, 20):
            output = self.controller.infer(error).heater_power_percent
            self.assertGreaterEqual(output, 0)
            self.assertLessEqual(output, 100)

    def test_large_positive_error_requests_more_heat_than_negative_error(self):
        cold = self.controller.infer(7).heater_power_percent
        hot = self.controller.infer(-5).heater_power_percent
        self.assertGreater(cold, hot)

    def test_setpoint_error_calculation(self):
        self.assertEqual(self.controller.predict(25, 18).error_c, 7)

    def test_zero_error_returns_valid_command(self):
        output = self.controller.predict(25, 25).heater_power_percent
        self.assertGreaterEqual(output, 0)
        self.assertLessEqual(output, 100)


if __name__ == "__main__":
    unittest.main()
