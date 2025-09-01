import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from typing import Dict, List, Optional, Union, Tuple
import json
import base64
import io
from datetime import datetime
import streamlit as st
import uuid
import zipfile
import tempfile
import os

class ExportManager:
    """
    Handles exporting visualizations and data in various formats
    """
    
    def __init__(self):
        self.supported_formats = {
            'image': ['png', 'svg', 'pdf', 'jpeg'],
            'data': ['csv', 'xlsx', 'json', 'parquet'],
            'document': ['html', 'pdf'],
            'social': ['instagram_post', 'instagram_story', 'twitter_card', 'facebook_post']
        }
        
        self.social_dimensions = {
            'instagram_post': {'width': 1080, 'height': 1080, 'dpi': 300},
            'instagram_story': {'width': 1080, 'height': 1920, 'dpi': 300},
            'twitter_card': {'width': 1200, 'height': 675, 'dpi': 150},
            'facebook_post': {'width': 1200, 'height': 630, 'dpi': 150},
            'linkedin_post': {'width': 1200, 'height': 627, 'dpi': 150}
        }
        
        self.dpi_settings = {
            'web': 72,
            'standard': 150,
            'print': 300,
            'ultra': 600
        }

def create_pdf_report(data: Dict, 
                     visualizations: Dict[str, go.Figure],
                     template: str = 'professional',
                     include_sections: List[str] = None) -> bytes:
    """
    Create PDF report with visualizations and analysis
    
    Args:
        data: Dictionary containing report data and metadata
        visualizations: Dictionary of Plotly figures to include
        template: Report template style
        include_sections: List of sections to include
        
    Returns:
        PDF bytes data
    """
    try:
        # This would typically use libraries like reportlab or weasyprint
        # For now, return HTML that can be converted to PDF
        
        html_content = _generate_html_report(data, visualizations, template, include_sections)
        
        # Convert HTML to PDF (placeholder implementation)
        # In a real implementation, use libraries like:
        # - weasyprint: weasyprint.HTML(string=html_content).write_pdf()
        # - pdfkit: pdfkit.from_string(html_content)
        
        # For now, return HTML as bytes
        return html_content.encode('utf-8')
        
    except Exception as e:
        st.error(f"Error creating PDF report: {str(e)}")
        return b"PDF generation failed"

