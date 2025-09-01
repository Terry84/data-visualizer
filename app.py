import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_source import DataSourceManager
from utils.visualization_helpers import create_hunger_overview_chart, create_malnutrition_chart
import os

# Configure page
st.set_page_config(
    page_title="SDG Goal 2: Zero Hunger Data Tool",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Main page header
st.title("🌾 SDG Goal 2: Zero Hunger Data Visualization Tool")
st.markdown("""
### Analyze and visualize global hunger and nutrition data for creative storytelling

This tool helps creatives analyze and create shareable visualizations focused on SDG Goal 2 indicators:
- **Hunger rates** and food insecurity trends
- **Child malnutrition** statistics (stunting, wasting, overweight)
- **Agricultural productivity** and sustainability metrics
- **Food security** across different regions and demographics
""")

# Key metrics overview
st.header("📊 Global Overview (2024-2025)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="People Facing Hunger",
        value="713-757M",
        delta="-2.1% from 2022",
        help="9.1% of global population faced hunger in 2023"
    )

with col2:
    st.metric(
        label="Food Insecure Population",
        value="2.33B",
        delta="Almost 3 in 10 people",
        help="Moderate or severe food insecurity in 2023"
    )

with col3:
    st.metric(
        label="Stunted Children",
        value="150.2M",
        delta="23.2% of under-5s",
        help="Children under 5 with stunting in 2024"
    )

with col4:
    st.metric(
        label="Exclusively Breastfed",
        value="47.8%",
        delta="+3.2% improvement",
        help="Infants under 6 months exclusively breastfed in 2023"
    )

# Quick visualization section
st.header("🎯 Key Indicators Snapshot")

# Load sample data for visualization
@st.cache_data
def load_sample_hunger_data():
    """Load sample hunger data for demonstration"""
    regions = ['Sub-Saharan Africa', 'Southern Asia', 'Western Asia', 'Latin America & Caribbean', 
               'Eastern Asia', 'Northern Africa', 'Oceania', 'Europe & Northern America']
    hunger_rates = [22.5, 13.1, 12.2, 6.5, 1.7, 7.8, 5.8, 2.4]
    food_insecurity = [67.2, 27.4, 31.2, 37.5, 11.8, 24.1, 15.2, 8.1]
    
    return pd.DataFrame({
        'Region': regions,
        'Hunger Rate (%)': hunger_rates,
        'Food Insecurity (%)': food_insecurity
    })

# Create visualizations
sample_data = load_sample_hunger_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Hunger Rates by Region")
    fig_hunger = px.bar(
        sample_data, 
        x='Region', 
        y='Hunger Rate (%)',
        color='Hunger Rate (%)',
        color_continuous_scale='Reds',
        title="Prevalence of Undernourishment by Region (2023)"
    )
    fig_hunger.update_xaxis(tickangle=45)
    st.plotly_chart(fig_hunger, use_container_width=True)

with col2:
    st.subheader("Food Insecurity Overview")
    fig_insecurity = px.scatter(
        sample_data,
        x='Hunger Rate (%)',
        y='Food Insecurity (%)',
        size='Food Insecurity (%)',
        color='Region',
        title="Hunger vs Food Insecurity by Region",
        hover_data=['Region']
    )
    st.plotly_chart(fig_insecurity, use_container_width=True)

# Progress tracking section
st.header("📈 Progress Toward SDG Goal 2")

progress_col1, progress_col2 = st.columns(2)

with progress_col1:
    st.subheader("2030 Target Progress")
    
    # Progress bars for key targets
    st.write("**Target 2.1: End Hunger**")
    hunger_progress = (100 - 9.1) / 100  # 9.1% still facing hunger
    st.progress(hunger_progress)
    st.caption(f"Current: 9.1% facing hunger | Target: 0% by 2030")
    
    st.write("**Target 2.2: End Child Stunting**")
    stunting_progress = (100 - 23.2) / 100  # 23.2% children stunted
    st.progress(stunting_progress)
    st.caption(f"Current: 23.2% children stunted | Target: Significant reduction by 2030")

with progress_col2:
    st.subheader("Regional Challenges")
    st.info("""
    **Key Insights:**
    - Sub-Saharan Africa remains most affected (22.5% hunger rate)
    - 670 million people projected to still face hunger by 2030
    - Child stunting affects 1 in 4 children globally
    - Food insecurity increased during COVID-19 pandemic
    """)

# Data sources information
st.header("📚 Data Sources & Methodology")

with st.expander("Primary Data Sources"):
    st.markdown("""
    **UN Agencies & Partners:**
    - **FAO (Food and Agriculture Organization)**: Hunger and food security indicators
    - **UNICEF**: Child malnutrition data and surveys
    - **WHO (World Health Organization)**: Health and nutrition standards
    - **World Bank**: Economic indicators and Living Standards Surveys
    
    **Key Data Collections:**
    - Joint Child Malnutrition Estimates (JME) - Updated biennially
    - State of Food Security and Nutrition (SOFI) - Annual reports
    - FAO SDG Data Portal - 22 indicators under FAO custodianship
    - Multiple Indicator Cluster Surveys (MICS)
    - Demographic Health Surveys (DHS)
    """)

# Getting started guide
st.header("🚀 Getting Started")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📤 Upload Data", "🎨 Templates", "📁 Export & Share"])

with tab1:
    st.markdown("""
    **Interactive Dashboard**
    - Explore pre-loaded SDG 2 datasets
    - Filter by region, time period, and indicators
    - Create custom visualizations with drag-and-drop interface
    - Real-time data updates from UN sources
    """)

with tab2:
    st.markdown("""
    **Data Upload & Import**
    - Upload CSV, Excel, or JSON files
    - Connect to FAO, UNICEF, WHO, and World Bank APIs
    - Validate data against SDG 2 standards
    - Merge with existing datasets
    """)

with tab3:
    st.markdown("""
    **Visualization Templates**
    - Pre-designed charts for common SDG 2 indicators
    - Customizable color schemes and themes
    - Mobile-responsive designs
    - Infographic-style templates for social media
    """)

with tab4:
    st.markdown("""
    **Export & Sharing**
    - High-quality PNG, SVG, and PDF exports
    - Interactive HTML visualizations
    - Social media optimized formats
    - Collaborative sharing links
    """)

# Footer
st.markdown("---")
st.markdown("""
**About SDG Goal 2: Zero Hunger**
The second Sustainable Development Goal aims to end hunger, achieve food security and improved nutrition, 
and promote sustainable agriculture by 2030. This tool provides creatives with the data and visualization 
capabilities to tell compelling stories about global food security challenges and progress.

*Data sources: FAO, UNICEF, WHO, World Bank | Last updated: September 2025*
""")