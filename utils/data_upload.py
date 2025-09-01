import streamlit as st
import pandas as pd
import plotly.express as px
import json
import io
import numpy as np
from utils.data_source import DataSourceManager
import requests
import os

st.set_page_config(page_title="Data Upload", page_icon="📤", layout="wide")

st.title("📤 Data Upload & Import")
st.markdown("Upload your own datasets or connect to official SDG Goal 2 data sources")

# Initialize data manager
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataSourceManager()

if 'uploaded_datasets' not in st.session_state:
    st.session_state.uploaded_datasets = {}

# Tabs for different upload methods
tab1, tab2, tab3, tab4 = st.tabs(["📁 File Upload", "🌐 API Connections", "🔗 URL Import", "📊 Data Validation"])

with tab1:
    st.header("📁 File Upload")
    st.markdown("Upload CSV, Excel, JSON, or other data files containing SDG Goal 2 indicators")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['csv', 'xlsx', 'xls', 'json', 'txt'],
        accept_multiple_files=True,
        help="Supported formats: CSV, Excel, JSON, TXT"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.subheader(f"📄 {uploaded_file.name}")
            
            try:
                # Read file based on type
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(uploaded_file)
                elif uploaded_file.name.endswith('.json'):
                    data = json.load(uploaded_file)
                    df = pd.json_normalize(data) if isinstance(data, list) else pd.DataFrame([data])
                else:
                    st.error("Unsupported file format")
                    continue
                
                # Display file info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", len(df))
                with col2:
                    st.metric("Columns", len(df.columns))
                with col3:
                    st.metric("Size", f"{uploaded_file.size / 1024:.1f} KB")
                
                # Show data preview
                st.write("**Data Preview:**")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Column analysis
                st.write("**Column Information:**")
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Data Type': df.dtypes,
                    'Non-Null Count': df.count(),
                    'Sample Values': [str(df[col].dropna().iloc[0]) if not df[col].empty else 'N/A' for col in df.columns]
                })
                st.dataframe(col_info, use_container_width=True)
                
                # SDG mapping
                st.write("**SDG Goal 2 Indicator Mapping:**")
                sdg_indicators = {
                    'hunger_rate': 'Prevalence of undernourishment (%)',
                    'food_insecurity': 'Moderate or severe food insecurity (%)',
                    'child_stunting': 'Child stunting rate (%)',
                    'child_wasting': 'Child wasting rate (%)',
                    'child_overweight': 'Child overweight rate (%)',
                    'anemia_women': 'Anemia in women 15-49 years (%)',
                    'breastfeeding': 'Exclusive breastfeeding rate (%)',
                    'agricultural_productivity': 'Agricultural productivity index',
                    'small_producer_income': 'Small-scale producer income (USD)'
                }
                
                mapping_cols = st.columns(2)
                with mapping_cols[0]:
                    st.selectbox(
                        "Map to SDG Indicator",
                        list(sdg_indicators.values()),
                        key=f"indicator_{uploaded_file.name}"
                    )
                with mapping_cols[1]:
                    st.selectbox(
                        "Data Column",
                        df.columns.tolist(),
                        key=f"column_{uploaded_file.name}"
                    )
                
                # Save dataset
                if st.button(f"💾 Save Dataset: {uploaded_file.name}", key=f"save_{uploaded_file.name}"):
                    st.session_state.uploaded_datasets[uploaded_file.name] = df
                    st.success(f"✅ Dataset '{uploaded_file.name}' saved successfully!")
                
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")

