# Sparse Metrology for Bosch Silicon Etching with Learned Measurement Sites and Process Data

Code and results for the paper *Sparse Metrology for Bosch Silicon Etching with Learned Measurement Sites and Process Data* (D. Sadekeen, submitted).

Fabs measure etch depth at only a few sites per wafer. Using the public Bosch etch dataset of Sayyed et al., this project asks:

- which sites to measure;
- how well the full 89-site depth map can be rebuilt for lots the model has never seen;
- how many measured sites process data (context, machine signals, optical emission spectra) are worth.

Main results:

- Four learned sites rebuild the map about as well as the dataset's nine standard sites.
- Nine learned sites are 34–38 % more accurate.
- The standard 9-site layout misses the edge ring and understates the within-wafer variation (CV 2.4 % instead of 8.2 %).
- Process data help most when no site is measured, for example to decide which wafers can skip measurement.

## Data

The data are **not** included. Download them from Zenodo:

> M. A. Sayyed, T. Seifert, S. Zieger, S. Schwarzenberg, A. Deshmukh, M. Haase and J. Langer, *A Multi-Model Dataset for BOSCH Plasma-Etching: Optical Emission Spectra, Process Parameters, and Wafer Measurements for Data-Driven Plasma Modeling*, Zenodo, 2025. https://doi.org/10.5281/zenodo.17122442 (CC BY 4.0)

Put these files in one folder:

- `Process_data.nc`
- `Dictionary_process.nc`
- `Dictionary_OES.nc`
- all ten `Day_2024_*.nc` spectra files
- `Si_Oxide_etch_89_points.csv`
- `Si_Oxide_etch_9_points.csv`
- `Lot_status.xlsx`

## How to run

1. Open `notebook/Bosch_sparse_metrology_v2.1.ipynb` in Google Colab or Jupyter.
2. Tell the notebook where the data are. In cell 0, either:
   - set `DATA_DIR` to the data folder; or
   - set `USE_GOOGLE_DRIVE = True` and `DRIVE_DATA_DIR` to the folder on your Drive.
3. Run all cells. A CPU is enough. The full run takes under an hour on a free Colab runtime, and most of that is reading the spectra once.
4. The results go to `results_sparse_metrology/` next to the data and are zipped at the end.

Python packages are listed in `requirements.txt`. The notebook installs `netCDF4`, `scikit-learn` and `openpyxl` itself if they are missing.

| Cell | What it does |
|---|---|
| 0 | Settings and setup |
| core | Data loading, features, models and site designs, experiments, figures |
| 1 | Data check (campaign alignment, gross errors) and map structure |
| 2 | Features: context, machine signals, OES |
| 3 | Experiments: site selection, value of process data, adaptive designs, uncertainty, measure-or-skip, in-line campaign, forward-in-time check |
| 4 | Tables and figures |
| 5 | Sensitivity checks |
| 6 | Summary (`results.json`) |
| 7 | Extra analyses reported in the paper (`results_extras.json`) |

## What is in this repository

```
notebook/      Bosch_sparse_metrology_v2.1.ipynb   the full analysis
figure_code/   make_figs.py                         draws the four paper figures
               figure_data/                         the numbers behind the figures and tables
results/       results.json, results_extras.json    the author's run (summary numbers)
               tables/                              CSV and LaTeX tables
               raw/                                 per-wafer results of every experiment
               features/                            cached machine-signal and OES features and checks
```

To redraw the figures:

```
python figure_code/make_figs.py <output folder>
```

## Where the paper's numbers come from

| Paper | File |
|---|---|
| Fig. 1 (maps and layouts) | `figure_code/figure_data/sites.csv`, `layouts.json` |
| Fig. 2 (data check, drift) | `figure_code/figure_data/audit_stepheight.csv`, `matched_pairs_si_etch.csv`, `wafer_means.csv` |
| Fig. 3 (error vs. number of sites) | `figure_code/figure_data/rq1_macro.csv`, `rq2_macro.csv` |
| Fig. 4 (CV error) | `figure_code/figure_data/uniformity_cv_errors.csv` |
| Table I (estimators) | `results/tables/table_rq1_estimators.csv` |
| Table II (value of process data) | `results/tables/table_rq2_information.csv`, `table_forward_in_time.csv`, `results/results.json` |
| Paired comparisons in the text | `results/tables/paired_comparisons_rmse.csv` |
| Variance split, wafer-mean R², forward skip counts, OES wavelength check | `results/results_extras.json` (cell 7) |

The files in `results/` come from the author's Colab run. `results_extras.json` was computed with cell 7 on the same cached features. Runs with other library versions changed lot-averaged map errors by at most about 0.004 µm. Skip decisions at tolerances of 0.2 µm or less are numerically fragile, as the paper explains.

## License

- **Code:** MIT (see `LICENSE`).
- **Data:** the dataset belongs to its authors and is licensed CC BY 4.0. The derived features and results in `results/` come from it, so please cite the dataset when you use them.

## Citation

