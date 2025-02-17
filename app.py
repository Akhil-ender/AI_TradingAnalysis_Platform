import streamlit as st
import warnings
import nest_asyncio
from dotenv import load_dotenv
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew, Process
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

# Load environment variables and setup
load_dotenv()
nest_asyncio.apply()

# Page configuration
st.set_page_config(
    page_title="AI Trading Crew Analysis",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for dark theme and better formatting
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .analysis-section {
        background-color: #2C3333;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .section-header {
        color: #00ADB5;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .section-content {
        color: #EEEEEE;
        line-height: 1.6;
    }
    .metric-card {
        background-color: #393E46;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .metric-value {
        color: #00ADB5;
        font-size: 1.4em;
        font-weight: bold;
    }
    .metric-label {
        color: #EEEEEE;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

def create_agents_and_crew(gemini_model):
    """Create and return the agents and crew"""
    # Initialize tools
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    
    # Create agents
    data_analyst_agent = Agent(
        role="Data Analyst",
        goal="Monitor and analyze market data in real-time to identify trends and predict market movements.",
        backstory="Specializing in financial markets, this agent uses statistical modeling and machine learning to provide crucial insights.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool],
        llm=gemini_model
    )
    
    trading_strategy_agent = Agent(
        role="Trading Strategy Developer",
        goal="Develop and test various trading strategies based on insights from the Data Analyst Agent.",
        backstory="Equipped with a deep understanding of financial markets and quantitative analysis, this agent devises and refines trading strategies.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool],
        llm=gemini_model
    )
    
    execution_agent = Agent(
        role="Trade Advisor",
        goal="Suggest optimal trade execution strategies based on approved trading strategies.",
        backstory="This agent specializes in analyzing the timing, price, and logistical details of potential trades.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool],
        llm=gemini_model
    )
    
    risk_management_agent = Agent(
        role="Risk Advisor",
        goal="Evaluate and provide insights on the risks associated with potential trading activities.",
        backstory="Armed with a deep understanding of risk assessment models and market dynamics, this agent scrutinizes potential risks.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool],
        llm=gemini_model
    )
    
    # Create tasks
    tasks = [
        Task(
            description="Analyze market data for {stock_selection}. Identify trends and predict movements.",
            expected_output="Market insights and alerts for {stock_selection}.",
            agent=data_analyst_agent
        ),
        Task(
            description="Develop trading strategies based on analysis and {risk_tolerance} risk tolerance.",
            expected_output="Trading strategies for {stock_selection}.",
            agent=trading_strategy_agent
        ),
        Task(
            description="Plan trade execution for {stock_selection} considering market conditions.",
            expected_output="Detailed execution plans for trades.",
            agent=execution_agent
        ),
        Task(
            description="Assess risks for {stock_selection} trading strategies.",
            expected_output="Risk analysis and mitigation recommendations.",
            agent=risk_management_agent
        )
    ]
    
    # Create crew
    crew = Crew(
        agents=[data_analyst_agent, trading_strategy_agent, execution_agent, risk_management_agent],
        tasks=tasks,
        manager_llm=gemini_model,
        process=Process.hierarchical,
        verbose=True
    )
    
    return crew

def initialize_apis():
    """Initialize API configurations from .env file"""
    try:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        serper_api_key = os.getenv("SERPER_API_KEY")
        
        if not google_api_key or not serper_api_key:
            st.error("API keys not found in .env file. Please check your .env configuration.")
            return False
        
        genai.configure(api_key=google_api_key)
        os.environ["SERPER_API_KEY"] = serper_api_key
        return True
    except Exception as e:
        st.error(f"Error initializing APIs: {str(e)}")
        return False

def main():
    st.title("🤖 AI Trading Crew Analysis")
    
    # Initialize APIs from .env file
    if not initialize_apis():
        return
    
    try:
        gemini_model = GoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    except Exception as e:
        st.error(f"Error initializing Gemini model: {str(e)}")
        return
    
    # Input form
    with st.form("trading_parameters"):
        col1, col2 = st.columns(2)
        
        with col1:
            stock_symbol = st.text_input("Stock Symbol", value="AAPL")
            initial_capital = st.number_input("Initial Capital ($)", 
                                           min_value=1000, 
                                           value=100000, 
                                           step=1000,
                                           format="%d")
        
        with col2:
            risk_tolerance = st.select_slider(
                "Risk Tolerance",
                options=["Very Low", "Low", "Medium", "High", "Very High"],
                value="Medium"
            )
            trading_strategy = st.selectbox(
                "Trading Strategy",
                ["Day Trading", "Swing Trading", "Position Trading", "Scalping"]
            )
        
        news_impact = st.checkbox("Consider News Impact", value=True)
        submit_button = st.form_submit_button("Generate Analysis")
    
    if submit_button:
        try:
            with st.spinner("🤖 AI Crew is analyzing your trading parameters..."):
                crew = create_agents_and_crew(gemini_model)
                trading_inputs = {
                    'stock_selection': stock_symbol,
                    'initial_capital': str(initial_capital),
                    'risk_tolerance': risk_tolerance,
                    'trading_strategy_preference': trading_strategy,
                    'news_impact_consideration': news_impact
                }
                
                result = crew.kickoff(inputs=trading_inputs)
                
                # Display summary metrics
                st.success("Analysis complete!")
                st.markdown(result)
                                
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            st.write("Please check the API keys and try again.")

if __name__ == "__main__":
    main()