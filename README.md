# ECEMF Scenario Processing Workflow

Copyright 2024 IIASA

This work is licensed under <a href="http://creativecommons.org/licenses/by/4.0/" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY 4.0</a> <a href="http://creativecommons.org/licenses/by/4.0/" target="_blank" rel="license noopener noreferrer" style="display:inline-block;"><img style="height:15px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg"><img style="height:15px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg"></a>

[![License: CC-BY 4.0](https://img.shields.io/github/license/iiasa/ecemf-workflow)](https://github.com/iiasa/ecemf-workflow/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview

<img src="./_static/ECEMF-logo.png" height="120" align="right" alt="ECEMF logo" />

ECEMF is a Horizon 2020 funded project whose aim is to establish a European forum for
energy and climate researchers and policy makers to achieve climate neutrality.  
Visit https://ecemf.eu for more information!

This workflow repository includes the workflow for scenario processing and validation
using the database infrastructure developed by the IIASA Scenario Services &
Scientific Software team. Read more at https://docs.ece.iiasa.ac.at!

## Using this repository

### Project nomenclature

The folder `definitions` can contain the project nomenclature, i.e., list of allowed
variables and regions, for use in the validation workflow. See the **nomenclature**
package for more information ([link](https://github.com/iamconsortium/nomenclature)).

The folder `mappings` can contain model mappings that are used to register models and
define how results should be processed upon upload to a Scenario Explorer.

### Model registration

This is the step-by-step guide to registering your model:

1. Fork this repository
2. Follow the instructions from the nomenclature documentation to [register your model](https://nomenclature-iamc.readthedocs.io/en/stable/user_guide/model-registration.html).  
Please make sure to follow the instructions completely, both the _Model mapping_ and the _Region definitions_ part. You'll have to end up with two files.
3. Open a pull request into this repository. Make sure that the tests run through and correct any potential issues. If the tests are failing you can view the details by clicking on the failed test run.

4. Set [@danielhuppmann](https://github.com/danielhuppmann) and [@phackstock](https://github.com/phackstock) as reviewers.
5. Once everything is in order we will merge your pull request and your model will be registered.

### Workflow

The module `workflow.py` has a function `main(df: pyam.IamDataFrame) -> pyam.IamDataFrame:`.

Per default, this function takes an **IamDataFrame** and returns it without
modifications. [Read the docs](https://pyam-iamc.readthedocs.io) for more information
about the **pyam** package for scenario analysis and data visualization.

**Important**: Do not change the name of the module `workflow.py` or the function `main`
as they are called like this by the Job Execution Service. Details can be found
[here](https://wiki.ece.iiasa.ac.at/wiki/index.php/Scenario_Explorer/Setup#Job_Execution_Service).

## Dependency

<img src="./_static/open_entrance-logo.png" width="152" height="96" align="right" alt="openENTRANCE logo" />

This project builds on the work in the Horizon 2020 project openENTRANCE.
Visit https://github.com/openENTRANCE/openentrance for more information!

## Funding acknowledgement

<img src="./_static/EU-logo-300x201.jpg" width="80" height="54" align="left" alt="EU logo" />
This project has received funding from the European Union’s <b>Horizon 2020</b> research
and innovation programme under grant agreement No. 101022622 (<b>ECEMF</b>).
