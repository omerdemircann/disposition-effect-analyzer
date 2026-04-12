import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="OMERDEMIRCAN BIST 30 Disposition Analyzer", layout="wide")

st.title("Behavioral Finance: Disposition Effect Analyzer")
st.markdown("This tool uses real BIST 30 data to simulate the **Disposition Effect** based on my Why Investors Sell Winners and Hold Losers research paper parameters.")

# 2. BIST 30 Selection
bist_tickers = {
    "Turkish Airlines": "THYAO.IS",
    "Erdemir": "EREGL.IS",
    "Tupras": "TUPRS.IS",
    "Aselsan": "ASELS.IS",
    "Isbank": "ISCTR.IS"
}

with st.sidebar:
    st.header("1. Data Selection")
    selected_name = st.selectbox("Select Stock:", list(bist_tickers.keys()))
    ticker = bist_tickers[selected_name]
    
    st.header("2. Investment Scenario")
    buy_date = st.date_input("Investment Start Date:", datetime.now() - timedelta(days=365))
    bias = st.slider("Disposition Bias Intensity:", 1.0, 5.0, 2.0)

# 3. Fetch Data
with st.spinner("Fetching data..."):
    data = yf.download(ticker, start=buy_date)
    c = data['Close'].squeeze()
    o = data['Open'].squeeze()
    h = data['High'].squeeze()
    l = data['Low'].squeeze()

# 4. Disposition Logic (PGR & PLR Calculation)
ref_price = float(c.iloc[0])

gains_opp = 0
losses_opp = 0
realized_gains = 0
realized_losses = 0

for price in c.values:
    if price > ref_price:
        gains_opp += 1
        if np.random.rand() < (0.1 * bias):
            realized_gains += 1
    elif price < ref_price:
        losses_opp += 1
        if np.random.rand() < (0.1 / bias):
            realized_losses += 1

pgr = realized_gains / gains_opp if gains_opp > 0 else 0
plr = realized_losses / losses_opp if losses_opp > 0 else 0

# 5. Visuals
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Price Chart & Reference Level")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=o, high=h, low=l, close=c, name="Price"))
    fig.add_hline(y=ref_price, line_dash="dash", line_color="blue", annotation_text="Buy Price")
    
    fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_white", height=500)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Behavioral Metrics")
    st.write(f"**Reference Price:** {ref_price:.2f} TRY")
    
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("PGR", f"{pgr:.2%}")
    m_col2.metric("PLR", f"{plr:.2%}")
    
    st.markdown("---")
    # SIFIRA BÖLME HATASINI ÇÖZEN KISIM
    if pgr > plr:
        if plr == 0:
            st.error("**Extreme Disposition Effect Detected!**\n\nThe investor realized gains, but held onto ALL losses (PLR is 0%). This is a severe case of 'Sell Winners, Hold Losers'.")
        else:
            st.error(f"**Disposition Effect Detected!**\n\nThe investor is {pgr/plr:.1f}x more likely to realize gains than losses. This confirms the 'Sell Winners, Hold Losers' bias.")
    else:
        st.success("No significant Disposition Effect detected in this simulation.")
    
    st.info(f"""
    **Stats Summary:**
    - Days in Profit (Opportunities): {gains_opp}
    - Days in Loss (Opportunities): {losses_opp}
    """)
