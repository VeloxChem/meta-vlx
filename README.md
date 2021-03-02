# meta-vlx

This repository collects recipes and scripts for the automated build of
[VeloxChem](https://veloxchem.org/).

Note that the recipes are *parametrized*: we store a template `meta.yaml.in`
which gets configured during execution of the
[`deploy-cxx.yml`](.github/workflows/deploy-cxx.yml) action.

## Using `conda-build` locally

#. Copy `meta.yaml.in` to `meta.yaml`.
#. Configure the parametrized fields to suit your needs. 
#. Install Miniconda: <https://docs.conda.io/en/latest/miniconda.html>
   This will get us the latest Miniconda for Linux. Configure the
   installation as you see fit.

   ``` bash
   $ curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   $ bash Miniconda3-latest-Linux-x86_64.sh
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

#. Install `conda-build`:
   <https://docs.conda.io/projects/conda-build/en/latest/> We also
   install `conda-verify`

   ``` bash
   $ conda install conda-build conda-verify
   $ conda update conda conda-build conda-verify
   ```
#. Clone the VeloxChem repository into a folder called `vlx-conda-build`. This
   clone **must be** at the same level as the clone of this repository.

#. You can build the package with:

   ``` bash
   $ conda build veloxchem -c conda-forge
   ```

#. The build packages are stored locally, but can be uploaded to the
   online index at Anaconda.org You need to install the anaconda client
   and get an account.

   ``` bash
   $ conda install anaconda-client
   ```

   You login with:

   ``` bash
   $ anaconda login
   ```

   And upload with:

   ``` bash
   $ anaconda upload /root/miniconda3/conda-bld/noarch/fortran-binary-1.0.6-py_0.tar.bz2
   ```
