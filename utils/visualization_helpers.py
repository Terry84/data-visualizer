import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime

class SDGVisualizationHelper:
    """
    Helper class for creating SDG Goal 2 specific visualizations
    """
    
    def __init__(self):
        # SDG official colors and theme
        self.sdg_colors = {
            'primary': '#e5243b',      # SDG Goal 2 official color
            'secondary': '#ff6b35',     # Complementary orange
            'success': '#2ecc71',       # Green for positive trends
            'warning': '#f39c12',       # Orange for warnings
            'danger': '#e74c3c',        # Red for critical issues
            'info': '#3498db',          # Blue for information
            'light': '#ecf0f1',         # Light gray
            'dark': '#2c3e50'           # Dark blue-gray
        }
        
        self.color_palettes = {
            'sdg_official': ['#e5243b', '#ff6b35', '#ffa500', '#ffcd00', '#2ecc71', '#3498db'],
            'hunger_severity': ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#8b0000'],
            'nutrition_status': ['#e74c3c', '#f39c12', '#2ecc71'],  # Malnutrition, At-risk, Healthy
            'regional': ['#e5243b', '#ff6347', '#ffa500', '#32cd32', '#4682b4', '#9370db', '#ff1493', '#00ced1']
        }
        
        # Regional coordinate mapping for maps
        self.regional_centers = {
            'Sub-Saharan Africa': {'lat': -1.0, 'lon': 15.0},
            'Southern Asia': {'lat': 20.0, 'lon': 77.0},
            'Western Asia': {'lat': 29.0, 'lon': 44.0},
            'Latin America & Caribbean': {'lat': -8.0, 'lon': -55.0},
            'Eastern Asia': {'lat': 35.0, 'lon': 104.0},
            'Northern Africa': {'lat': 28.0, 'lon': 10.0},
            'Oceania': {'lat': -25.0, 'lon': 140.0},
            'Europe & Northern America': {'lat': 54.0, 'lon': 15.0}
        }

