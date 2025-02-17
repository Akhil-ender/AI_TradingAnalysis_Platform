# 📈 AI Trading Crew Analysis Platform
An interactive AI-driven platform designed to assist traders in making data-backed decisions with ease and confidence. This tool employs multiple AI agents for analyzing market data, developing trading strategies, planning execution, and assessing risks, all wrapped in a sleek and user-friendly Streamlit interface.

# 🌟 Key Features
## AI Agents for Trading Support:

- Data Analyst Agent: Monitors real-time market trends to identify patterns and predict movements.
- Trading Strategy Developer: Crafts and tests trading strategies tailored to risk preferences.
- Trade Advisor: Optimizes trade execution strategies.
- Risk Advisor: Assesses and provides insights on potential risks.
## User-Customizable Input:
Choose stock symbols, initial capital, trading strategy, and risk tolerance.
Toggle the option to consider the impact of news on market behavior.

# Integration of AI Models:
Powered by Google Generative AI (Gemini 2.0) for decision-making insights.
Utilizes SerperDevTool and ScrapeWebsiteTool for market research and news scraping.

# Real-Time Analysis:
Dynamically generate market insights and alerts.
Get tailored execution plans and risk mitigation strategies.

# 🛠️ Technology Stack
- Streamlit: For an intuitive and interactive web application interface.
- Google Generative AI (Gemini): To generate personalized trading insights.
- LangChain: For orchestrating multi-agent tasks and communication.
- Python: Core development language.
- SerperDevTool & ScrapeWebsiteTool: For web scraping and news analysis.

# 🚀 How to Run
Clone the repository.
Install dependencies with 
``` bash
pip install -r requirements.txt.
```
Make sure you add your API keys to the .env file:
GOOGLE_API_KEY
SERPER_API_KEY

- Run the application with:
``` bash
streamlit run app.py
```

# 📢 Usage
Enter trading parameters (stock symbol, capital, risk tolerance, etc.) through the form.
Submit to generate an AI-driven analysis report tailored to your selections.
View the output, including trading strategy suggestions, market trends, and risk assessment.

# 💡 Future Enhancements
Support for more AI agents and trading strategies.
Enhanced visualizations for market trends and risk analysis.
Integration of more data sources for deeper market insights.
