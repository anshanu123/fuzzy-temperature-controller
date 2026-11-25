"""Command-line entry point for the fuzzy temperature controller."""
import argparse
from pathlib import Path

from src.fuzzy_temperature.dataset import process_dataset

ROOT = Path(__file__).resolve().parent


def create_plot(results, output_path):
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            "Plotting requires matplotlib. Install it with: python -m pip install -r requirements.txt"
        ) from exc

    samples = range(1, len(results) + 1)
    measured = [row["measured_temperature_c"] for row in results]
    setpoints = [row["setpoint_c"] for row in results]
    heater = [row["heater_power_percent"] for row in results]

    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    axes[0].plot(samples, measured, marker="o", label="Measured temperature")
    axes[0].plot(samples, setpoints, linestyle="--", label="Setpoint")
    axes[0].set_ylabel("Temperature (°C)")
    axes[0].set_title("Fuzzy Temperature Controller — Dataset Results")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(samples, heater, marker="s", label="Heater power")
    axes[1].set_xlabel("Dataset sample")
    axes[1].set_ylabel("Heater command (%)")
    axes[1].set_ylim(0, 100)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    fig.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Run the Mamdani fuzzy temperature controller.")
    parser.add_argument("--input", default=str(ROOT / "data" / "temperature_dataset.csv"))
    parser.add_argument("--output", default=str(ROOT / "results" / "fuzzy_controller_results.csv"))
    parser.add_argument("--plot", action="store_true", help="Generate an optional PNG plot")
    args = parser.parse_args()

    results = process_dataset(args.input, args.output)

    print("\nFUZZY TEMPERATURE CONTROLLER")
    print("=" * 70)
    print(f"{'ID':<8}{'Setpoint °C':>14}{'Measured °C':>15}{'Error °C':>12}{'Heater %':>12}")
    print("-" * 70)
    for row in results:
        print(
            f"{str(row['sample_id']):<8}"
            f"{row['setpoint_c']:>14.1f}"
            f"{row['measured_temperature_c']:>15.1f}"
            f"{row['error_c']:>12.1f}"
            f"{row['heater_power_percent']:>12.2f}"
        )
    print("-" * 70)
    print(f"Processed {len(results)} rows.")
    print(f"Results saved to: {args.output}")

    if args.plot:
        plot_path = ROOT / "visualizations" / "controller_output.png"
        create_plot(results, plot_path)
        print(f"Plot saved to: {plot_path}")


if __name__ == "__main__":
    main()
