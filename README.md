# Modified Dispersion Equation to Sellmeier Equation

This project derives an exact algebraic conversion from the
three-term modified dispersion equation

$$
\frac{n^2-1}{n^2+2}=\sum_{i=1}^{3}\frac{P_i\lambda^2}{\lambda^2-Q_i}
$$

to the standard three-term Sellmeier equation

$$
n^2 =1+\sum_{i=1}^{3}\frac{B_i\lambda^2}{\lambda^2-C_i}.
$$

The two representations are mathematically equivalent: the
conversion can be obtained exactly by algebraic transformation.

The conversion was tested using 152 glasses for which three-term
coefficients of the modified dispersion formula are available in the
HIKARI GLASS catalog. All 152 datasets produced three real converted
Sellmeier poles.

For the discrete validation wavelengths sampled between 0.400 to 0.800 µm
(400 to 800 nm), the maximum
absolute difference in refractive index between the original and
converted representations was $8.88\times10^{-16}$, while the mean of
the per-glass maximum absolute errors was approximately $3\times10^{-16}$.

The numerical implementation therefore provides conversion accuracy
at the scale of double-precision floating-point round-off for the
tested datasets.

> **Note:** Wavelengths are expressed in micrometers (µm).
> Consequently, the $C_i$ coefficients are in $\mathrm{\mu m^2}$.

---

## Status

The numerical conversion is considered stable for the tested datasets
and is the primary intended use of this project.

The exact symbolic conversion is currently provided as an
experimental verification tool. It is used to verify the algebraic
equivalence of the two representations rather than as the primary
conversion path.

## How to use

Prepare a CSV file containing the glass name and the coefficients
$P_1,Q_1,P_2,Q_2,P_3,Q_3$ of the three-term modified dispersion
equation.

For example:

```text
name,P1,Q1,P2,Q2,P3,Q3
J-BK7A,0.132131192,85.2147898,0.0348697207,0.0183584959,0.262754051,0.00439929773
```
The input CSV is assumed to contain valid numerical coefficients in the
expected format.

The wavelength variable is expressed in micrometers (µm).

Set the input and output paths in main():

```python
input_path = Path("data/input.csv")
coefficients_path = Path("output/sellmeier_coefficients.csv")
report_path = Path("output/conversion_report.csv")
```

Then run:
```shell
python main.py
```

The program produces two CSV files:

- sellmeier_coefficients.csv
    
    Contains the converted Sellmeier coefficients $B_1,B_2,B_3,C_1,C_2,C_3$.

- conversion_report.csv

    Contains numerical validation results, including the maximum absolute
and relative refractive-index errors over the validation wavelengths.

## Data

The glass data used for validation are not included in this repository.
The validation was performed using three-term modified dispersion
coefficients from the HIKARI GLASS catalog.

## 1. Modified dispersion equation

Let

$$
x=\lambda^2.
$$

The modified dispersion equation is

$$
S(x)= \frac{n^2-1}{n^2+2} = \sum_{i=1}^{3} \frac{P_i x}{x-Q_i}.
$$

Writing the right-hand side as

$$
S(x)=\frac{N(x)}{D(x)},
$$

where

$$
D(x)=\prod_{i=1}^{3}(x-Q_i),
$$

and

$$
N(x)=\sum_{i=1}^{3}P_i x\prod_{j\ne i}(x-Q_j),
$$

we obtain

$$
n^2=\frac{1+2S}{1-S}=\frac{D+2N}{D-N}.
$$

Therefore,

$$
n^2-1=\frac{3N}{D-N}.
$$

---

## 2. Determination of the Sellmeier poles

The poles of the converted Sellmeier representation are obtained
from the roots of

$$
D(x)-N(x)=0.
$$

Since D and N are polynomials of degree at most three, D−N is a polynomial of degree at most three.

$$
D(x)-N(x)
$$

is a cubic polynomial in $x$.

Let its three roots be

$$
C_1,\ C_2,\ C_3.
$$

Thus,

$$
D(x)-N(x)=K\prod_{i=1}^{3}(x-C_i).
$$

The roots $C_i$ therefore correspond directly to the $C_i$ parameters
in the Sellmeier equation.

The explicit Cardano expressions for the roots are not written out
here because they are lengthy and do not provide additional insight.
The roots are instead defined by the cubic equation above and are
calculated symbolically using SymPy.

---

## 3. Determination of the Sellmeier coefficients

Starting from

$$
n^2-1=\frac{3N(x)}{D(x)-N(x)},
$$

perform a partial-fraction decomposition:

$$
n^2-1=A+\sum_{i=1}^{3}\frac{R_i}{x-C_i}.
$$

For a simple root $C_i$,