def _generate_html_report(data: Dict,
                         visualizations: Dict[str, go.Figure],
                         template: str,
                         include_sections: List[str]) -> str:
    """Generate HTML report content"""
    
    title = data.get('title', 'SDG Goal 2: Zero Hunger Analysis')
    author = data.get('author', 'SDG Data Analyst')
    date = datetime.now().strftime("%B %d, %Y")
    
    # Convert visualizations to HTML
    viz_html = {}
    for name, fig in visualizations.items():
        viz_html[name] = pio.to_html(fig, include_plotlyjs='cdn', div_id=f"viz_{name.replace(' ', '_')}")
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
                color: #333;
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 3px solid #e5243b;
                padding-bottom: 20px;
            }}
            .title {{
                color: #e5243b;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .subtitle {{
                color: #666;
                font-size: 16px;
            }}
            .section {{
                margin: 30px 0;
            }}
            .section h2 {{
                color: #e5243b;
                border-left: 4px solid #e5243b;
                padding-left: 10px;
            }}
            .key-stat {{
                background: #f8f9fa;
                padding: 15px;
                border-left: 4px solid #e5243b;
                margin: 10px 0;
            }}
            .viz-container {{
                margin: 20px 0;
                text-align: center;
            }}
            .footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                text-align: center;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">{title}</div>
            <div class="subtitle">Prepared by {author} | {date}</div>
        </div>
        
        {''.join([_generate_section_html(section, viz_html, data) for section in (include_sections or ['executive_summary'])])}
        
        <div class="footer">
            <p>Report generated using SDG Goal 2 Data Visualization Tool</p>
            <p>Data sources: FAO, UNICEF, WHO, World Bank</p>
        </div>
    </body>
    </html>
    """
    
    return html_template

def _generate_section_html(section: str, viz_html: Dict, data: Dict) -> str:
    """Generate HTML for a specific report section"""
    
    sections = {
        'executive_summary': {
            'title': 'Executive Summary',
            'content': f"""
                <p>The global fight against hunger faces significant challenges in 2024. Despite progress in some areas, 
                <strong>713-757 million people</strong> still face hunger worldwide, representing 9.1% of the global population.</p>
                
                <div class="key-stat">
                    <strong>Key Finding:</strong> Child stunting affects 150.2 million children globally (23.2% of under-5s), 
                    while 2.33 billion people experience moderate or severe food insecurity.
                </div>
                
                <p>Regional disparities remain stark, with Sub-Saharan Africa showing the highest hunger rates at 22.5%, 
                followed by Southern Asia at 13.1%.</p>
            """
        },
        'key_metrics': {
            'title': 'Key Metrics Dashboard',
            'content': """
                <div class="viz-container">
                    <!-- Key visualizations would be embedded here -->
                </div>
            """
        },
        'regional_analysis': {
            'title': 'Regional Analysis',
            'content': """
                <p>Regional analysis reveals significant disparities in hunger and malnutrition rates across different areas:</p>
                <ul>
                    <li><strong>Sub-Saharan Africa:</strong> Highest hunger rate (22.5%) and child stunting (30.7%)</li>
                    <li><strong>Southern Asia:</strong> Second highest hunger rate (13.1%) with severe child wasting (14.7%)</li>
                    <li><strong>Europe & Northern America:</strong> Lowest hunger rate (2.4%) but highest child overweight (12.3%)</li>
                </ul>
            """
        },
        'recommendations': {
            'title': 'Recommendations',
            'content': """
                <ol>
                    <li><strong>Accelerate Investment:</strong> Increase funding for nutrition-specific interventions</li>
                    <li><strong>Climate Resilience:</strong> Build climate-smart agricultural systems</li>
                    <li><strong>Social Protection:</strong> Expand social safety nets for vulnerable populations</li>
                    <li><strong>Data Systems:</strong> Strengthen monitoring and evaluation systems</li>
                </ol>
            """
        }
    }
    
    section_info = sections.get(section, {'title': section.title(), 'content': '<p>Section content not available.</p>'})
    
    return f"""
        <div class="section">
            <h2>{section_info['title']}</h2>
            {section_info['content']}
        </div>
    """

def create_social_media_assets(figures: Dict[str, go.Figure],
                             platform: str = 'instagram',
                             content_type: str = 'post',
                             branding: Dict = None) -> Dict[str, bytes]:
    """
    Create social media optimized assets
    
    Args:
        figures: Dictionary of Plotly figures
        platform: Target platform
        content_type: Type of content (post, story, etc.)
        branding: Branding elements to include
        
    Returns:
        Dictionary of asset names and their binary data
    """
    export_manager = ExportManager()
    assets = {}
    
    format_key = f"{platform}_{content_type}"
    if format_key not in export_manager.social_dimensions:
        format_key = 'instagram_post'  # Default fallback
    
    dimensions = export_manager.social_dimensions[format_key]
    
    try:
        for name, fig in figures.items():
            # Update figure for social media dimensions
            fig_copy = go.Figure(fig)
            fig_copy.update_layout(
                width=dimensions['width'],
                height=dimensions['height'],
                font_size=16,
                title_font_size=24,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            
            # Add branding if provided
            if branding:
                _add_branding_to_figure(fig_copy, branding, platform)
            
            # Convert to image bytes
            img_bytes = pio.to_image(
                fig_copy,
                format='png',
                width=dimensions['width'],
                height=dimensions['height'],
                scale=dimensions['dpi'] / 72  # Convert DPI to scale factor
            )
            
            assets[f"{name}_{format_key}.png"] = img_bytes
            
    except Exception as e:
        st.error(f"Error creating social media assets: {str(e)}")
        assets['error.txt'] = f"Asset creation failed: {str(e)}".encode()
    
    return assets

def _add_branding_to_figure(fig: go.Figure, branding: Dict, platform: str):
    """Add branding elements to a figure"""
    
    # Add logo or watermark
    if branding.get('logo_url'):
        fig.add_layout_image(
            dict(
                source=branding['logo_url'],
                xref="paper", yref="paper",
                x=0.95, y=0.05,
                sizex=0.1, sizey=0.1,
                xanchor="right", yanchor="bottom"
            )
        )
    
    # Add hashtags
    hashtags = branding.get('hashtags', '#ZeroHunger #SDG2 #GlobalGoals')
    fig.add_annotation(
        text=hashtags,
        xref="paper", yref="paper",
        x=0.5, y=0.02,
        xanchor='center', yanchor='bottom',
        font=dict(size=12, color="gray"),
        showarrow=False
    )
    
    # Add website/attribution
    if branding.get('attribution'):
        fig.add_annotation(
            text=branding['attribution'],
            xref="paper", yref="paper",
            x=0.02, y=0.02,
            xanchor='left', yanchor='bottom',
            font=dict(size=10, color="gray"),
            showarrow=False
        )

def generate_share_link(content_data: Dict,
                       share_type: str = 'public_view',
                       expiry_days: int = 30,
                       password: str = None) -> Dict[str, str]:
    """
    Generate shareable links for visualizations
    
    Args:
        content_data: Dictionary containing the content to share
        share_type: Type of sharing (public_view, embed, collaborative)
        expiry_days: Number of days until link expires
        password: Optional password protection
        
    Returns:
        Dictionary with share link information
    """
    try:
        # Generate unique link ID
        link_id = str(uuid.uuid4())[:12]
        
        # Base URL (would be configured based on deployment)
        base_url = "https://sdg-hunger-dashboard.streamlit.app"
        
        share_info = {
            'link_id': link_id,
            'share_url': f"{base_url}/share/{link_id}",
            'share_type': share_type,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now().timestamp() + (expiry_days * 24 * 3600)) if expiry_days > 0 else None,
            'password_protected': password is not None,
            'content_type': content_data.get('type', 'visualization')
        }
        
        # Generate different types of sharing links
        if share_type == 'embed':
            share_info['embed_code'] = f'''<iframe src="{share_info['share_url']}/embed" 
                width="800" height="600" frameborder="0" 
                allowfullscreen></iframe>'''
        
        elif share_type == 'api':
            share_info['api_endpoint'] = f"{base_url}/api/v1/share/{link_id}"
            share_info['api_key'] = f"sdg_{str(uuid.uuid4()).replace('-', '')[:16]}"
        
        # Store share information (in a real implementation, this would go to a database)
        _store_share_data(link_id, content_data, share_info, password)
        
        return share_info
        
    except Exception as e:
        st.error(f"Error generating share link: {str(e)}")
        return {'error': str(e)}

def _store_share_data(link_id: str, content_data: Dict, share_info: Dict, password: str = None):
    """Store share data (placeholder implementation)"""
    # In a real implementation, this would store data in a database
    # For now, we'll simulate storage
    pass

def export_data_package(datasets: Dict[str, pd.DataFrame],
                       metadata: Dict = None,
                       format: str = 'zip') -> bytes:
    """
    Export multiple datasets as a data package
    
    Args:
        datasets: Dictionary of dataset names and DataFrames
        metadata: Optional metadata to include
        format: Export format (zip, tar)
        
    Returns:
        Binary data of the package
    """
    try:
        if format == 'zip':
            # Create in-memory zip file
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add datasets
                for name, df in datasets.items():
                    csv_data = df.to_csv(index=False)
                    zip_file.writestr(f"{name}.csv", csv_data)
                
                # Add metadata
                if metadata:
                    metadata_json = json.dumps(metadata, indent=2, default=str)
                    zip_file.writestr("metadata.json", metadata_json)
                
                # Add README
                readme_content = _generate_readme_content(datasets, metadata)
                zip_file.writestr("README.md", readme_content)
            
            zip_buffer.seek(0)
            return zip_buffer.getvalue()
            
    except Exception as e:
        st.error(f"Error creating data package: {str(e)}")
        return b"Export failed"

def _generate_readme_content(datasets: Dict[str, pd.DataFrame], metadata: Dict) -> str:
    """Generate README content for data package"""
    
    readme = f"""# SDG Goal 2 Data Package

