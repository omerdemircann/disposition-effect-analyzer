
# 📈 BIST 30 Behavioral Finance: Disposition Effect Analyzer

**Live Interactive Dashboard:** https://omerdemircan-behavioral-finance.streamlit.app
## 📌 About the Project
This interactive web application was developed to simulate and analyze the **Disposition Effect** within the Borsa Istanbul (BIST 30) index. The Disposition Effect is a well-documented behavioral bias where investors tend to sell assets that have increased in value (winners) too early, while holding onto depreciating assets (losers) for too long.

This project bridges the gap between theoretical academic research and practical quantitative analysis. By utilizing real market data, the tool calculates the **Proportion of Gains Realized (PGR)** and **Proportion of Losses Realized (PLR)** to diagnose irrational trading behavior based on user-defined psychological bias intensities.

## 🚀 Key Features
* **Live Market Data:** Fetches real-time and historical financial data for major BIST 30 components.
* **Algorithmic Simulation:** Simulates trader behavior using a probabilistic model to test the "Sell Winners, Hold Losers" hypothesis over a customized investment timeline.
* **Interactive Visualizations:** Features interactive candlestick charts and dynamic behavioral metric calculations.

## 🔮 Future Roadmap & Enhancements
While the current version utilizes probabilistic modeling to simulate investor decisions, the next iterations of this tool will focus on deeper empirical integrations:
* **Volume-Weighted Decision Making:** Transitioning from probabilistic sale triggers to incorporating real-world trading volume as empirical evidence of market-wide profit realization.
* **Market-Wide Barometer:** Expanding the script to scan all 30 assets simultaneously, creating a daily, aggregate "BIST 30 Disposition Bias Index" rather than single-stock evaluations.
* **Strategy Benchmarking:** Introducing a comparative yield analyzer to measure the simulated emotional investor's returns against a strict 'Buy and Hold' (Rational) strategy to quantify the financial cost of the bias.

## 🛠️ Technologies Used
* **Python** (Core logic and simulation)
* **Streamlit** (Web framework & cloud deployment)
* **Pandas & NumPy** (Data manipulation and mathematical modeling)
* **Plotly** (Interactive financial charting)
* **yfinance API** (Market data retrieval)

---
*Developed by Ömer Demircan as part of an academic exploration in Quantitative Economics and Behavioral Finance.*
