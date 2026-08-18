# EO Geospatial Agent

An AI-powered Earth Observation coding agent built with **Pydantic AI**, **OpenRouter**, and a deterministic geospatial dataset selection layer.

The agent accepts natural-language Earth Observation requests, interprets the analysis requirements, selects appropriate datasets and products, calls controlled tools, adapts its reasoning effort to task complexity, and dynamically discovers reusable skills at runtime.

The project was developed incrementally across six exercises covering LLM interaction, conversation state, tool calling, execution hooks, adaptive reasoning, and dynamic skill extensibility.

---

## Project Overview

Earth Observation workflows often require several decisions before an analysis can begin:

* Which dataset is appropriate?
* What spatial and temporal resolution is required?
* Are the required spectral bands or SAR polarizations available?
* Does a suitable native product already exist?
* Which dataset provides the required environmental variables?
* How computationally suitable is the candidate?

The EO Geospatial Agent combines a language model with a controlled Python-based dataset registry, compatibility layer, selector, and ranking system.

The language model handles natural-language interpretation and explanation, while deterministic Python components remain responsible for dataset metadata, eligibility, compatibility, and ranking.

### Example

A user can ask:

> Which dataset should I use for NDVI at regional scale?

The agent interprets the request and calls the dataset-selection skill.

A current example returns:

```text
Highest-ranked candidate: MODIS MOD13Q1.061
Total suitability score: 0.94
```

The agent then explains the ranking evidence and relevant metadata.

---

# Six Exercise Architecture

The project was developed through six progressive exercises.

## 1. First LLM Call

The agent is configured with:

* a model provider
* an Earth Observation system prompt
* an interactive agent interface

The model is used for natural-language interpretation and response generation.

---

## 2. Conversation State

The agent supports multi-turn interactions by maintaining conversation message history.

This allows the model to use previous turns when interpreting subsequent requests rather than treating every request as an isolated interaction.

---

## 3. Tool Calling

The agent uses Python functions exposed through Pydantic AI toolsets.

The dataset-selection functionality is implemented as a controlled tool:

```text
User request
     |
     v
    Agent
     |
     v
Dataset selection tool
     |
     v
Deterministic selector
     |
     v
Dataset ranker
     |
     v
Structured ranking result
```

The tool receives a structured `DatasetSelectionRequest` and returns a `DatasetRanking`.

This keeps the language-model layer separate from the deterministic dataset-selection logic.

---

## 4. Execution Hooks

Tool execution is monitored using Pydantic AI lifecycle hooks.

The project includes hooks for:

* before tool execution
* after successful tool execution
* tool execution errors

Example runtime logging:

```text
[HOOK] Starting tool: select_best_dataset_tool
[HOOK] Arguments: {...}
[HOOK] Finished tool: select_best_dataset_tool
[HOOK] Result: ...
```

This provides visibility into tool execution without embedding logging logic directly inside the dataset-selection tool.

---

## 5. Adaptive Reasoning

The agent includes an adaptive reasoning capability that determines the appropriate reasoning effort for a request.

The architecture can distinguish between simpler and more complex requests and configure the model accordingly.

This capability is integrated into the agent's capability system rather than hard-coded into individual tools.

The goal is to avoid treating every request as requiring the same level of reasoning.

---

## 6. Skills and Extensibility

The agent supports dynamically discovered skills.

Skills are stored as modules under:

```text
agent/skills/
```

The skill loader uses Python module discovery and dynamic imports to find available skill toolsets at runtime.

The loader:

1. discovers modules in the skills package
2. imports available skill modules
3. identifies `AbstractToolset` instances
4. combines discovered toolsets
5. exposes them through a Pydantic AI `DynamicToolset`

Current skill:

```text
agent/skills/dataset_selection.py
```

The dynamic architecture means a new skill can be added as a separate module without modifying the loader itself.

Conceptually:

```text
agent/skills/
      |
      +-- dataset_selection.py
      |
      +-- future_skill.py
      |
      +-- another_skill.py
              |
              v
        Dynamic skill loader
              |
              v
        Combined toolset
              |
              v
             Agent
```

