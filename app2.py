import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from utils import COLOR_SCHEME, PLOT_LAYOUT
from data_loader import load_country_tax_band_data

# Set up page configuration
st.set_page_config(
    page_title="UK Tax Band Distribution",
    page_icon="📊",
    layout="wide"
)

st.title("UK Tax Band Distribution")

# Load tax band data
df = load_country_tax_band_data()

# Group by country and tax band, summing person counts
tax_distribution = df.groupby(["country", "tax_band"], as_index=False)["person_id"].count()

# Create a pivot table to calculate percentages within each country
pivot = tax_distribution.pivot_table(
    index="country", 
    columns="tax_band", 
    values="person_id", 
    aggfunc="sum"
).fillna(0)

# Calculate percentages for each country
percentages = pivot.div(pivot.sum(axis=1), axis=0) * 100
percentages = percentages.reset_index().melt(
    id_vars="country", 
    var_name="tax_band", 
    value_name="percentage"
)

st.write("This chart compares tax band distribution across the different countries of the UK.")
st.write("It shows the proportion of taxpayers in each tax band for England, Scotland, Wales, and Northern Ireland.")

# Plot as 100% stacked bar chart
fig = px.bar(
    percentages,
    x="country",
    y="percentage",
    color="tax_band",
    labels={
        "country": "Country", 
        "percentage": "Percentage", 
        "tax_band": "Tax band"
    },
    height=600
)

# Update layout to show percentages
layout = PLOT_LAYOUT.copy()
layout.update({
    'yaxis_title': "Percentage (%)",
    'title': "",
    'yaxis': {'ticksuffix': "%"},
    'bargap': 0.2
})
fig.update_layout(**layout)

st.plotly_chart(fig, use_container_width=True)

# Add footer with attribution
st.markdown("---")
st.markdown(
    """<div style="text-align: center; color: gray; font-size: 0.8em;">
    Built with <a href="https://policyengine.org" target="_blank">PolicyEngine</a> | 
    Data source: FRS 2022-23 | 
    Dashboard created by Janan Sadeqian
    </div>""", 
    unsafe_allow_html=True
)