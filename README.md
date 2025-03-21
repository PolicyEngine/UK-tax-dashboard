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

Run the full dashboard:
```
streamlit run app.py
```

Run the simplified dashboard (tax bands only):
```
streamlit run app2.py
```

Or use the convenience script:
```
# For full dashboard
./run.sh

# For simplified dashboard
./run.sh simple
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

## Project Structure

```
uk-tax-dashboard/
├── app.py                # Main Streamlit app with full dashboard
├── app2.py               # Simplified Streamlit app (tax bands only)
├── utils.py              # Utility functions
├── data_loader.py        # Data loading functions
├── requirements.txt      # Project dependencies
├── run.sh                # Convenience script to run either dashboard
├── setup.sh              # Setup script for deployment
├── Procfile              # Heroku deployment configuration
├── assets/               # Static assets
│   └── styles.css        # Custom CSS styles
└── data/                 # Data directory (for custom data files)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Built with [PolicyEngine](https://policyengine.org), an open-source tax and benefit microsimulation model.