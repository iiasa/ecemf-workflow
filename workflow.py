from pathlib import Path
import pyam
from nomenclature import DataStructureDefinition, RegionProcessor, process


here = Path(__file__).absolute().parent


def main(df: pyam.IamDataFrame) -> pyam.IamDataFrame:
    """Project/instance-specific workflow for scenario processing"""

    # Run the validation and region-processing
    dsd = DataStructureDefinition(
        here / "definitions", dimensions=["scenario", "region", "variable"]
    )
    processor = RegionProcessor.from_directory(path=here / "mappings", dsd=dsd)
    df = process(df, dsd, processor=processor)

    # assign meta indicator for scenario "work package" category
    for model, scenario in df.index:
        if "DIAG" in scenario:
            df.meta.loc[(model, scenario), "Work package"] = "Diagnostic"
        elif scenario.startswith("WP"):
            df.meta.loc[(model, scenario), "Work package"] = (
                "Work Package " + scenario[2:4]
            )

    return df
