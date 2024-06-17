from pathlib import Path
import pyam
from nomenclature import DataStructureDefinition, RegionProcessor, process
from nomenclature.codelist import RegionCode
from datetime import datetime, timedelta


# datetime must be in Central European Time (CET)
EXP_TZ = "UTC+01:00"
EXP_TIME_OFFSET = timedelta(seconds=3600)
OE_SUBANNUAL_FORMAT = lambda x: x.strftime("%m-%d %H:%M%z").replace("+0100", "+01:00")

here = Path(__file__).absolute().parent


def main(df: pyam.IamDataFrame) -> pyam.IamDataFrame:
    """Project/instance-specific workflow for scenario processing"""

    dimensions = ["scenario", "region", "variable"]
    if "subannual" in df.dimensions or df.time_col == "time":
        dimensions = dimensions + ["subannual"]

    # initialize the codelists and region-processing
    dsd = DataStructureDefinition(here / "definitions", dimensions=dimensions)
    processor = RegionProcessor.from_directory(path=here / "mappings", dsd=dsd)

    # check if directional data exists in the scenario data, add to region codelist
    if any([r for r in df.region if ">" in r]):
        for r in df.region:
            if r in dsd.region:
                continue
            r_split = r.split(">")
            if len(r_split) > 2:
                raise ValueError(
                    f"Directional data other than `origin>destination` not allowed: {r}"
                )
            elif len(r_split) == 2:
                if all([_r in dsd.region for _r in r_split]):
                    # add the directional-region to the codelist (without attributes)
                    dsd.region[r] = RegionCode(name=r, hierarchy="directional")

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

    # convert to subannual format if data provided in datetime format
    if df.time_col == "time":
        logger.info('Re-casting from "time" column to categorical "subannual" format')
        df = df.swap_time_for_year(subannual=OE_SUBANNUAL_FORMAT)

    # check that any datetime-like items in "subannual" are valid datetime and UTC+01:00
    if "subannual" in df.dimensions:
        _datetime = [s for s in df.subannual if s not in dsd.subannual]

        for d in _datetime:
            try:
                _dt = datetime.strptime(f"2020-{d}", "%Y-%m-%d %H:%M%z")
            except ValueError:
                try:
                    datetime.strptime(f"2020-{d}", "%Y-%m-%d %H:%M")
                except ValueError:
                    raise ValueError(f"Invalid subannual timeslice: {d}")

                raise ValueError(f"Missing timezone: {d}")

            # casting to datetime with timezone was successful
            if not (_dt.tzname() == EXP_TZ or _dt.utcoffset() == EXP_TIME_OFFSET):
                raise ValueError(f"Invalid timezone: {d}")

    return df
