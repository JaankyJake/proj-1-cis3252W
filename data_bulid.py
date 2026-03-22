import csv
import math
import uuid
import random
import datetime
import time

def generate_symbols(n=190):
    symbols = []
    baselines = {}
    
    # Generate random 3-5 letter symbols
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while len(symbols) < n:
        length = random.randint(3, 5)
        # weight towards 3 letter symbols as they are more common
        if random.random() < 0.7:
             length = 3
        sym = ''.join(random.choice(letters) for _ in range(length))
        if sym not in symbols:
            symbols.append(sym)
            # Baseline price: mix of low (<$1), med ($1-$100), high ($100-$50000)
            # Use loguniform distribution approximation
            # np.exp(np.random.uniform(np.log(0.001), np.log(60000))) -> math.exp(random.uniform(...))
            
            min_log = math.log(0.001)
            max_log = math.log(60000)
            price = math.exp(random.uniform(min_log, max_log))
            baselines[sym] = round(price, 6)
            
    return symbols, baselines

def generate_data():
    symbols, baselines = generate_symbols(190)
    data = []
    
    # Start date - let's say it's 30 days ago from now, rounded to start of day
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    total_days = 30
    trades_per_day = 3000
    
    print(f"Generating data for {total_days} days with {trades_per_day} trades per day...")
    
    output_file = "synthetic_crypto_transactions.csv"
    headers = [
        'transaction_id', 'symbol', 'bid_price', 'bid_order_id', 
        'bid_time', 'sell_time', 'sell_price', 'sell_order_id', 
        'sell_order_settle_time'
    ]
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for day in range(total_days):
            current_day_start = start_date + datetime.timedelta(days=day)
            # Base timestamp for the day in unix seconds
            day_base_ts = current_day_start.timestamp()
            
            # We need to distribute 3000 trades over the day (86400 seconds)
            avg_interval = 86400 / trades_per_day
            
            for i in range(trades_per_day):
                # Select random symbol
                sym = random.choice(symbols)
                base_price = baselines[sym]
                
                # Bid Price: baseline +/- 1-10%
                change_pct = random.uniform(0.01, 0.10)
                if random.random() < 0.5:
                    bid_price = base_price * (1 - change_pct)
                else:
                    bid_price = base_price * (1 + change_pct)
                    
                # Bid Time: Day start + i * interval + jitter
                # jitter +/- 50% of interval
                jitter = random.uniform(-0.5 * avg_interval, 0.5 * avg_interval)
                bid_time_offset = (i * avg_interval) + jitter
                
                # Ensure we don't go negative or past 24h too much
                if bid_time_offset < 0: bid_time_offset = 0
                
                bid_time = day_base_ts + bid_time_offset
                
                # Sell Time: 1 second later
                sell_time = bid_time + 1
                
                # Sell Price: 1% higher than bid price
                sell_price = bid_price * 1.01
                
                # Settle Time: Sell time + random delay (0-5s)
                sell_order_settle_time = sell_time + random.uniform(0, 5)
                
                # IDs
                transaction_id = str(uuid.uuid4())
                bid_order_id = str(uuid.uuid4())
                sell_order_id = str(uuid.uuid4())
                
                # We save to file but also keep track of count
                row = {
                    'transaction_id': transaction_id,
                    'symbol': sym,
                    'bid_price': round(bid_price, 8),
                    'bid_order_id': bid_order_id,
                    'bid_time': bid_time,
                    'sell_time': sell_time,
                    'sell_price': round(sell_price, 8),
                    'sell_order_id': sell_order_id,
                    'sell_order_settle_time': sell_order_settle_time
                }
                writer.writerow(row)
                data.append(row)
            
    return output_file, len(data), symbols

if __name__ == "__main__":
    output_file, row_count, symbols = generate_data()
    print(f"Successfully generated {row_count} rows to {output_file}")
    
    # Verification output
    print(f"Unique Symbols: {len(set(symbols))}")
