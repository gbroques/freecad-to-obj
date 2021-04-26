# Contributing Guidelines

## Prerequisites
1. Install [conda](https://docs.conda.io/en/latest/miniconda.html).
2. Create a dedicated conda environment named `freecad-to-obj` from the `environment.yaml` file in the root of this repository.
   
       conda env create --file environment.yml

3. Activate `freecad-to-obj`.

       conda activate freecad-to-obj

4. Execute `add_conda_path_to_python_path.sh`.

       ./add_conda_path_to_python_path.sh

5. Reactivate conda environment for changes to take effect.

       conda deactivate && conda activate freecad-to-obj

## How to Run Unit Tests
After following the [Prerequisites](#Prerequisites), with the `freecad-to-obj` conda environment activated, execute the following command:

    pytest

Additionally, you can generate a code coverage report in `htmcov/` by executing the following command:

    pytest --cov-report html --cov=freecad_to_obj tests