$$
R_i=\frac{3N(C_i)}{(D-N)'(C_i)}.
$$

Using

$$
\frac{R_i}{x-C_i}=\frac{R_i}{C_i}\frac{x}{x-C_i}-\frac{R_i}{C_i},
$$

we obtain

$$
B_i=\frac{R_i}{C_i}.
$$

The constant term is then

$$
B_0=1+A-\sum_{i=1}^{3}B_i.
$$


For the present transformation, the converted equation takes the
standard form

$$
\boxed{n^2=1+\sum_{i=1}^{3}\frac{B_i x}{x-C_i}}.
$$

### Why is the constant term 1?

The constant term $1$ in the standard Sellmeier equation is not an
additional assumption. It follows directly from the structure of the
original Lorentz--Lorenz-type equation.

Recall that

$$
S(x)=\frac{n^2-1}{n^2+2}=\sum_{i=1}^{3}\frac{P_i x}{x-Q_i},\qquad x=\lambda^2.
$$

If $Q_i\neq0$, then

$$
\lim_{x\to0} S(x)=0.
$$

Therefore,

$$
\lim_{x\to0}n^2=\lim_{x\to0}\frac{1+2S(x)}{1-S(x)}=1.
$$

On the converted side, if $C_i\neq0$,

$$
\lim_{x\to0}n^2=\lim_{x\to0}\left(B_0+\sum_{i=1}^{3}\frac{B_i x}{x-C_i}\right)=B_0.
$$

Consequently,

$$
\boxed{B_0=1}.
$$

Thus, the constant term $1$ in the standard Sellmeier equation is a
consequence of the Lorentz--Lorenz-type form of the original
dispersion equation, rather than an assumption imposed during the
conversion.


For completeness, the same result can also be seen from the
partial-fraction decomposition.

Starting from

$$
n^2-1=A+\sum_{i=1}^{3}\frac{R_i}{x-C_i},
$$

taking $x\to\infty$ gives

$$
A=\lim_{x\to\infty}(n^2-1).
$$

The Sellmeier representation gives

$$
n^2-1=\sum_{i=1}^{3}\frac{B_i x}{x-C_i},
$$

and therefore

$$
\lim_{x\to\infty}(n^2-1)=\sum_{i=1}^{3}B_i.
$$

Hence,

$$
A=\sum_{i=1}^{3}B_i.
$$

Since the partial-fraction decomposition gives

$$
B_0=1+A-\sum_{i=1}^{3}B_i,
$$

it follows again that

$$
\boxed{B_0=1}.
$$

---

## 4. Exactness of the conversion

The symbolic implementation represents the supplied decimal coefficients
as exact rational numbers rather than floating-point numbers.

For example,

$$
1.32131192\times10^{-1}
$$

is represented exactly as the rational number corresponding to its
decimal representation.

This removes floating-point round-off from the symbolic algebra and
allows the algebraic identity to be checked exactly.

The implementation verifies

$$
n^2_{\mathrm{original}}-n^2_{\mathrm{converted}}=0
$$

symbolically.

Therefore, the conversion is an exact algebraic transformation for
the supplied values of $P_i$ and $Q_i$.

This exactness applies to the supplied numerical coefficients; it does
not imply infinite physical accuracy of the original glass data.

---

## 5. Reality of the converted coefficients

The fact that $P_i$ and $Q_i$ are real does not by itself guarantee
that all $C_i$ are real.

The cubic

$$
D(x)-N(x)
$$

has real coefficients when all $P_i$ and $Q_i$ are real.

Its discriminant determines the nature of its roots:

- $\Delta>0$: three distinct real roots
- $\Delta=0$: repeated real roots
- $\Delta<0$: one real root and one complex-conjugate pair

The implementation evaluates the cubic discriminant and also checks
the exact reality of the resulting roots.

When the $C_i$ are real and nonzero, the corresponding $B_i$ are also
real.

---

## 6. Numerical validation

The refractive index calculated from the converted Sellmeier equation is

$$
n_{\mathrm{converted}}(\lambda)=\sqrt{1+\sum_{i=1}^{3}\frac{B_i\lambda^2}{\lambda^2-C_i}}.
$$

This is compared with the refractive index calculated directly from
the original modified dispersion equation,

$$
n_{\mathrm{original}}(\lambda)=\sqrt{\frac{1+2S(\lambda)}{1-S(\lambda)}}.
$$

Of the 155 glasses listed in the HIKARI GLASS catalog, 152 provide
coefficients for the three-term fractional dispersion formula.
All 152 datasets were successfully converted and yielded three real
Sellmeier poles.

Data are available from the
[HIKARI GLASS optical glass catalog](https://www.hikari-g.co.jp/optical_glass/catalog/).

---

## 7. Example

For the J-BK7A data used in this project, the converted coefficients
are approximately

$$
C_1=0.00593256273685039,
$$

$$
C_2=0.0193823242791576,
$$

$$
C_3=104.96045868732,
$$

and

$$
B_1=1.01984136489569,
$$

$$
B_2=0.251325574355409,
$$

$$
B_3=0.989729358006160.
$$

The converted representation is symbolically identical to the
original representation for the supplied input coefficients.

---

## Future work

The current implementation focuses on the three-term case used by the
available glass data. The underlying algebra extends naturally to an
$m$-term modified dispersion equation, for which the converted
Sellmeier poles are given by the roots of an $m$-th degree polynomial.

The numerical implementation could therefore be generalized to
arbitrary numbers of terms.