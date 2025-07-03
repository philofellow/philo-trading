import math
import time
import yfinance as yf
import pandas as pd

# usage: python main.py > res

#data_file = "sp500.data"
#data_file = "russell2000.data"
data_file = "russell3000.data"
#data_file = "custom.data"
topn = 200
low = 0.7
high = 0.95

# Step 1: Get stock list from local data file
def parse_data(datafile):
    f = open(datafile)
    symbols = []
    for line in f:
        line = line.strip()
        print(line)
        if line[0] == '#':
            continue
        s = line.split()[0].strip()
        if s != '-':
          symbols.append(s)
    print(f"{len(symbols)} stocks {symbols}.")
    return symbols
        
# Step 2: Calculate the weekly volatility for each stock
def calculate_weekly_volatility(stock_symbols, topn, batch_size=300):
    volatility_data = []
    
    # Split stock symbols into batches
    for i in range(0, len(stock_symbols), batch_size):
        batch = stock_symbols[i:i + batch_size]
        print(f"Fetching data for batch {i // batch_size + 1} ({len(batch)} stocks)...")

        time.sleep(30)  # Sleep for 5 seconds between requests
        # Download historical data for all symbols in the batch
        hist = yf.download(batch, period="5d", group_by="ticker", progress=False)

        for symbol in batch:
            print(f"Processing stock {symbol}...")

            # Handle cases where data is missing
            if symbol not in hist or hist[symbol].empty:
                print(f"Skipping {symbol}: No data found.")
                continue  

            stock_hist = hist[symbol]

            if len(stock_hist) < 2:
                print(f"Skipping {symbol}: Insufficient data.")
                continue  

            # Calculate daily returns and volatility
            daily_returns = stock_hist['Close'].pct_change().dropna()
            volatility = daily_returns.std()  # Standard deviation as volatility
            
            print(f"Volatility for {symbol}: {volatility}")
            volatility_data.append((symbol, volatility))

    # Convert to DataFrame and sort by volatility
    vol_df = pd.DataFrame(volatility_data, columns=["Ticker", "Volatility"]).sort_values(by="Volatility", ascending=False)
    topn_stocks = vol_df.head(topn)

    print(f"\nTop {topn} Most Volatile Stocks (Past Week):")
    print(topn_stocks)

    return topn_stocks["Ticker"].tolist()

# Step 3: Get the price of the put options for the selected stocks
def get_put_options(stock_ticker):
    print(f"\nCalculating put selling metrics for {stock_ticker}")
    stock = yf.Ticker(stock_ticker)
    price = -1
    
    # Get the current trading price or the previous close price
    try:
        stock_info = stock.info
        # Check if the market is currently open
        current_price = stock_info.get("currentPrice", None)
        previous_close = stock_info.get("regularMarketPreviousClose", None)

        if current_price:
            price = current_price
        elif previous_close:
            price = previous_close 
        else:
            print("Price data is unavailable.")
    except Exception as e:
        print(f"An error occurred when getting {stock_ticker} price: {e}")

    # Get the next earnings date
    try:
       #  earnings_date = stock.earnings_dates.index[3].strftime("%Y%m%d") if len(stock.earnings_dates) >= 4 else "N/A"
       earnings_date = stock.calendar['Earnings Date'][0])
    except (KeyError, TypeError):
        print(f"\n{stock_ticker} does not have valid earnings date")
        earnings_date = "N/A"

    # Filter options that expire in 1 to 4 weeks from now
    exp_dates = stock.options[:4]  # Assumes options expiration dates are sorted chronologically
    if len(exp_dates) < 2:
        return None  # Skip if there aren't enough expiration dates

    option_data = []

    for exp_date in exp_dates:
        options_chain = stock.option_chain(exp_date)
        puts = options_chain.puts

        # Filter puts with strike prices 10-20% below current price
        min_strike = price * low 
        max_strike = price * high 
        filtered_puts = puts[(puts["strike"] >= min_strike) & (puts["strike"] <= max_strike)]

        for _, put in filtered_puts.iterrows():
            # Calculate the average of bid and ask prices
            put_price = ((0 if math.isnan(put["bid"]) else put["bid"]) + (0 if math.isnan(put["ask"]) else put["ask"])) / 2
            metric = (price - put["strike"]) * put_price / (price * price)

            # Calculate maximum contracts based on $10,000 exposure risk
            max_contracts = 10000 // (put["strike"] * 100) if put["strike"] > 0 else 0
            profit = max_contracts * 100 * put_price  # Potential profit from selling puts

            option_data.append({
                "Ticker": stock_ticker,
                "Price": price,
                "Expiration": exp_date,
                "StrikePrice": put["strike"],
                "Bid": put["bid"],
                "Ask": put["ask"],
                "Avg": put_price,
                "Metric": metric,
                "ContractsToSell": max_contracts,
                "PotentialProfit": profit,
                "EarningsDate": earnings_date
            })
            print(option_data[-1])
    return pd.DataFrame(option_data)

def get_stars(metric):
    # Start with an empty string for stars
    star_count = int(metric * 1000)  # Multiply metric by 1000 to determine the number of stars
    return '*' * star_count

# Step 4: Calculate and display the metric for each option
def main():
    # Display results in a nicely formatted output
    #pd.set_option("display.float_format", "{:.4f}".format)  # Set decimal precision
    # Set the display option to show more columns
    pd.set_option('display.max_rows', None)  # No row limit
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', None)        # No width limit, let it auto-adjust

    stock_symbols = parse_data(data_file)
    top_stocks = calculate_weekly_volatility(stock_symbols, topn)
    all_options_data = []

    for stock_ticker in top_stocks:
        time.sleep(5)  # Delay to avoid rate limiting
        try:
          option_data = get_put_options(stock_ticker)
          if option_data is not None and not option_data.empty:
              all_options_data.append(option_data)
        except Exception as e:
          print(f"An error occurred when getting put option data for {stock_ticker}: {e}")

    # Concatenate all dataframes into one for easy viewing
    final_df = pd.concat(all_options_data, ignore_index=True)
    final_df['Rank'] = final_df['Metric'].apply(get_stars)

    final_df['Price'] = final_df['Price'].round(2)
    final_df['StrikePrice'] = final_df['StrikePrice'].round(2)
    final_df['Bid'] = final_df['Bid'].round(2)
    final_df['Ask'] = final_df['Ask'].round(2)
    final_df['Avg'] = final_df['Avg'].round(3)
    final_df['Metric'] = final_df['Metric'].round(4)
    final_df['ContractsToSell'] = final_df['ContractsToSell'].round(0).astype(int)
    final_df['PotentialProfit'] = final_df['PotentialProfit'].round(2)

    print("\nOption Data with Computed Metric:")
    print(final_df)

if __name__ == "__main__":
    main()
