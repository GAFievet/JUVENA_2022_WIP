# JUVENA_2022 - Glider Echosounding for European Juvenile Anchovy Distribution in the SE Bay of Biscay

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Project Objectives](#2-project-objectives)
3.  [Centrality of Glider Echosounding](#3-centrality-of-glider-echosounding)
4.  [Data](#4-data)
5.  [Installation](#5-installation)
6.  [Usage](#6-usage)
7.  [Results & Visualizations](#7-results--visualizations)
8.  [Testing](#8-testing)
9.  [Contribution](#9-contribution)
10. [License](#10-license)
11. [Contact](#11-contact)

## 1. Introduction
This `JUVENA_2022` project is a dedicated suite of Python tools and scripts primarily focused on the **analysis and processing of data collected through glider echosounding to understand the distribution of European juvenile anchovy (Engraulis encrasicolus) in the southeast Bay of Biscay**. While it integrates various complementary oceanographic and fisheries datasets, its core purpose is to extract, process, and interpret acoustic data from autonomous gliders for targeted insights into this specific pelagic species. The project aims to centralize and streamline data processing steps to facilitate advanced research and visualization critical for fisheries management and ecological studies.

## 2. Project Objectives
* **Glider Echosounding Data Ingestion & Pre-processing:** Develop robust pipelines for handling raw acoustic data from gliders, including data processing for visualization and statistics, while accounting for potential impacts of harsh meteorological conditions on data quality.
* **Acoustic Anchovy Visualisation:** Implement and refine algorithms specifically for plotting relevant acoustic signals indicative of European juvenile anchovy from glider echograms pre-processed with Echoview or any other equivalent.
* **Environmental Contextualization:** Integrate glider echosounding data with concurrent oceanographic parameters (glider-mounted CTD, satellite SST and CHLA, modelled oceanic currents) to analyze how environmental drivers and harsh weather conditions influence anchovy distribution within the southeast Bay of Biscay.
* **Spatial and Temporal Distribution Analysis:** Analyze the spatial and temporal patterns of juvenile anchovy distribution based on acoustic observations, considering the influence of highly dynamic and potentially harsh meteorological conditions during surveys.
* **Advanced Data Analysis:** Perform specialized analyses such as Brunt-Väisälä frequencies (BV_ferq) and generate T-S diagrams to enhance echosounding interpretations relevant to anchovy habitat, especially in the context of observed meteorological variability.
* **Visualization:** Generate high-quality plots and reports to effectively communicate findings on anchovy distribution and associated environmental conditions, including the impact of meteorological events.
* **Reproducibility:** Ensure the reproducibility of all analyses through a well-defined dependency environment and clear code structure.ty of all analyses through a well-defined dependency environment and clear code structure.

## 3. Centrality of Glider Echosounding
The architecture and functionalities of this project are designed with **glider-mounted echosounding** as the central pillar for understanding juvenile anchovy distribution. All other data processing modules (CTD, SST, CHLA, fishing data, etc.) serve to contextualize, validate, or enhance the analysis of the acoustic data, directly contributing to a comprehensive picture of the anchovy's habitat and behavior in the targeted region. The project's evolution is driven by the specific challenges and opportunities presented by this innovative data acquisition method for small pelagic species.

## 4. Data
The project primarily processes and analyzes data from **glider-mounted echosounders**, with a specific emphasis on acoustic signatures of European juvenile anchovy. This is complemented by various other oceanographic and fisheries datasets collected within the southeast Bay of Biscay.
* **Raw Data:** Should be placed in the `data/raw/` directory. These files are considered immutable by the scripts. This includes raw acoustic files (e.g., .raw, .nc), alongside glider GPS logs, CTD outputs, satellite imagery, and potentially raw fisheries logbook data.
* **Processed Data:** Scripts will generate cleaned and transformed data, including processed echograms with classified anchovy schools, acoustic biomass estimates, and integrated environmental datasets, into the `data/processed/` directory.

**Expected Data Examples:**
* `data/raw/ctd_sensor_data_2022.csv`
* `data/processed/glider_echogram_anchovy_classified_001.csv`

*(**Note:** This project is adapted to the format and methodology applied within the context of JUEVNA 2022. More recent studies may require tweaking some scripts or some may not be relevant anymore.)*

## 5. Installation
To set up the development environment and run the project scripts:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/GAFievet/JUVENA_2022_WIP](https://github.com/GAFievet/JUVENA_2022_WIP)
    cd JUVENA_2022
    ```

2.  **Create and activate a Conda environment (highly recommended):**
    If you have Conda installed (Anaconda or Miniconda), you can create a dedicated environment:
    ```bash
    conda create -n juvena_env python=3.9  # You can specify your preferred Python version here
    conda activate juvena_env
    ```
    *(Alternatively, if you prefer `venv`, you can use: `python3 -m venv venv` followed by `source venv/bin/activate` on Linux/macOS or `venv\Scripts\activate` on Windows.)*


3.  **Install dependencies:**
    Once your Conda environment is active, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration (if necessary):**
    Review and adjust paths and parameters in `src/config.py`, especially those related to echosounder specifications, anchovy-specific acoustic thresholds, and data locations, according to your local environment.
## 6. Usage
The primary use case involves processing and analyzing **glider echosounding data for pelagic fish distribution**, with other modules serving to complement and provide context for this analysis within the southeast Bay of Biscay.

**Example: Core Glider Acoustic Data Processing & Anchovy Mapping**
```bash
python src/core/sampling_effort.py
python src/core/summarizing_anchovy_detection.py
python src/core/glider_survey_profile.py
```

## 7. Results & Visualizations
Processing results and generated visualizations are saved in the `plots/` directory.
* Figures will typically be in `.png` format.
* Intermediate or final processed data, including processed echograms with classified anchovy schools and acoustic biomass estimates, are saved in the `data/processed/` directory.


## 8. Testing
The project uses `pytest` for unit and integration testing. These tests ensure the robustness and accuracy of our data processing pipelines, particularly for critical glider echosounding routines and anchovy detection algorithms.
To run the test suite:

1.  Ensure `pytest` is installed (it should be included in `requirements.txt`).
2.  From the project root directory, execute:
    ```bash
    pytest
    ```

## 9. Contribution
Contributions are welcome, especially those enhancing the glider echosounding processing capabilities, improving anchovy detection algorithms, or integrating new complementary datasets relevant to the southeast Bay of Biscay ecosystem. If you'd like to contribute to this project, please follow these steps:
1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/ImprovedAnchovyDetection`).
3.  Commit your changes (`git commit -m 'Description of your implementation'`).
4.  Push to the branch (`git push origin feature/implementation`).
5.  Open a Pull Request.

Please ensure your contributions adhere to the existing code style and include appropriate tests.

## 10. License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## 11. Contact
Guy-Aurèle Fiévet - [guy.aurele@gmail.com](mailto:your.email@example.com) - [LinkedIn](https://www.linkedin.com/in/guyaurele/)

---
*This project, initiated in 2024, is a key component of both JUVENA activities and my Master's Thesis, primarily focusing on advancing glider-based acoustic research for European juvenile anchovy in the southeast Bay of Biscay.*