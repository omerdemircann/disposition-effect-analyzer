import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf

# 1. Page Configuration (Dashboard Ayarları)
st.set_page_config(page_title="Disposition Effect Analyzer", layout="wide")
st.title("📈 Behavioral Finance: The Disposition Effect Analyzer")
st.markdown("""
This dashboard analyzes simulated investor behavior to detect the **Disposition Effect** (the tendency of investors to sell assets that have increased in value, while keeping assets that have dropped in value).
""")

# 2. Sidebar for User Inputs (Sol Menü)
st.sidebar.header("Simulation Parameters")
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL, MSFT)", "AAPL")
trades_count = st.sidebar.slider("Number of Simulated Trades", 50, 500, 100)

st.sidebar.markdown("---")
st.sidebar.write("**Behavioral Biases**")
# Kullanıcının yatırımcı psikolojisini belirlediği alan
prob_sell_gain = st.sidebar.slider("Prob. of Selling a Winner (PGR)", 0.0, 1.0, 0.65)
prob_sell_loss = st.sidebar.slider("Prob. of Selling a Loser (PLR)", 0.0, 1.0, 0.25)

# 3. Data Simulation Function (Gerçek veri seti gelene kadar simülasyon)
def simulate_investor_behavior(trades_count, pgr, plr):
    """
    Simulates investor trades. 
    Paper reference: Proportion of Gains Realized (PGR) vs Proportion of Losses Realized (PLR)
    """
    np.random.seed(42)
    # Generate random market movements (1 = Gain, 0 = Loss)
    market_movement = np.random.choice([1, 0], size=trades_count, p=[0.5, 0.5])
    
    realized_gains = 0
    paper_gains = 0
    realized_losses = 0
    paper_losses = 0
    
    for movement in market_movement:
        if movement == 1: # Stock goes up
            if np.random.rand() < pgr:
                realized_gains += 1 # Sold early
            else:
                paper_gains += 1    # Held
        else: # Stock goes down
            if np.random.rand() < plr:
                realized_losses += 1 # Cut losses
            else:
                paper_losses += 1    # Held (Bag holding)
                
    # Calculate Ratios (Formulas from behavioral finance literature)
    total_gains = realized_gains + paper_gains
    total_losses = realized_losses + paper_losses
    
    actual_pgr = realized_gains / total_gains if total_gains > 0 else 0
    actual_plr = realized_losses / total_losses if total_losses > 0 else 0
    
    return actual_pgr, actual_plr, realized_gains, paper_gains, realized_losses, paper_losses

# 4. Run Analysis
pgr_result, plr_result, rg, pg, rl, pl = simulate_investor_behavior(trades_count, prob_sell_gain, prob_sell_loss)

# 5. Dashboard Layout & Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 PGR vs PLR Analysis")
    
    # Plotly ile şık bir bar grafiği
    df_chart = pd.DataFrame({
        'Metric': ['PGR (Gains Realized)', 'PLR (Losses Realized)'],
        'Value': [pgr_result, plr_result]
    })
    
    fig = px.bar(df_chart, x='Metric', y='Value', color='Metric', 
                 text_auto='.2%', title="Investor Realization Propensity",
                 color_discrete_sequence=['#2ecc71', '#e74c3c'])
    fig.update_layout(yaxis_tickformat='.0%')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🧠 Behavioral Diagnosis")
    
    if pgr_result > plr_result:
        st.error(f"**Disposition Effect Detected!** \n\nThe investor is {(pgr_result/plr_result):.1f}x more likely to sell a winning stock than a losing one. This is a classic behavioral bias.")
    else:
        st.success("**Rational / Momentum Investor** \n\nThe investor demonstrates good discipline by cutting losses quickly or letting winners ride.")
        
    st.markdown("### Raw Trade Data")
    metric_cols = st.columns(2)
    metric_cols[0].metric("Realized Gains", rg)
    metric_cols[0].metric("Paper Gains (Held)", pg)
    metric_cols[1].metric("Realized Losses", rl)
    metric_cols[1].metric("Paper Losses (Held)", pl)

st.markdown("---")
st.markdown("*Developed as part of academic research on quantitative behavioral finance.*")
