# Core Components Reference

## 1. GlobalStockDataFetcher

**File**: `scripts/stock_fetcher.py`

### Key Methods
```python
class GlobalStockDataFetcher:
    def get_stock_data(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """Fetches historical OHLCV data"""
    
    def validate_symbol(self, symbol: str, check_trading_data: bool = False) -> dict:
        """Validates symbol format and trading status"""
    
    def get_company_info(self, symbol: str) -> dict:
        """Retrieves company fundamentals"""
```

### Usage Patterns
```python
# Basic data fetch
fetcher = GlobalStockDataFetcher()
df = fetcher.get_stock_data('AAPL', '2024-01-01', '2024-12-31')

# Symbol validation
validation = fetcher.validate_symbol('000001.SS', check_trading_data=True)
```

## 2. TechnicalAnalyzer

**File**: `scripts/technical_analysis.py`

### Indicator Calculations
| Indicator | Method | Parameters |
|-----------|--------|------------|
| RSI | `calculate_rsi()` | period=14 |
| MACD | `calculate_macd()` | fast=12, slow=26, signal=9 |
| Bollinger | `calculate_bollinger()` | window=20, num_std=2 |
| KDJ | `calculate_kdj()` | n=9, m1=3, m2=3 |

### Signal Generation
```python
class TechnicalAnalyzer:
    def generate_signals(self, df: pd.DataFrame) -> List[TradingSignal]:
        """Generates BUY/SELL signals based on indicator consensus"""
```

## 3. GlobalStockAnalyzer

**File**: `scripts/stock_analyzer.py`

### Workflow
1. Fetch data via `GlobalStockDataFetcher`
2. Calculate indicators via `TechnicalAnalyzer`
3. Generate signals and confidence scores
4. Format bilingual report

### Example Output
```json
{
  "current_price": 192.34,
  "price_change_pct": -1.25,
  "choices": [
    {"type": "SELL", "indicator": "RSI", "value": 72.3},
    {"type": "SELL", "indicator": "MACD", "value": -0.45}
  ],
  "confidence": 0.85
}
```

### Error Example
```json
{
  "error": {
    "code": "invalid_symbol",
    "message": "Invalid stock symbol format",
    "details": "Use .SS suffix for Shanghai stocks"
  }
}
```

## 4. StockVisualizer

**File**: `scripts/visualization.py`

### Supported Charts
- Price chart with volume
- Technical indicator overlays
- Bollinger Bands visualization
- Candlestick patterns

### Best Practices
- Always call `plt.close()` after saving figures
- Use `dpi=300` for print-quality output
- Include grid lines for readability