def create_hunger_overview_chart(data: pd.DataFrame, 
                                chart_type: str = 'bar',
                                color_scheme: str = 'sdg_official',
                                title: str = None) -> go.Figure:
    """
    Create hunger rate overview chart
    
    Args:
        data: DataFrame with hunger data
        chart_type: Type of chart ('bar', 'horizontal_bar', 'treemap', 'pie')
        color_scheme: Color scheme to use
        title: Custom title for the chart
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        return _create_empty_state_chart("No hunger data available")
    
    helper = SDGVisualizationHelper()
    colors = helper.color_palettes.get(color_scheme, helper.color_palettes['sdg_official'])
    
    if title is None:
        title = "Hunger Prevalence by Region"
    
    try:
        if chart_type == 'bar':
            fig = px.bar(
                data,
                x='Region' if 'Region' in data.columns else data.columns[0],
                y='Hunger Rate' if 'Hunger Rate' in data.columns else data.columns[1],
                color='Hunger Rate' if 'Hunger Rate' in data.columns else data.columns[1],
                color_continuous_scale=colors[0],
                title=title,
                labels={'Hunger Rate': 'Hunger Rate (%)', 'Region': 'Region'}
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                height=500,
                showlegend=False
            )
            
        elif chart_type == 'horizontal_bar':
            fig = px.bar(
                data.sort_values('Hunger Rate' if 'Hunger Rate' in data.columns else data.columns[1]),
                x='Hunger Rate' if 'Hunger Rate' in data.columns else data.columns[1],
                y='Region' if 'Region' in data.columns else data.columns[0],
                orientation='h',
                color='Hunger Rate' if 'Hunger Rate' in data.columns else data.columns[1],
                color_continuous_scale=colors[0],
                title=title
            )
            fig.update_layout(height=600, showlegend=False)
            
        elif chart_type == 'treemap':
            # Add population data if not available
            if 'Population' not in data.columns:
                data['Population'] = np.random.randint(50, 2000, len(data))  # Millions
                
            fig = px.treemap(
                data,
                path=['Region'],
                values='Population',
                color='Hunger Rate' if 'Hunger Rate' in data.columns else data.columns[1],
                color_continuous_scale=colors[0],
                title=title
            )
            
        elif chart_type == 'pie':
            # Calculate hungry population
            if 'Population' not in data.columns:
                data['Population'] = np.random.randint(50, 2000, len(data))
            
            data['Hungry Population'] = (data['Hunger Rate'] * data['Population'] / 100).round(1)
            
            fig = px.pie(
                data,
                values='Hungry Population',
                names='Region',
                title=f"{title} - Distribution of Hungry Population",
                color_discrete_sequence=colors
            )
            
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        # Add data source annotation
        fig.add_annotation(
            text="Source: FAO, UNICEF, WHO (2024)",
            xref="paper", yref="paper",
            x=1, y=-0.1,
            xanchor='right', yanchor='bottom',
            font=dict(size=10, color="gray")
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating hunger overview chart: {str(e)}")
        return _create_error_chart(f"Chart creation failed: {str(e)}")

def create_malnutrition_chart(data: pd.DataFrame,
                             indicators: List[str] = None,
                             chart_type: str = 'grouped_bar',
                             title: str = None) -> go.Figure:
    """
    Create child malnutrition visualization
    
    Args:
        data: DataFrame with malnutrition data
        indicators: List of indicators to include
        chart_type: Type of chart ('grouped_bar', 'stacked_bar', 'radar', 'heatmap')
        title: Custom title
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        return _create_empty_state_chart("No malnutrition data available")
    
    helper = SDGVisualizationHelper()
    colors = helper.color_palettes['nutrition_status']
    
    if indicators is None:
        indicators = ['Child Stunting', 'Child Wasting', 'Child Overweight']
    
    if title is None:
        title = "Child Malnutrition Status by Region"
    
    try:
        # Ensure we have the required columns
        available_indicators = [col for col in indicators if col in data.columns]
        if not available_indicators:
            return _create_empty_state_chart("No malnutrition indicators found in data")
        
        if chart_type == 'grouped_bar':
            # Reshape data for grouped bar chart
            melted_data = data.melt(
                id_vars=['Region'] if 'Region' in data.columns else [data.columns[0]],
                value_vars=available_indicators,
                var_name='Indicator',
                value_name='Percentage'
            )
            
            fig = px.bar(
                melted_data,
                x='Region',
                y='Percentage',
                color='Indicator',
                barmode='group',
                color_discrete_sequence=colors,
                title=title,
                labels={'Percentage': 'Percentage (%)', 'Region': 'Region'}
            )
            fig.update_xaxis(tickangle=-45)
            
        elif chart_type == 'stacked_bar':
            fig = go.Figure()
            
            for i, indicator in enumerate(available_indicators):
                fig.add_trace(go.Bar(
                    name=indicator,
                    x=data['Region'] if 'Region' in data.columns else data.iloc[:, 0],
                    y=data[indicator],
                    marker_color=colors[i % len(colors)]
                ))
            
            fig.update_layout(
                barmode='stack',
                title=title,
                xaxis_title='Region',
                yaxis_title='Percentage (%)',
                xaxis_tickangle=-45
            )
            
        elif chart_type == 'radar':
            fig = go.Figure()
            
            for _, row in data.iterrows():
                region_name = row['Region'] if 'Region' in data.columns else row.iloc[0]
                values = [row[indicator] for indicator in available_indicators]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=available_indicators,
                    fill='toself',
                    name=region_name,
                    line_color=colors[_ % len(colors)]
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max([data[col].max() for col in available_indicators]) * 1.1]
                    )
                ),
                title=title,
                showlegend=True
            )
            
        elif chart_type == 'heatmap':
            # Prepare heatmap data
            heatmap_data = data.set_index('Region' if 'Region' in data.columns else data.columns[0])
            heatmap_data = heatmap_data[available_indicators]
            
            fig = px.imshow(
                heatmap_data.values,
                labels=dict(x="Indicator", y="Region", color="Percentage"),
                x=available_indicators,
                y=heatmap_data.index,
                color_continuous_scale='Reds',
                title=title
            )
            
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        fig.update_layout(height=500)
        
        # Add data source
        fig.add_annotation(
            text="Source: UNICEF, WHO Joint Malnutrition Estimates (2025)",
            xref="paper", yref="paper",
            x=1, y=-0.15,
            xanchor='right', yanchor='bottom',
            font=dict(size=10, color="gray")
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating malnutrition chart: {str(e)}")
        return _create_error_chart(f"Chart creation failed: {str(e)}")

def create_world_map(data: pd.DataFrame,
                    indicator: str = 'Hunger Rate',
                    map_type: str = 'choropleth',
                    projection: str = 'robinson',
                    title: str = None) -> go.Figure:
    """
    Create world map visualization
    
    Args:
        data: DataFrame with geographic data
        indicator: Column name for the indicator to visualize
        map_type: Type of map ('choropleth', 'bubble', 'scatter_geo')
        projection: Map projection
        title: Custom title
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        return _create_empty_state_chart("No geographic data available")
    
    helper = SDGVisualizationHelper()
    
    if title is None:
        title = f"Global {indicator} Distribution"
    
    try:
        if map_type == 'choropleth':
            fig = px.choropleth(
                data,
                locations='Country Code' if 'Country Code' in data.columns else 'country_code',
                color=indicator,
                hover_name='Country' if 'Country' in data.columns else 'country_name',
                color_continuous_scale='Reds',
                title=title,
                projection=projection
            )
            
        elif map_type == 'bubble':
            # Add population data if not available for bubble size
            if 'Population' not in data.columns:
                data['Population'] = np.random.randint(1, 1400, len(data))  # Millions
                
            fig = px.scatter_geo(
                data,
                locations='Country Code' if 'Country Code' in data.columns else 'country_code',
                color=indicator,
                size='Population',
                hover_name='Country' if 'Country' in data.columns else 'country_name',
                color_continuous_scale='Reds',
                title=title,
                projection=projection,
                size_max=50
            )
            
        elif map_type == 'scatter_geo':
            fig = px.scatter_geo(
                data,
                locations='Country Code' if 'Country Code' in data.columns else 'country_code',
                color=indicator,
                hover_name='Country' if 'Country' in data.columns else 'country_name',
                color_continuous_scale='Reds',
                title=title,
                projection=projection
            )
            
        else:
            raise ValueError(f"Unsupported map type: {map_type}")
        
        fig.update_layout(
            height=600,
            geo=dict(showframe=False, showcoastlines=True)
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating world map: {str(e)}")
        return _create_error_chart(f"Map creation failed: {str(e)}")

def create_trend_chart(data: pd.DataFrame,
                      x_column: str = 'Year',
                      y_column: str = 'Value',
                      group_column: str = 'Region',
                      chart_type: str = 'line',
                      title: str = None) -> go.Figure:
    """
    Create trend analysis chart
    
    Args:
        data: DataFrame with time series data
        x_column: Column name for x-axis (usually time)
        y_column: Column name for y-axis (values)
        group_column: Column name for grouping/colors
        chart_type: Type of chart ('line', 'area', 'bar')
        title: Custom title
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        return _create_empty_state_chart("No trend data available")
    
    helper = SDGVisualizationHelper()
    colors = helper.color_palettes['regional']
    
    if title is None:
        title = f"{y_column} Trends Over Time"
    
    try:
        if chart_type == 'line':
            fig = px.line(
                data,
                x=x_column,
                y=y_column,
                color=group_column,
                color_discrete_sequence=colors,
                title=title,
                markers=True
            )
            
        elif chart_type == 'area':
            fig = px.area(
                data,
                x=x_column,
                y=y_column,
                color=group_column,
                color_discrete_sequence=colors,
                title=title
            )
            
        elif chart_type == 'bar':
            fig = px.bar(
                data,
                x=x_column,
                y=y_column,
                color=group_column,
                color_discrete_sequence=colors,
                title=title,
                barmode='group'
            )
            
        else:
            raise ValueError(f"Unsupported trend chart type: {chart_type}")
        
        # Add SDG adoption line
        if x_column == 'Year' and data[x_column].min() <= 2015 <= data[x_column].max():
            fig.add_vline(
                x=2015,
                line_dash="dash",
                line_color="gray",
                annotation_text="SDGs Adopted"
            )
        
        # Add COVID-19 impact line
        if x_column == 'Year' and data[x_column].min() <= 2020 <= data[x_column].max():
            fig.add_vline(
                x=2020,
                line_dash="dash",
                line_color="red",
                annotation_text="COVID-19 Pandemic"
            )
        
        fig.update_layout(height=500)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating trend chart: {str(e)}")
        return _create_error_chart(f"Trend chart creation failed: {str(e)}")

def create_comparison_chart(data: pd.DataFrame,
                           x_indicator: str,
                           y_indicator: str,
                           size_indicator: str = None,
                           color_indicator: str = None,
                           chart_type: str = 'scatter',
                           title: str = None) -> go.Figure:
    """
    Create comparison/correlation chart
    
    Args:
        data: DataFrame with comparison data
        x_indicator: Column name for x-axis
        y_indicator: Column name for y-axis
        size_indicator: Column name for bubble size (optional)
        color_indicator: Column name for colors (optional)
        chart_type: Type of chart ('scatter', 'bubble')
        title: Custom title
        
    Returns:
        Plotly Figure object
    """
    if data.empty:
        return _create_empty_state_chart("No comparison data available")
    
    helper = SDGVisualizationHelper()
    
    if title is None:
        title = f"{y_indicator} vs {x_indicator}"
    
    try:
        if chart_type == 'scatter':
            fig = px.scatter(
                data,
                x=x_indicator,
                y=y_indicator,
                color=color_indicator,
                size=size_indicator,
                hover_name='Region' if 'Region' in data.columns else data.columns[0],
                title=title,
                color_continuous_scale='Reds' if color_indicator else None,
                color_discrete_sequence=helper.color_palettes['regional'] if not color_indicator else None
            )
            
        elif chart_type == 'bubble':
            if size_indicator is None:
                # Use population or create dummy size data
                if 'Population' not in data.columns:
                    data['Population'] = np.random.randint(10, 1400, len(data))
                size_indicator = 'Population'
                
            fig = px.scatter(
                data,
                x=x_indicator,
                y=y_indicator,
                size=size_indicator,
                color=color_indicator or 'Region',
                hover_name='Region' if 'Region' in data.columns else data.columns[0],
                title=title,
                size_max=60
            )
            
        else:
            raise ValueError(f"Unsupported comparison chart type: {chart_type}")
        
        fig.update_layout(height=500)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating comparison chart: {str(e)}")
        return _create_error_chart(f"Comparison chart creation failed: {str(e)}")

def create_progress_chart(current_values: Dict[str, float],
                         targets: Dict[str, float],
                         chart_type: str = 'gauge',
                         title: str = None) -> go.Figure:
    """
    Create SDG progress tracking visualization
    
    Args:
        current_values: Dictionary of current indicator values
        targets: Dictionary of 2030 target values
        chart_type: Type of chart ('gauge', 'progress_bar', 'bullet')
        title: Custom title
        
    Returns:
        Plotly Figure object
    """
    helper = SDGVisualizationHelper()
    
    if title is None:
        title = "SDG Goal 2 Progress Toward 2030 Targets"
    
    try:
        if chart_type == 'gauge':
            # Create subplot for multiple gauges
            indicators = list(current_values.keys())
            cols = min(len(indicators), 3)
            rows = (len(indicators) + cols - 1) // cols
            
            fig = make_subplots(
                rows=rows, cols=cols,
                specs=[[{"type": "indicator"}] * cols] * rows,
                subplot_titles=indicators
            )
            
            for i, (indicator, current) in enumerate(current_values.items()):
                target = targets.get(indicator, 100)
                progress = min(100, (current / target) * 100) if target > 0 else 0
                
                row = (i // cols) + 1
                col = (i % cols) + 1
                
                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=progress,
                        title={"text": f"{indicator}<br>Progress"},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": helper.sdg_colors['primary']},
                            "steps": [
                                {"range": [0, 50], "color": "lightgray"},
                                {"range": [50, 80], "color": "gray"}
                            ],
                            "threshold": {
                                "line": {"color": "red", "width": 4},
                                "thickness": 0.75,
                                "value": 90
                            }
                        }
                    ),
                    row=row, col=col
                )
            
        elif chart_type == 'progress_bar':
            fig = go.Figure()
            
            indicators = list(current_values.keys())
            progress_values = []
            
            for indicator in indicators:
                current = current_values[indicator]
                target = targets.get(indicator, 100)
                progress = min(100, (current / target) * 100) if target > 0 else 0
                progress_values.append(progress)
            
            fig.add_trace(go.Bar(
                y=indicators,
                x=progress_values,
                orientation='h',
                marker_color=helper.sdg_colors['primary'],
                name='Progress %'
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Progress (%)",
                yaxis_title="SDG Indicators",
                xaxis_range=[0, 100]
            )
            
        else:
            raise ValueError(f"Unsupported progress chart type: {chart_type}")
        
        fig.update_layout(title=title, height=600)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating progress chart: {str(e)}")
        return _create_error_chart(f"Progress chart creation failed: {str(e)}")

def create_infographic_chart(key_stats: Dict[str, Union[str, float]],
                           layout: str = 'grid',
                           color_scheme: str = 'sdg_official') -> go.Figure:
    """
    Create infographic-style visualization for social media
    
    Args:
        key_stats: Dictionary of key statistics to display
        layout: Layout type ('grid', 'vertical', 'horizontal')
        color_scheme: Color scheme to use
        
    Returns:
        Plotly Figure object
    """
    helper = SDGVisualizationHelper()
    colors = helper.color_palettes.get(color_scheme, helper.color_palettes['sdg_official'])
    
    try:
        fig = go.Figure()
        
        if layout == 'grid':
            # Create grid layout for statistics
            stats_items = list(key_stats.items())
            
            for i, (label, value) in enumerate(stats_items[:6]):  # Max 6 items
                x_pos = (i % 2) * 0.5 + 0.25  # 2 columns
                y_pos = 0.8 - (i // 2) * 0.3   # 3 rows
                
                # Add statistic value
                fig.add_annotation(
                    x=x_pos, y=y_pos,
                    text=str(value),
                    font=dict(size=40, color=colors[i % len(colors)], family="Arial Black"),
                    showarrow=False
                )
                
                # Add label
                fig.add_annotation(
                    x=x_pos, y=y_pos - 0.1,
                    text=label,
                    font=dict(size=14, color="black"),
                    showarrow=False
                )
        
        fig.update_layout(
            width=1080, height=1080,  # Instagram square format
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0, 1]),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title="SDG Goal 2: Zero Hunger Key Statistics"
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating infographic: {str(e)}")
        return _create_error_chart(f"Infographic creation failed: {str(e)}")

def create_social_media_chart(data: pd.DataFrame,
                             platform: str = 'instagram',
                             content_type: str = 'statistic',
                             main_message: str = None) -> go.Figure:
    """
    Create social media optimized visualization
    
    Args:
        data: DataFrame with data to visualize
        platform: Target platform ('instagram', 'twitter', 'facebook')
        content_type: Type of content ('statistic', 'chart', 'infographic')
        main_message: Main message to highlight
        
    Returns:
        Plotly Figure object optimized for social media
    """
    helper = SDGVisualizationHelper()
    
    # Platform-specific dimensions
    dimensions = {
        'instagram': {'width': 1080, 'height': 1080},
        'twitter': {'width': 1200, 'height': 675},
        'facebook': {'width': 1200, 'height': 630}
    }
    
    dim = dimensions.get(platform, dimensions['instagram'])
    
    try:
        fig = go.Figure()
        
        if content_type == 'statistic' and main_message:
            # Extract number and text from main message
            import re
            numbers = re.findall(r'[\d.]+[MBK]?', main_message)
            main_stat = numbers[0] if numbers else "N/A"
            
            fig.add_annotation(
                x=0.5, y=0.6,
                text=main_stat,
                font=dict(size=80, color=helper.sdg_colors['primary'], family="Arial Black"),
                showarrow=False
            )
            
            # Add context text
            context_text = main_message.replace(main_stat, "").strip()
            fig.add_annotation(
                x=0.5, y=0.4,
                text=context_text[:50] + "..." if len(context_text) > 50 else context_text,
                font=dict(size=24, color="black"),
                showarrow=False
            )
            
            # Add SDG branding
            fig.add_annotation(
                x=0.5, y=0.2,
                text="#ZeroHunger #SDG2 #GlobalGoals",
                font=dict(size=16, color=helper.sdg_colors['secondary']),
                showarrow=False
            )
        
        fig.update_layout(
            width=dim['width'],
            height=dim['height'],
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0, 1]),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating social media chart: {str(e)}")
        return _create_error_chart(f"Social media chart creation failed: {str(e)}")

def _create_empty_state_chart(message: str) -> go.Figure:
    """Create empty state visualization"""
    fig = go.Figure()
    
    fig.add_annotation(
        x=0.5, y=0.5,
        text=message,
        font=dict(size=20, color="gray"),
        showarrow=False
    )
    
    fig.update_layout(
        width=800, height=400,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def _create_error_chart(error_message: str) -> go.Figure:
    """Create error state visualization"""
    fig = go.Figure()
    
    fig.add_annotation(
        x=0.5, y=0.6,
        text="❌ Visualization Error",
        font=dict(size=24, color="red"),
        showarrow=False
    )
    
    fig.add_annotation(
        x=0.5, y=0.4,
        text=error_message,
        font=dict(size=14, color="gray"),
        showarrow=False
    )
    
    fig.update_layout(
        width=800, height=400,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig