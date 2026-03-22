# Crypto Business Intelligence Dashboard - Project Highlights

## 📊 Overview
This project features a Business Intelligence (BI) dashboard built with Streamlit and Pandas to analyze a dataset of synthesized cryptocurrency transactions. The interactive web application provides key insights into trading frequencies, overall capitalization/spend, and recent trade activities.

<img width="1902" height="987" alt="image" src="https://github.com/user-attachments/assets/137c1586-761d-4de4-bb91-26ec6ec68e5b" />

---

## 🔑 Key Features & Highlights

### 1. Data Context & Reference Time 
The dashboard dynamically determines its reference time by parsing the most recent transaction in the dataset. Because the data is synthetic, this allows all time-based visualizations (like the last 24 hours or the past 7-day trend) to remain logically consistent regardless of the current real-world date.

### 2. Most Frequently Traded Symbols
Allows the user to view the cryptocurrency pairs/symbols with the highest number of transactions.
* **Interactive Element:** A slider to adjust the Top N symbols displayed (from 5 to 20).
* **Visualization:** A green bar chart plotting Transaction Count against Symbol.
<img width="937" height="701" alt="image" src="https://github.com/user-attachments/assets/6db779f5-1a63-408a-b3eb-e4806e0f041b" />


### 3. Symbols with Highest Spend (Capitalization)
Identifies which cryptocurrency symbols encapsulate the largest total spend (summing `bid_price` across all relevant transactions).
* **Interactive Element:** A slider to adjust the Top N symbols by spend.
* **Visualization:** A blue bar chart plotting Total Spend (USD) against Symbol.
<img width="931" height="667" alt="image" src="https://github.com/user-attachments/assets/12849114-8fa8-4a3d-a11c-22ce871406dd" />


### 4. Recent Market Activity (Last 24 Hours)
Isolates and details the most immediate trading data relative to the dataset's maximum date.
* **Metrics:** A high-level metric card displaying the exact count of transactions in the last 24 hours.
* **Data Table:** A detailed, sortable, and scrollable data frame showing the exact `transaction_id`, `symbol`, `bid_price` (formatted functionally to two decimal places), and `bid_time_dt` for the last day's trades.
<img width="1758" height="731" alt="image" src="https://github.com/user-attachments/assets/3313929b-e116-4688-ad75-0fa8b788a1fb" />


### 5. Weekly Capitalization Trend
Provides a time-series perspective on market capitalization over the past 7 days.
* **Visualization:** A smooth line graph with markers, plotting the daily aggregated sum of spend (USD) over the past week.
* Provides a quick visual summary of whether the local timeframe was a bull or bear trend for the logged transactions.
<img width="1855" height="967" alt="image" src="https://github.com/user-attachments/assets/ae331b7a-f783-46c0-be7e-34496d08d32e" />


---

## 🛠️ Technical Implementation details
- **Framework:** `streamlit` for frontend UI and interactivity.
- **Data Manipulation:** `pandas` for grouping, aggregating, and time-series filtering.
- **Visualizations:** `matplotlib` integrated into Streamlit layouts.
- **Performance:** Implements `@st.cache_data` to ensure the core dataset is not redundantly reloaded on every interactive state change, significantly speeding up the dashboard.
- **Custom Styling:** Includes a custom CSS block to apply sleek, dark `#1e1e1e` metric card stylings to the front-end layout.
