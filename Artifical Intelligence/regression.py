import numpy as np


def add_bias_column(matrix: np.ndarray) -> np.ndarray:
    """Prepend a bias column of ones to the feature matrix."""
    return np.hstack([np.ones((matrix.shape[0], 1)), matrix])


def train_linear_regression(features: np.ndarray, targets: np.ndarray) -> np.ndarray:
    """
    Fit a linear regression model using the normal equation.

    Returns the parameter vector (bias first, then feature weights).
    """
    x_with_bias = add_bias_column(features)
    # Moore-Penrose pseudo-inverse gives a stable closed-form solution.
    return np.linalg.pinv(x_with_bias) @ targets


def predict(features: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Run inference with the learned weights."""
    return add_bias_column(features) @ weights


def r2_score(actual: np.ndarray, predicted: np.ndarray) -> float:
    """Compute the coefficient of determination."""
    residual = actual - predicted
    total = actual - actual.mean()
    return 1.0 - (residual @ residual) / (total @ total)


def main() -> None:
    rng = np.random.default_rng(seed=42)

    # Generate a toy dataset following y = 4x + 7 + noise.
    samples = 200
    x = rng.uniform(0, 10, size=(samples, 1))
    y = 4.0 * x[:, 0] + 7.0 + rng.normal(0.0, 1.5, size=samples)

    weights = train_linear_regression(x, y)
    y_hat = predict(x, weights)
    score = r2_score(y, y_hat)

    print("Learned weights:", weights)
    print("R^2 score:", round(score, 3))

    # Predict a new value.
    new_feature = np.array([[12.0]])
    prediction = predict(new_feature, weights)[0]
    print("Prediction for x=12:", round(prediction, 3))


if __name__ == "__main__":
    main()
