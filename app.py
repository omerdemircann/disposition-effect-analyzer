import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

# --- PAGE CONFIGURATION ---
# Bu komut her zaman dosyanın en üstünde olmalıdır
st.set_page_config(page_title="Behavioral Finance & Experimental Economics", layout="wide")

st.title("Behavioral Finance & Experimental Economics")
st.markdown("Explore real-time market data and test your psychological biases as an investor.")

# --- DICTIONARIES (STOCKS) ---
bist_stocks = {
    "Turkish Airlines": "THYAO.IS", "Garanti BBVA": "GARAN.IS", "Aselsan": "ASELS.IS",
    "Koc Holding": "KCHOL.IS", "Akbank": "AKBNK.IS", "Isbank": "ISCTR.IS",
    "Tupras": "TUPRS.IS", "Sisecam": "SISE.IS", "BIM": "BIMAS.IS",
    "Erdemir": "EREGL.IS", "Sabanci Holding": "SAHOL.IS", "Yapi Kredi": "YKBNK.IS",
    "Enka Insaat": "ENKAI.IS", "Ford Otosan": "FROTO.IS", "Turkcell": "TCELL.IS",
    "Tofas": "TOASO.IS", "Pegasus Airlines": "PGSUS.IS", "Arcelik": "ARCLK.IS",
    "Turk Telekom": "TTKOM.IS", "Petkim": "PETKM.IS"
}

global_stocks = {
    "Apple": "AAPL", "Microsoft": "MSFT", "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN", "Tesla": "TSLA", "Meta (Facebook)": "META",
    "Nvidia": "NVDA", "Netflix": "NFLX", "JPMorgan Chase": "JPM", "Visa": "V"
}

# Dropdown menüsü için tüm hisseleri birleştiriyoruz
all_stocks = {**bist_stocks, **global_stocks}

# --- TABS CREATION ---
tab1, tab2, tab3 = st.tabs(["📈 Market Dashboard", "🧠 Framing Effect Test", "📉 Disposition Effect Simulator"])

