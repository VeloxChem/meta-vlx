# meta-vlx

How to build these recipes:

1.  Install Miniconda: <https://docs.conda.io/en/latest/miniconda.html>
    This will get us the latest Miniconda for Linux. Configure the
    installation as you see fit.

    ``` bash
    $ curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    $ bash Miniconda3-latest-Linux-x86_64.sh
    ```

    You should log out and log back in (or close and re-open the
    terminal) for the changes to take effect.

2.  Install `conda-build`:
    <https://docs.conda.io/projects/conda-build/en/latest/> We also
    install `conda-verify`

    ``` bash
    $ conda install conda-build conda-verify
    $ conda update conda conda-build conda-verify
    ```
3.  Clone the VeloxChem repository into a folder called `vlx-conda-build`. This
    clone **must be** at the same level as the clone of this repository.

5.  You can build the package with:

    ``` bash
    $ conda build veloxchem -c conda-forge
    ```

6.  The build packages are stored locally, but can be uploaded to the
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
