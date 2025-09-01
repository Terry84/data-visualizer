import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import base64
import numpy as np
import json
from datetime import datetime
import io
from utils.export_helpers import create_pdf_report, create_social_media_assets, generate_share_link

st.set_page_config(page_title="Export & Share", page_icon="📁", layout="wide")

st.title("📁 Export & Share")
st.markdown("Export your visualizations and create shareable content for various platforms")

# Initialize session state for exports
if 'export_history' not in st.session_state:
    st.session_state.export_history = []

if 'current_visualizations' not in st.session_state:
    # Create sample visualizations for demonstration
    sample_data = pd.DataFrame({
        'Region': ['Sub-Saharan Africa', 'Southern Asia', 'Western Asia', 'Latin America', 'Eastern Asia'],
        'Hunger Rate': [22.5, 13.1, 12.2, 6.5, 1.7],
        'Child Stunting': [30.7, 31.7, 13.8, 11.3, 4.8]
    })
    
    fig1 = px.bar(sample_data, x='Region', y='Hunger Rate', title='Hunger Rates by Region')
    fig2 = px.scatter(sample_data, x='Hunger Rate', y='Child Stunting', title='Hunger vs Stunting Correlation')
    
    st.session_state.current_visualizations = {
        'Hunger Rates Chart': fig1,
        'Correlation Analysis': fig2
    }

# Export options tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Export Visualizations", "📄 Generate Reports", "📱 Social Media", "🔗 Share & Collaborate", "📋 Export History"])

with tab1:
    st.header("📊 Export Visualizations")
    st.markdown("Export your charts and graphs in various formats for different use cases")
    
    # Visualization selector
    if st.session_state.current_visualizations:
        selected_viz = st.selectbox(
            "Select Visualization to Export",
            list(st.session_state.current_visualizations.keys())
        )
        
        # Show preview
        st.subheader("🔍 Preview")
        st.plotly_chart(st.session_state.current_visualizations[selected_viz], use_container_width=True)
        
        # Export format options
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📐 Format & Quality")
            
            export_format = st.selectbox(
                "Export Format",
                ["PNG (Raster)", "SVG (Vector)", "PDF (Document)", "HTML (Interactive)", "JSON (Data)"]
            )
            
            if export_format == "PNG (Raster)":
                quality_options = ["Standard (72 DPI)", "High (150 DPI)", "Print (300 DPI)", "Ultra (600 DPI)"]
                quality = st.selectbox("Image Quality", quality_options, index=2)
                
                dimension_options = ["800x600", "1200x800", "1920x1080", "2560x1440", "Custom"]
                dimensions = st.selectbox("Dimensions", dimension_options, index=2)
                
                if dimensions == "Custom":
                    width = st.number_input("Width (px)", value=1920, min_value=100, max_value=5000)
                    height = st.number_input("Height (px)", value=1080, min_value=100, max_value=5000)
                    dimensions = f"{width}x{height}"
            
            elif export_format == "SVG (Vector)":
                st.info("SVG format preserves quality at any size - perfect for print materials")
                
            elif export_format == "PDF (Document)":
                pdf_layout = st.selectbox("PDF Layout", ["Portrait", "Landscape"])
                pdf_size = st.selectbox("Page Size", ["A4", "Letter", "Legal", "A3"])
            
            elif export_format == "HTML (Interactive)":
                include_plotly = st.checkbox("Include Plotly.js library", value=True, 
                                           help="Uncheck if embedding in existing webpage")
        
        with col2:
            st.subheader("🎨 Styling Options")
            
            background_color = st.color_picker("Background Color", "#FFFFFF")
            transparent_bg = st.checkbox("Transparent Background", value=False)
            
            title_font_size = st.slider("Title Font Size", 12, 32, 20)
            axis_font_size = st.slider("Axis Font Size", 8, 24, 12)
            
            include_watermark = st.checkbox("Include Watermark", value=False)
            if include_watermark:
                watermark_text = st.text_input("Watermark Text", "SDG Goal 2 Dashboard")
        
        # Export button
        if st.button("📤 Export Visualization", type="primary"):
            with st.spinner("Generating export..."):
                # Simulate export process
                import time
                time.sleep(2)
                
                export_record = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'visualization': selected_viz,
                    'format': export_format,
                    'settings': {
                        'background': background_color,
                        'transparent': transparent_bg,
                        'dimensions': dimensions if export_format == "PNG (Raster)" else "Vector",
                        'quality': quality if export_format == "PNG (Raster)" else "Vector"
                    }
                }
                
                st.session_state.export_history.append(export_record)
                
                st.success(f"✅ '{selected_viz}' exported successfully as {export_format}!")
                
                # Provide download link (simulated)
                if export_format == "PNG (Raster)":
                    st.download_button(
                        label="💾 Download PNG",
                        data="sample_png_data",
                        file_name=f"{selected_viz.replace(' ', '_')}.png",
                        mime="image/png"
                    )
                elif export_format == "SVG (Vector)":
                    st.download_button(
                        label="💾 Download SVG",
                        data="sample_svg_data",
                        file_name=f"{selected_viz.replace(' ', '_')}.svg",
                        mime="image/svg+xml"
                    )
    else:
        st.info("📊 No visualizations available. Please create charts in the Dashboard or Templates sections first.")

