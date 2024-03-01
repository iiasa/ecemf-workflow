from pathlib import Path
import pyam
from nomenclature import DataStructureDefinition, RegionProcessor, process


here = Path(__file__).absolute().parent


def main(df: pyam.IamDataFrame) -> pyam.IamDataFrame:
    """Project/instance-specific workflow for scenario processing"""

    # initialize the codelists and region-processing
    dsd = DataStructureDefinition(
        here / "definitions", dimensions=["scenario", "region", "variable"]
    )
    processor = RegionProcessor.from_directory(path=here / "mappings", dsd=dsd)

    # check if directional data exists in the scenario data, add to region codelist
    if any([r for r in df.region if ">" in r]):
        for r in df.region:
            if r in definition.region:
                continue
            r_split = r.split(">")
            if len(r_split) > 2:
                raise ValueError(
                    f"Directional data other than `origin>destination` not allowed: {r}"
                )
            elif len(r_split) == 2:
                if all([_r in definition.region for _r in r_split]):
                    # add the directional-region to the codelist (without attributes)
                    definition.region[r] = None

    # run the validation and region-processing
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
