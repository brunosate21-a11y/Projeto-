# Snakemake workflow: `microbial-community-modeling`
 
[![Snakemake](https://img.shields.io/badge/snakemake-%E2%89%A58.0.0-brightgreen.svg)](https://snakemake.github.io)
[![GitHub actions status](https://github.com/brunosate21-a11y/Repositrio-Codigo/workflows/Tests/badge.svg?branch=main)](https://github.com/brunosate21-a11y/Repositrio-Codigo/actions?query=branch%3Amain+workflow%3ATests)
[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)
[![workflow catalog](https://img.shields.io/badge/Snakemake%20workflow%20catalog-darkgreen)](https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows/brunosate21-a11y/Repositrio-Codigo)
 
A Snakemake workflow for `metabolic modeling of microbial communities from metagenome-assembled genomes (MAGs)`
 
## Table of Contents
 
- [Overview](#overview)
- [Workflow steps](#workflow-steps)
- [Usage](#usage)
- [Deployment options](#deployment-options)
- [Workflow profiles](#workflow-profiles)
- [Authors](#authors)
- [References](#references)
## Overview
 
This workflow implements a modular and reproducible pipeline for genome-scale metabolic modeling of microbial communities, starting from previously assembled MAGs or genomes. It integrates genome quality assessment, automatic reconstruction of genome-scale metabolic models (GEMs), and community-level metabolic simulations.
 
The pipeline is structured around Snakemake wrappers, allowing individual components to be replaced or adapted without modifying the rest of the workflow. This promotes automation, traceability, and reusability across different metagenomic datasets.
 
## Workflow steps
 
1. **Input data preparation** — collection and organization of previously assembled MAGs or genomes.
2. **Genome quality assessment** — evaluation of completeness and contamination using CheckM, retaining only genomes that meet minimum quality criteria consistent with MIMAG recommendations (>50% completeness, <10% contamination).
3. **Automatic GEM reconstruction** — generation of genome-scale metabolic models using CarveMe, in a format compatible with downstream community analysis tools.
4. **Model verification and compatibility** — assessment of basic model viability and harmonization of metabolite and reaction identifiers to ensure consistent use in community context.
5. **Community-level simulation** — application of validated models in SMETANA, SteadyCom, and MICOM to explore metabolic dependencies, community growth, relative abundances, and possible exchange fluxes between organisms.
6. **Comparative analysis** — comparison of results from the three tools, focusing on: (i) potentially shared or competed metabolites; (ii) metabolic dependencies inferred by SMETANA; and (iii) growth and abundance estimates from SteadyCom and MICOM.
## Tools integrated
 
| Tool | Purpose |
|------|---------|
| [CheckM](https://ecogenomics.github.io/CheckM/) | Genome quality assessment |
| [CarveMe](https://carveme.readthedocs.io/) | Genome-scale metabolic model reconstruction |
| [Memote](https://memote.readthedocs.io/) | Metabolic model quality testing |
| [SMETANA](https://smetana.readthedocs.io/) | Metabolic interaction inference between community members |
| [SteadyCom](https://github.com/hongzhonglu/SteadyCom) | Steady-state community flux and abundance prediction |
| [MICOM](https://micom-dev.github.io/micom/) | Metagenome-scale community metabolic modeling |
 
## Usage
 
The usage of this workflow is described in the [Snakemake Workflow Catalog](https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows/brunosate21-a11y/Repositrio-Codigo).
 
Detailed information about input data and workflow configuration can be found in [`config/README.md`](config/README.md).
 
If you use this workflow in a paper, please cite the URL of this repository and give credits to the authors.
 
## Deployment options
 
To run the workflow from command line, change the working directory:
 
```bash
cd path/to/Repositrio-Codigo
```
 
Adjust options in the default config file `config/config.yaml`.
 
Before running the complete workflow, perform a dry run using:
 
```bash
snakemake --dry-run
```
 
To run the workflow with test files using **conda**:
 
```bash
snakemake --cores 2 --sdm conda --directory .test
```
 
To run the workflow with **apptainer** / **singularity**:
 
```bash
snakemake --cores 2 --sdm conda apptainer --directory .test
```
 
## Workflow profiles
 
The `profiles/` directory contains [workflow-specific profiles](https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles) that users can choose from. See the [profiles README.md](profiles/README.md) for more details.
 
## Authors
 
- **Bruno Ferreira**
  - Universidade do Minho, Portugal
  - pg58814@uminho.pt
- **Artur Gomes**
  - Universidade do Minho, Portugal
  - pg55692@alunos.uminho.pt
- **Andreia Salvador**
  - Centre of Biological Engineering (CEB), Universidade do Minho, Portugal
  - asalvador@ceb.uminho.pt
- **Óscar Dias**
  - Centre of Biological Engineering (CEB), Universidade do Minho, Portugal
  - odias@ceb.uminho.pt
