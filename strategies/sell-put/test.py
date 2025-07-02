import yfinance as yf
import pandas as pd
import numpy as np

# Function to get option data and handle errors
def get_option_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        options_dates = stock.options  # Get available expiration dates
        if not options_dates:
            print(f"No options available for {symbol}")
            return None

        # Select the closest expiration (around 30 days)
        exp_date = options_dates[0]  

        # Fetch option chain for the selected expiration
        opt_chain = stock.option_chain(exp_date)
        puts = opt_chain.puts

        # Get stock price
        stock_price = stock.history(period="1d")["Close"].iloc[-1]

        print(f"Fetching option data for {symbol} (Stock Price: {stock_price})")

        return puts, stock_price
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Function to find best put-selling candidates
def find_put_selling_candidates(tickers):
    results = []
    for symbol in tickers:
        option_data = get_option_data(symbol)
        if option_data is None:
            continue
        
        puts, stock_price = option_data

        # Print the first few rows to check the data
        print(puts.head())

        # Filter OTM puts (strike < stock price)
        otm_puts = puts[puts["strike"] < stock_price]

        # Ensure we're not filtering out all options by checking if otm_puts is empty
        if otm_puts.empty:
            print(f"No OTM puts for {symbol}")
            continue

        # Add additional filtering for valid options (e.g., minimum bid price)
        otm_puts = otm_puts[otm_puts["bid"] > 0.1]  # Minimum bid price threshold

        # Select a put with delta between -0.20 and -0.30 (just an approximation using the bid-ask spread)
        if not otm_puts.empty:
            best_put = otm_puts.iloc[0]  # You can refine this logic to choose based on delta
            strike_price = best_put["strike"]
            bid_price = best_put["bid"]
            ask_price = best_put["ask"]
            mid_price = (bid_price + ask_price) / 2  # Take midpoint price

            # Calculate premium return
            collateral = strike_price * 100  # Required margin
            premium = mid_price * 100  # Premium collected
            annualized_return = (premium / collateral) * (365 / 30) * 100  # Annualized %

            results.append({
                "Stock": symbol,
                "Stock Price": round(stock_price, 2),
                "Strike Price": round(strike_price, 2),
                "Mid Premium": round(mid_price, 2),
                "Annualized Return %": round(annualized_return, 2),
            })

    return pd.DataFrame(results)

# Example: List of high IV stocks (you can replace this with a dynamic IV screener)
high_iv_stocks = ["TSLA", "NVDA", "AMD", "AAPL", "AMZN"]

# Get best put-selling opportunities
df_puts = find_put_selling_candidates(high_iv_stocks)

# Show results
print(df_puts)
