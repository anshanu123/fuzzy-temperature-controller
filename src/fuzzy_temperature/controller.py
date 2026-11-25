"""Mamdani fuzzy inference controller for a teaching temperature-control example."""
from dataclasses import dataclass
from typing import Dict, List

from .membership import triangular, trapezoidal


@dataclass(frozen=True)
class ControllerResult:
    error_c: float
    heater_power_percent: float
    input_memberships: Dict[str, float]
    rule_strengths: Dict[str, float]


class FuzzyTemperatureController:
    """Convert setpoint error to a heater-power recommendation.

    Input range: -10 to +10 degrees C.
    Mamdani min implication, max aggregation and centroid defuzzification.
    """

    INPUT_MIN = -10.0
    INPUT_MAX = 10.0
    OUTPUT_MIN = 0
    OUTPUT_MAX = 100

    def fuzzify(self, error_c: float) -> Dict[str, float]:
        error = max(self.INPUT_MIN, min(self.INPUT_MAX, float(error_c)))
        return {
            "negative": trapezoidal(error, -10, -10, -4, 0),
            "zero": triangular(error, -3, 0, 3),
            "positive_small": triangular(error, 0, 3, 7),
            "positive_large": trapezoidal(error, 4, 7, 10, 10),
        }

    @staticmethod
    def _output_memberships(power: int) -> Dict[str, float]:
        return {
            "off": trapezoidal(power, 0, 0, 5, 20),
            "low": triangular(power, 5, 25, 45),
            "medium": triangular(power, 30, 55, 80),
            "high": trapezoidal(power, 65, 85, 100, 100),
        }

    def infer(self, error_c: float) -> ControllerResult:
        memberships = self.fuzzify(error_c)
        strengths = {
            "off": memberships["negative"],
            "low": memberships["zero"],
            "medium": memberships["positive_small"],
            "high": memberships["positive_large"],
        }

        aggregated: List[float] = []
        for power in range(self.OUTPUT_MIN, self.OUTPUT_MAX + 1):
            output_sets = self._output_memberships(power)
            clipped = [
                min(strengths[label], output_sets[label])
                for label in ("off", "low", "medium", "high")
            ]
            aggregated.append(max(clipped))

        denominator = sum(aggregated)
        if denominator == 0.0:
            crisp_output = 0.0
        else:
            crisp_output = sum(
                power * degree
                for power, degree in zip(
                    range(self.OUTPUT_MIN, self.OUTPUT_MAX + 1), aggregated
                )
            ) / denominator

        return ControllerResult(
            error_c=float(error_c),
            heater_power_percent=round(crisp_output, 2),
            input_memberships=memberships,
            rule_strengths=strengths,
        )

    def predict(self, setpoint_c: float, measured_temperature_c: float) -> ControllerResult:
        """Calculate error and infer heater-power recommendation."""
        return self.infer(float(setpoint_c) - float(measured_temperature_c))
