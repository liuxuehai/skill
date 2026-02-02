# Usage Examples Reference

## Quick Global Analysis

```python
from scripts.stock_analyzer import GlobalStockAnalyzer

analyzer = GlobalStockAnalyzer()

# US stock analysis
result = analyzer.analyze_global_stock('AAPL', days_back=90)
analyzer.print_global_stock_report(result)

# Chinese stock analysis
result = analyzer.analyze_global_stock('000001.SS', days_back=180)
analyzer.print_global_stock_report(result)

# Hong Kong stock analysis
result = analyzer.analyze_global_stock('0700.HK', days_back=90)
analyzer.print_global_stock_report(result)
```

## Custom Date Range

```python
from scripts.stock_fetcher import GlobalStockDataFetcher

fetcher = GlobalStockDataFetcher()
validation = fetcher.validate_symbol('000001.SS', check_trading_data=True)

result = analyzer.analyze_global_stock(
    stock_code='600519.SS',
    start_date='2024-06-01',
    end_date='2024-12-31'
)
analyzer.print_global_stock_report(result)
```

## Multi-Market Batch Processing

```python
global_stocks = [
    'AAPL',        # US
    '000001.SS',   # China SSE
    '0700.HK',     # Hong Kong
    '7203.T',      # Japan
    'SAP.DE',      # Germany
    'MC.PA'        # France
]

for symbol in global_stocks:
    print(f"\nAnalyzing {symbol}...")
    result = analyzer.analyze_global_stock(symbol, days_back=90)
    if result['success']:
        print(f"Price: {result['current_price']:.2f}")
        print(f"Change: {result['price_change_pct']:+.2f}%")
    time.sleep(1)  # API rate limit compliance
```

## Market Information Retrieval

```python
exchanges = fetcher.get_supported_exchanges()
for market, info in exchanges.items():
    print(f"{market}: {info['description']}")
    print(f"Examples: {', '.join(info['examples'][:3])}")

recommendations = fetcher.get_stock_recommendations('AAPL')
if recommendations['has_recommendations']:
    print(f"\n{recommendations['symbol']} Analyst Ratings:")
    print(f"Buy: {recommendations['buy_count']} ({recommendations['buy_percent']:.1f}%)")
    print(f"Hold: {recommendations['hold_count']} ({recommendations['hold_percent']:.1f}%)")
    print(f"Sell: {recommendations['sell_count']} ({recommendations['sell_percent']:.1f}%)")
```

## Error Handling Patterns

```python
test_symbols = ['AAPL', '000001.SS', 'INVALID']
for symbol in test_symbols:
    validation = fetcher.validate_symbol(symbol)
    if validation['is_valid']:
        print(f"✓ Valid: {validation['company_name']}")
    else:
        print(f"✗ Invalid: {validation['error']}")
```

## Best Practices
1. Always validate symbols before analysis
2. Add `time.sleep(1)` between requests
3. Check `result['success']` before accessing data
4. Use bilingual reporting for international teams
5. Combine multiple indicators for signal confirmation