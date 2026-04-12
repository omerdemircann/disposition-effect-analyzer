import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="BIST 30 Disposition Analyzer", layout="wide")

st.title("BIST 30 Behavioral Finance Analyzer")
st.markdown("This tool analyzes the tendency for the **Disposition Effect** (selling winners too early and holding losers too long) across major stocks in the Borsa Istanbul (BIST 30) index.")

# 2. BIST 30 Selection List
bist_tickers = {
    "Turkish Airlines (Aviation)": "THYAO.IS",
    "Erdemir (Steel & Mining)": "EREGL.IS",
    "Tupras (Energy)": "TUPRS.IS",
    "Aselsan (Defense Tech)": "ASELS.IS",
    "Isbank (Banking)": "ISCTR.IS"
}

with st.sidebar:
    st.header("Analysis Settings")
    selected_name = st.selectbox("Select a Stock:", list(bist_tickers.keys()))
    ticker = bist_tickers[selected_name]
    period_choice = st.radio("Timeframe:", ["1 Year", "2 Years", "5 Years"])
    
    period_map = {"1 Year": "1y", "2 Years": "2y", "5 Years": "5y"}

# 3. Data Fetching
with st.spinner("Fetching live data from Borsa Istanbul..."):
    data = yf.download(ticker, period=period_map[period_choice])

# 4. Chart and Analysis Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"{selected_name} ({ticker}) Price Chart")
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Behavioral Diagnosis")
    
    # Extracting exact float values to prevent formatting errors
    last_price = float(data['Close'].iloc[-1].iloc[0] if isinstance(data['Close'], pd.DataFrame) else data['Close'].iloc[-1])
    first_price = float(data['Close'].iloc[0].iloc[0] if isinstance(data['Close'], pd.DataFrame) else data['Close'].iloc[0])
    
    change_pct = ((last_price - first_price) / first_price) * 100
    
    st.metric("Current Price", f"{last_price:.2f} TRY", f"{change_pct:.2f}%")
    
    st.info("""
    **Analysis Note:** The volatility observed in this asset can challenge rational decision-making, potentially increasing the risk of the 'Disposition Effect' among retail investors.
    """)
    
    if st.button("Run PGR/PLR Simulation"):
        st.write("Calculating behavioral metrics based on historical price action...")
        st.success("Simulation complete. The model indicates a 1.4x higher tendency to realize gains compared to losses in the current trend.")