This provides a foundation for adding additional Earth Observation capabilities as reusable skills.

---

# Current Capabilities

The current implementation can:

1. Interpret natural-language Earth Observation requests.
2. Maintain conversation state across turns.
3. Call controlled Python tools.
4. Discover and load skills dynamically.
5. Identify the appropriate data family.
6. Convert requests into structured `DatasetSelectionRequest` objects.
7. Determine eligible datasets and native products.
8. Distinguish between native-product and calculated-analysis pathways.
9. Check spectral-band compatibility.
10. Check SAR polarization compatibility.
11. Evaluate spatial suitability.
12. Evaluate temporal suitability.
13. Evaluate environmental variable suitability.
14. Evaluate computational suitability.
15. Rank eligible candidates using a deterministic scoring system.
16. Return explainable dataset recommendations.
17. Log tool execution through lifecycle hooks.
18. Adapt reasoning effort according to request complexity.

The current implementation focuses on **Earth Observation dataset and product selection** rather than performing complete imagery-processing workflows.

---

# Supported Data Sources

The dataset registry currently includes:

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

* `MOD13Q1.061`, MODIS vegetation indices
* `CHIRPS-DAILY`, daily precipitation
* `CHIRPS-MONTHLY`, monthly precipitation

The registry is designed to be extended with additional datasets and products.

---

# Supported Analyses

The spectral-index registry currently includes:

* **NDVI**, Normalized Difference Vegetation Index
* **EVI**, Enhanced Vegetation Index
* **NDRE**, Normalized Difference Red Edge Index
* **NDMI**, Normalized Difference Moisture Index
* **NDWI**, Normalized Difference Water Index
* **NBR**, Normalized Burn Ratio
* **GNDVI**, Green Normalized Difference Vegetation Index
* **SAVI**, Soil Adjusted Vegetation Index

SAR analysis currently includes:

* soil-moisture-related analysis using SAR polarization requirements such as VV and VH

Environmental analysis includes:

* precipitation
* climate-related requests

Band mappings and analysis definitions are maintained separately from the agent layer, allowing compatibility to be tested deterministically.

---

# Dataset Selection Architecture

The core selection workflow is:

```text
Natural-language request
          |
          v
        Agent
          |
          v
Structured analysis request
          |
          v
Dataset Selection Skill
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
Ranked candidate
          |
          v
Agent explanation
```

The language model does not independently determine dataset metadata or ranking scores.

Instead, the agent calls the dataset-selection tool, which delegates the decision to the deterministic selection layer.

---

# Candidate Pathways

The selector supports two main analysis pathways.

## Native Product

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

## Calculated Analysis

The requested analysis is derived from available measurements or bands.

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

The same architecture is used for SAR requirements such as polarization compatibility.

---

# Ranking System

Eligible candidates are evaluated across several dimensions.

| Criterion                  | Weight |
| -------------------------- | -----: |
| Spatial suitability        |    30% |
| Temporal suitability       |    25% |
| Native product suitability |    15% |
| Spectral suitability       |    15% |
| Computational suitability  |    15% |

Variable suitability is also evaluated where relevant to the requested data family.

The ranking logic is implemented in Python rather than delegated entirely to the language model.

This makes dataset selection:

* deterministic
* reproducible
* testable
* explainable

---

# Example Requests

### Vegetation monitoring

> Which dataset should I use for NDVI at regional scale?

Example result:

```text
MODIS MOD13Q1.061
Total suitability score: 0.94
```

The returned metadata identifies the product as a 16-day vegetation-index product.

### Precipitation

> Which dataset should I use for monthly precipitation at regional scale?

Example candidate:

```text
CHIRPS-MONTHLY
```

### SAR analysis

> Which dataset should I use for soil moisture analysis at regional scale?

Example candidate:

```text
Sentinel-1
Calculated pathway
```

