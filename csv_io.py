import csv
import sympy as sp


def format_numeric(expr, digits=15):
    return sp.N(expr, digits)


def load_glass_data(csv_path):
    """
    Load modified dispersion coefficients from a CSV file.

    Parameters
    ----------
    csv_path : str or pathlib.Path
        Path to the input CSV file.

    Returns
    -------
    list of dict
        Glass data containing the name and P/Q coefficients.
    """

    glasses = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            glasses.append(
                {
                    "name": row["name"],
                    "P": [
                        row["P1"],
                        row["P2"],
                        row["P3"],
                    ],
                    "Q": [
                        row["Q1"],
                        row["Q2"],
                        row["Q3"],
                    ],
                }
            )

    return glasses


def save_sellmeier_coefficients_csv(results, csv_path):
    """
    Save converted Sellmeier coefficients to a CSV file.

    Parameters
    ----------
    results : sequence of dict
        Conversion results containing the glass name, B coefficients,
        and converted C coefficients.
    csv_path : str or pathlib.Path
        Path to the output CSV file.
    """

    fieldnames = [
        "name",
        "B1",
        "B2",
        "B3",
        "C1",
        "C2",
        "C3",
    ]

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )
        writer.writeheader()

        for result in results:
            writer.writerow(
                {
                    "name": result["name"],
                    "B1": format_numeric(result["B"][0]),
                    "B2": format_numeric(result["B"][1]),
                    "B3": format_numeric(result["B"][2]),
                    "C1": format_numeric(result["roots"][0]),
                    "C2": format_numeric(result["roots"][1]),
                    "C3": format_numeric(result["roots"][2]),
                }
            )


def save_conversion_report_csv(evaluations, csv_path):
    """
    Save numerical conversion validation results to a CSV file.

    Parameters
    ----------
    evaluations : sequence of dict
        Evaluation results containing error metrics for each glass.
    csv_path : str or pathlib.Path
        Path to the output CSV file.
    """

    fieldnames = [
        "name",
        "discriminant_positive",
        "max_abs_error",
        "max_relative_error",
    ]

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for evaluation in evaluations:
            writer.writerow(
                {
                    "name": evaluation["name"],
                    "discriminant_positive": (evaluation["discriminant_positive"]),
                    "max_abs_error": format_numeric(evaluation["max_abs_error"]),
                    "max_relative_error": format_numeric(
                        evaluation["max_abs_relative_error"]
                    ),
                }
            )
