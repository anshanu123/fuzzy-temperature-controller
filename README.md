# Fuzzy Temperature Controller

A small, reproducible **Mamdani Fuzzy Inference System (FIS)** that converts temperature error into a heater-power command (0–100%).

This project was prepared as the implementation for the **Soft Computing, Unit II** activity:

> Implement a soft-computing algorithm using a dataset and present the results.

## What it demonstrates

- Crisp input calculation: `error = setpoint - measured_temperature`
- Fuzzification with triangular and trapezoidal membership functions
- Mamdani min implication and max aggregation
- Centroid defuzzification
- Batch processing of a CSV dataset
- Unit tests and optional visualizations

**Safety:** this is an educational software simulation. It does not read a physical sensor or control a real heater. Do not connect it to hardware without independent safety controls, engineering review and hardware-in-the-loop validation.

## Project structure

```text
fuzzy-temperature-controller/
├── data/
│   └── temperature_dataset.csv
├── docs/
│   └── methodology.md
├── results/
│   └── .gitkeep
├── src/
│   └── fuzzy_temperature/
│       ├── __init__.py
│       ├── controller.py
│       ├── membership.py
│       └── dataset.py
├── tests/
│   └── test_controller.py
├── visualizations/
│   └── .gitkeep
├── main.py
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Requirements

- Python 3.9+
- Core implementation uses only the Python standard library.
- `matplotlib` is optional and only needed for plots.

## Run on Windows

Open Command Prompt in the repository folder:

```bash
python --version
python main.py
```

The program reads `data/temperature_dataset.csv`, prints a result table and writes:

```text
results/fuzzy_controller_results.csv
```

### Optional plots

```bash
python -m pip install -r requirements.txt
python main.py --plot
```

The plot is saved to `visualizations/controller_output.png`.

### Run tests

```bash
python -m unittest discover -s tests -v
```

## Input dataset

`data/temperature_dataset.csv` contains illustrative sample values with these columns:

| Column | Meaning |
|---|---|
| `sample_id` | Unique sample number |
| `setpoint_c` | Desired temperature in °C |
| `measured_temperature_c` | Measured/simulated temperature in °C |

The sample CSV is a **synthetic teaching dataset**, not actual sensor readings.

## Controller design

The error is:

\[
e = T_{set} - T_{measured}
\]

The input universe is limited to -10°C through +10°C.

Input fuzzy sets:

- `negative`: temperature is above the setpoint
- `zero`: temperature is approximately at the setpoint
- `positive_small`: temperature is slightly below the setpoint
- `positive_large`: temperature is significantly below the setpoint

Output universe: heater power from 0% to 100%.

Mamdani rules:

1. IF error is Negative THEN heater is Off.
2. IF error is Zero THEN heater is Low.
3. IF error is Positive Small THEN heater is Medium.
4. IF error is Positive Large THEN heater is High.

The implementation clips each output membership function by its rule firing strength, aggregates the clipped sets using maximum, then calculates the centroid.

## Important interpretation

The output is a **control recommendation**, not a simulated room-temperature trajectory. The dataset supplies independent temperature samples; it does not model thermal inertia, heater dynamics, room heat loss or sensor delay. To evaluate closed-loop control performance (overshoot, settling time and steady-state error), a separate plant/thermal model is needed.

## Academic details

- Course: Soft Computing
- Course code: RN226MD303
- Class: SY M.Tech, Semester III
- Academic year: 2026–27
- Student: Anshanu Birajdar
- Roll No.: 07
- Institute: D. Y. Patil College of Engineering, Akurdi

## Suggested demonstration

1. Explain the setpoint and measured temperature.
2. Show the CSV input.
3. Explain the membership functions and IF–THEN rules.
4. Run `python main.py`.
5. Open the generated result CSV and explain how heater power changes as the error changes.
6. Run the unit tests to demonstrate correctness of core functions.
