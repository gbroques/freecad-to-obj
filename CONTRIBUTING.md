# Contributing Guidelines

## Prerequisites
1. Install [conda](https://docs.conda.io/en/latest/miniconda.html).
2. Create a dedicated conda environment named `freecad-to-obj` with `freecad` as a dependency.
   
       conda create --name freecad-to-obj freecad

3. Activate `freecad-to-obj`.

       conda activate freecad-to-obj

4. Execute `add_conda_path_to_python_path.sh`.

       ./add_conda_path_to_python_path.sh

5. Reactivate conda environment for changes to take effect.

       conda deactivate && conda activate freecad-to-obj

## How to Run Unit Tests
After following the [Prerequisites](#Prerequisites), with the `freecad-to-obj` conda environment activated, execute the following command:

    python -m unittest discover -s tests -p '*_test.py'
