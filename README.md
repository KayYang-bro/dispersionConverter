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

### Evaluation Results

Absolute difference in refractive index $n$ between the original and
converted representations for the discrete validation wavelengths 
sampled between 0.400 to 0.800 µm is shown below.

$$
\varDelta n_\mathrm{max\_ abs}=\max_{\lambda \in \Lambda} {\left| n_{\mathrm{original}}(\lambda)-n_{\mathrm{converted}}(\lambda)\right|},
$$
$$
\Lambda=\lbrace \lambda \ \mathrm{\mu m} | \lambda \in \lbrace 0.400, 0.450, 0.486133, 0.500, 0.550, 0.587562, 0.600, 0.650, 0.700, 0.800 \rbrace \rbrace
$$

- 0.0e-16

    J-KZFH11

- 2.2e-16

    J-FK5, J-FKH1, J-PKH1, J-PSK02, J-PSK03, J-PSKH1, J-PSKH8, 
J-BK7A, J-BAK1, J-BAK2, J-BAK4, J-K3, J-K5, J-KZFH1, J-KZFH4, 
J-KZFH6, J-KZFH7, J-KZFH9, J-KZFH10, J-KF6, J-BALF4, J-BAF10, 
J-BASF2, J-BASF7, J-BASF8, J-SK2, J-SK4, J-SK5, J-SK11, J-SK12, 
J-SK14, J-SK15, J-SK16, J-SK18, J-SSK5, J-LLF1, J-LLF2, J-LLF6, 
J-F2, J-F5, J-SF1, J-SF2, J-SF4, J-SF5, J-SF6, J-SF6HS, J-SF7, 
J-SF8, J-SF10, J-SF14, J-SF03, J-SF03HS, J-SFS3, J-SFH1, J-SFH1HS, 
J-SFH2, J-SFH5, J-SFH6, J-SFH8, J-SFH9, J-LAK7R, J-LAK8, J-LAK10, 
J-LAK12, J-LAK18, J-LAK01, J-LASKH2, J-LAF2, J-LAF7, J-LAF01, 
J-LAF05, J-LAF010, J-LASF01, J-LASF02, J-LASF05, J-LASF05HS, 
J-LASF08A, J-LASF09A, J-LASF010, J-LASF013, J-LASF014, J-LASF015, 
J-LASF015HS, J-LASF016, J-LASF017, J-LASFH2, J-LASFH6, J-LASFH9A, 
J-LASFH13, J-LASFH13HS, J-LASFH21, J-LASFH22, J-LASFH24, J-LASFH24HS, 
Q-FKH1S, Q-PSKH2S, Q-SK55S, Q-SF6S, Q-LAK53S, Q-LAF010S, Q-LASF03S, 
Q-LASFH11S, Q-LASFH58S, Q-LASFH59S, Q-LASFPH2S, Q-LASFPH3S,

- 4.4e-16

     J-FK01A, J-PSKH4, J-BAF11, J-BASF6, J-SK10, J-SSK1, J-SSK8, J-LF5, 
 J-LF6, J-LF7, J-F8, J-SF11, J-SF13, J-SF15, J-SFH4, J-LAK7, J-LAK13, 
 J-LAK14, J-LAK09, J-LAK011, J-LAF3, J-LAF02, J-LAF04, J-LAFH3, J-LAFH3HS, 
 J-LASF03, J-LASF021, J-LASF021HS, J-LASFH15, J-LASFH15HS, J-LASFH15SS, 
 J-LASFH16, J-LASFH16HS, J-LASFH17, J-LASFH17HS, J-LASFH23, Q-PSKH1S, 
 Q-PSKH4S, Q-SK15S, Q-LAK52S, Q-LAFPH1S, 

- 6.6e-16

    J-F1, Q-LASFH12S

- 8.8e-16

    J-LAF016, J-LAF016HS

Let $$G = \lbrace g_1, g_2, \dots, g_{152} \rbrace $$ be the set of 152 optical glass types from HIKARI GLASS Co., Ltd., and $n(g)$ denote the refractive index of a glass $g \in G$.

$$
E\left[\varDelta n_\mathrm{max\_ abs}(g)\mid {g \in G}\right]=2.9\times 10^{-16}
$$

---

## Future work

The current implementation focuses on the three-term case used by the
available glass data. The underlying algebra extends naturally to an
$m$-term modified dispersion equation, for which the converted
Sellmeier poles are given by the roots of an $m$-th degree polynomial.

The numerical implementation could therefore be generalized to
arbitrary numbers of terms.