# ==========================================
# TAB 1: MARKET DASHBOARD
# ==========================================
with tab1:
    st.header("Real-Time Market Data")
    st.write("Select a company to view its recent price performance.")
    
    # Kullanıcıdan hisse ve zaman aralığı seçmesini istiyoruz
    selected_company = st.selectbox("Choose a Stock:", list(all_stocks.keys()))
    ticker_symbol = all_stocks[selected_company]
    
    period = st.selectbox("Select Time Period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    
    if st.button("Fetch Market Data"):
        with st.spinner("Loading data from Yahoo Finance..."):
            stock_data = yf.Ticker(ticker_symbol)
            hist = stock_data.history(period=period)
            
            if not hist.empty:
                st.subheader(f"{selected_company} ({ticker_symbol}) - {period.upper()} Performance")
                st.line_chart(hist['Close'])
            else:
                st.error("No data found for this ticker. It might be delisted or temporarily unavailable.")

# ==========================================
# TAB 2: FRAMING EFFECT TEST
# ==========================================
with tab2:
    st.header("Risk Profile & Framing Effect")
    st.markdown("Let's see how rational your decision-making is under different 'frames'.")
    
    st.divider()
    
    st.subheader("Scenario 1: The Gain Frame")
    st.write("You are given **$10,000** for sure. Now you must choose one of the following:")
    ans1 = st.radio(
        "What is your decision?",
        ("A) Receive an additional $5,000 for sure.", 
         "B) Flip a coin: If heads, you receive an additional $10,000. If tails, you receive nothing extra."),
        key="q1"
    )
    
    st.divider()
    
    st.subheader("Scenario 2: The Loss Frame")
    st.write("You are given **$20,000** for sure. However, you must now choose one of the following:")
    ans2 = st.radio(
        "What is your decision?",
        ("A) Give back $5,000 for sure.", 
         "B) Flip a coin: If heads, you give back nothing. If tails, you give back $10,000."),
        key="q2"
    )
    
    if st.button("Analyze My Risk Profile"):
        st.subheader("Your Behavioral Analysis:")
        
        is_safe_1 = ans1.startswith("A")
        is_safe_2 = ans2.startswith("A")
        
        if is_safe_1 and not is_safe_2:
            st.error("🚨 You exhibited the **Framing Effect**.")
            st.write("Mathematically, both scenarios offer the exact same outcomes (a guaranteed $15,000 OR a 50/50 chance of having $10,000 or $20,000). However, you were risk-averse when options were framed as **gains**, but risk-seeking when framed as **losses**. You hate losing!")
        elif (is_safe_1 and is_safe_2) or (not is_safe_1 and not is_safe_2):
            st.success("✅ Congratulations! You are a highly rational investor.")
            st.write("You were not tricked by the wording ('gain' vs 'loss'). You maintained a consistent risk profile regardless of how the problem was framed.")
        else:
            st.warning("⚠️ Interesting Profile!")
            st.write("You took a risk to gain more, but chose the safe route when faced with a loss. This is quite rare and goes against traditional prospect theory.")

# ==========================================
# TAB 3: DISPOSITION EFFECT SIMULATOR
# ==========================================
with tab3:
    st.header("The Disposition Effect Simulator")
    
    st.info("""
    ### Why Investors Sell Winners and Hold Losers?
    In **Experimental Economics**, the *Disposition Effect* describes a specific behavioral bias: the tendency of investors to prematurely sell assets that have made financial gains, while stubbornly holding on to assets that are losing money. 
    
    Instead of making rational decisions based on future potential, investors often sell winners to lock in the "feeling of success" and hold losers to avoid the "regret of a realized loss."
    """)
    
    st.write("Let's see how you handle a simulated crisis. Imagine you bought a stock exactly **one year ago**.")
    
    sim_stock = st.selectbox("Choose a stock to simulate:", list(bist_stocks.keys()), key="sim_stock")
    sim_ticker = bist_stocks[sim_stock]
    
    if st.button("Start Simulation"):
        with st.spinner("Generating scenario..."):
            end_date = datetime.date.today()
            start_date = end_date - relativedelta(years=1)
            mid_date = start_date + relativedelta(months=6)
            
            data = yf.download(sim_ticker, start=start_date, end=end_date, progress=False)
            
            if not data.empty and len(data) > 100:
                buy_price = float(data.loc[:str(start_date + relativedelta(days=10))]['Close'].iloc[0])
                mid_price = float(data.loc[:str(mid_date)]['Close'].iloc[-1])
                current_price = float(data['Close'].iloc[-1])
                
                mid_return = ((mid_price - buy_price) / buy_price) * 100
                
                st.session_state['sim_data'] = {
                    'buy': buy_price, 'mid': mid_price, 'current': current_price,
                    'return': mid_return, 'full_data': data['Close']
                }
            else:
                st.error("Not enough historical data to run the simulation for this stock.")
    
    if 'sim_data' in st.session_state:
        sim = st.session_state['sim_data']
        st.divider()
        st.subheader("6 Months Later...")
        
        if sim['return'] < 0:
            st.error(f"Oh no! The stock dropped by **{abs(sim['return']):.2f}%**.")
            st.write(f"You bought at {sim['buy']:.2f} TL, and it is now at {sim['mid']:.2f} TL.")
            st.write("**Do you sell to cut your losses, or hold hoping it goes back up?**")
        else:
            st.success(f"Great! The stock is up by **{sim['return']:.2f}%**.")
            st.write(f"You bought at {sim['buy']:.2f} TL, and it is now at {sim['mid']:.2f} TL.")
            st.write("**Do you sell now to lock in profits, or hold for more gains?**")
            
        if st.button("Reveal Today's Price"):
            st.divider()
            st.subheader("Fast Forward to Today")
            st.line_chart(sim['full_data'])
            
            final_return = ((sim['current'] - sim['buy']) / sim['buy']) * 100
            st.write(f"Today's price is **{sim['current']:.2f} TL**.")
            
            if final_return > sim['return']:
                st.success("Holding was mathematically the better choice! The price improved compared to the 6-month mark.")
            else:
                st.error("Selling at the 6-month mark would have been better! The price deteriorated further.")
                
            st.info("Did you feel the urge to hold a losing stock, or sell a winning one quickly? If so, you experienced the Disposition Effect firsthand.")