## Overview
This package contains datasets related to SDG Goal 2: Zero Hunger indicators.

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Datasets Included

"""
    
    for name, df in datasets.items():
        readme += f"""### {name}
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Columns: {', '.join(df.columns.tolist())}

"""
    
    readme += """
## Data Sources
- FAO (Food and Agriculture Organization)
- UNICEF (United Nations Children's Fund)
- WHO (World Health Organization)  
- World Bank

## Usage
These datasets can be used for analysis, visualization, and research related to global hunger and malnutrition indicators.

## License
Data is provided under the terms of the respective source organizations.

## Contact
For questions about this data package, please refer to the original data sources.
"""
    
    return readme

def convert_figure_format(fig: go.Figure,
                         target_format: str,
                         **kwargs) -> bytes:
    """
    Convert Plotly figure to specified format
    
    Args:
        fig: Plotly figure object
        target_format: Target format (png, svg, pdf, html, json)
        **kwargs: Additional format-specific options
        
    Returns:
        Binary data in target format
    """
    try:
        if target_format.lower() == 'png':
            return pio.to_image(
                fig, 
                format='png',
                width=kwargs.get('width', 1200),
                height=kwargs.get('height', 800),
                scale=kwargs.get('scale', 2)
            )
        
        elif target_format.lower() == 'svg':
            return pio.to_image(fig, format='svg').encode('utf-8')
        
        elif target_format.lower() == 'pdf':
            return pio.to_image(fig, format='pdf')
        
        elif target_format.lower() == 'html':
            return pio.to_html(
                fig,
                include_plotlyjs=kwargs.get('include_plotlyjs', True),
                div_id=kwargs.get('div_id', None)
            ).encode('utf-8')
        
        elif target_format.lower() == 'json':
            return json.dumps(fig.to_dict(), indent=2).encode('utf-8')
        
        else:
            raise ValueError(f"Unsupported format: {target_format}")
            
    except Exception as e:
        st.error(f"Error converting figure to {target_format}: {str(e)}")
        return f"Conversion to {target_format} failed: {str(e)}".encode('utf-8')

def create_export_manifest(exports: List[Dict]) -> Dict:
    """
    Create manifest file for batch exports
    
    Args:
        exports: List of export operations
        
    Returns:
        Manifest dictionary
    """
    manifest = {
        'export_session': str(uuid.uuid4()),
        'created_at': datetime.now().isoformat(),
        'total_exports': len(exports),
        'formats': list(set([exp.get('format', 'unknown') for exp in exports])),
        'total_size_mb': sum([exp.get('size_mb', 0) for exp in exports]),
        'exports': exports
    }
    
    return manifest