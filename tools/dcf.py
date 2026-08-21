import sys
import yfinance as yf

# ANSI Color Codes for Terminal Styling
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def format_currency(val):
    if val is None:
        return "N/A"
    abs_val = abs(val)
    sign = "-" if val < 0 else ""
    if abs_val >= 1e12:
        return f"{sign}${abs_val/1e12:.2f}T"
    elif abs_val >= 1e9:
        return f"{sign}${abs_val/1e9:.2f}B"
    elif abs_val >= 1e6:
        return f"{sign}${abs_val/1e6:.2f}M"
    else:
        return f"{sign}${abs_val:,.2f}"

def parse_financial_number(s):
    s = s.strip().replace("$", "").replace(",", "").upper()
    if not s:
        raise ValueError("Empty string")

    multiplier = 1.0
    if s.endswith("T"):
        multiplier = 1e12
        s = s[:-1]
    elif s.endswith("B"):
        multiplier = 1e9
        s = s[:-1]
    elif s.endswith("M"):
        multiplier = 1e6
        s = s[:-1]
    elif s.endswith("K"):
        multiplier = 1e3
        s = s[:-1]

    return float(s) * multiplier

def get_user_float(prompt_text, default=None, is_percent=False):
    while True:
        if default is not None:
            default_str = f" [{default:.2f}%]" if is_percent else f" [{format_currency(default)}]"
        else:
            default_str = ""

        user_in = input(f"{Color.CYAN}{prompt_text}{default_str}: {Color.RESET}").strip()

        if not user_in and default is not None:
            return (float(default) / 100.0) if is_percent else float(default)

        try:
            if is_percent:
                val = float(user_in.replace("%", "").replace(",", ""))
                return val / 100.0
            else:
                return parse_financial_number(user_in)
        except ValueError:
            print(f"{Color.RED}Invalid input. Enter a number or shorthand like 123K, 123M, 1.5B.{Color.RESET}")

def get_user_int(prompt_text, default=None):
    while True:
        default_str = f" [{default}]" if default is not None else ""
        user_in = input(f"{Color.CYAN}{prompt_text}{default_str}: {Color.RESET}").strip()
        if not user_in and default is not None:
            return int(default)
        try:
            return int(user_in)
        except ValueError:
            print(f"{Color.RED}Invalid input. Please enter an integer.{Color.RESET}")