with tab2:
    st.header("📄 Generate Reports")
    st.markdown("Create comprehensive reports combining multiple visualizations and analysis")
    
    # Report type selector
    report_type = st.selectbox(
        "Report Type",
        ["Executive Summary", "Detailed Analysis", "Regional Overview", "Progress Report", "Custom Report"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Report Configuration")
        
        report_title = st.text_input("Report Title", value="SDG Goal 2: Zero Hunger Analysis")
        report_subtitle = st.text_input("Subtitle", value="Global hunger and malnutrition assessment")
        
        author_name = st.text_input("Author", value="SDG Data Analyst")
        organization = st.text_input("Organization", value="UN Development Organization")
        
        # Date range for report
        date_range = st.date_input(
            "Report Period",
            value=[datetime(2023, 1, 1).date(), datetime(2024, 12, 31).date()],
            help="Select the time period covered by this report"
        )
        
        # Include sections
        st.subheader("📑 Report Sections")
        include_executive_summary = st.checkbox("Executive Summary", value=True)
        include_key_metrics = st.checkbox("Key Metrics Dashboard", value=True)
        include_regional_analysis = st.checkbox("Regional Analysis", value=True)
        include_trend_analysis = st.checkbox("Trend Analysis", value=True)
        include_recommendations = st.checkbox("Recommendations", value=True)
        include_methodology = st.checkbox("Data Sources & Methodology", value=True)
    
    with col2:
        st.subheader("🎨 Report Styling")
        
        template_style = st.selectbox(
            "Report Template",
            ["Professional", "Executive", "Academic", "Creative", "Minimal"]
        )
        
        color_theme = st.selectbox(
            "Color Theme",
            ["SDG Official", "Blue Professional", "Earth Tones", "Monochrome", "Custom"]
        )
        
        page_format = st.selectbox("Page Format", ["A4 Portrait", "A4 Landscape", "Letter", "Legal"])
        
        include_charts = st.multiselect(
            "Include Visualizations",
            list(st.session_state.current_visualizations.keys()) if st.session_state.current_visualizations else [],
            default=list(st.session_state.current_visualizations.keys())[:2] if st.session_state.current_visualizations else []
        )
        
        # Report language
        report_language = st.selectbox("Report Language", ["English", "Spanish", "French", "Arabic", "Chinese"])
    
    # Report preview
    if st.button("👀 Preview Report Structure"):
        st.subheader("📄 Report Preview")
        
        sections = []
        if include_executive_summary:
            sections.append("1. Executive Summary")
        if include_key_metrics:
            sections.append("2. Key Metrics Dashboard")
        if include_regional_analysis:
            sections.append("3. Regional Analysis")
        if include_trend_analysis:
            sections.append("4. Trend Analysis")
        if include_recommendations:
            sections.append("5. Recommendations")
        if include_methodology:
            sections.append("6. Data Sources & Methodology")
        
        for section in sections:
            st.write(f"**{section}**")
    
    # Generate report
    if st.button("📊 Generate Report", type="primary"):
        with st.spinner("Generating comprehensive report..."):
            import time
            time.sleep(3)
            
            # Create report record
            report_record = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'title': report_title,
                'type': report_type,
                'author': author_name,
                'pages': len([s for s in [include_executive_summary, include_key_metrics, 
                             include_regional_analysis, include_trend_analysis, 
                             include_recommendations, include_methodology] if s]) * 2 + 3,
                'format': page_format
            }
            
            st.session_state.export_history.append(report_record)
            
            st.success(f"✅ Report '{report_title}' generated successfully!")
            
            # Download options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📄 Download PDF",
                    data="sample_pdf_data",
                    file_name=f"{report_title.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
            
            with col2:
                st.download_button(
                    label="📝 Download Word",
                    data="sample_docx_data",
                    file_name=f"{report_title.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            
            with col3:
                st.download_button(
                    label="🌐 Download HTML",
                    data="sample_html_data",
                    file_name=f"{report_title.replace(' ', '_')}.html",
                    mime="text/html"
                )

with tab3:
    st.header("📱 Social Media Assets")
    st.markdown("Create optimized content for different social media platforms")
    
    # Platform selector
    platform_tabs = st.tabs(["📸 Instagram", "🐦 Twitter", "📘 Facebook", "💼 LinkedIn", "📺 YouTube"])
    
    with platform_tabs[0]:  # Instagram
        st.subheader("📸 Instagram Content")
        
        col1, col2 = st.columns(2)
        
        with col1:
            instagram_format = st.selectbox(
                "Instagram Format",
                ["Post (1080x1080)", "Story (1080x1920)", "Reel Cover (1080x1920)", "IGTV Cover (420x654)"]
            )
            
            content_type = st.selectbox(
                "Content Type",
                ["Key Statistic", "Data Visualization", "Infographic", "Quote Card", "Progress Update"]
            )
            
            if content_type == "Key Statistic":
                main_stat = st.text_input("Main Statistic", "713M")
                stat_description = st.text_input("Description", "people face hunger worldwide")
                context = st.text_input("Context", "That's 9.1% of global population")
            
            hashtags = st.text_area("Hashtags", "#ZeroHunger #SDG2 #EndHunger #GlobalGoals #Sustainability")
        
        with col2:
            st.write("**Preview**")
            
            # Create Instagram-style preview
            if content_type == "Key Statistic":
                fig_insta = go.Figure()
                
                fig_insta.add_annotation(
                    x=0.5, y=0.7,
                    text=main_stat,
                    font=dict(size=50, color="#e5243b", family="Arial Black"),
                    showarrow=False
                )
                
                fig_insta.add_annotation(
                    x=0.5, y=0.5,
                    text=stat_description,
                    font=dict(size=18, color="black"),
                    showarrow=False
                )
                
                fig_insta.add_annotation(
                    x=0.5, y=0.3,
                    text=context,
                    font=dict(size=14, color="#666666"),
                    showarrow=False
                )
                
                fig_insta.update_layout(
                    width=400, height=400,
                    xaxis=dict(visible=False, range=[0, 1]),
                    yaxis=dict(visible=False, range=[0, 1]),
                    plot_bgcolor='white',
                    paper_bgcolor='#f8f9fa'
                )
                
                st.plotly_chart(fig_insta, use_container_width=True)
        
        if st.button("🎨 Generate Instagram Content"):
            st.success("✅ Instagram content generated!")
            st.download_button(
                "💾 Download Instagram Asset",
                data="instagram_asset_data",
                file_name="sdg2_instagram_post.png",
                mime="image/png"
            )
    
    with platform_tabs[1]:  # Twitter
        st.subheader("🐦 Twitter Content")
        
        twitter_format = st.selectbox(
            "Twitter Format",
            ["Tweet Image (1200x675)", "Header (1500x500)", "Profile Image (400x400)"]
        )
        
        tweet_text = st.text_area(
            "Tweet Text",
            "🌍 URGENT: 713 million people still face hunger worldwide. That's 9.1% of our global population. We must accelerate action toward #ZeroHunger by 2030. #SDG2 #GlobalGoals",
            max_chars=280
        )
        
        st.write(f"Character count: {len(tweet_text)}/280")
        
        if st.button("🐦 Generate Twitter Content"):
            st.success("✅ Twitter content generated!")
    
    with platform_tabs[2]:  # Facebook
        st.subheader("📘 Facebook Content")
        
        facebook_format = st.selectbox(
            "Facebook Format",
            ["Post Image (1200x630)", "Cover Photo (851x315)", "Event Cover (1920x1080)", "Story (1080x1920)"]
        )
        
        post_text = st.text_area(
            "Post Text",
            """🌾 SDG Goal 2 Update: Zero Hunger Progress
            
Despite global efforts, 713 million people still face hunger - that's 9.1% of our world's population. 

Key challenges:
• Child stunting affects 150M children globally  
• Food insecurity impacts 2.33B people
• Climate change threatens food systems

But there's hope! Learn how you can contribute to ending hunger by 2030.

#ZeroHunger #SDG2 #GlobalGoals #FoodSecurity #EndHunger"""
        )
        
        if st.button("📘 Generate Facebook Content"):
            st.success("✅ Facebook content generated!")

with tab4:
    st.header("🔗 Share & Collaborate")
    st.markdown("Create shareable links and collaborative workspaces")
    
    # Sharing options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔗 Generate Share Links")
        
        share_type = st.selectbox(
            "Share Type",
            ["Public View", "Embed Code", "Collaborative Edit", "Download Link", "Presentation Mode"]
        )
        
        if share_type == "Public View":
            st.write("Create a public link that allows viewing without editing")
            expiry_options = ["Never", "24 hours", "7 days", "30 days", "90 days"]
            expiry = st.selectbox("Link Expiry", expiry_options)
            
        elif share_type == "Embed Code":
            st.write("Generate HTML embed code for websites")
            embed_width = st.number_input("Width (px)", value=800, min_value=300)
            embed_height = st.number_input("Height (px)", value=600, min_value=200)
            
        elif share_type == "Collaborative Edit":
            st.write("Allow others to edit and modify visualizations")
            st.warning("⚠️ Only share with trusted collaborators")
            
        password_protect = st.checkbox("Password Protection")
        if password_protect:
            share_password = st.text_input("Access Password", type="password")
        
        if st.button("🔗 Generate Share Link", type="primary"):
            # Generate unique link (simulated)
            import uuid
            link_id = str(uuid.uuid4())[:8]
            share_url = f"https://sdg-dashboard.app/share/{link_id}"
            
            st.success("✅ Share link generated!")
            st.code(share_url)
            
            if share_type == "Embed Code":
                embed_code = f'<iframe src="{share_url}/embed" width="{embed_width}" height="{embed_height}" frameborder="0"></iframe>'
                st.code(embed_code, language="html")
            
            # Copy to clipboard button
            st.button("📋 Copy to Clipboard")
    
    with col2:
        st.subheader("👥 Collaboration Features")
        
        st.write("**Active Collaborators:**")
        collaborators = [
            {"name": "Dr. Sarah Johnson", "role": "Data Analyst", "status": "Online"},
            {"name": "Miguel Rodriguez", "role": "Visualization Designer", "status": "Offline"},
            {"name": "Dr. Aisha Patel", "role": "SDG Coordinator", "status": "Online"}
        ]
        
        for collab in collaborators:
            status_color = "🟢" if collab["status"] == "Online" else "⚫"
            st.write(f"{status_color} **{collab['name']}** - {collab['role']}")
        
        st.write("**Invite New Collaborators:**")
        invite_email = st.text_input("Email Address")
        invite_role = st.selectbox("Role", ["Viewer", "Editor", "Admin"])
        
        if st.button("📧 Send Invitation"):
            st.success(f"✅ Invitation sent to {invite_email}")
        
        # Version control
        st.write("**Version History:**")
        versions = [
            {"version": "v1.3", "date": "2024-09-01 14:30", "author": "Dr. Sarah Johnson", "changes": "Updated hunger statistics"},
            {"version": "v1.2", "date": "2024-08-28 09:15", "author": "Miguel Rodriguez", "changes": "Improved chart styling"},
            {"version": "v1.1", "date": "2024-08-25 16:45", "author": "Dr. Aisha Patel", "changes": "Added regional breakdown"}
        ]
        
        for version in versions:
            with st.expander(f"{version['version']} - {version['date']}"):
                st.write(f"**Author:** {version['author']}")
                st.write(f"**Changes:** {version['changes']}")
                st.button(f"Restore {version['version']}", key=f"restore_{version['version']}")
    
    # API access
    st.subheader("🔌 API Access")
    
    api_col1, api_col2 = st.columns(2)
    
    with api_col1:
        st.write("**REST API Endpoints:**")
        st.code("""
GET /api/v1/visualizations/{id}
POST /api/v1/visualizations
PUT /api/v1/visualizations/{id}
DELETE /api/v1/visualizations/{id}
GET /api/v1/data/export/{format}
        """)
    
    with api_col2:
        st.write("**Generate API Key:**")
        api_key_name = st.text_input("API Key Name", "SDG Dashboard Integration")
        api_permissions = st.multiselect(
            "Permissions",
            ["Read", "Write", "Export", "Share"],
            default=["Read", "Export"]
        )
        
        if st.button("🔑 Generate API Key"):
            api_key = "sdg_" + str(uuid.uuid4()).replace("-", "")[:16]
            st.success("✅ API Key generated!")
            st.code(api_key)

with tab5:
    st.header("📋 Export History")
    st.markdown("Track and manage all your exports and downloads")
    
    if st.session_state.export_history:
        # Export statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Exports", len(st.session_state.export_history))
        
        with col2:
            formats = [item.get('format', 'Unknown') for item in st.session_state.export_history]
            most_common = max(set(formats), key=formats.count) if formats else 'None'
            st.metric("Most Used Format", most_common)
        
        with col3:
            today_exports = [item for item in st.session_state.export_history 
                           if item['timestamp'].startswith(datetime.now().strftime("%Y-%m-%d"))]
            st.metric("Today's Exports", len(today_exports))
        
        with col4:
            st.metric("Storage Used", "156 MB")
        
        # Export history table
        st.subheader("📊 Export History")
        
        # Convert history to DataFrame for better display
        history_data = []
        for item in st.session_state.export_history:
            history_data.append({
                'Timestamp': item['timestamp'],
                'Item': item.get('visualization', item.get('title', 'Report')),
                'Type': item.get('format', item.get('type', 'Unknown')),
                'Author': item.get('author', 'Current User'),
                'Size': f"{np.random.randint(50, 500)} KB"  # Simulated file sizes
            })
        
        if history_data:
            history_df = pd.DataFrame(history_data)
            
            # Search and filter
            search_term = st.text_input("🔍 Search exports", placeholder="Search by name, format, or date...")
            if search_term:
                mask = history_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                history_df = history_df[mask]
            
            # Display table with actions
            for idx, row in history_df.iterrows():
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 1, 1, 1])
                
                with col1:
                    st.write(f"**{row['Item']}**")
                with col2:
                    st.write(row['Timestamp'])
                with col3:
                    st.write(row['Type'])
                with col4:
                    st.write(row['Size'])
                with col5:
                    if st.button("📥", key=f"download_{idx}", help="Download again"):
                        st.success("✅ Download started!")
                with col6:
                    if st.button("🗑️", key=f"delete_{idx}", help="Delete from history"):
                        # Remove from history
                        if idx < len(st.session_state.export_history):
                            st.session_state.export_history.pop(idx)
                        st.success("✅ Removed from history!")
                        st.rerun()
        
        # Bulk actions
        st.subheader("🔧 Bulk Actions")
        bulk_col1, bulk_col2, bulk_col3 = st.columns(3)
        
        with bulk_col1:
            if st.button("📦 Download All"):
                st.success("✅ Creating bulk download archive...")
        
        with bulk_col2:
            if st.button("🗑️ Clear History"):
                st.session_state.export_history = []
                st.success("✅ Export history cleared!")
                st.rerun()
        
        with bulk_col3:
            if st.button("📊 Export Report"):
                st.success("✅ Usage report generated!")
    
    else:
        st.info("📁 No exports yet. Start creating and exporting visualizations to see your history here.")

