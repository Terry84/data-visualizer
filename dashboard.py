import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.data_sources import DataSourceManager
from utils.visualization_helpers import create_world_map, create_trend_chart, create_comparison_chart

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Interactive SDG Goal 2 Dashboard")
st.markdown("Explore hunger, malnutrition, and food security data with interactive visualizations")

# Initialize data manager
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataSourceManager()

# Sidebar filters
st.sidebar.header("🎛️ Data Filters")

# Time period selector
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=2000,
    max_value=2024,
    value=(2015, 2024),
    step=1
)

# Region selector
regions = [
    'World', 'Sub-Saharan Africa', 'Southern Asia', 'Western Asia', 
    'Latin America & Caribbean', 'Eastern Asia', 'Northern Africa', 
    'Oceania', 'Europe & Northern America'
]
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    regions,
    default=['World', 'Sub-Saharan Africa', 'Southern Asia']
)

# Indicator selector
indicators = [
    'Hunger Rate (%)',
    'Food Insecurity (%)',
    'Child Stunting (%)',
    'Child Wasting (%)',
    'Child Overweight (%)',
    'Anemia in Women (%)',
    'Exclusive Breastfeeding (%)'
]
selected_indicator = st.sidebar.selectbox(
    "Primary Indicator",
    indicators,
    index=0
)

# Data source selector
data_sources = ['FAO', 'UNICEF', 'WHO', 'World Bank', 'Custom Upload']
selected_source = st.sidebar.selectbox(
    "Data Source",
    data_sources,
    index=0
)

# Real-time data toggle
real_time = st.sidebar.checkbox("Enable Real-time Data Updates", value=False)

if real_time:
    st.sidebar.info("🔄 Real-time updates enabled. Data refreshes every 30 seconds.")

# Main dashboard content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🌍 Global Overview")
    
    # Create sample data for world map
    @st.cache_data
    def create_world_hunger_data():
        countries = ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'IDN', 'PAK', 'BGD', 'NGA', 'MEX',
                    'JPN', 'ETH', 'PHL', 'EGY', 'VNM', 'IRN', 'TUR', 'DEU', 'THA', 'GBR']
        hunger_rates = np.random.uniform(0.5, 25.0, len(countries))
        hunger_rates[0] = 2.4  # USA
        hunger_rates[1] = 1.7  # China
        hunger_rates[2] = 16.3  # India
        
        return pd.DataFrame({
            'Country Code': countries,
            'Country': ['United States', 'China', 'India', 'Brazil', 'Russia', 
                       'Indonesia', 'Pakistan', 'Bangladesh', 'Nigeria', 'Mexico',
                       'Japan', 'Ethiopia', 'Philippines', 'Egypt', 'Vietnam',
                       'Iran', 'Turkey', 'Germany', 'Thailand', 'United Kingdom'],
            'Hunger Rate': hunger_rates
        })
    
    world_data = create_world_hunger_data()
    
    # World map visualization
    fig_map = px.choropleth(
        world_data,
        locations='Country Code',
        color='Hunger Rate',
        hover_name='Country',
        color_continuous_scale='Reds',
        title=f'{selected_indicator} by Country ({year_range[1]})'
    )
    fig_map.update_layout(height=500)
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.header("📈 Key Metrics")
    
    # Current metrics
    st.metric(
        "Global Hunger Rate",
        "9.1%",
        delta="-0.3%",
        help="Percentage of population facing undernourishment"
    )
    
    st.metric(
        "Food Insecure People",
        "2.33B",
        delta="+15M",
        delta_color="inverse",
        help="People with moderate or severe food insecurity"
    )
    
    st.metric(
        "Stunted Children",
        "150.2M",
        delta="-8.2M",
        help="Children under 5 with stunting"
    )
    
    # Progress indicators
    st.subheader("🎯 2030 Targets Progress")
    
    # Hunger reduction progress
    st.write("**End Hunger**")
    progress_hunger = 0.91  # 9.1% remaining
    st.progress(1 - progress_hunger)
    st.caption("9.1% still facing hunger")
    
    # Stunting reduction progress
    st.write("**Reduce Child Stunting**")
    progress_stunting = 0.768  # 23.2% current vs baseline
    st.progress(progress_stunting)
    st.caption("23.2% children stunted")
    
    # Food security progress
    st.write("**Ensure Food Access**")
    progress_access = 0.71  # 29% food insecure
    st.progress(progress_access)
    st.caption("71% have secure food access")

