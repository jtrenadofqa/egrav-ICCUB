# NR-Catalog-ICCUB

## Instructions 
- Clone this repo

- Install virtual environment from the environment file `environment.yml` (this creates it with the default name iccub-catalog). For example you can do `conda env create -f environment.yml` or `mamba env create -f environment.yml`

- Activate the environment with e.g. `conda activate iccub-catalog`

- Install the necessary packages to use jupyter notebooks (e.g. ipykernel, notebook, nb_conda_kernels, etc). This could be system dependent so we do not include it in the dependencies yml file.  

- Install the nr_iccub package in your environemtn using e.g. `pip install .`. This invokes the `pyproject.toml` file but you do not need to call it explicitly. 

- Follow the `demo.ipynb` for simple examples

You can use this code to explore our NR simulations as explained below. 

## NR data

You can download our NR data from this URL. After unzipping the downloaded file, you should
see a folder structure like the following 

```
.
├── ICCUB-0001
│   ├── 0001_metadata.json
│   ├── 0001_parameter_file.par
│   └── 0001_wf.h5
└── ICCUB-0002
    ├── 0002_metadata.json
    ├── 0002_parameter_file.par
    └── 0002_wf.h5
```

Each simulation folder is labeled as `ICCUB-nnnn`. The simulation id `nnnn` is for identification
purpuses only and does not have a physical meaning. Within each folder, you will find 

- h5 file with waveform data. This has the psi4 and strain modes extracted at various radii. We also include here the signals extrapolated to infinity. 

- json file with the metadata, including the initial conditions and remnant properties

- par file to launch the simulation in `EinsteinToolkit` [URL to toolkit]

You can find a more detailed description of the data at [our paper]

The data provided in `sample_data/` in this repo has the same structure and can 
be used for testing. 

