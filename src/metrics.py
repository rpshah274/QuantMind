import yfinance as yf

def get_metrics(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "revenue": info.get("totalRevenue"),
        "profit_margin": info.get("profitMargins"),
        "debt_to_equity": info.get("debtToEquity"),
        "current_ratio": info.get("currentRatio"),
        "return_on_equity": info.get("returnOnEquity"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "analyst_rating": info.get("recommendationKey")
    }
    
def format_metrics(metrics: dict) -> str:
    """
    Convert the metrics dict into a readable string
    that can be injected into a prompt.
    
    Example output:
    Company: Apple Inc. (AAPL)
    Sector: Technology
    Market Cap: $3.2T
    P/E Ratio: 28.5
    ...
    Format numbers nicely:
    - Market cap in trillions/billions
    - Margins as percentages
    - Round floats to 2 decimal places
    """
    mc = metrics["market_cap"]
    mc_str = f"${mc/1e12:.2f}T" if mc and mc >= 1e12 else f"${mc/1e9:.2f}B" if mc and mc >= 1e9 else f"${mc/1e6:.2f}M" if mc and mc >= 1e6 else "N/A"
     
    rev = metrics["revenue"]
    rev_str = f"${rev/1e12:.2f}T" if rev and rev >= 1e12 else f"${rev/1e9:.2f}B" if rev and rev >= 1e9 else f"${rev/1e6:.2f}M" if rev and rev >= 1e6 else "N/A"

    return f"""
    Company: {metrics['company_name']} ({metrics['ticker']})
    Sector: {metrics['sector']}
    Market Cap: {mc_str}
    Revenue: {rev_str}
    P/E Ratio: {metrics['pe_ratio']}
    Forward P/E: {metrics['forward_pe']}
    Profit Margin: {round(metrics['profit_margin'] * 100, 2) if metrics['profit_margin'] else 'N/A'}%
    Debt to Equity: {metrics['debt_to_equity']}
    Current Ratio: {metrics['current_ratio']}
    Return on Equity: {round(metrics['return_on_equity'] * 100, 2) if metrics['return_on_equity'] else 'N/A'}%
    52 Week High: ${metrics['52_week_high']}
    52 Week Low: ${metrics['52_week_low']}
    Analyst Rating: {metrics['analyst_rating']}
    """