import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Page configuration
st.set_page_config(page_title="Crypto BI Dashboard", layout="wide")

# Theme / Style
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Crypto Business Intelligence Dashboard")

# 1. Data Loading and Preprocessing
@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        # Convert timestamps to datetime
        # Analyzing the data sample, timestamps are floats like 1766563200.0
        df['bid_time_dt'] = pd.to_datetime(df['bid_time'], unit='s')
        df['sell_time_dt'] = pd.to_datetime(df['sell_time'], unit='s')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

DATA_PATH = "synthetic_crypto_transactions.csv"
df = load_data(DATA_PATH)

if df is not None:
    # Determine Reference Time (Max Date in Dataset)
    max_date = df['bid_time_dt'].max()
    st.markdown(f"**Data Reference Date:** {max_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    st.warning("Note: All 'current' queries are relative to the latest transaction in the dataset, not today's real-time date.")

    # Layout
    col1, col2 = st.columns(2)

    # Query 1: Most Frequently Traded Symbols
    with col1:
        st.subheader("1. Most Frequently Traded Symbols")
        top_n_freq = st.slider("Select Top N Symbols (Frequency)", 5, 20, 10)
        freq_data = df['symbol'].value_counts().head(top_n_freq)
        
        fig_freq, ax_freq = plt.subplots(figsize=(10, 5))
        freq_data.plot(kind='bar', ax=ax_freq, color='#4CAF50')
        ax_freq.set_ylabel("Transaction Count")
        ax_freq.set_xlabel("Symbol")
        plt.xticks(rotation=45)
        st.pyplot(fig_freq)

    # Query 2: Symbols with Highest Spend (Capitalization)
    with col2:
        st.subheader("2. Symbols with Highest Spend")
        # Assumption: bid_price is the total spend for the transaction
        top_n_spend = st.slider("Select Top N Symbols (Spend)", 5, 20, 10)
        spend_data = df.groupby('symbol')['bid_price'].sum().sort_values(ascending=False).head(top_n_spend)
        
        fig_spend, ax_spend = plt.subplots(figsize=(10, 5))
        spend_data.plot(kind='bar', ax=ax_spend, color='#2196F3')
        ax_spend.set_ylabel("Total Spend (USD)")
        ax_spend.set_xlabel("Symbol")
        plt.xticks(rotation=45)
        st.pyplot(fig_spend)

    # Query 3: Trades from "24 Hours Ago" (Last 24h window relative to Max Date)
    st.subheader("3. Trades in the Last 24 Hours")
    
    # Calculate 24h window
    start_24h = max_date - datetime.timedelta(hours=24)
    last_24h_df = df[(df['bid_time_dt'] >= start_24h) & (df['bid_time_dt'] <= max_date)]
    
    st.metric("Transactions (Last 24h)", len(last_24h_df))
    
    st.dataframe(
        last_24h_df[['transaction_id', 'symbol', 'bid_price', 'bid_time_dt']]
        .sort_values(by='bid_time_dt', ascending=False)
        .style.format({"bid_price": "{:.2f}"})
    )

    # Query 4: Past Week Aggregated Capitalization (Line Graph)
    st.subheader("4. Daily Capitalization (Past 7 Days)")
    
    start_week = max_date - datetime.timedelta(days=7)
    # Filter for last week
    week_df = df[(df['bid_time_dt'] >= start_week) & (df['bid_time_dt'] <= max_date)].copy()
    
    # Group by Date
    week_df['date'] = week_df['bid_time_dt'].dt.date
    daily_cap = week_df.groupby('date')['bid_price'].sum()
    
    # Plotting
    if not daily_cap.empty:
        fig_line, ax_line = plt.subplots(figsize=(12, 6))
        daily_cap.plot(kind='line', ax=ax_line, marker='o', color='#FF9800', linewidth=2)
        ax_line.set_ylabel("Total Spend (USD)")
        ax_line.set_title("Capitalization per Day")
        ax_line.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig_line)
    else:
        st.info("No data available for the past week based on the current reference date.")

else:
    st.error("Data could not be loaded. Please ensure 'synthetic_crypto_transactions.csv' is in the directory.")