# Storage and quota information
st.header("💾 Storage & Quotas")

storage_col1, storage_col2 = st.columns(2)

with storage_col1:
    st.subheader("📈 Usage Statistics")
    
    # Storage usage chart
    storage_data = pd.DataFrame({
        'Category': ['Visualizations', 'Reports', 'Images', 'Data Files', 'Available'],
        'Size (MB)': [45, 78, 23, 10, 844],
        'Color': ['#e5243b', '#ff6347', '#ffa500', '#32cd32', '#e0e0e0']
    })
    
    fig_storage = px.pie(
        storage_data, 
        values='Size (MB)', 
        names='Category',
        title='Storage Usage (1GB Total)',
        color_discrete_sequence=storage_data['Color']
    )
    st.plotly_chart(fig_storage, use_container_width=True)

with storage_col2:
    st.subheader("📊 Export Quotas")
    
    quotas = {
        'Daily Exports': {'used': 12, 'limit': 50},
        'Monthly Storage': {'used': 156, 'limit': 1000},
        'Share Links': {'used': 3, 'limit': 10},
        'API Calls': {'used': 245, 'limit': 1000}
    }
    
    for quota_name, quota_info in quotas.items():
        progress = quota_info['used'] / quota_info['limit']
        st.write(f"**{quota_name}**")
        st.progress(progress)
        st.caption(f"{quota_info['used']}/{quota_info['limit']} used")
        st.write("")

# Footer with tips
st.markdown("---")
st.markdown("""
💡 **Export Tips:**
- Use SVG format for scalable graphics that work at any size
- PNG with 300 DPI is ideal for high-quality print materials
- HTML exports preserve interactivity for web embedding
- Social media formats are optimized for each platform's specifications
""")