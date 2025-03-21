# UK Tax Dashboard

A Streamlit dashboard for exploring UK tax data using PolicyEngine simulations.

## Overview

This dashboard visualizes various aspects of the UK tax system, including:
- Effective tax rates across income levels
- Tax composition by income decile
- Council tax burden
- Tax credits distribution
- Business rates distribution
- Tax inequality (Gini coefficient)
- Tax band distribution by country

## Setup

### Prerequisites
- Python 3.8+
- PolicyEngine UK
- Streamlit

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/policyengine/uk-tax-dashboard.git
   cd uk-tax-dashboard
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the dashboard:
```
streamlit run app.py
```

Navigate to http://localhost:8501 in your web browser to view the dashboard.

## Dashboard Features

The dashboard provides multiple views accessible from the sidebar:

1. **Introduction**: Overview of UK tax terminology and concepts
2. **Effective tax rate**: Visualizations of tax burdens by income
3. **Tax composition**: Breakdown of tax types across income groups
4. **Council tax burden**: Analysis of council tax as a percentage of income
5. **Tax credits distribution**: Distribution of tax credits across income deciles
6. **Business rates distribution**: Relationship between business taxes and household taxes
7. **Tax Gini coefficient**: Inequality measures for tax burden
8. **Tax bands**: Distribution of tax bands across UK countries

## License

[Insert license information here]

## Acknowledgements

Built with [PolicyEngine](https://policyengine.org), an open-source tax and benefit microsimulation model.