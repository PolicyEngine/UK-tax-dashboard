import numpy as np
import pandas as pd
import streamlit as st

# Define a consistent color scheme for all plots
COLOR_SCHEME = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'tertiary': '#2ca02c',
    'quaternary': '#d62728',
    'quinary': '#9467bd',
    'senary': '#8c564b',
    'septenary': '#e377c2',
    'octonary': '#7f7f7f',
    'nonary': '#bcbd22',
    'denary': '#17becf'
}

# Define consistent layout settings
PLOT_LAYOUT = {
    'template': 'plotly_white',
    'height': 500,
    'margin': {'l': 50, 'r': 50, 't': 50, 'b': 100},
    'legend': {
        'orientation': 'h',
        'yanchor': 'top',
        'y': -0.25,
        'xanchor': 'center',
        'x': 0.5
    },
    'title': "",
}

# Function to compute Gini coefficient
def gini(array):
    """
    Calculate the Gini coefficient from an array of values.
    
    A Gini coefficient of 0 represents perfect equality, while 1 represents perfect inequality.
    
    Parameters:
    -----------
    array : np.array
        Array of values (e.g., income, tax rates, etc.)
        
    Returns:
    --------
    float
        Gini coefficient between 0 and 1
    """
    if len(array) <= 0:
        return 0
    
    # Remove NaN values
    array = np.array(array)
    array = array[~np.isnan(array)]
    
    if len(array) <= 0:
        return 0
    
    array = np.sort(array)  # Sort values
    index = np.arange(1, array.shape[0] + 1)  # Rank index
    return (np.sum((2 * index - array.shape[0] - 1) * array)) / (array.shape[0] * np.sum(array))

# Function to create income deciles/percentiles
def create_income_groups(df, column="household_market_income", groups=10, labels=None):
    """
    Create income groups (deciles, quintiles, etc.) based on a specified column.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the income data
    column : str
        Column name to use for grouping
    groups : int
        Number of groups to create (e.g., 10 for deciles, 5 for quintiles)
    labels : list, optional
        Custom labels for the groups. If None, will use D1, D2, etc. for deciles
        
    Returns:
    --------
    pd.DataFrame
        Original DataFrame with a new column '{column}_group' added
    """
    df_copy = df.copy()
    
    if labels is None:
        # Default labels (e.g., D1, D2, D3, etc. for deciles)
        labels = [f"D{i}" for i in range(1, groups + 1)]
    
    # Create the groups
    df_copy[f"{column}_group"] = pd.qcut(
        df_copy[column], 
        groups, 
        labels=labels,
        duplicates='drop'
    )
    
    return df_copy

# Function to display custom CSS
def load_css():
    """
    Load custom CSS styles from assets/styles.css
    """
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # No CSS file found, continue without custom styling