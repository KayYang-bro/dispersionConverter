import sympy as sp

# --------------------------------------------------------
# Math / Conversion
# --------------------------------------------------------

# ============================================================
# Convert modified dispersion equation
#
# (n^2 - 1)/(n^2 + 2)
#     = sum(P_i*x/(x-Q_i))
#
# x = lambda^2
#
# to
#
# n^2 =
# B0
# + B1*x/(x-C1)
# + B2*x/(x-C2)
# + B3*x/(x-C3)
# ============================================================


def build_N_D(P, Q):
    """Construct the numerator and denominator polynomials."""

    if len(P) != len(Q):
        raise ValueError("P and Q must have the same length")

    x = sp.symbols("x")

    # --------------------------------------------------------
    # S = N/D
    # --------------------------------------------------------

    D = sp.prod(x - q for q in Q)

    N = sum(
        p * x * sp.prod(x - q for j, q in enumerate(Q) if j != i)
        for i, p in enumerate(P)
    )

    return sp.expand(D), sp.expand(N)


def convert_exact(P_values, Q_values):
    """
    Convert modified dispersion coefficients to Sellmeier coefficients
    using exact symbolic arithmetic.

    This function is intended for verification and experimentation,
    rather than routine numerical conversion.
    """

    x = sp.symbols("x")

    # --------------------------------------------------------
    # Represent decimal input exactly as rational numbers
    # --------------------------------------------------------

    P = [sp.Rational(str(v)) for v in P_values]

    Q = [sp.Rational(str(v)) for v in Q_values]

    D, N = build_N_D(P, Q)

    D_minus_N = sp.expand(D - N)

    # --------------------------------------------------------
    # Cubic discriminant
    # --------------------------------------------------------

    discriminant = sp.factor(sp.discriminant(D_minus_N, x))

    # --------------------------------------------------------
    # Exact roots
    # --------------------------------------------------------

    roots = sorted(sp.solve(D_minus_N, x), key=lambda r: float(sp.N(sp.re(r))))

    # --------------------------------------------------------
    # Residues
    # --------------------------------------------------------

    derivative = sp.diff(D_minus_N, x)

    residues = [3 * N.subs(x, root) / derivative.subs(x, root) for root in roots]

    # --------------------------------------------------------
    # Sellmeier coefficients
    # --------------------------------------------------------

    B = [sp.cancel(residue / root) for residue, root in zip(residues, roots)]

    # Constant term

    Psum = sum(P)

    A = sp.cancel(3 * Psum / (1 - Psum))

    B0 = sp.cancel(1 + A - sum(B))

    # --------------------------------------------------------
    # Return everything
    # --------------------------------------------------------

    return {
        "x": x,
        "discriminant": discriminant,
        "P": P,
        "Q": Q,
        "D": D,
        "N": N,
        "D_minus_N": D_minus_N,
        "roots": roots,
        "residues": residues,
        "B0": B0,
        "B": B,
    }


def convert_numeric(P_values, Q_values):
    """
    Convert three-term modified dispersion coefficients (P, Q)
    to Sellmeier coefficients (B, C) using numerical root finding.

    Parameters
    ----------
    P_values : sequence of float
        Numerator coefficients P_i.
    Q_values : sequence of float
        Pole coefficients Q_i, in µm².

    Returns
    -------
    dict
        Conversion results including the Sellmeier coefficients
        B_i and C_i.
    """

    x = sp.symbols("x")

    # --------------------------------------------------------
    # Represent decimal input exactly as rational numbers
    # --------------------------------------------------------

    P = [sp.Rational(str(v)) for v in P_values]

    Q = [sp.Rational(str(v)) for v in Q_values]

    D, N = build_N_D(P, Q)

    D_minus_N = sp.expand(D - N)

    # --------------------------------------------------------
    # Cubic discriminant
    # --------------------------------------------------------

    discriminant = sp.discriminant(D_minus_N, x)

    # --------------------------------------------------------
    # Numeric roots
    # --------------------------------------------------------

    roots = sorted(sp.nroots(D_minus_N), key=lambda r: float(sp.re(r)))

    # --------------------------------------------------------
    # Residues
    # --------------------------------------------------------

    derivative = sp.diff(D_minus_N, x)

    residues = [3 * N.subs(x, root) / derivative.subs(x, root) for root in roots]

    # --------------------------------------------------------
    # Sellmeier coefficients
    # --------------------------------------------------------

    B = [residue / root for residue, root in zip(residues, roots)]

    # Constant term

    Psum = sum(P)

    A = 3 * Psum / (1 - Psum)

    B0 = 1 + A - sum(B)

    # --------------------------------------------------------
    # Return everything
    # --------------------------------------------------------

    return {
        "x": x,
        "discriminant": discriminant,
        "P": P,
        "Q": Q,
        "D": D,
        "N": N,
        "D_minus_N": D_minus_N,
        "roots": roots,
        "residues": residues,
        "B0": B0,
        "B": B,
    }
