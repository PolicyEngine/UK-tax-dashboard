from policyengine_uk import Microsimulation
from policyengine import Simulation
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_baseline_data(period=2025):
    """
    Load baseline microsimulation data from PolicyEngine UK.
    
    Parameters:
    -----------
    period : int
        The tax year to simulate (e.g., 2025 for 2025-26 tax year)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing household tax and income data
    """
    # Initialize the microsimulation
    baseline = Microsimulation(dataset="hf://policyengine/policyengine-uk-data/enhanced_frs_2022_23.h5")
    
    # Calculate required variables
    df = baseline.calculate_dataframe(
        [
            "household_id",
            "household_weight",
            "household_tax",
            "household_market_income",
            "consumption",
            "earned_income_tax",
            "savings_income_tax",
            "dividend_income_tax",
            "capital_gains_tax",
            "council_tax",
            "working_tax_credit",
            "child_tax_credit",
            "tax_free_childcare",
            "taxed_savings_income",
            "taxed_income",
            "business_rates",
            "marginal_tax_rate",
        ],
        period=period,
    )
    
    # Calculate effective tax rate
    df["etr"] = df.household_tax / df.household_market_income
    
    # Filter out extreme values for better visualization
    df = df[
        df.household_market_income.between(0, 200_000)
        & df.etr.between(0, 1)
    ]
    
    # Calculate derived fields
    df["direct_taxes"] = df.earned_income_tax + df.savings_income_tax + df.dividend_income_tax + df.capital_gains_tax
    df["indirect_taxes"] = df.household_tax - df.direct_taxes  
    df["direct_tax_share"] = df["direct_taxes"] / df["household_tax"]
    df["indirect_tax_share"] = df["indirect_taxes"] / df["household_tax"]
    df["earned_income_tax_share"] = df["earned_income_tax"] / df["household_tax"]
    df["savings_income_tax_share"] = df["savings_income_tax"] / df["household_tax"]
    df["dividend_income_tax_share"] = df["dividend_income_tax"] / df["household_tax"]
    df["capital_gains_tax_share"] = df["capital_gains_tax"] / df["household_tax"]
    df["other_taxes_share"] = (df["household_tax"] - df["earned_income_tax"] - df["savings_income_tax"] - 
                              df["dividend_income_tax"] - df["capital_gains_tax"]) / df["household_tax"]
    df["council_tax_burden"] = df.council_tax / df.household_market_income
    df["total_tax_credits"] = df.working_tax_credit + df.child_tax_credit + df.tax_free_childcare
    df["business_tax_ratio"] = df.business_rates / df.household_tax
    df["other_taxes"] = df["household_tax"] - df["earned_income_tax"] - df["savings_income_tax"] - \
                        df["dividend_income_tax"] - df["capital_gains_tax"]
    
    return df

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_country_tax_band_data(period=2025):
    """
    Load tax band distribution data across UK countries.
    
    Parameters:
    -----------
    period : int
        The tax year to simulate (e.g., 2025 for 2025-26 tax year)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing tax band distribution by country
    """
    # Initialize the macro simulation
    sim = Simulation({
        "country": "uk",
        "scope": "macro",
    })

    # Extract data
    df = sim.baseline_simulation.calculate_dataframe(
        [
            "person_id",
            "household_weight",
            "household_tax",
            "household_market_income",
            "tax_band",
            "country",
        ],
        period=period,
    )
    
    return df