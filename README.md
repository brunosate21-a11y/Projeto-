# Metabolic Modeling Workflow

> Automated genome-scale metabolic reconstruction and microbial community simulation from MAGs.

[![Snakemake](https://img.shields.io/badge/snakemake-≥8.0-brightgreen.svg)](https://snakemake.github.io)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Conda](https://img.shields.io/badge/conda-managed-44A833.svg)](https://docs.conda.io)

A reproducible **Snakemake** pipeline that reconstructs genome-scale metabolic models (GEMs) from previously assembled genomes — with a focus on **metagenome-assembled genomes (MAGs)** — and simulates their metabolic interactions at the community level using three complementary tools.

The whole analysis runs as a single, traceable flow: quality control → model reconstruction → model validation → community simulation → cross-method comparison. Everything is parameterised through config files, so the **same code runs on different datasets** without any edits.

---

## What it does

| Stage | Tool | Purpose |
|-------|------|---------|
| Genome QC | **CheckM** / **CheckM2** | Completeness & contamination filtering |
| Reconstruction | **CarveMe** | Builds one GEM per genome (SBML) |
| Model QC | **Memote** | Standardised model quality score & filtering |
| Community sim. | **SMETANA** | Resource overlap (MRO/MIP) + cross-feeding |
| Community sim. | **MICOM** | Cooperative community FBA, exchange fluxes |
| Community sim. | **SteadyCom** | Steady-state growth & abundances |
| Analysis | *(built-in)* | Cross-method comparison + sensitivity analysis |

**Key capabilities**

- **Flexible MAG detection** — via a sample sheet, a config list, or auto-detection of `.faa` files
- **CheckM2 bypass** — if you already have a CheckM2 quality report, the pipeline skips re-running CheckM and reuses your numbers
- **Abundance re-normalisation** — after filtering, relative abundances of the surviving genomes are recomputed to sum to 1
- **Sensitivity analysis** — sweeps quality-threshold grids and produces robustness heatmaps
- **Cross-method comparison** — correlates the three community tools and exports a summary figure
- **Reproducible** — isolated per-rule Conda environments
- **Solver-agnostic** — SCIP (free), CPLEX, or Gurobi

---

## Requirements

- **OS:** Linux (native) or **Windows + WSL2** — *CarveMe is not supported on native Windows*
- **Miniconda / Anaconda**
- **Snakemake ≥ 8.0**
- **LP solver:** SCIP (free) or **CPLEX** (recommended — much faster for community simulations)

---

## Quick Start

### 1. Get the code

```bash
git clone https://github.com/brunosate21-a11y/Projeto-.git
cd "Projeto-/Fase 2"
```

> The workflow lives inside the `Fase 2/` folder. All commands below are run from there.

### 2. Create the Snakemake environment

```bash
conda create -n snakemake -c bioconda -c conda-forge snakemake -y
conda activate snakemake
```

### 3. Add your genomes

Place protein FASTA files (`.faa`) into `data/mags/`:

```
data/mags/
├── Ecoli_K12.faa
├── Bsubtilis_168.faa
└── ...
```

The four reference genomes used to validate the pipeline are *Bacillus subtilis* 168, *Escherichia coli* K-12, *Pseudomonas putida* NBRC 14164 and *Streptococcus pneumoniae* TIGR4.

You can also fetch genomes from NCBI with the included helper (Windows PowerShell):

```powershell
.\download_mags.ps1
```

### 4. Run

```bash
snakemake --use-conda --cores 12
```

Snakemake handles dependency resolution, the Conda environments, and parallel execution. On start it prints which mode it is using (CheckM vs CheckM2 bypass, uniform vs real abundances, number of MAGs detected).

---

## Running on real MAGs (with external metadata)

In a real scenario your MAGs usually already come with a CheckM2 quality report and relative abundances. The pipeline supports this directly through a second config file — **no code changes**, just point Snakemake at it:

```bash
snakemake --configfile config/config_real.yaml --use-conda --cores 12
```

Three ready-made configs are provided:

| Config | Dataset | Notes |
|--------|---------|-------|
| `config/config.yaml` | 4 reference genomes | Default; CheckM + uniform abundances |
| `config/config_real.yaml` | 22 real MAGs | CheckM2 bypass + real abundances |
| `config/config_real12.yaml` | top-12 subset | For the (expensive) detailed SMETANA analysis |

When a `checkm_report:` is set, the pipeline **bypasses CheckM** and splits your TSV per genome. When `abundances:` is set, the community tools use your real abundances (re-normalised after filtering) instead of a uniform `1/n` distribution.

The real dataset expects this layout:

```
data/real/
├── proteins/                  # the .faa files
├── samples.tsv                # sample sheet (id + path)
└── metadata/
    ├── checkm_quality.tsv     # CheckM2 report
    └── abundances.tsv         # relative abundances
```

---

## Project Structure

```
Fase 2/
├── config/
│   ├── config.yaml             # Default (reference) config
│   ├── config_real.yaml        # Real 22-MAG dataset
│   ├── config_real12.yaml      # Top-12 subset
│   └── README.md
├── data/
│   ├── mags/                   # Drop reference .faa files here
│   └── real/                   # Real MAGs + metadata
├── workflow/
│   ├── Snakefile               # Main entry point (rule all + sample detection)
│   ├── envs/                   # One Conda env per tool
│   ├── rules/                  # One .smk per stage
│   └── scripts/                # Python logic behind each rule
├── profiles/                   # Snakemake execution profiles
├── download_mags.ps1           # NCBI download helper
├── CHANGELOG.md
└── LICENSE
```

---

## Outputs

After a run, the results directory (`results/` by default, `results/real/` for the real dataset) contains:

```
results/
├── gems/<MAG>.xml                      # CarveMe GEMs (SBML)
├── checkm/
│   ├── checkm_summary.tsv              # QC metrics per genome
│   └── filtered_mags.txt              # Genomes passing CheckM/CheckM2
├── memote/
│   ├── <MAG>/report.html               # Interactive Memote reports
│   ├── memote_summary.tsv              # Aggregated scores
│   └── filtered_models.txt             # Models passing the score threshold
├── abundances/abundances_filtered.tsv  # Re-normalised abundances
├── micom/exchange_fluxes.tsv           # Produced/consumed metabolites
├── smetana/
│   ├── global.tsv                      # MIP / MRO community scores
│   └── detailed.tsv                    # Pairwise cross-feeding
├── steadycom/abundances.tsv            # Steady-state growth & abundances
└── comparison/
    ├── per_species.tsv                 # All three methods, per organism
    ├── community_summary.tsv           # Community-level synthesis
    └── comparison.png                  # Cross-method comparison figure
```

---

## Configuration Reference

| Parameter | Description | Default |
|-----------|-------------|---------|
| `solver` | LP/MILP solver (`scip`, `cplex`, `gurobi`) | `cplex` |
| `media` | Gap-fill culture medium | `M9` |
| `mags_dir` | Directory with input `.faa` files | `data/mags` |
| `results_dir` | Output directory | `results` |
| `sample_sheet` | TSV with `id` + `path` columns *(optional)* | — |
| `checkm_report` | CheckM2 report → enables bypass *(optional)* | — |
| `abundances` | Real relative abundances *(optional)* | uniform `1/n` |
| `quality_filters.checkm.min_completeness` | Min completeness (%) | `50.0` |
| `quality_filters.checkm.max_contamination` | Max contamination (%) | `10.0` |
| `quality_filters.memote.min_total_score` | Min Memote total score | `0.4` |
| `sensitivity_analysis.*` | Threshold grids to sweep | see config |

> **Note:** the defaults ship with `solver: cplex`. If you don't have CPLEX, set `solver: scip` — it's free and works out of the box (just slower).

---

## Sensitivity analysis

The pipeline can sweep the quality-filter thresholds to see how robust the community is to the choices you make. It sweeps the CheckM completeness/contamination grid and the Memote score grid defined under `sensitivity_analysis:` in the config, then writes:

- `results/sensitivity/threshold_grid.tsv` — how many genomes survive each threshold combination
- `results/sensitivity/mag_robustness.tsv` — per-genome robustness
- `results/sensitivity/heatmaps.png` — visual summary

In our runs the **Memote total score was the binding filter**, with a critical transition between 0.6 and 0.7.

---

## Performance: prefer CPLEX

For community simulations (especially the detailed SMETANA mode) the LP solver dominates runtime, and SMETANA's detailed cost grows with the **square** of the number of organisms:

| Solver | SMETANA, 4 organisms |
|--------|----------------------|
| SCIP (free) | ~60–90 min |
| **CPLEX (academic)** | **~5–15 min**  |

CPLEX is free for academia via the [IBM Academic Initiative](https://academic.ibm.com). Install CPLEX Optimization Studio and set `solver: cplex`.

> For large communities, run the **global** SMETANA (MIP/MRO) on all genomes but restrict the **detailed** cross-feeding analysis to the most abundant subset (e.g. `config_real12.yaml`) — that's exactly what the top-12 config is for.

---

## Tools integrated

- **[CarveMe](https://github.com/cdanielmachado/carveme)** — GEM reconstruction
- **[CheckM](https://github.com/Ecogenomics/CheckM)** / **[CheckM2](https://github.com/chklovski/CheckM2)** — genome quality
- **[Memote](https://github.com/opencobra/memote)** — model quality assessment
- **[SMETANA](https://github.com/cdanielmachado/smetana)** — metabolic interaction analysis
- **[MICOM](https://github.com/micom-dev/micom)** — community modelling (also runs SteadyCom)
- **[Snakemake](https://snakemake.readthedocs.io/)** — workflow management

---

## Troubleshooting

- **No MAGs found** — make sure `.faa` files are in `data/mags/`, or that `sample_sheet:` / `MAGS:` is set in the config.
- **CarveMe fails on Windows** — run inside WSL2; CarveMe is not supported on native Windows.
- **Solver errors** — if you don't have CPLEX, set `solver: scip` in the config.
- **SMETANA is very slow** — switch to CPLEX, or run the detailed analysis only on a subset (`config_real12.yaml`).

---

## 👤 Authors

**Bruno Ferreira**  
Supervised by **Artur Gomes** **Doutora Andreia Salvador** and **Professor Óscar Dias**
Universidade do Minho — Centre of Biological Engineering (CEB)

---

## 📄 License

Released under the MIT License — see [LICENSE](LICENSE) for details.
