import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import json

# Page config
st.set_page_config(
    page_title="CogniChat - Data Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Login container */
    .login-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 400px;
        margin: 0 auto;
        margin-top: 10vh;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 8px 0;
        max-width: 75%;
        margin-left: auto;
        margin-right: 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: rgba(255, 255, 255, 0.95);
        color: #333;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 8px 0;
        max-width: 75%;
        margin-right: auto;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Welcome card styling */
    .welcome-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 20px 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 5px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        height: 120px;
    }
    
    /* Text styling */
    .main-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    
    .feature-title {
        color: white;
        font-weight: bold;
        margin-bottom: 8px;
    }
    
    .feature-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
    }
    
    .login-title {
        color: white;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide sidebar when not logged in */
    .login-mode .css-1d391kg {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'messages' not in st.session_state:
    st.session_state.messages = []

def create_sample_dataset():
    """Create a sample dataset - replace this with your actual data loading logic"""
    import numpy as np
    
    # Sample e-commerce data
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
    
    data = {
        'Date': np.random.choice(dates, 1000),
        'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], 1000),
        'Revenue': np.random.normal(1000, 300, 1000).round(2),
        'Units_Sold': np.random.poisson(5, 1000),
        'Customer_Type': np.random.choice(['New', 'Returning'], 1000, p=[0.3, 0.7]),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 1000),
        'Rating': np.random.choice([1, 2, 3, 4, 5], 1000, p=[0.05, 0.1, 0.2, 0.35, 0.3])
    }
    
    df = pd.DataFrame(data)
    df['Revenue'] = df['Revenue'].abs()  # Ensure positive revenue
    return df.sort_values('Date').reset_index(drop=True)

if 'dataset' not in st.session_state:
    # Load your backend dataset here
    # For demo purposes, I'll create sample data
    st.session_state.dataset = create_sample_dataset()

if 'user_info' not in st.session_state:
    st.session_state.user_info = None



def authenticate_user(username, password):
    """Replace with your actual authentication logic"""
    # Demo authentication - replace with real logic
    valid_users = {
        "admin": "password123",
        "analyst": "data2024",
        "demo": "demo"
    }
    
    return username in valid_users and valid_users[username] == password

def login_screen():
    """Display login form"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-title">🧠 CogniChat</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("#### Welcome back!")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b, col_c = st.columns([1, 1, 1])
            with col_b:
                submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.user_info = {"username": username}
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        # Demo credentials
        st.markdown("""
        <div style="margin-top: 30px; padding: 15px; background: rgba(255, 255, 255, 0.1); 
                    border-radius: 10px; text-align: center;">
            <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem;">
                <strong>Demo Credentials:</strong><br>
                Username: <code>demo</code> | Password: <code>demo</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

def chat_interface():
    """Main chat interface"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🧠 CogniChat")
        st.markdown(f"**Welcome, {st.session_state.user_info['username']}!**")
        st.markdown("---")
        
        # Dataset info
        st.markdown("#### 📊 Current Dataset")
        df = st.session_state.dataset
        st.info(f"**Rows:** {df.shape[0]:,}\n\n**Columns:** {df.shape[1]}")
        
        # Show column info
        with st.expander("📋 View Columns"):
            for col in df.columns:
                dtype_str = str(df[col].dtype)
                if dtype_str.startswith('int') or dtype_str.startswith('float'):
                    icon = "🔢"
                elif dtype_str == 'object':
                    icon = "📝"
                elif 'datetime' in dtype_str:
                    icon = "📅"
                else:
                    icon = "❓"
                st.write(f"{icon} {col}")
        
        st.markdown("---")
        
        # Chat History Management
        st.markdown("#### 💬 Chat")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f"Messages: {len(st.session_state.messages)}")
        
        st.markdown("---")
        
        # Settings
        st.markdown("#### ⚙️ Settings")
        show_code = st.checkbox("Show Python code", value=False)
        max_rows = st.slider("Max rows to display", 5, 50, 10)
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.session_state.messages = []
            st.rerun()

    # Main chat area
    st.markdown("""
    <div style="color: white; font-size: 1.8rem; font-weight: bold; margin-bottom: 20px;">
        🧠 CogniChat - Your Data Analytics Assistant
    </div>
    """, unsafe_allow_html=True)
    
    # Show welcome message if no chat history
    if len(st.session_state.messages) == 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">📈 Examples</div>
                <div class="feature-text">"Show me revenue trends by month"</div><br>
                <div class="feature-text">"What are the top product categories?"</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🚀 Capabilities</div>
                <div class="feature-text">Natural language data queries</div><br>
                <div class="feature-text">Interactive visualizations</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">💡 Tips</div>
                <div class="feature-text">Ask about trends, comparisons, or summaries</div><br>
                <div class="feature-text">Be specific for better results</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Display any charts or data
            if "chart" in message:
                st.plotly_chart(message["chart"], use_container_width=True)
            if "dataframe" in message:
                st.dataframe(message["dataframe"], use_container_width=True)
            if "code" in message and show_code:
                st.code(message["code"], language="python")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your data..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        with st.spinner("🤔 Analyzing your data..."):
            response = process_query(prompt, st.session_state.dataset, max_rows)
            st.session_state.messages.append(response)
        
        st.rerun()

def process_query(query, df, max_rows=20):
    """Process natural language query and return response with visualizations"""
    
    query_lower = query.lower()
    
    try:
        # Revenue analysis
        if any(word in query_lower for word in ['revenue', 'sales', 'income', 'earnings']):
            if 'trend' in query_lower or 'time' in query_lower or 'month' in query_lower:
                # Revenue trend over time
                monthly_revenue = df.groupby(df['Date'].dt.to_period('M'))['Revenue'].sum().reset_index()
                monthly_revenue['Date'] = monthly_revenue['Date'].astype(str)
                
                fig = px.line(
                    monthly_revenue,
                    x='Date',
                    y='Revenue',
                    title="Monthly Revenue Trend",
                    template="plotly_dark"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                
                total_revenue = df['Revenue'].sum()
                avg_monthly = monthly_revenue['Revenue'].mean()
                
                response = {
                    "role": "assistant",
                    "content": f"📈 **Revenue Analysis:**\n\n• **Total Revenue:** ${total_revenue:,.2f}\n• **Average Monthly:** ${avg_monthly:,.2f}\n• **Best Month:** {monthly_revenue.loc[monthly_revenue['Revenue'].idxmax(), 'Date']}",
                    "chart": fig,
                    "dataframe": monthly_revenue,
                    "code": "df.groupby(df['Date'].dt.to_period('M'))['Revenue'].sum()"
                }
                return response
            
            elif any(word in query_lower for word in ['category', 'product']):
                # Revenue by category
                category_revenue = df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False)
                
                fig = px.bar(
                    x=category_revenue.values,
                    y=category_revenue.index,
                    orientation='h',
                    title="Revenue by Product Category",
                    template="plotly_dark",
                    labels={'x': 'Revenue', 'y': 'Category'}
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                
                response = {
                    "role": "assistant",
                    "content": f"💰 **Revenue by Category:**\n\nTop performer: **{category_revenue.index[0]}** (${category_revenue.iloc[0]:,.2f})",
                    "chart": fig,
                    "dataframe": pd.DataFrame({"Revenue": category_revenue}),
                    "code": "df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False)"
                }
                return response
        
        # Top products/categories
        elif any(word in query_lower for word in ['top', 'best', 'highest']):
            if 'category' in query_lower or 'product' in query_lower:
                top_categories = df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False).head(5)
                
                fig = px.pie(
                    values=top_categories.values,
                    names=top_categories.index,
                    title="Top 5 Product Categories by Revenue",
                    template="plotly_dark"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                
                response = {
                    "role": "assistant",
                    "content": f"🏆 **Top 5 Product Categories:**\n\n1. **{top_categories.index[0]}**: ${top_categories.iloc[0]:,.2f}",
                    "chart": fig,
                    "dataframe": pd.DataFrame({"Revenue": top_categories}),
                    "code": "df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False).head(5)"
                }
                return response
        
        # Customer analysis
        elif any(word in query_lower for word in ['customer', 'new', 'returning']):
            customer_analysis = df.groupby('Customer_Type').agg({
                'Revenue': 'sum',
                'Units_Sold': 'sum'
            }).reset_index()
            
            fig = px.bar(
                customer_analysis,
                x='Customer_Type',
                y='Revenue',
                title="Revenue by Customer Type",
                template="plotly_dark"
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            
            response = {
                "role": "assistant",
                "content": "👥 **Customer Type Analysis:**\n\nBreaking down performance by customer type...",
                "chart": fig,
                "dataframe": customer_analysis,
                "code": "df.groupby('Customer_Type').agg({'Revenue': 'sum', 'Units_Sold': 'sum'})"
            }
            return response
        
        # Regional analysis
        elif any(word in query_lower for word in ['region', 'location', 'geographic']):
            regional_data = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)
            
            fig = px.bar(
                x=regional_data.index,
                y=regional_data.values,
                title="Revenue by Region",
                template="plotly_dark",
                labels={'x': 'Region', 'y': 'Revenue'}
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            
            response = {
                "role": "assistant",
                "content": f"🌍 **Regional Performance:**\n\nTop region: **{regional_data.index[0]}** with ${regional_data.iloc[0]:,.2f}",
                "chart": fig,
                "dataframe": pd.DataFrame({"Revenue": regional_data}),
                "code": "df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)"
            }
            return response
        
        # Summary/overview
        elif any(word in query_lower for word in ['summary', 'overview', 'describe']):
            total_revenue = df['Revenue'].sum()
            total_units = df['Units_Sold'].sum()
            avg_rating = df['Rating'].mean()
            date_range = f"{df['Date'].min().date()} to {df['Date'].max().date()}"
            
            response = {
                "role": "assistant",
                "content": f"""📊 **Dataset Overview:**

• **Time Period:** {date_range}
• **Total Revenue:** ${total_revenue:,.2f}
• **Units Sold:** {total_units:,}
• **Average Rating:** {avg_rating:.1f}/5
• **Product Categories:** {df['Product_Category'].nunique()}
• **Regions:** {df['Region'].nunique()}
• **Records:** {len(df):,}""",
                "dataframe": df.head(max_rows),
                "code": "df.describe()"
            }
            return response
        
        # Default response
        response = {
            "role": "assistant",
            "content": f"""🤔 I'd love to help analyze: "{query}"

Here are some things you can ask me:

**📈 Revenue & Sales:**
• "Show me revenue trends over time"
• "Which product category generates the most revenue?"

**🏆 Performance:**
• "What are the top performing regions?"
• "Compare new vs returning customers"

**📊 General:**
• "Give me a summary of the data"
• "Show me customer ratings analysis"

What would you like to explore?"""
        }
        
        return response
        
    except Exception as e:
        return {
            "role": "assistant", 
            "content": f"❌ I encountered an error: {str(e)}\n\nTry asking for a 'summary' or be more specific about what you'd like to analyze."
        }

# Main app logic
if not st.session_state.authenticated:
    login_screen()
else:
    chat_interface()