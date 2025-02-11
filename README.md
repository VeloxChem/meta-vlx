# meta-vlx

This repository collects recipes and scripts for the automated build of
[VeloxChem](https://veloxchem.org/).

Note that the recipes are *parametrized*: we store a template `meta.yaml.in`
which gets configured during execution of the
[`deploy-cxx.yml`](.github/workflows/deploy-cxx.yml) action.

## Using `conda-build` locally

1. Copy `meta.yaml.in` to `meta.yaml`.

2. Configure the parametrized fields to suit your needs. 

3. Install Miniforge: <https://conda-forge.org/download/>
   This will get us the latest Miniforge for Linux. Configure the
   installation as you see fit.

   ``` bash
   $ curl -LO https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
   $ bash Miniforge3-Linux-x86_64.sh
   ```

   You should log out and log back in (or close and re-open the
   terminal) for the changes to take effect.

   - On macOS, you need a non-broken SDK:

     ```bash
     $ curl -fsSL https://github.com/phracker/MacOSX-SDKs/releases/download/10.15/MacOSX10.9.sdk.tar.xz > ${HOME}/MacOSX10.9.sdk.tar.xz
     $ tar -xzf ${HOME}/MacOSX10.9.sdk.tar.xz
     ```
     and then you must edit `conda-recipes/veloxchem/conda_build_config.yaml`
     such that `CONDA_BUILD_SYSROOT` points to the location of the SDK.

4. Install `conda-build`:
   <https://docs.conda.io/projects/conda-build/en/latest/> We also
   install `conda-verify`

   ``` bash
   $ conda activate base
   $ conda install conda-build conda-verify python=3.11
   ```
5. Clone the veloxchem repository. Note that the `veloxchem` folder
   **must be** at the same level as the `conda-recipes` folder of
   this repository.

6. You can build the package with:

   ``` bash
   $ cd conda-recipes
   $ conda build veloxchem -c conda-forge
   ```

7. The build packages are stored locally, but can be uploaded to the
   online index at Anaconda.org You need to install the anaconda client
   and get an account.

   ``` bash
   $ conda install anaconda-client
   $ conda config --set anaconda_upload no
   ```

   You login with:

   ``` bash
   $ anaconda login
   ```

   And upload with:

   ``` bash
   $ anaconda upload $HOME/miniforge3/conda-bld/linux-64/veloxchem-1.0rc3-py_0.tar.bz2 -u veloxchem -l test
   ```

