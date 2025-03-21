import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
from policyengine import Simulation
from policyengine_uk import Microsimulation
import plotly.express as px

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

st.set_page_config(layout="wide")


# Create a sidebar with tabs
st.sidebar.title("UK tax dashboard")
# st.sidebar.markdown("Select a view to explore UK tax data:")

# Define tab options
tabs = [
    "Introduction",
    "Effective tax rate",
    "Tax composition",
    "Council tax burden",
    "Tax credits distribution",
    "Business rates distribution",
    "Tax gini coefficient",
    "Tax bands"
]

# Create the tab selection
selected_tab = st.sidebar.radio("", tabs)

# Load and prepare data
baseline = Microsimulation(dataset="hf://policyengine/policyengine-uk-data/enhanced_frs_2022_23.h5")

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
    period=2025,
)
df["etr"] = df.household_tax / df.household_market_income

df = df[
    df.household_market_income.between(0, 200_000)
    & df.etr.between(0, 1)
]

df.sample(100, weights=df.household_weight)

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

# Function to compute Gini coefficient
def gini(array):
    array = np.sort(array)  # Sort values
    index = np.arange(1, array.shape[0] + 1)  # Rank index
    return (np.sum((2 * index - array.shape[0] - 1) * array)) / (array.shape[0] * np.sum(array))

# Display the selected tab content
if selected_tab == "Introduction":
    st.header("UK tax system")
    
    st.subheader("Taxes")
    st.markdown("""
    - **Household tax**: Household tax refers to the various taxes applied collectively to a family unit rather than individuals in the UK tax system.
    - **Council tax**: Council tax is a local tax set by councils to fund essential services such as waste collection, street lighting, and local facilities.
    - **Wealth tax**: Wealth tax is a theoretical tax not currently implemented in the UK that would apply to the total value of an individual's assets rather than just their income.
    - **Income tax**: Income tax is the main tax on personal earnings in the UK, applied progressively across different tax bands on wages, pensions, and other forms of income.
    - **Earned income tax**: Earned income tax applies specifically to money received through employment, self-employment, or pension payments in the UK tax system.
    - **Savings income tax**: Savings income tax is levied on interest earned from bank accounts and other savings vehicles once it exceeds the Personal Savings Allowance.
    - **Dividend income tax**: Dividend income tax is charged on payments received from company shares at special rates that differ from standard income tax rates.
    - **Capital gains tax**: Capital gains tax is paid on the profit made when you sell or dispose of an asset that has increased in value since you acquired it.
    """)
    
    st.subheader("Incomes")
    st.markdown("""
    - **Total income**: Total income encompasses all money received from every source before any deductions or allowances are applied.
    - **Taxed income**: Taxed income is the portion of your earnings that remains subject to taxation after accounting for all applicable allowances and reliefs.
    - **Earned taxable income**: Earned taxable income refers to employment or self-employment income that exceeds the personal allowance threshold and therefore becomes subject to income tax.
    - **Taxed savings income**: Taxed savings income consists of interest earnings that exceed the Personal Savings Allowance and consequently become liable for taxation.
    - **Taxed dividend income**: Taxed dividend income represents dividend payments that surpass the Dividend Allowance and therefore become subject to the dividend tax rates.
    - **Household market income**: Household market income comprises the combined pre-tax earnings from all sources for all members of a single household.
    """)
    
    st.subheader("Tax Credits")
    st.markdown("""
    - **Working tax credit**: Working tax credit is a government benefit designed to supplement the income of working people on lower wages, currently being phased out in favor of Universal Credit.
    - **Child tax credit**: Child tax credit is a means-tested benefit provided to help families with the costs of raising children, also being gradually replaced by Universal Credit.
    - **Tax-free childcare**: Tax-free childcare is a government scheme that provides working parents with up to £2,000 per child per year to help with registered childcare costs.
    """)
    
    st.subheader("Rates and Bands")
    st.markdown("""
    - **Marginal tax rate**: Marginal tax rate refers to the percentage of tax applied to your income at the highest applicable tax band, affecting only the portion of income that falls within that band.
    - **Business rates**: Business rates are taxes levied on non-domestic properties such as shops, offices, and factories based on their estimated rental value.
    - **Council tax band**: Council tax band is the property classification (ranging from A to H in England) that determines how much council tax is payable, based on the property's value.
    - **Tax band**: Tax band refers to the income thresholds that determine which rate of income tax applies to different portions of your taxable income.
    """)