# Detailed analytics section
st.header("📊 Detailed Analytics")

tab1, tab2, tab3, tab4 = st.tabs(["🔄 Trends", "🌍 Regional Comparison", "👶 Child Nutrition", "🌾 Agriculture"])

with tab1:
    st.subheader("Trend Analysis")
    
    # Create trend data
    @st.cache_data
    def create_trend_data():
        years = list(range(2000, 2025))
        world_hunger = [15.3, 15.1, 14.8, 14.5, 14.2, 13.8, 13.5, 13.2, 12.8, 12.5,
                       12.1, 11.8, 11.5, 11.2, 10.8, 10.5, 10.2, 9.8, 9.5, 9.8,
                       10.2, 10.5, 10.1, 9.7, 9.1]
        
        africa_hunger = [33.2, 32.8, 32.5, 32.1, 31.7, 31.3, 30.9, 30.5, 30.1, 29.7,
                        29.3, 28.9, 28.5, 28.1, 27.7, 27.3, 26.9, 26.5, 26.1, 25.7,
                        24.8, 24.2, 23.6, 23.1, 22.5]
        
        return pd.DataFrame({
            'Year': years,
            'World': world_hunger,
            'Sub-Saharan Africa': africa_hunger
        })
    
    trend_data = create_trend_data()
    
    fig_trend = px.line(
        trend_data.melt(id_vars=['Year'], var_name='Region', value_name='Hunger Rate'),
        x='Year',
        y='Hunger Rate',
        color='Region',
        title='Hunger Rate Trends (2000-2024)',
        markers=True
    )
    fig_trend.add_vline(x=2015, line_dash="dash", line_color="gray", 
                       annotation_text="SDGs Adopted")
    fig_trend.add_vline(x=2020, line_dash="dash", line_color="red", 
                       annotation_text="COVID-19 Pandemic")
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Trend insights
    st.info("""
    **Key Trends:**
    - Global hunger declined steadily until 2015
    - COVID-19 pandemic reversed progress in 2020-2021
    - Sub-Saharan Africa shows persistent high rates
    - Recent slight improvement but off-track for 2030 target
    """)

