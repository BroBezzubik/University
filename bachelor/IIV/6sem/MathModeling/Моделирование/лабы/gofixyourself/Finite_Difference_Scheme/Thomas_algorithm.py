def thomas_algorithm(low_values, middle_values, upper_values, function_values):
    alpha = [-upper_values[0] / middle_values[0]]
    beta = [function_values[0] / middle_values[0]]
    n = len(function_values)
    x = [0 for _ in range(n)]

    for i in range(1, n - 1):
        alpha.append(-upper_values[i] / (middle_values[i] + low_values[i - 1] * alpha[i - 1]))
        beta.append((function_values[i] - low_values[i - 1] * beta[i - 1]) / (
                middle_values[i] + low_values[i - 1] * alpha[i - 1]))

    x[n - 1] = (-low_values[n - 2] * beta[n - 2] + function_values[n - 1]) / (
            middle_values[n - 1] + low_values[n - 2] * alpha[n - 2])
    for i in reversed(range(n - 1)):
        x[i] = alpha[i] * x[i + 1] + beta[i]

    return x
