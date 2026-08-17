# EO Geospatial Agent

An AI-powered Earth Observation agent for selecting suitable remote sensing and geospatial datasets based on an analysis request.

The agent combines a language model with a controlled dataset selection and ranking system. It interprets a user's natural-language request, converts it into a structured analysis requirement, evaluates eligible datasets and products, ranks them according to multiple suitability criteria, and explains the recommendation.

## Project Overview

Selecting an appropriate Earth Observation dataset is often a multi-criteria decision. The best dataset depends on factors such as:

* spatial scale and resolution
* temporal requirements
* spectral or SAR band availability
* whether a suitable native product exists
* required environmental variables
* computational requirements

The EO Geospatial Agent automates this decision process while keeping dataset selection deterministic and testable through a controlled registry and ranking layer.

### Example

A user can ask:

> Which dataset should I use to calculate NDVI for a regional area using monthly observations?

The agent interprets the request, identifies the relevant data family and requirements, evaluates available candidates, and can recommend:

**MODIS MOD13Q1.061**, with an overall suitability score of 0.94.

The agent also explains the trade-offs, including the product's 16-day temporal resolution and the possibility of aggregating observations to a monthly cadence.

---

## Current Capabilities

The current version of the agent can:

1. Interpret natural-language Earth Observation requests.
2. Convert requests into structured `DatasetSelectionRequest` objects.
3. Identify the appropriate data family.
4. Determine eligible datasets and native products.
5. Distinguish between native-product and calculated-analysis pathways.
6. Check spectral-band or SAR-polarization compatibility.
7. Evaluate spatial suitability.
8. Evaluate temporal suitability.
9. Evaluate variable suitability.
10. Evaluate computational suitability.
11. Rank eligible candidates using a weighted scoring system.
12. Return an explainable recommendation through the AI agent.

The current implementation focuses on **dataset and product selection**. Automated imagery acquisition, preprocessing, index calculation, and map generation are planned extensions rather than current capabilities.

---

## Supported Data Sources

The dataset registry currently includes the following Earth Observation and environmental datasets:

| Dataset    | Data family   | Typical role                                       |
| ---------- | ------------- | -------------------------------------------------- |
| Sentinel-2 | Optical       | High-resolution vegetation and spectral analysis   |
| Landsat-8  | Optical       | Multispectral Earth Observation                    |
| Landsat-9  | Optical       | Multispectral Earth Observation                    |
| MODIS      | Optical       | Large-area and long-term vegetation monitoring     |
| HLS        | Optical       | Harmonized Landsat and Sentinel-2 analysis         |
| Sentinel-1 | SAR           | SAR backscatter and soil-moisture-related analysis |
| CHIRPS     | Precipitation | Daily and monthly precipitation analysis           |
| ERA5       | Climate       | Meteorological and climate analysis                |
| ERA5-Land  | Climate       | Higher-resolution land-surface climate analysis    |

### Native products currently represented

Examples include:

* `MOD13Q1.061`, MODIS 16-day vegetation indices at 250 m
* `CHIRPS-DAILY`, daily precipitation
* `CHIRPS-MONTHLY`, monthly precipitation

The registry is designed to be extensible, allowing additional datasets and products to be added without redesigning the selection architecture.

---

## Supported Analyses

The current spectral-index registry includes:

* NDVI, Normalized Difference Vegetation Index
* EVI, Enhanced Vegetation Index
* NDRE, Normalized Difference Red Edge Index
* NDMI, Normalized Difference Moisture Index
* NDWI, Normalized Difference Water Index
* NBR, Normalized Burn Ratio
* GNDVI, Green Normalized Difference Vegetation Index
* SAVI, Soil Adjusted Vegetation Index

SAR analysis currently includes:

* Soil moisture analysis using SAR polarization requirements such as VV and VH

Environmental analysis includes:

* precipitation
* climate-related requests

The analysis registry and band mappings are designed so that compatibility can be checked before a candidate is selected.

---

## Dataset Selection Architecture

The selection workflow is:

```text
User's natural-language request
            |
            v
       AI Agent
            |
            v
 Structured analysis request
            |
            v
     Dataset Selector
            |
            v
  Eligibility and compatibility
            |
            v
      Dataset Ranker
            |
            v
       Ranked candidates
            |
            v
   Explainable recommendation
```

### Candidate pathways

The selector considers two main pathways:

**Native product**

A dataset already provides a suitable product for the requested analysis.

Example:

```text
NDVI request
    |
    v
MODIS MOD13Q1.061
    |
    v
Native NDVI product
```

**Calculated analysis**

The requested analysis must be derived from available bands or measurements.

Example:

```text
NDMI request
    |
    v
Sentinel-2
    |
    v
Required spectral bands
    |
    v
Calculated NDMI
```

For SAR analysis, the same concept is applied to required polarization information.

---

## Ranking System

