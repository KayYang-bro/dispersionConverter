import sympy as sp


def evaluate_conversion(result, wavelengths):
    """
    Compare refractive indices from the original and converted equations.

    Parameters
    ----------
    result : dict
        Conversion result containing the original polynomial
        representation and the converted Sellmeier coefficients.
    wavelengths : sequence of float
        Wavelengths in micrometers (µm) at which the two representations
        are compared.

    Returns
    -------
    dict
        Numerical validation results, including the refractive-index
        errors and their maximum absolute and relative values.
    """

    x = result["x"]
    D = result["D"]
    N = result["N"]
    D_minus_N = result["D_minus_N"]

    # --------------------------------------------------------
    # Original equation
    #
    # n^2 = (D + 2N)/(D-N)
    # --------------------------------------------------------

    n2_original = (D + 2 * N) / D_minus_N

    B0 = result["B0"]
    B = result["B"]
    roots = result["roots"]

    n2_converted = B0 + sum(b * x / (x - c) for b, c in zip(B, roots))

    n_original = sp.sqrt(n2_original)
    n_converted = sp.sqrt(n2_converted)

    errors = []

    for wavelength in wavelengths:
        xx = sp.Rational(str(wavelength)) ** 2

        n_org = float(sp.N(n_original.subs(x, xx), 20))

        n_conv = float(sp.N(n_converted.subs(x, xx), 20))

        error = n_conv - n_org

        relative_error = error / n_org

        errors.append(
            {
                "wavelength": wavelength,
                "n_original": n_org,
                "n_converted": n_conv,
                "error": error,
                "relative_error": relative_error,
            }
        )

    max_abs_error = max(abs(row["error"]) for row in errors)

    max_abs_relative_error = max(abs(row["relative_error"]) for row in errors)

    return {
        "name": result["name"],
        "discriminant_positive": result["discriminant"] > 0,
        "results": errors,
        "max_abs_error": max_abs_error,
        "max_abs_relative_error": max_abs_relative_error,
    }


def verify_exact_conversion(result):

    x = result["x"]
    D = result["D"]
    N = result["N"]
    D_minus_N = result["D_minus_N"]

    # --------------------------------------------------------
    # Original equation
    #
    # n^2 = (D + 2N)/(D-N)
    # --------------------------------------------------------

    n2_original = (D + 2 * N) / D_minus_N

    B0 = result["B0"]
    B = result["B"]
    roots = result["roots"]

    n2_converted = B0 + sum(b * x / (x - c) for b, c in zip(B, roots))

    difference = sp.cancel(n2_original - n2_converted)

    return difference
