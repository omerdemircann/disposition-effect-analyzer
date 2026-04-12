import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="BIST 30 Disposition Analyzer", layout="wide")

st.title("🇹🇷 BIST 30 Behavioral Finance Analyzer")
st.markdown("Bu araç, Borsa İstanbul'un dev hisseleri üzerinden **Disposition Effect** (Kazananı erken satma) eğilimini analiz eder.")

# 1. BIST 30 Seçki Listesi
bist_hisseleri = {
    "Türk Hava Yolları": "THYAO.IS",
    "Erdemir": "EREGL.IS",
    "Tüpraş": "TUPRS.IS",
    "Aselsan": "ASELS.IS",
    "İş Bankası": "ISCTR.IS"
}

with st.sidebar:
    st.header("Analiz Ayarları")
    secilen_ad = st.selectbox("Hisse Seçin:", list(bist_hisseleri.keys()))
    ticker = bist_hisseleri[secilen_ad]
    donem = st.radio("Zaman Aralığı:", ["1 Yıl", "2 Yıl", "5 Yıl"])
    
    period_map = {"1 Yıl": "1y", "2 Yıl": "2y", "5 Yıl": "5y"}

# 2. Veri Çekme
with st.spinner('Veriler Borsa İstanbul'dan çekiliyor...'):
    data = yf.download(ticker, period=period_map[donem])

# 3. Grafik ve Analiz
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"{secilen_ad} ({ticker}) Fiyat Grafiği")
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Davranışsal Analiz")
    son_fiyat = data['Close'].iloc[-1]
    degisim = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
    
    st.metric("Güncel Fiyat", f"{son_fiyat:.2f} TL", f"%{degisim:.2f}")
    
    st.info("""
    **Analiz Notu:** Bu hissedeki yüksek volatilite, yatırımcıların rasyonel karar verme süreçlerini zorlaştırarak 'Disposition Effect' riskini artırabilir.
    """)
    
    # Basit bir stres testi / simülasyon butonu
    if st.button("PGR/PLR Simülasyonunu Çalıştır"):
        st.write("Hesaplanıyor...")
        # Buraya makalendeki matematiksel formülü gerçek verilere (data['Close']) uygulayan kodu ekleyeceğiz.