Eligible candidates are scored across several dimensions.

| Criterion                  | Weight |
| -------------------------- | -----: |
| Spatial suitability        |    30% |
| Temporal suitability       |    25% |
| Native product suitability |    15% |
| Spectral suitability       |    15% |
| Computational suitability  |    15% |

Variable suitability is also evaluated where relevant to the requested data family.

The ranking system uses normalized temporal and spatial information from the dataset and product registries rather than relying solely on the language model.

This separation makes the selection process more transparent, reproducible, and testable.

---

## Example Requests

### Vegetation monitoring

> Which dataset should I use to calculate NDVI for a regional area using monthly observations?

Possible recommendation:

```text
MODIS MOD13Q1.061
Total suitability score: 0.94
```

### Precipitation

> Which dataset should I use for monthly precipitation at regional scale?

Possible recommendation:

```text
CHIRPS-MONTHLY
Total suitability score: 0.94
```

### SAR analysis

> Which dataset should I use for soil moisture analysis at regional scale?

Possible recommendation:

```text
Sentinel-1
Calculated pathway
Total suitability score: 0.92
```

The agent also explains relevant limitations and trade-offs rather than returning only a dataset name.

---

## Project Structure

```text
eo-geospatial-agent/
|
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   └── model.py
|
├── core/
│   ├── __init__.py
│   ├── band_mapping.py
│   ├── dataset_ranker.py
│   ├── dataset_registry.py
│   ├── dataset_selector.py
│   ├── product_registry.py
│   ├── registry.py
│   └── schemas.py
|
├── tests/
│   ├── test_agent_tool.py
│   ├── test_dataset_ranker.py
│   └── test_dataset_selector.py
|
├── data/
├── outputs/
├── test_agent.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Technology Stack

The project uses:

* Python
* Pydantic
* Pydantic AI
* OpenRouter
* Python-dotenv
* Pytest
* Raster and geospatial libraries used by the project architecture

The agent uses a language model for natural-language interpretation and explanation, while dataset compatibility and ranking are handled by controlled Python components.

---

## Installation

Clone the repository and create the project environment.

Example using Conda:

```bash
conda create -n eo_agent python=3.12
conda activate eo_agent
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a local `.env` file based on `.env.example` and provide the required model API configuration.

API keys should not be committed to the repository.

---

## Running the Agent

The example agent script can be run with:

```bash
python test_agent.py
```

The script sends a natural-language Earth Observation request to the agent and prints the resulting recommendation.

---

## Running Tests

Run the complete test suite with:

```bash
python -m pytest -q
```

The current test suite contains **106 passing tests** covering dataset schemas, registry functionality, band compatibility, temporal and spatial suitability, dataset ranking, dataset selection, and agent-level dataset-selection behavior.

Latest validated result:

```text
106 passed
```

---

## Design Principles

The project follows several principles:

### Controlled tool use

The language model does not independently invent dataset metadata. Dataset information is maintained in structured registries and evaluated by deterministic selection and ranking functions.

### Explainability

The agent provides the reasoning behind a recommendation, including individual suitability scores and relevant metadata.

### Extensibility

Datasets, products, spectral indices, SAR analyses, and band mappings can be added through the registry architecture.

### Separation of concerns

Natural-language interpretation, dataset eligibility, ranking, and agent orchestration are separated into different components.

### Testability

Core selection and ranking behavior is covered by automated tests, allowing the system to evolve without losing established behavior.

---

## Current Limitations

The current implementation is primarily a **dataset-selection and recommendation agent**.

It does not yet provide a complete automated workflow for:

* downloading imagery from remote sensing data providers
* automatically interpreting arbitrary geographic locations
* retrieving user-specified imagery for a date range
* cloud and quality masking of downloaded imagery
* resampling and preprocessing imagery
* calculating an index directly from newly acquired imagery
* generating and returning an interactive geospatial map

These capabilities are intended as future extensions.

---

## Future Development

The next stage of the project is to extend the agent from dataset selection into an end-to-end Earth Observation analysis workflow.

A potential workflow is:

```text
User request
    |
    v
Interpret analysis, AOI and time period
    |
    v
Select appropriate dataset
    |
    v
Retrieve imagery
    |
    v
Clip to AOI
    |
    v
Preprocess and quality-mask data
    |
    v
Calculate requested index or variable
    |
    v
Generate visualization
    |
    v
Return result and explanation
```

Potential future agent capabilities include reusable toolsets, function tools, lifecycle hooks, dynamic instructions, model configuration, and controlled web or data-access tools.

---

## Project Status

**Current stage: Dataset-selection agent**

The project has a functioning natural-language agent, a controlled dataset and product registry, an eligibility and compatibility layer, a multi-criteria ranking system, and automated test coverage.

The next development stage is to connect dataset selection with actual Earth Observation data acquisition and analysis.
