# Methodology — Fuzzy Temperature Controller

## 1. Problem definition

The controller receives a desired setpoint temperature and a measured temperature. It calculates the difference and recommends a heater command between 0% and 100%.

\[
e = T_{set} - T_{measured}
\]

A positive error indicates that the measured temperature is below the setpoint. A negative error indicates that it is above the setpoint.

## 2. Fuzzy sets

The input error is clipped to the universe [-10, +10] °C and fuzzified into:

| Fuzzy set | Membership function | Interpretation |
|---|---|---|
| Negative | Trapezoidal (-10, -10, -4, 0) | Above setpoint |
| Zero | Triangular (-3, 0, 3) | Near setpoint |
| Positive Small | Triangular (0, 3, 7) | Slightly below setpoint |
| Positive Large | Trapezoidal (4, 7, 10, 10) | Significantly below setpoint |

The output universe is heater power from 0% to 100%, with Off, Low, Medium and High fuzzy sets.

## 3. Rule base

- IF error is Negative THEN output is Off.
- IF error is Zero THEN output is Low.
- IF error is Positive Small THEN output is Medium.
- IF error is Positive Large THEN output is High.

These are simple educational rules. A real thermal plant may need more rules and an input for rate of change of error.

## 4. Inference

Mamdani inference is used. Each rule clips its consequent membership function using the minimum operator. The rule outputs are combined using maximum aggregation.

## 5. Defuzzification

The centroid method converts the aggregated fuzzy output into a crisp heater command:

\[
u^* = \frac{\sum_u u\,\mu_{agg}(u)}{\sum_u \mu_{agg}(u)}
\]

The implementation samples integer output values from 0 to 100.

## 6. Dataset and limitations

The included CSV is synthetic and demonstrates batch inference. It is not a time-series simulation of a physical room. It does not model thermal inertia, ambient heat loss, actuator dynamics or sensor lag. Therefore, this experiment demonstrates fuzzy inference and output generation, not closed-loop control performance.

## 7. Evaluation

The program checks that outputs remain within 0–100%, and tests membership functions, error calculation and expected behavior for cold versus hot conditions. To study overshoot, settling time or steady-state error, extend the project with a thermal plant model and compare against a baseline controller.
