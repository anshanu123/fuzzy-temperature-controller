"""CSV input/output helpers for the temperature-controller practical."""
import csv
from pathlib import Path
from typing import Dict, List

from .controller import FuzzyTemperatureController

REQUIRED_COLUMNS = {"sample_id", "setpoint_c", "measured_temperature_c"}


def process_dataset(input_path: str, output_path: str) -> List[Dict[str, object]]:
    """Run the controller for every CSV row and write calculated results."""
    controller = FuzzyTemperatureController()
    results: List[Dict[str, object]] = []

    with open(input_path, newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain columns: sample_id, setpoint_c, measured_temperature_c"
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                setpoint = float(row["setpoint_c"])
                measured = float(row["measured_temperature_c"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid temperature value on CSV line {line_number}") from exc

            result = controller.predict(setpoint, measured)
            results.append({
                "sample_id": row["sample_id"],
                "setpoint_c": setpoint,
                "measured_temperature_c": measured,
                "error_c": round(result.error_c, 2),
                "heater_power_percent": result.heater_power_percent,
            })

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "sample_id", "setpoint_c", "measured_temperature_c",
        "error_c", "heater_power_percent"
    ]
    with output.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    return results
