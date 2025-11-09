"""
Streamlit UI for EV Battery Health Prediction

This application provides a user-friendly interface to predict battery health
by connecting to the Flask API backend.
"""

import streamlit as st
import requests
import json
import plotly.graph_objects as go
from typing import Dict, Any, Optional
import os
from datetime import datetime
import io

# PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Try to import OpenAI, fallback to HuggingFace if not available
OPENAI_AVAILABLE = False
HUGGINGFACE_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from transformers import pipeline
    import torch
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="EV Battery Health Prediction",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .stSlider > div > div > div {
        background-color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
API_URL = os.getenv("FLASK_API_URL", "http://127.0.0.1:5000")

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

@st.cache_data(ttl=300)  # Cache for 5 minutes
def check_api_health() -> bool:
    """Check if the Flask API is running and healthy."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get('model_loaded', False) and data.get('scaler_loaded', False)
        return False
    except requests.exceptions.RequestException:
        return False

def predict_battery_health(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Send prediction request to Flask API.
    
    Args:
        data: Dictionary containing battery parameters
    
    Returns:
        Prediction results or None if error
    """
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            st.error(f"API Error: {error_data.get('error', 'Unknown error')}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(" Cannot connect to the API. Please ensure the Flask server is running on http://127.0.0.1:5000")
        return None
    except requests.exceptions.Timeout:
        st.error(" Request timed out. Please try again.")
        return None
    except Exception as e:
        st.error(f" Unexpected error: {str(e)}")
        return None

def create_battery_health_gauge(health_percentage: float) -> go.Figure:
    """
    Create a gauge chart for battery health percentage.
    
    Args:
        health_percentage: Battery health percentage (0-100)
    
    Returns:
        Plotly figure object
    """
    # Determine color based on health percentage
    if health_percentage >= 80:
        color = '#28a745'  # Green
        status = "Excellent"
    elif health_percentage >= 60:
        color = '#ffc107'  # Yellow
        status = "Good"
    elif health_percentage >= 40:
        color = '#fd7e14'  # Orange
        status = "Fair"
    else:
        color = '#dc3545'  # Red
        status = "Poor"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = health_percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Battery Health: {status}", 'font': {'size': 24}},
        delta = {'reference': 100, 'position': "top"},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#dc3545'},
                {'range': [40, 60], 'color': '#fd7e14'},
                {'range': [60, 80], 'color': '#ffc107'},
                {'range': [80, 100], 'color': '#28a745'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 20
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"},
        height=400
    )
    
    return fig

def create_progress_bar(health_percentage: float) -> str:
    """Create HTML progress bar for battery health."""
    # Determine color based on health
    if health_percentage >= 80:
        color = '#28a745'
    elif health_percentage >= 60:
        color = '#ffc107'
    elif health_percentage >= 40:
        color = '#fd7e14'
    else:
        color = '#dc3545'
    
    return f"""
    <div style="background-color: #f0f0f0; border-radius: 10px; padding: 3px;">
        <div style="background-color: {color}; width: {health_percentage}%; 
                    height: 30px; border-radius: 8px; display: flex; 
                    align-items: center; justify-content: center; color: white; 
                    font-weight: bold; transition: width 0.5s;">
            {health_percentage:.1f}%
        </div>
    </div>
    """

def generate_ai_insights_openai(
    input_data: Dict[str, Any],
    prediction_result: Dict[str, Any],
    api_key: str
) -> Optional[str]:
    """
    Generate AI insights using OpenAI API.
    
    Args:
        input_data: Battery input parameters
        prediction_result: Prediction results from the model
        api_key: OpenAI API key
    
    Returns:
        AI-generated insights string or None if error
    """
    if not OPENAI_AVAILABLE:
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Create prompt for AI analysis
        health_pct = prediction_result.get('battery_health_percentage', 50)
        rul = prediction_result.get('predicted_rul', 500)
        temp = input_data.get('battery_temperature', 25)
        voltage = input_data.get('voltage', 3.7)
        current = input_data.get('current', 1.0)
        cycles = input_data.get('charging_cycles', 500)
        soc = input_data.get('state_of_charge', 75)
        
        prompt = f"""You are an expert EV battery health analyst. Analyze the following battery parameters and provide clear, actionable insights.

Battery Status:
- Health: {health_pct:.1f}%
- Remaining Useful Life (RUL): {rul:.0f} cycles
- Temperature: {temp}°C
- Voltage: {voltage}V
- Current: {current}A
- Charging Cycles: {cycles}
- State of Charge: {soc}%

Please provide:
1. A brief analysis (2-3 sentences) explaining why the battery health is at {health_pct:.1f}%
2. Identify the MAIN factor(s) causing health decline (e.g., "Your battery health is declining mainly due to high temperature" or "Try keeping your charging cycles below 600 to extend lifespan")
3. Provide 2-3 specific, actionable recommendations
4. Use a friendly, professional tone with appropriate emojis

Keep the response concise (100-150 words) and focused on practical advice."""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert battery health analyst providing clear, actionable insights about EV battery health."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.warning(f"⚠️ OpenAI API error: {str(e)}")
        return None

def generate_ai_insights_huggingface(
    input_data: Dict[str, Any],
    prediction_result: Dict[str, Any]
) -> Optional[str]:
    """
    Generate AI insights using HuggingFace transformers (fallback).
    
    Args:
        input_data: Battery input parameters
        prediction_result: Prediction results from the model
    
    Returns:
        AI-generated insights string or None if error
    """
    if not HUGGINGFACE_AVAILABLE:
        return None
    
    try:
        # Cache the model in session state to avoid reloading
        if 'hf_generator' not in st.session_state:
            with st.spinner("Loading HuggingFace model (first time only)..."):
                st.session_state['hf_generator'] = pipeline(
                    "text-generation",
                    model="gpt2",  # Can be changed to a more suitable model
                    device=0 if torch.cuda.is_available() else -1
                )
        
        generator = st.session_state['hf_generator']
        
        # Create a more structured prompt for better results
        health_pct = prediction_result.get('battery_health_percentage', 50)
        temp = input_data.get('battery_temperature', 25)
        cycles = input_data.get('charging_cycles', 500)
        voltage = input_data.get('voltage', 3.7)
        
        # Generate context-aware insights
        insights_parts = []
        
        # Analyze health status
        if health_pct < 40:
            insights_parts.append(f"🔴 Your battery health is critically low at {health_pct:.1f}%.")
        elif health_pct < 60:
            insights_parts.append(f"🟡 Your battery health is declining at {health_pct:.1f}%.")
        elif health_pct >= 80:
            insights_parts.append(f"✅ Your battery health is excellent at {health_pct:.1f}%.")
        else:
            insights_parts.append(f"🟠 Your battery health is fair at {health_pct:.1f}%.")
        
        # Analyze main factors
        factors = []
        if temp > 45:
            factors.append("high temperature")
        elif temp < 0:
            factors.append("low temperature")
        if cycles > 1000:
            factors.append("high cycle count")
        if voltage < 3.2:
            factors.append("low voltage")
        elif voltage > 4.3:
            factors.append("high voltage")
        
        if factors:
            insights_parts.append(f"Main contributing factors: {', '.join(factors)}.")
        
        # Generate recommendations
        recommendations = []
        if temp > 45:
            recommendations.append("Keep the battery cool (below 35°C) to extend lifespan.")
        if cycles > 1000:
            recommendations.append(f"With {cycles} cycles, consider planning for battery replacement soon.")
        if voltage < 3.2:
            recommendations.append("Charge the battery to maintain optimal voltage levels.")
        if health_pct < 60:
            recommendations.append("Monitor battery health regularly and adjust usage patterns.")
        
        if recommendations:
            insights_parts.append("Recommendations: " + " ".join(recommendations))
        
        # Combine insights
        insights = " ".join(insights_parts)
        
        return insights
    
    except Exception as e:
        st.warning(f"⚠️ HuggingFace error: {str(e)}")
        return None

def generate_ai_insights(
    input_data: Dict[str, Any],
    prediction_result: Dict[str, Any],
    api_key: Optional[str] = None,
    use_openai: bool = True
) -> Optional[str]:
    """
    Generate AI insights using OpenAI or HuggingFace.
    
    Args:
        input_data: Battery input parameters
        prediction_result: Prediction results from the model
        api_key: OpenAI API key (required if use_openai=True)
        use_openai: Whether to use OpenAI (True) or HuggingFace (False)
    
    Returns:
        AI-generated insights string or None if error
    """
    # Try OpenAI first if requested and available
    if use_openai and OPENAI_AVAILABLE and api_key:
        insights = generate_ai_insights_openai(input_data, prediction_result, api_key)
        if insights:
            return insights
    
    # Fallback to HuggingFace
    if HUGGINGFACE_AVAILABLE:
        insights = generate_ai_insights_huggingface(input_data, prediction_result)
        if insights:
            return insights
    
    # If both fail, return None
    return None

def get_health_recommendations(data: Dict[str, Any], health_percentage: float) -> list:
    """Generate recommendations based on battery parameters and health."""
    recommendations = []
    
    # Temperature recommendations
    temp = data.get('battery_temperature', 25)
    if temp > 45:
        recommendations.append("🔥 High temperature detected! Keep battery cool to extend lifespan.")
    elif temp < 0:
        recommendations.append("❄️ Low temperature detected! Battery performance may be reduced.")
    
    # Voltage recommendations
    voltage = data.get('voltage', 3.7)
    if voltage < 3.2:
        recommendations.append("⚠️ Low voltage detected! Battery may need charging.")
    elif voltage > 4.3:
        recommendations.append("⚠️ High voltage detected! Monitor battery carefully.")
    
    # Current recommendations
    current = data.get('current', 1.0)
    if current > 5:
        recommendations.append("⚡ High current draw detected! This may accelerate degradation.")
    
    # Cycle recommendations
    cycles = data.get('charging_cycles', 0)
    if cycles > 1000:
        recommendations.append("🔄 High cycle count! Consider battery replacement soon.")
    
    # Health-based recommendations
    if health_percentage < 40:
        recommendations.append("🔴 Battery health is critically low! Consider replacement.")
    elif health_percentage < 60:
        recommendations.append("🟡 Battery health is declining. Monitor closely.")
    elif health_percentage >= 80:
        recommendations.append(" Battery health is excellent! Continue proper maintenance.")
    
    return recommendations

def display_ai_configuration():
    """Display AI configuration section in the sidebar."""
    st.sidebar.markdown("### AI Insights Configuration")
    
    # AI Provider selection
    ai_provider = st.sidebar.selectbox(
        "AI Provider",
        options=["OpenAI (GPT-4)", "HuggingFace", "Disabled"],
        index=0,
        help="Select AI provider for generating insights"
    )
    
    use_openai = ai_provider == "OpenAI (GPT-4)"
    use_huggingface = ai_provider == "HuggingFace"
    ai_enabled = ai_provider != "Disabled"
    
    api_key = None
    if use_openai:
        # Try to get API key from environment variable first
        api_key = os.getenv("OPENAI_API_KEY")
        
        # Allow user to input API key
        api_key_input = st.sidebar.text_input(
            "OpenAI API Key",
            value=api_key if api_key else "",
            type="password",
            help="Enter your OpenAI API key. You can also set OPENAI_API_KEY environment variable."
        )
        
        if api_key_input:
            api_key = api_key_input
        elif not api_key:
            st.sidebar.warning("⚠️ OpenAI API key required for AI insights")
    
    # Store in session state
    st.session_state['ai_enabled'] = ai_enabled
    st.session_state['use_openai'] = use_openai
    st.session_state['use_huggingface'] = use_huggingface
    st.session_state['openai_api_key'] = api_key if use_openai else None
    
    # Display availability status
    if ai_enabled:
        if use_openai:
            if OPENAI_AVAILABLE:
                if api_key:
                    st.sidebar.success("✅ OpenAI ready")
                else:
                    st.sidebar.warning("⚠️ OpenAI available but API key needed")
            else:
                st.sidebar.error(" OpenAI library not installed. Install with: pip install openai")
        elif use_huggingface:
            if HUGGINGFACE_AVAILABLE:
                st.sidebar.success("✅ HuggingFace available")
                st.sidebar.caption("ℹ️ Using rule-based insights")
            else:
                st.sidebar.error(" HuggingFace not installed. Install with: pip install transformers torch")
        
        # Add info about AI feature
        with st.sidebar.expander("ℹ️ About AI Insights", expanded=False):
            st.markdown("""
            **AI Insights** provide intelligent analysis of your battery health:
            
            - **OpenAI GPT-4**: Advanced AI analysis with natural language
            - **HuggingFace**: Rule-based insights (free, local)
            
            Insights are generated after predictions and include:
            - Health status analysis
            - Main contributing factors
            - Actionable recommendations
            
            See `AI_SETUP.md` for setup instructions.
            """)
    
    return ai_enabled, use_openai, api_key

def generate_pdf_report(
    input_data: Dict[str, Any],
    prediction_result: Dict[str, Any],
    ai_insights: Optional[str] = None,
    recommendations: list = None
) -> bytes:
    """
    Generate a PDF report with battery health prediction results.
    
    Args:
        input_data: Battery input parameters
        prediction_result: Prediction results
        ai_insights: AI-generated insights (optional)
        recommendations: List of recommendations (optional)
    
    Returns:
        PDF file as bytes
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("🔋 EV Battery Health Prediction Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Input Data Section
    story.append(Paragraph("Input Parameters", heading_style))
    input_table_data = [
        ['Parameter', 'Value'],
        ['Battery Temperature', f"{input_data.get('battery_temperature', 'N/A')}°C"],
        ['Voltage', f"{input_data.get('voltage', 'N/A')}V"],
        ['Current', f"{input_data.get('current', 'N/A')}A"],
        ['Charging Cycles', f"{input_data.get('charging_cycles', 'N/A')}"],
        ['State of Charge', f"{input_data.get('state_of_charge', 'N/A')}%"]
    ]
    input_table = Table(input_table_data, colWidths=[3*inch, 2*inch])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(input_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Prediction Results Section
    story.append(Paragraph("Prediction Results", heading_style))
    health_pct = prediction_result.get('battery_health_percentage', 0)
    rul = prediction_result.get('predicted_rul', 0)
    
    results_table_data = [
        ['Metric', 'Value'],
        ['Battery Health', f"{health_pct:.2f}%"],
        ['Predicted RUL', f"{rul:.1f} cycles"]
    ]
    results_table = Table(results_table_data, colWidths=[3*inch, 2*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(results_table)
    story.append(Spacer(1, 0.3*inch))
    
    # AI Insights Section
    if ai_insights:
        story.append(Paragraph("AI-Generated Insights", heading_style))
        story.append(Paragraph(ai_insights, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
    
    # Recommendations Section
    if recommendations:
        story.append(Paragraph("Recommendations", heading_style))
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
    else:
        story.append(Paragraph("Recommendations", heading_style))
        story.append(Paragraph(" All parameters are within optimal ranges!", styles['Normal']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("EV Battery Health Prediction System", 
                          ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)))
    story.append(Paragraph("Powered by Machine Learning & AI", 
                          ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def toggle_theme():
    """Toggle between light and dark theme."""
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

def apply_theme():
    """Apply theme based on session state."""
    theme = st.session_state.get('theme', 'light')
    
    if theme == 'dark':
        st.markdown("""
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .main-header {
            color: #4CAF50;
        }
        .info-box {
            background-color: #2d2d2d;
            color: #ffffff;
        }
        .metric-card {
            background-color: #2d2d2d;
        }
        .stMetric {
            background-color: #2d2d2d;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light theme is default
        pass

def display_parameter_info():
    """Display information about battery parameters in the sidebar."""
    st.sidebar.markdown("### 📊 Parameter Information")
    
    with st.sidebar.expander("🌡️ Battery Temperature", expanded=False):
        st.markdown("""
        **Range:** -20°C to 60°C
        
        **Impact:**
        - High temperature (>45°C) accelerates degradation
        - Low temperature (<0°C) reduces performance
        - Optimal range: 15°C to 35°C
        """)
    
    with st.sidebar.expander("⚡ Voltage", expanded=False):
        st.markdown("""
        **Range:** 2.5V to 4.5V
        
        **Impact:**
        - Low voltage (<3.2V) indicates low charge
        - High voltage (>4.3V) may indicate overcharging
        - Normal operating range: 3.0V to 4.2V
        """)
    
    with st.sidebar.expander("🔌 Current", expanded=False):
        st.markdown("""
        **Range:** 0A to 10A
        
        **Impact:**
        - High current draws accelerate degradation
        - Optimal charging current: 0.5C to 1C
        - Fast charging (>2C) reduces battery lifespan
        """)
    
    with st.sidebar.expander("🔄 Charging Cycles", expanded=False):
        st.markdown("""
        **Range:** 0 to 10,000 cycles
        
        **Impact:**
        - Each cycle reduces capacity slightly
        - Typical lifespan: 500-2000 cycles
        - Cycles >1000 indicate aging battery
        """)
    
    with st.sidebar.expander("📊 State of Charge", expanded=False):
        st.markdown("""
        **Range:** 0% to 100%
        
        **Impact:**
        - Keep between 20% and 80% for optimal lifespan
        - Avoid deep discharge (<10%)
        - Avoid full charge (>95%) for extended periods
        """)

def main():
    """Main application function."""
    # Apply theme
    apply_theme()
    
    # Header with theme toggle
    col_header1, col_header2 = st.columns([5, 1])
    with col_header1:
        st.markdown('<h1 class="main-header">🔋 EV Battery Health Prediction</h1>', unsafe_allow_html=True)
    with col_header2:
        theme_icon = "🌙" if st.session_state.get('theme', 'light') == 'light' else "☀️"
        if st.button(theme_icon, help="Toggle dark/light mode"):
            toggle_theme()
            st.rerun()
    
    st.markdown("---")
    
    # Check API health
    api_healthy = check_api_health()
    
    if not api_healthy:
        st.error("""
        ⚠️ **API Connection Failed**
        
        Please ensure the Flask API server is running:
        1. Open a terminal
        2. Navigate to the project directory
        3. Run: `python app.py`
        4. Wait for the server to start on http://127.0.0.1:5000
        5. Refresh this page
        """)
        st.stop()
    
    # Sidebar for inputs
    st.sidebar.title("⚙️ Battery Parameters")
    st.sidebar.markdown("Adjust the parameters below to predict battery health:")
    
    # Input widgets
    battery_temperature = st.sidebar.slider(
        "🌡️ Battery Temperature (°C)",
        min_value=-20.0,
        max_value=60.0,
        value=25.0,
        step=0.5,
        help="Current battery temperature in Celsius"
    )
    
    voltage = st.sidebar.slider(
        "⚡ Voltage (V)",
        min_value=2.5,
        max_value=4.5,
        value=3.7,
        step=0.1,
        help="Current battery voltage"
    )
    
    current = st.sidebar.slider(
        "🔌 Current (A)",
        min_value=0.0,
        max_value=10.0,
        value=1.0,
        step=0.1,
        help="Current draw in Amperes"
    )
    
    charging_cycles = st.sidebar.slider(
        "🔄 Charging Cycles",
        min_value=0,
        max_value=10000,
        value=500,
        step=10,
        help="Number of charging cycles completed"
    )
    
    state_of_charge = st.sidebar.slider(
        "📊 State of Charge (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=1.0,
        help="Current state of charge percentage"
    )
    
    # Display AI configuration
    ai_enabled, use_openai, openai_api_key = display_ai_configuration()
    
    # Display parameter information
    display_parameter_info()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Prediction Results")
        
        # Predict button
        if st.button("🔮 Predict Battery Health", type="primary", use_container_width=True):
            # Prepare input data
            input_data = {
                "battery_temperature": battery_temperature,
                "voltage": voltage,
                "current": current,
                "charging_cycles": charging_cycles,
                "state_of_charge": state_of_charge
            }
            
            # Show input summary
            with st.expander("📋 Input Parameters", expanded=False):
                st.json(input_data)
            
            # Make prediction
            with st.spinner("🔄 Predicting battery health..."):
                result = predict_battery_health(input_data)
            
            if result and result.get('status') == 'success':
                # Store results in session state
                st.session_state['prediction_result'] = result
                st.session_state['input_data'] = input_data
                
                # Generate AI insights if enabled
                if ai_enabled:
                    with st.spinner("🤖 Generating AI insights..."):
                        ai_insights = generate_ai_insights(
                            input_data,
                            result,
                            api_key=openai_api_key if use_openai else None,
                            use_openai=use_openai
                        )
                        st.session_state['ai_insights'] = ai_insights
                
                # Display success message
                st.success("✅ Prediction completed successfully!")
        
        # Display results if available
        if 'prediction_result' in st.session_state:
            result = st.session_state['prediction_result']
            
            # Metrics
            col_metric1, col_metric2 = st.columns(2)
            
            with col_metric1:
                st.metric(
                    "🔋 Predicted RUL",
                    f"{result['predicted_rul']:.1f} cycles",
                    help="Remaining Useful Life in charging cycles"
                )
            
            with col_metric2:
                st.metric(
                    "💚 Battery Health",
                    f"{result['battery_health_percentage']:.1f}%",
                    help="Battery health as a percentage"
                )
            
            # Gauge visualization
            st.subheader("📊 Battery Health Gauge")
            health_percentage = result['battery_health_percentage']
            gauge_fig = create_battery_health_gauge(health_percentage)
            st.plotly_chart(gauge_fig, use_container_width=True)
            
            # Progress bar
            st.subheader("📈 Health Progress")
            progress_html = create_progress_bar(health_percentage)
            st.markdown(progress_html, unsafe_allow_html=True)
            
            # AI-Generated Insights
            if ai_enabled and 'ai_insights' in st.session_state and st.session_state['ai_insights']:
                st.subheader("🤖 AI-Generated Insights")
                st.markdown("""
                <div class="info-box" style="background-color: #e8f4f8; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #1f77b4;">
                """, unsafe_allow_html=True)
                
                # Display AI insights with nice formatting
                insights = st.session_state['ai_insights']
                st.markdown(insights)
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("---")
            
            # Recommendations
            st.subheader("💡 Recommendations")
            recommendations = get_health_recommendations(
                st.session_state['input_data'],
                health_percentage
            )
            
            if recommendations:
                for rec in recommendations:
                    st.info(rec)
            else:
                st.success("✅ All parameters are within optimal ranges!")
            
            # Download Report Button
            st.markdown("---")
            st.subheader("📄 Download Report")
            
            try:
                if REPORTLAB_AVAILABLE:
                    pdf_data = generate_pdf_report(
                        st.session_state['input_data'],
                        result,
                        ai_insights=st.session_state.get('ai_insights'),
                        recommendations=recommendations
                    )
                    
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_data,
                        file_name=f"battery_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.warning("⚠️ PDF generation requires reportlab. Install with: `pip install reportlab`")
                    # Fallback: Generate text report
                    report_text = f"""
# Battery Health Prediction Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Input Parameters
- Battery Temperature: {st.session_state['input_data'].get('battery_temperature')}°C
- Voltage: {st.session_state['input_data'].get('voltage')}V
- Current: {st.session_state['input_data'].get('current')}A
- Charging Cycles: {st.session_state['input_data'].get('charging_cycles')}
- State of Charge: {st.session_state['input_data'].get('state_of_charge')}%

## Prediction Results
- Battery Health: {health_percentage:.2f}%
- Predicted RUL: {result['predicted_rul']:.1f} cycles

## AI Insights
{st.session_state.get('ai_insights', 'N/A')}

## Recommendations
{chr(10).join([f"- {rec}" for rec in recommendations]) if recommendations else "- All parameters are within optimal ranges!"}
"""
                    st.download_button(
                        label="📥 Download Text Report",
                        data=report_text,
                        file_name=f"battery_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
    
    with col2:
        st.subheader("ℹ️ Information & Tips")
        
        # General information
        st.markdown("""
        <div class="info-box">
        <h4>🔋 About Battery Health</h4>
        <p>Battery health indicates the remaining capacity and performance of your battery. 
        Higher percentages mean better health and longer lifespan.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key factors
        st.markdown("### 🔑 Key Factors")
        
        factors = [
            ("🌡️ Temperature", "High temperature can degrade battery health faster. Optimal range: 15-35°C"),
            ("⚡ Voltage", "Low voltage might indicate underperformance. Monitor voltage levels regularly."),
            ("🔌 Current", "High current draws accelerate degradation. Use appropriate charging rates."),
            ("🔄 Cycles", "Each charging cycle reduces capacity slightly. More cycles = lower health."),
            ("📊 State of Charge", "Avoid extreme states (0% or 100%) for extended periods.")
        ]
        
        for factor, description in factors:
            with st.expander(factor, expanded=False):
                st.markdown(description)
        
        # Health status guide
        st.markdown("### 📊 Health Status Guide")
        st.markdown("""
        - **🟢 80-100%**: Excellent - Battery in great condition
        - **🟡 60-79%**: Good - Battery performing well
        - **🟠 40-59%**: Fair - Monitor battery closely
        - **🔴 0-39%**: Poor - Consider replacement
        """)
        
        # Best practices
        st.markdown("### ✅ Best Practices")
        st.markdown("""
        1. **Temperature Control**: Keep battery between 15-35°C
        2. **Charging Habits**: Avoid full charge/discharge cycles
        3. **Current Management**: Use appropriate charging rates
        4. **Regular Monitoring**: Check battery health regularly
        5. **Proper Storage**: Store at 50% charge in cool place
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🔋 EV Battery Health Prediction System | Powered by Machine Learning</p>
        <p>For best results, ensure accurate parameter input and regular monitoring</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