elif selected_tab == "Effective tax rate":
    st.header("Effective tax rate")
    
    # Create tabs within the main content area
    etr_tabs = st.tabs(["By household income", "By income decile"])
    
    with etr_tabs[0]:
        st.subheader("Effective tax rate by household market income")
        st.write("This plot shows how tax burden varies across different income levels. Each point represents a household, showing what percentage of income is paid in taxes.")
        
        fig = px.scatter(
            df,
            x="household_market_income",
            y="etr",
            opacity=0.02,
            color_discrete_sequence=[COLOR_SCHEME['primary']],
            labels={
                "household_market_income": "Household market income (£)",
                "etr": "Effective tax rate" 
            }
        )
        
        # Apply consistent layout
        fig.update_layout(**PLOT_LAYOUT)
        
        st.plotly_chart(fig, use_container_width=True)

    with etr_tabs[1]:
        st.subheader("Effective tax rate by income decile")
        st.write("This visualization shows the distribution of tax rates within each income group. Box plots display the median, quartiles and variability of tax rates across income levels.")
        
        df_copy = df.copy()
        df_copy["income_decile"] = pd.qcut(df_copy.household_market_income, q=10, labels=range(1, 11))
        
        fig = px.box(
            df_copy,
            x="income_decile",
            y="etr",
            color_discrete_sequence=[COLOR_SCHEME['primary']],
            labels={
                "income_decile": "Income decile",
                "etr": "Effective tax rate"
            }
        )
        
        # Apply consistent layout
        fig.update_layout(**PLOT_LAYOUT)
        
        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Tax composition":
    st.header("Tax composition by income decile")
    
    # Create tabs within the main content area
    tax_comp_tabs = st.tabs(["Proportion of total tax", "Average tax amounts"])
    
    # Create income groups (deciles) - used by both tabs
    df['income_group'] = pd.qcut(
        df['household_market_income'], 
        10,
        labels=['P10', 'P20', 'P30', 'P40', 'P50', 'P60', 'P70', 'P80', 'P90', 'P100'],
        duplicates='drop'
    )
    
    with tax_comp_tabs[0]:
        st.subheader("Tax composition proportions by income decile")
        st.write("This chart shows how different tax types contribute to overall taxation across income groups. Higher income households tend to pay more through earned income tax and capital gains tax.")
        
        # Group by income group and calculate average tax shares
        tax_shares = [
            'earned_income_tax_share', 
            'savings_income_tax_share', 
            'dividend_income_tax_share', 
            'capital_gains_tax_share', 
            'other_taxes_share'
        ]
        
        grouped = df.groupby('income_group')[tax_shares].mean().reset_index()
        
        # Reshape data for stacked bar chart
        plot_data = pd.melt(
            grouped, 
            id_vars=['income_group'], 
            value_vars=tax_shares,
            var_name='tax_component', 
            value_name='proportion'
        )
        
        # Clean up labels for display
        plot_data['tax_component'] = plot_data['tax_component'].str.replace('_share', '').str.replace('_', ' ').str.capitalize()
        
        # Create the stacked bar chart
        fig = px.bar(
            plot_data,
            x='income_group',
            y='proportion',
            color='tax_component',
            labels={
                'income_group': 'Income group (P10=Poorest, P100=Richest)',
                'proportion': 'Proportion of total tax',
                'tax_component': 'Tax component'
            },
            color_discrete_map={
                'Earned income tax': COLOR_SCHEME['primary'],
                'Savings income tax': COLOR_SCHEME['secondary'],
                'Dividend income tax': COLOR_SCHEME['tertiary'],
                'Capital gains tax': COLOR_SCHEME['quaternary'],
                'Other taxes share': COLOR_SCHEME['quinary']
            },
            barmode='stack'
        )
        
        # Apply consistent layout with specific y-axis settings
        layout = PLOT_LAYOUT.copy()
        layout.update({
            'yaxis': {
                'tickformat': '.0%',  # Format as percentage
                'range': [0, 1]  # Ensure y-axis goes from 0 to 100%
            }
        })
        fig.update_layout(**layout)
        
        st.plotly_chart(fig, use_container_width=True)

    with tax_comp_tabs[1]:
        st.subheader("Average tax paid per household by income decile")
        st.write("This chart shows the monetary amount of different taxes paid across income groups. The highest income group pays substantially more tax than lower income groups.")
        
        # Define tax components
        tax_components = [
            'earned_income_tax', 
            'savings_income_tax', 
            'dividend_income_tax', 
            'capital_gains_tax',
            'other_taxes'
        ]
        
        # Group by income group and calculate MEAN tax per household (not sum)
        grouped = df.groupby('income_group')[tax_components].mean().reset_index()
        
        # Reshape data for stacked bar chart
        plot_data = pd.melt(
            grouped, 
            id_vars=['income_group'], 
            value_vars=tax_components,
            var_name='tax_component', 
            value_name='tax_amount'
        )
        
        # Clean up labels for display
        plot_data['tax_component'] = plot_data['tax_component'].str.replace('_', ' ').str.capitalize()
        
        # Create the stacked bar chart
        fig = px.bar(
            plot_data,
            x='income_group',
            y='tax_amount',
            color='tax_component',
            labels={
                'income_group': 'Income group (P10=Poorest, P100=Richest)',
                'tax_amount': 'Average tax per household (£)',
                'tax_component': 'Tax component'
            },
            color_discrete_map={
                'Earned income tax': COLOR_SCHEME['primary'],
                'Savings income tax': COLOR_SCHEME['secondary'],
                'Dividend income tax': COLOR_SCHEME['tertiary'],
                'Capital gains tax': COLOR_SCHEME['quaternary'],
                'Other taxes': COLOR_SCHEME['quinary']
            },
            barmode='stack'
        )
        
        # Apply consistent layout with specific y-axis settings
        layout = PLOT_LAYOUT.copy()
        layout.update({
            'yaxis': {
                'tickformat': ',.0f',  # Add commas for thousands
            }
        })
        fig.update_layout(**layout)
        
        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Council tax burden":
    st.header("Council tax burden vs household income")
    st.write("This visualization shows how council tax impacts households at different income levels. Lower income households face a relatively higher council tax burden as a percentage of income.")
    
    fig = px.scatter(
        df,
        x="household_market_income",
        y="council_tax_burden",
        opacity=0.02,
        color_discrete_sequence=[COLOR_SCHEME['primary']],
        labels={
            "household_market_income": "Household market income (£)",
            "council_tax_burden": "Council tax as percentage of income"
        }
    )
    
    # Apply consistent layout
    fig.update_layout(**PLOT_LAYOUT)
    
    st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Tax credits distribution":
    st.header("Distribution of tax credits by income decile")
    st.write("This chart shows how tax credits are distributed across different income groups. Lower income households typically receive more tax credits as a form of income support.")
    
    # Create income deciles
    df['income_decile'] = pd.qcut(
        df['household_market_income'], 
        10, 
        labels=['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
        duplicates='drop'
    )
    
    # Create box plot without individual points, showing standard deviation and mean
    fig = px.box(
        df,
        x="income_decile",
        y="total_tax_credits",
        labels={
            'income_decile': 'Income decile (D1=Poorest, D10=Richest)',
            'total_tax_credits': 'Total tax credits (£)'
        },
        points=False,  # Hide individual data points
        boxmode='overlay',  # Keep standard deviation representation
        color_discrete_sequence=[COLOR_SCHEME['tertiary']]
    )
    
    # Show mean inside the box
    fig.update_traces(boxmean=True)  
    
    # Apply consistent layout with specific y-axis settings
    layout = PLOT_LAYOUT.copy()
    layout.update({
        'yaxis': {
            'tickformat': ',.0f',  # Add commas for thousands
        }
    })
    fig.update_layout(**layout)
    
    st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Business rates distribution":
    st.header("Distribution of business rates vs household taxes")
    st.write("This distribution shows the relationship between business taxes and total household taxes. The curve illustrates how business rates make up varying proportions of total tax burden.")
    
    # First, clean the data by removing NaN and inf values
    x = df["business_tax_ratio"]
    x_clean = x[~np.isnan(x) & ~np.isinf(x)]
    
    # Create the distribution plot with clean data
    hist_data = [x_clean]
    group_labels = ['Business tax ratio']
    
    fig = ff.create_distplot(
        hist_data, 
        group_labels,
        bin_size=(x_clean.max() - x_clean.min()) / 30,
        histnorm='probability', 
        show_rug=False,
        colors=[COLOR_SCHEME['quaternary']]
    )
    
    # Apply consistent layout
    layout = PLOT_LAYOUT.copy()
    layout.update({
        'xaxis_title': "Business tax ratio",
        'yaxis_title': "Density"
    })
    fig.update_layout(**layout)
    
    st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Tax gini coefficient":
    st.header("Tax gini coefficient by income decile")
    st.write("This chart shows tax inequality within different income groups using the Gini coefficient. Higher values indicate greater inequality in tax burden across households in the same income group.")
    
    # Compute overall Tax Gini Coefficient
    tax_gini = gini(df.etr)
    st.metric("Overall Tax Gini Coefficient", f"{tax_gini:.3f}")
    
    # Work on a copy to preserve df
    df_copy = df[df.etr.notna()].copy()
    
    # Assign income deciles
    df_copy["income_decile"] = pd.qcut(df_copy.household_market_income, q=10, labels=range(1, 11))
    
    # Compute Gini coefficient within each decile
    gini_by_decile = df_copy.groupby("income_decile")["etr"].apply(gini).reset_index()
    gini_by_decile.columns = ["income_decile", "tax_gini"]
    
    # Plot Tax Gini across income deciles
    fig = px.line(
        gini_by_decile,
        x="income_decile",
        y="tax_gini",
        markers=True,
        labels={"income_decile": "Income decile", "tax_gini": "Gini coefficient"},
        color_discrete_sequence=[COLOR_SCHEME['primary']]
    )
    
    # Apply consistent layout
    fig.update_layout(**PLOT_LAYOUT)
    
    st.plotly_chart(fig, use_container_width=True)
    
elif selected_tab == "Tax bands":
    st.header("Tax band distribution by country")
    st.write("This chart compares tax band distribution across the different countries of the UK. It shows the proportion of taxpayers in each tax band for England, Scotland, Wales, and Northern Ireland.")
    
    # Initialize the simulation
    sim = Simulation({
        "country": "uk",
        "scope": "macro",
    })

    # Extract data
    df_tax_distribution = sim.baseline_simulation.calculate_dataframe(
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
    tax_distribution = df_tax_distribution.groupby(["country", "tax_band"], as_index=False)["person_id"].count()

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