def main():
    print(f"{Color.BOLD}{Color.MAGENTA}\n============================================")
    print("      DISCOUNTED CASH FLOW (DCF) CALCULATOR  ")
    print(f"============================================{Color.RESET}\n")

    symbol = input(f"{Color.CYAN}Enter US Stock Ticker (e.g., AAPL, MSFT, NVDA): {Color.RESET}").strip().upper()
    if not symbol:
        print(f"{Color.RED}Ticker symbol cannot be empty.{Color.RESET}")
        sys.exit(1)

    print(f"\n{Color.YELLOW}Fetching financial data from Yahoo Finance for {symbol}...{Color.RESET}")
    ticker = yf.Ticker(symbol)

    try:
        info = ticker.info
    except Exception as e:
        print(f"{Color.RED}Error fetching data for {symbol}: {e}{Color.RESET}")
        sys.exit(1)

    current_price = info.get('currentPrice') or info.get('regularMarketPrice') or 0.0
    total_cash = info.get('totalCash') or 0.0
    total_debt = info.get('totalDebt') or 0.0
    shares_outstanding = info.get('sharesOutstanding') or 0.0

    # =========================================================
    # Calculate TTM Free Cash Flow from latest 4 quarters
    # =========================================================

    try:
        quarterly_cf = ticker.quarterly_cashflow

        if quarterly_cf.empty:
            raise ValueError("Quarterly cash-flow statement is empty.")

        # Newest quarters first
        quarterly_cf = quarterly_cf.sort_index(axis=1, ascending=False)

        ocf_row = "Operating Cash Flow"
        capex_row = "Capital Expenditure"

        if ocf_row not in quarterly_cf.index:
            raise ValueError(
                f"Could not find '{ocf_row}' in Yahoo cash-flow data."
            )

        if capex_row not in quarterly_cf.index:
            raise ValueError(
                f"Could not find '{capex_row}' in Yahoo cash-flow data."
            )

        # Latest 4 quarters
        latest_quarters = quarterly_cf.columns[:4]

        if len(latest_quarters) < 4:
            raise ValueError(
                f"Yahoo only returned {len(latest_quarters)} quarters; "
                "4 quarters are required for TTM FCF."
            )

        ocf_values = quarterly_cf.loc[ocf_row, latest_quarters]
        capex_values = quarterly_cf.loc[capex_row, latest_quarters]

        ttm_ocf = ocf_values.sum()
        ttm_capex = capex_values.sum()

        # Yahoo reports CapEx as a negative cash outflow.
        # Therefore FCF = OCF + CapEx.
        fcf_baseline = ttm_ocf + ttm_capex

    except Exception as e:
        print(
            f"{Color.RED}"
            f"Error calculating TTM FCF: {e}"
            f"{Color.RESET}"
        )
        sys.exit(1)

    if not current_price or not shares_outstanding:
        print(f"{Color.RED}Could not retrieve essential price or share data for '{symbol}'. Verify symbol.{Color.RESET}")
        sys.exit(1)

    print(f"\n{Color.BOLD}{Color.GREEN}--- Yahoo Finance Data Retrieved ---{Color.RESET}")
    print(f" Current Share Price : {Color.BOLD}${current_price:,.2f}{Color.RESET}")
    print(f" TTM Operating CF    : {format_currency(ttm_ocf)}")
    print(f" TTM Capital Expend. : {format_currency(ttm_capex)}")
    print(f" TTM Free Cash Flow  : {format_currency(fcf_baseline)}")
    print(f" Total Cash          : {format_currency(total_cash)}")
    print(f" Total Debt          : {format_currency(total_debt)}")
    print(f" Shares Outstanding  : {shares_outstanding:,.0f}")
    print(f"{Color.GREEN}------------------------------------{Color.RESET}\n")

    # =========================================================
    # Show the four quarterly FCF calculations
    # =========================================================

    print(f"{Color.BOLD}{Color.GREEN}--- TTM Free Cash Flow Calculation ---{Color.RESET}")

    print(
        f"{'Quarter':<18} | "
        f"{'Operating CF':<18} | "
        f"{'CapEx':<18} | "
        f"{'FCF':<18}"
    )

    print("-" * 78)

    for quarter in latest_quarters:
        quarter_ocf = float(ocf_values[quarter])
        quarter_capex = float(capex_values[quarter])
        quarter_fcf = quarter_ocf + quarter_capex

        print(
            f"{str(quarter):<18} | "
            f"{format_currency(quarter_ocf):<18} | "
            f"{format_currency(quarter_capex):<18} | "
            f"{format_currency(quarter_fcf):<18}"
        )

    print("-" * 78)

    print(
        f"{Color.BOLD}"
        f"TTM Free Cash Flow: "
        f"{Color.YELLOW}{format_currency(fcf_baseline)}"
        f"{Color.RESET}\n"
    )

    # =========================================================
    # DCF Assumptions
    # =========================================================

    print(f"{Color.BOLD}{Color.MAGENTA}--- Input DCF Assumptions (Shorthand allowed, e.g., 123M, 1.5B) ---{Color.RESET}")

    base_fcf = get_user_float("Starting Free Cash Flow ($)", default=fcf_baseline)
    years = get_user_int("Projection Horizon (Years)", default=5)
    growth_rate = get_user_float("Annual Growth Rate for Next X Years (%)", default=10.0, is_percent=True)
    discount_rate = get_user_float("Discount Rate / WACC (%)", default=9.0, is_percent=True)
    terminal_growth = get_user_float("Terminal Growth Rate (%)", default=2.5, is_percent=True)

    if discount_rate <= terminal_growth:
        print(f"\n{Color.RED}Error: Discount rate ({discount_rate*100:.2f}%) must be strictly greater than terminal growth rate ({terminal_growth*100:.2f}%).{Color.RESET}")
        sys.exit(1)

    print(f"\n{Color.BOLD}{Color.MAGENTA}============================================")
    print("         DCF CALCULATION BREAKDOWN          ")
    print(f"============================================{Color.RESET}")

    print(f"\n{Color.BOLD}1. Projected Free Cash Flows & Present Value (PV){Color.RESET}")
    print(f"{'Year':<6} | {'Projected FCF':<20} | {'Discount Factor':<18} | {'PV of FCF':<20}")
    print("-" * 72)

    pv_stage1_sum = 0.0
    latest_fcf = base_fcf

    for t in range(1, years + 1):
        latest_fcf *= (1 + growth_rate)
        discount_factor = (1 + discount_rate) ** t
        pv = latest_fcf / discount_factor
        pv_stage1_sum += pv
        print(f"{t:<6} | {format_currency(latest_fcf):<20} | {discount_factor:<18.4f} | {format_currency(pv):<20}")

    print("-" * 72)
    print(f"{Color.BOLD}Cumulative PV of Stage 1 Cash Flows: {Color.YELLOW}{format_currency(pv_stage1_sum)}{Color.RESET}\n")

    terminal_fcf = latest_fcf * (1 + terminal_growth)
    terminal_value = terminal_fcf / (discount_rate - terminal_growth)
    pv_terminal_value = terminal_value / ((1 + discount_rate) ** years)

    print(f"{Color.BOLD}2. Terminal Value Calculation{Color.RESET}")
    print(f" {f'Year {years} Terminal FCF':<28} : {format_currency(terminal_fcf)}")
    print(f" {'Undiscounted Terminal Value':<28} : {format_currency(terminal_value)}")
    print(f" {'PV of Terminal Value':<28} : {Color.YELLOW}{format_currency(pv_terminal_value)}{Color.RESET}\n")

    enterprise_value = pv_stage1_sum + pv_terminal_value
    equity_value = enterprise_value + total_cash - total_debt
    intrinsic_value_per_share = equity_value / shares_outstanding

    print(f"{Color.BOLD}3. Valuation Summary & Equity Bridge{Color.RESET}")
    print(f" Enterprise Value (EV)        : {format_currency(enterprise_value)}")
    print(f" (+) Total Cash               : {format_currency(total_cash)}")
    print(f" (-) Total Debt               : {format_currency(total_debt)}")
    print(f" = Equity Value               : {format_currency(equity_value)}")
    print(f" Shares Outstanding           : {shares_outstanding:,.0f}")

    upside_downside = ((intrinsic_value_per_share - current_price) / current_price) * 100
    color_verdict = Color.GREEN if upside_downside >= 0 else Color.RED

    print(f"\n{Color.BOLD}{Color.MAGENTA}============================================")
    print("                FINAL VERDICT               ")
    print(f"============================================{Color.RESET}")
    print(f" Current Market Price         : ${current_price:,.2f}")
    print(f" Intrinsic Value              : {Color.BOLD}${intrinsic_value_per_share:,.2f}{Color.RESET}")
    print(f" Estimated Upside/Downside    : {color_verdict}{Color.BOLD}{upside_downside:+.2f}%{Color.RESET}")

    if upside_downside >= 0:
        print(f" Status                       : {Color.GREEN}{Color.BOLD}UNDERVALUED{Color.RESET}")
    else:
        print(f" Status                       : {Color.RED}{Color.BOLD}OVERVALUED{Color.RESET}")

    print(f"{Color.MAGENTA}============================================{Color.RESET}\n")


if __name__ == "__main__":
    main()