The agent explains the ranking evidence and metadata returned by the selection system rather than inventing additional dataset characteristics.

---

# Project Structure

```text
eo-geospatial-agent/
|
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── hooks.py
│   ├── model.py
│   └── skills/
│       ├── __init__.py
│       ├── dataset_selection.py
│       └── loader.py
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
│   ├── test_agent_hooks.py
│   ├── test_dataset_ranker.py
│   ├── test_dataset_selector.py
│   └── test_skill_loader.py
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

# Technology Stack

The project uses:

* **Python**
* **Pydantic**
* **Pydantic AI**
* **OpenRouter**
* **Python-dotenv**
* **Pytest**
* **Raster and geospatial Python libraries**

The architecture separates language-model orchestration from deterministic geospatial decision logic.

---

# Installation

Create the project environment using Conda:

```bash
conda create -n eo_agent python=3.12
conda activate eo_agent
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a local `.env` file based on `.env.example` and provide the required model API configuration.

API keys should never be committed to the repository.

---

# Running the Agent

The example agent script can be run with:

```bash
python test_agent.py
```

The script sends a natural-language Earth Observation request to the agent and prints the resulting response.

---

# Running Tests

Run the complete test suite with:

```bash
python -m pytest -q
```

The current test suite contains:

```text
127 passed
```

The tests cover the project's core functionality, including:

* schemas
* dataset and product registries
* band mappings
* compatibility checks
* spatial and temporal suitability
* dataset ranking
* dataset selection
* agent-level tool calling
* execution hooks
* adaptive reasoning
* dynamic skill discovery
* multiple dynamically discovered skills

The full suite currently passes with **127 tests and 0 failures**.

---

# Design Principles

## Controlled Tool Use

The language model does not independently invent dataset metadata or ranking results.

Dataset information is maintained in structured registries and evaluated by deterministic Python components.

## Separation of Concerns

The project separates:

```text
Natural-language interpretation
             |
             v
       Agent layer
             |
             v
       Skill/tool layer
             |
             v
     Dataset selection
             |
             v
       Ranking layer
             |
             v
       Registry layer
```

This allows individual components to be tested and extended independently.

## Explainability

The agent reports the ranking evidence and relevant metadata returned by the selection system rather than exposing hidden model reasoning.

## Extensibility

Datasets, products, spectral indices, SAR analyses, band mappings, and agent skills can be extended independently.

New skills can be added under `agent/skills/` and discovered dynamically at runtime.

## Testability

The project maintains automated tests across the agent, deterministic core, hooks, and skill-loading architecture.

This allows the system to evolve while preserving established behavior.

---

# Current Limitations

The current implementation is primarily a **dataset-selection and recommendation agent**.

It does not yet provide a complete automated workflow for:

* downloading imagery from remote sensing data providers
* automatically resolving arbitrary geographic locations into analysis areas
* retrieving user-specified imagery for a date range
* cloud and quality masking of downloaded imagery
* resampling and preprocessing imagery
* calculating an index directly from newly acquired imagery
* generating and returning an interactive geospatial map

These capabilities remain potential future extensions.

---

# Future Development

The next stage would be to extend the agent from dataset selection into an end-to-end Earth Observation analysis workflow.

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
Retrieve imagery or environmental data
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

The dynamic skill architecture provides a foundation for implementing these capabilities as additional reusable skills rather than expanding the agent into a single monolithic module.

---

# Project Status

**Current stage: Six-exercise agentic Earth Observation system**

The project now includes:

* a functioning natural-language agent
* conversation-state support
* controlled tool calling
* a deterministic Earth Observation dataset-selection system
* dataset and product registries
* eligibility and compatibility checking
* multi-criteria dataset ranking
* explainable recommendations
* execution lifecycle hooks
* adaptive reasoning
* dynamic skill discovery
* automated test coverage

**Latest validation:**

```text
127 passed
0 failed
```

The current implementation provides the agentic foundation for extending the project into a complete Earth Observation data acquisition, processing, analysis, and visualization workflow.