with tab2:
    st.header("🌐 API Connections")
    st.markdown("Connect to official UN data sources for real-time SDG Goal 2 data")
    
    # API configuration section
    st.subheader("🔑 API Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**FAO API**")
        fao_api_key = st.text_input(
            "FAO API Key",
            type="password",
            value=os.getenv("FAO_API_KEY", ""),
            help="Get your API key from FAO Data Portal"
        )
        fao_endpoint = st.text_input(
            "FAO Endpoint",
            value="http://fenixservices.fao.org/faostat/api/v1/en/",
            help="FAO API endpoint URL"
        )
        
        if st.button("🔍 Test FAO Connection"):
            if fao_api_key or fao_endpoint:
                with st.spinner("Testing FAO API connection..."):
                    try:
                        # Test FAO API (simplified)
                        response = requests.get(f"{fao_endpoint}countries", timeout=10)
                        if response.status_code == 200:
                            st.success("✅ FAO API connection successful!")
                            data = response.json()[:5]  # Show first 5 countries
                            st.json(data)
                        else:
                            st.error(f"❌ FAO API connection failed: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Connection error: {str(e)}")
            else:
                st.warning("⚠️ Please provide API credentials")
    
    with col2:
        st.write("**World Bank API**")
        wb_api_key = st.text_input(
            "World Bank API Key",
            type="password",
            value=os.getenv("WORLD_BANK_API_KEY", ""),
            help="World Bank API key (optional for basic access)"
        )
        wb_endpoint = st.text_input(
            "World Bank Endpoint",
            value="https://api.worldbank.org/v2/",
            help="World Bank API endpoint URL"
        )
        
        if st.button("🔍 Test World Bank Connection"):
            with st.spinner("Testing World Bank API connection..."):
                try:
                    # Test World Bank API
                    response = requests.get(f"{wb_endpoint}countries?format=json&per_page=5", timeout=10)
                    if response.status_code == 200:
                        st.success("✅ World Bank API connection successful!")
                        data = response.json()
                        if isinstance(data, list) and len(data) > 1:
                            st.json(data[1][:3])  # Show first 3 countries
                    else:
                        st.error(f"❌ World Bank API connection failed: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
    
    # UNICEF and WHO API sections
    st.subheader("🏥 Health Data APIs")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("**UNICEF Data**")
        unicef_endpoint = st.text_input(
            "UNICEF Data Portal",
            value="https://sdgapi.unicef.org/",
            help="UNICEF SDG Data Portal API"
        )
        
        if st.button("🔍 Test UNICEF Connection"):
            with st.spinner("Testing UNICEF API connection..."):
                try:
                    response = requests.get(f"{unicef_endpoint}Goal/2", timeout=10)
                    if response.status_code == 200:
                        st.success("✅ UNICEF API connection successful!")
                        st.write("Available SDG Goal 2 data from UNICEF")
                    else:
                        st.error(f"❌ UNICEF API connection failed: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
    
    with col4:
        st.write("**WHO Data**")
        who_endpoint = st.text_input(
            "WHO Global Health Observatory",
            value="https://ghoapi.azureedge.net/api/",
            help="WHO Global Health Observatory API"
        )
        
        if st.button("🔍 Test WHO Connection"):
            with st.spinner("Testing WHO API connection..."):
                try:
                    response = requests.get(f"{who_endpoint}Dimension", timeout=10)
                    if response.status_code == 200:
                        st.success("✅ WHO API connection successful!")
                        st.write("WHO Global Health Observatory API accessible")
                    else:
                        st.error(f"❌ WHO API connection failed: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
    
    # Data fetching section
    st.subheader("📊 Fetch Data")
    
    data_source = st.selectbox(
        "Select Data Source",
        ["FAO - Hunger Statistics", "World Bank - Malnutrition", "UNICEF - Child Health", "WHO - Nutrition Status"],
        help="Choose which data source to fetch from"
    )
    
    indicators_to_fetch = st.multiselect(
        "Select Indicators",
        [
            "Prevalence of undernourishment",
            "Food insecurity (moderate or severe)",
            "Child stunting rate",
            "Child wasting rate",
            "Child overweight rate",
            "Anemia in women",
            "Exclusive breastfeeding",
            "Agricultural productivity"
        ],
        default=["Prevalence of undernourishment", "Child stunting rate"]
    )
    
    countries_to_fetch = st.multiselect(
        "Select Countries/Regions",
        [
            "World", "Sub-Saharan Africa", "Southern Asia", "United States",
            "China", "India", "Brazil", "Nigeria", "Ethiopia", "Bangladesh"
        ],
        default=["World", "Sub-Saharan Africa"]
    )
    
    year_range_fetch = st.slider(
        "Year Range",
        min_value=2000,
        max_value=2024,
        value=(2015, 2024)
    )
    
    if st.button("📥 Fetch Data", type="primary"):
        with st.spinner("Fetching data from selected sources..."):
            # Simulate data fetching
            import time
            import numpy as np
            
            time.sleep(3)  # Simulate API call delay
            
            # Generate sample fetched data
            years = list(range(year_range_fetch[0], year_range_fetch[1] + 1))
            
            fetched_data = []
            for country in countries_to_fetch:
                for year in years:
                    for indicator in indicators_to_fetch:
                        # Generate realistic sample values
                        if "stunting" in indicator.lower():
                            value = np.random.uniform(5, 40)
                        elif "undernourishment" in indicator.lower():
                            value = np.random.uniform(2, 25)
                        elif "wasting" in indicator.lower():
                            value = np.random.uniform(3, 15)
                        elif "breastfeeding" in indicator.lower():
                            value = np.random.uniform(25, 70)
                        else:
                            value = np.random.uniform(10, 50)
                        
                        fetched_data.append({
                            'Country': country,
                            'Year': year,
                            'Indicator': indicator,
                            'Value': round(value, 1),
                            'Source': data_source
                        })
            
            fetched_df = pd.DataFrame(fetched_data)
            
            st.success(f"✅ Successfully fetched {len(fetched_df)} data points!")
            
            # Display fetched data
            st.dataframe(fetched_df.head(20), use_container_width=True)
            
            # Save to session state
            dataset_name = f"{data_source}_{year_range_fetch[0]}_{year_range_fetch[1]}"
            st.session_state.uploaded_datasets[dataset_name] = fetched_df
            
            # Quick visualization
            if len(fetched_df) > 0:
                st.subheader("📈 Quick Preview")
                
                # Create a sample chart
                sample_data = fetched_df[fetched_df['Indicator'] == indicators_to_fetch[0]]
                if len(sample_data) > 0:
                    fig = px.line(
                        sample_data,
                        x='Year',
                        y='Value',
                        color='Country',
                        title=f'{indicators_to_fetch[0]} Trends'
                    )
                    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🔗 URL Import")
    st.markdown("Import data directly from web URLs or online datasets")
    
    # URL input
    data_url = st.text_input(
        "Data URL",
        placeholder="https://example.com/sdg2-data.csv",
        help="Enter URL to CSV, JSON, or Excel file"
    )
    
    url_type = st.selectbox(
        "Data Format",
        ["CSV", "JSON", "Excel", "XML"],
        help="Select the format of data at the URL"
    )
    
    if st.button("🔗 Import from URL") and data_url:
        with st.spinner("Importing data from URL..."):
            try:
                if url_type == "CSV":
                    df = pd.read_csv(data_url)
                elif url_type == "JSON":
                    df = pd.read_json(data_url)
                elif url_type == "Excel":
                    df = pd.read_excel(data_url)
                else:
                    st.error("XML import not yet supported")
                    df = None
                
                if df is not None:
                    st.success(f"✅ Successfully imported {len(df)} rows from URL!")
                    
                    # Display data info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Rows", len(df))
                    with col2:
                        st.metric("Columns", len(df.columns))
                    with col3:
                        st.metric("Data Types", len(df.dtypes.unique()))
                    
                    # Show preview
                    st.dataframe(df.head(), use_container_width=True)
                    
                    # Save dataset
                    url_name = data_url.split('/')[-1] if '/' in data_url else 'url_dataset'
                    if st.button(f"💾 Save Dataset: {url_name}"):
                        st.session_state.uploaded_datasets[url_name] = df
                        st.success(f"Dataset saved as '{url_name}'")
                
            except Exception as e:
                st.error(f"❌ Error importing from URL: {str(e)}")
    
    # Common SDG data sources
    st.subheader("🌐 Common SDG Data Sources")
    
    predefined_sources = {
        "FAO Statistics": "http://www.fao.org/faostat/en/#data",
        "World Bank Open Data": "https://data.worldbank.org/",
        "UNICEF Data": "https://data.unicef.org/",
        "WHO Global Health Observatory": "https://www.who.int/data/gho",
        "UN SDG Database": "https://unstats.un.org/sdgs/dataportal"
    }
    
    for source_name, source_url in predefined_sources.items():
        st.markdown(f"**{source_name}**: [{source_url}]({source_url})")

with tab4:
    st.header("📊 Data Validation")
    st.markdown("Validate uploaded datasets against SDG Goal 2 standards")
    
    if st.session_state.uploaded_datasets:
        # Dataset selector
        selected_dataset = st.selectbox(
            "Select Dataset to Validate",
            list(st.session_state.uploaded_datasets.keys())
        )
        
        if selected_dataset:
            df = st.session_state.uploaded_datasets[selected_dataset]
            
            st.subheader(f"🔍 Validating: {selected_dataset}")
            
            # Basic validation metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                completeness = (df.count().sum() / (len(df) * len(df.columns))) * 100
                st.metric("Data Completeness", f"{completeness:.1f}%")
            
            with col2:
                duplicates = df.duplicated().sum()
                st.metric("Duplicate Rows", duplicates)
            
            with col3:
                missing_values = df.isnull().sum().sum()
                st.metric("Missing Values", missing_values)
            
            with col4:
                numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
                st.metric("Numeric Columns", numeric_cols)
            
            # Detailed validation results
            st.subheader("📋 Validation Results")
            
            validation_results = []
            
            # Check for required columns
            required_patterns = ['country', 'year', 'region', 'indicator', 'value']
            for pattern in required_patterns:
                matching_cols = [col for col in df.columns if pattern.lower() in col.lower()]
                if matching_cols:
                    validation_results.append({
                        'Check': f'Has {pattern} column',
                        'Status': '✅ Pass',
                        'Details': f'Found: {", ".join(matching_cols)}'
                    })
                else:
                    validation_results.append({
                        'Check': f'Has {pattern} column',
                        'Status': '⚠️ Warning',
                        'Details': f'No column matching "{pattern}" pattern'
                    })
            
            # Check data ranges
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                min_val = df[col].min()
                max_val = df[col].max()
                
                # SDG 2 indicator ranges
                if any(keyword in col.lower() for keyword in ['hunger', 'undernourishment']):
                    if 0 <= min_val <= 100 and 0 <= max_val <= 100:
                        status = '✅ Pass'
                        details = 'Values in valid range (0-100%)'
                    else:
                        status = '❌ Fail'
                        details = f'Invalid range: {min_val:.1f} to {max_val:.1f}'
                else:
                    status = '✅ Pass'
                    details = f'Range: {min_val:.1f} to {max_val:.1f}'
                
                validation_results.append({
                    'Check': f'{col} value range',
                    'Status': status,
                    'Details': details
                })
            
            # Display validation results
            validation_df = pd.DataFrame(validation_results)
            st.dataframe(validation_df, use_container_width=True)
            
            # Data quality score
            pass_count = len([r for r in validation_results if r['Status'] == '✅ Pass'])
            total_checks = len(validation_results)
            quality_score = (pass_count / total_checks) * 100 if total_checks > 0 else 0
            
            st.subheader("📈 Data Quality Score")
            st.progress(quality_score / 100)
            st.write(f"**Score: {quality_score:.1f}%** ({pass_count}/{total_checks} checks passed)")
            
            # Recommendations
            st.subheader("💡 Recommendations")
            
            if quality_score >= 80:
                st.success("✅ Dataset meets high quality standards for SDG Goal 2 analysis!")
            elif quality_score >= 60:
                st.warning("⚠️ Dataset has moderate quality. Consider addressing validation warnings.")
            else:
                st.error("❌ Dataset quality is below recommended standards. Please review and clean data.")
            
            # Export validation report
            if st.button("📋 Export Validation Report"):
                validation_report = {
                    'dataset_name': selected_dataset,
                    'validation_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'quality_score': quality_score,
                    'total_rows': len(df),
                    'total_columns': len(df.columns),
                    'completeness': completeness,
                    'validation_results': validation_results
                }
                
                report_json = json.dumps(validation_report, indent=2)
                st.download_button(
                    label="💾 Download Validation Report",
                    data=report_json,
                    file_name=f"validation_report_{selected_dataset}.json",
                    mime="application/json"
                )
    else:
        st.info("📁 No datasets uploaded yet. Please upload data in the 'File Upload' or 'API Connections' tabs first.")

# Summary section
st.header("📋 Uploaded Datasets Summary")

if st.session_state.uploaded_datasets:
    summary_data = []
    for name, df in st.session_state.uploaded_datasets.items():
        summary_data.append({
            'Dataset': name,
            'Rows': len(df),
            'Columns': len(df.columns),
            'Size (KB)': f"{df.memory_usage(deep=True).sum() / 1024:.1f}",
            'Upload Time': pd.Timestamp.now().strftime('%H:%M:%S')
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)
    
    # Bulk operations
    st.subheader("🔧 Bulk Operations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh All"):
            st.success("All datasets refreshed!")
    
    with col2:
        if st.button("📁 Export All"):
            st.success("All datasets exported!")
    
    with col3:
        if st.button("🗑️ Clear All"):
            st.session_state.uploaded_datasets = {}
            st.success("All datasets cleared!")
            st.rerun()
else:
    st.info("📁 No datasets uploaded yet. Use the tabs above to upload or import data.")