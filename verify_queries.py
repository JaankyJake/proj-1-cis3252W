import pandas as pd
import datetime

def verify():
    filepath = "synthetic_crypto_transactions.csv"
    print(f"Loading {filepath}...")
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print("Error: File not found.")
        return

    # Convert timestamps
    df['bid_time_dt'] = pd.to_datetime(df['bid_time'], unit='s')
    
    max_date = df['bid_time_dt'].max()
    print(f"Max Date in DB: {max_date}")

    # 1. Frequency
    print("\n--- Top 3 Frequent Symbols ---")
    print(df['symbol'].value_counts().head(3))

    # 2. Spend
    print("\n--- Top 3 Highest Spend Symbols ---")
    print(df.groupby('symbol')['bid_price'].sum().sort_values(ascending=False).head(3))

    # 3. 24h Trades
    start_24h = max_date - datetime.timedelta(hours=24)
    last_24h_df = df[(df['bid_time_dt'] >= start_24h) & (df['bid_time_dt'] <= max_date)]
    print(f"\n--- Trades in Last 24h ({start_24h} to {max_date}) ---")
    print(f"Count: {len(last_24h_df)}")
    if not last_24h_df.empty:
        print("Sample:")
        print(last_24h_df[['symbol', 'bid_price', 'bid_time_dt']].head(2))

    # 4. Weekly Cap
    start_week = max_date - datetime.timedelta(days=7)
    week_df = df[(df['bid_time_dt'] >= start_week) & (df['bid_time_dt'] <= max_date)].copy()
    week_df['date'] = week_df['bid_time_dt'].dt.date
    daily_cap = week_df.groupby('date')['bid_price'].sum()
    print(f"\n--- Daily Cap (Last 7 Days) ---")
    print(daily_cap)

if __name__ == "__main__":
    verify()
