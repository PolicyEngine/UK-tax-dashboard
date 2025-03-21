import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from policyengine import Simulation

st.title("UK Taxes")

# Initialize the simulation
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
    period=2025,
)

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
    title="Tax band distribution by country (Percentage)",
    labels={
        "country": "Country", 
        "percentage": "Percentage", 
        "tax_band": "Tax band"
    },
    height=600
)

# Update layout to show percentages
fig.update_layout(
    yaxis_title="Percentage (%)",
    yaxis=dict(ticksuffix="%"),
    bargap=0.2
)

st.plotly_chart(fig)

