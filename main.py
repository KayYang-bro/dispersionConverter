from pathlib import Path

from conversion import convert_numeric
from evaluation import evaluate_conversion
from csv_io import (
    load_glass_data,
    save_conversion_report_csv,
    save_sellmeier_coefficients_csv,
)

DEFAULT_VALIDATION_WAVELENGTHS = [
    0.400,
    0.450,
    0.486133,
    0.500,
    0.550,
    0.587562,
    0.600,
    0.650,
    0.700,
    0.800,
]


def main():
    input_path = Path("data/HIKARI_ALL_Catalog_Data.csv")
    coefficients_path = Path("output/sellmeier_coefficients.csv")
    report_path = Path("output/conversion_report.csv")

    results = []
    evaluations = []

    glasses = load_glass_data(csv_path=input_path)

    for glass in glasses:
        result = {
            "name": glass["name"],
            **convert_numeric(glass["P"], glass["Q"]),
        }
        results.append(result)

        evaluation = evaluate_conversion(
            result=result,
            wavelengths=DEFAULT_VALIDATION_WAVELENGTHS,
        )
        evaluations.append(evaluation)

    save_sellmeier_coefficients_csv(
        results=results,
        csv_path=coefficients_path,
    )

    save_conversion_report_csv(
        evaluations=evaluations,
        csv_path=report_path,
    )

    print(f"Converted {len(results)} glasses.")
    print(f"Saved: {coefficients_path}")
    print(f"Saved: {report_path}")


if __name__ == "__main__":
    main()
