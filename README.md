# OnboardingFlow

**OnboardingFlow** is an end-to-end data engineering and visualization project designed to analyze how new contributors join and progress through *any mailing list*. By processing over 20 years of mailing list archives (2004–2024), this project identifies key milestones, bottlenecks, and retention patterns in the open-source onboarding process.

## 🚀 Overview

The project transforms raw `lore.kernel.org` archives into actionable insights through a multi-stage pipeline:

1. **ETL Pipeline**: Built with **Apache Spark**, it processes the LKML5Ws dataset to reconstruct conversation threads and track individual contributor lifecycles.

2. **Metric Computation**: Calculates critical KPIs such as Mean Time to First Patch (MTTFP), Review Conversion Rates, and Cohort Retention.

3. **Interactive Dashboard**: A **Streamlit** application providing interactive visualizations (Sankey diagrams, heatmaps, and trend lines).

## 📊 Data & Configurability

### Dataset

The primary dataset used in this project is publicly available on Zenodo:

[👉 LKML5Ws Dataset on Zenodo](https://zenodo.org/records/17567225?preview=1&token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjRiN2Q4ZjM4LTI3YjktNGI0MS05ZDI5LTU3YTllNTk1OTRhYSIsImRhdGEiOnt9LCJyYW5kb20iOiI4MDEyM2ZiMWQ4M2Y3OTI0ZmU4YzU1N2UyNGNlOTcwNyJ9.OoLyFXTzTZwWJd9z_g3WxHkzzEGSBhORhDjkiOS0pTRDH0gW-cBrmMg0YbHIRQlBddigA-mSXm9dCf0ODr-GQw)

### Multi-List Support

While the initial focus was the `netdev` list, OnboardingFlow is designed to be mailing-list agnostic. You can analyze **any mailing list** provided in the dataset.

- To switch the analyzed list, simply modify the input settings in the `input.json` file.

## 🛠️ Tech Stack

- **Data Processing**: Apache Spark (PySpark), DuckDB
- **Dashboard**: Streamlit, Plotly
- **Data Source**: LKML5Ws (Linux Kernel Mailing List dataset)
- **Environment**: Python 3.13

## 📂 Project Structure

```
.
├── lkml_onboarding_funnel.ipynb     # Spark ETL - Jupiter Notebook
├── input.json                       # Configuration file 
├── requirements.txt                 # Requirements for Jupiter Notebook 
├── dashboard/
│   ├── app.py                       # Streamlit app
│   └── requirements.txt             # Requirements for streamlit app
└── README.md
```

## 🚦 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/lauraarakakii/onboarding-flow.git
cd onboarding-flow
```

2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the Jupiter Notebook
5. Run the dashboard requirements

```bash
cd dashboard
pip install -r requirements.txt
```

6. Run the dashboard
```bash
streamlit run app.py
```

## 🔗 Related Links

- **Blog Post - ETL & Logic:** [OnboardingFlow - Journal](https://lauraarakakii.github.io/posts/manuscript/)
- **Blog Post - Results:** [Visualization & Insights](https://lauraarakakii.github.io/posts/manuscript-results/)
- **Dashboard Netdev sample**: [Streamlit Dashboard](https://dashflow.streamlit.app/)