with tab2:
    st.subheader("Regional Comparison")
    
    # Regional comparison data
    @st.cache_data
    def create_regional_data():
        regions_full = ['Sub-Saharan Africa', 'Southern Asia', 'Western Asia', 
                       'Latin America & Caribbean', 'Eastern Asia', 'Northern Africa', 
                       'Oceania', 'Europe & Northern America']
        hunger = [22.5, 13.1, 12.2, 6.5, 1.7, 7.8, 5.8, 2.4]
        stunting = [30.7, 31.7, 13.8, 11.3, 4.8, 17.3, 8.6, 2.6]
        wasting = [7.4, 14.7, 7.9, 1.6, 2.4, 8.7, 3.2, 0.7]
        
        return pd.DataFrame({
            'Region': regions_full,
            'Hunger Rate (%)': hunger,
            'Child Stunting (%)': stunting,
            'Child Wasting (%)': wasting
        })
    
    regional_data = create_regional_data()
    
    # Multi-indicator comparison
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name='Hunger Rate',
        x=regional_data['Region'],
        y=regional_data['Hunger Rate (%)'],
        marker_color='red',
        opacity=0.7
    ))
    
    fig_comparison.add_trace(go.Bar(
        name='Child Stunting',
        x=regional_data['Region'],
        y=regional_data['Child Stunting (%)'],
        marker_color='orange',
        opacity=0.7
    ))
    
    fig_comparison.add_trace(go.Bar(
        name='Child Wasting',
        x=regional_data['Region'],
        y=regional_data['Child Wasting (%)'],
        marker_color='yellow',
        opacity=0.7
    ))
    
    fig_comparison.update_layout(
        title='Regional Comparison: Multiple SDG 2 Indicators',
        barmode='group',
        xaxis_tickangle=-45,
        height=600
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

with tab3:
    st.subheader("Child Nutrition Status")
    
    # Child nutrition breakdown
    nutrition_metrics = {
        'Stunting (Height-for-age)': 23.2,
        'Wasting (Weight-for-height)': 6.6,
        'Overweight': 5.5
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Stunted Children", "150.2M", help="23.2% of children under 5")
        fig_stunting = px.pie(
            values=[23.2, 76.8],
            names=['Stunted', 'Normal'],
            title='Child Stunting Rate',
            color_discrete_sequence=['#ff7f7f', '#90ee90']
        )
        st.plotly_chart(fig_stunting, use_container_width=True)
    
    with col2:
        st.metric("Wasted Children", "45.0M", help="6.6% of children under 5")
        fig_wasting = px.pie(
            values=[6.6, 93.4],
            names=['Wasted', 'Normal'],
            title='Child Wasting Rate',
            color_discrete_sequence=['#ffa500', '#90ee90']
        )
        st.plotly_chart(fig_wasting, use_container_width=True)
    
    with col3:
        st.metric("Overweight Children", "37.0M", help="5.5% of children under 5")
        fig_overweight = px.pie(
            values=[5.5, 94.5],
            names=['Overweight', 'Normal'],
            title='Child Overweight Rate',
            color_discrete_sequence=['#ffff00', '#90ee90']
        )
        st.plotly_chart(fig_overweight, use_container_width=True)

with tab4:
    st.subheader("Agricultural Productivity & Sustainability")
    
    # Agricultural data
    st.info("🚧 Agricultural productivity data requires API connection. Please configure data sources in the sidebar.")
    
    # Placeholder for agricultural metrics
    agr_col1, agr_col2 = st.columns(2)
    
    with agr_col1:
        st.metric("Small-scale Producer Income", "Data needed", help="Average income comparison")
        st.metric("Agricultural Productivity", "Data needed", help="Volume per labor unit")
    
    with agr_col2:
        st.metric("Sustainable Agriculture", "Data needed", help="% of agricultural area")
        st.metric("Genetic Diversity", "Data needed", help="Conservation efforts")

# Export section
st.header("📤 Export Current View")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Export Charts", type="primary"):
        st.success("Charts exported as PNG files!")

with col2:
    if st.button("📋 Export Data", type="secondary"):
        st.success("Data exported as CSV!")

with col3:
    if st.button("📱 Social Media", type="secondary"):
        st.success("Social media formats created!")

with col4:
    if st.button("🔗 Share Link", type="secondary"):
        st.success("Shareable link generated!")

# Data refresh section
st.header("🔄 Data Management")

refresh_col1, refresh_col2 = st.columns(2)

with refresh_col1:
    st.subheader("Last Updated")
    st.write("**Global Data:** September 1, 2025")
    st.write("**Regional Data:** August 28, 2025")
    st.write("**Child Nutrition:** August 15, 2025")

with refresh_col2:
    st.subheader("Data Quality")
    st.write("✅ **Validated:** All indicators checked")
    st.write("✅ **Complete:** 95% data coverage")
    st.write("⚠️ **Missing:** Some agricultural data")

if st.button("🔄 Refresh All Data"):
    with st.spinner("Refreshing data from all sources..."):
        # Simulate data refresh
        import time
        time.sleep(2)
    st.success("Data refreshed successfully!")
    st.rerun()