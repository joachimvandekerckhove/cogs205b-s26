import numpy as np

def fit_regression(X, y, add_intercept=True):
    """Fit a linear regression model to the provided data.

    Args:
        X (np.ndarray): The feature matrix. Shape (n_samples, n_features).
        y (np.ndarray): The target vector. Shape (n_samples,).
        add_intercept (bool): If True, an intercept term is added to the model.

    Returns:
        np.ndarray: The regression coefficients (beta).
                    If add_intercept is True, beta[0] is the intercept and beta[1:] are the feature coefficients.
                    If add_intercept is False, beta are the feature coefficients.
    """
    if X.ndim == 1:
        X = X.reshape(-1, 1)

    if add_intercept:
        # Add an intercept term (a column of ones) to X
        X = np.hstack((np.ones((X.shape[0], 1)), X))

    # Calculate beta using the normal equation: beta = (X^T X)^(-1) X^T y
    # Using least squares solution to avoid direct matrix inversion for numerical stability
    beta, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)

    return beta
