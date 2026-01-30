# AGENTS.md

## Overview
This repository provides tools for analyzing both **US stocks** (via Yahoo Finance) and **Chinese A-shares** (via AKShare/Tushare). While two parallel implementations exist, the primary CLI interface targets US stocks.

## Essential Commands

### Setup
```bash
# Recommended: use uv for dependency management
uv sync

# Alternative: use pip
pip install -r requirements.txt
```

### Run Analysis
```bash
# Analyze single US stock
python scripts/us_stock_analyzer.py BABA

# Batch analyze default US stocks (BABA, AAPL, TSLA, MSFT)
python scripts/us_stock_analyzer.py

# Use CLI after installation (if built)
stock-analyzer BABA
```

### Test Functionality
```bash
# Run functional test (checks mock and akshare data)
python test_skill.py

# Run usage example
python example.py
```

### Development Tools
```bash
# Format code
black .

# Lint
flake8

# Future note: no test runner defined yet (e.g., pytest)
```

## Code Organization

```
stock-analysis/
├── scripts/
│   ├── us_stock_analyzer.py       # Main entry for US stocks
│   ├── us_stock_fetcher.py        # Data fetcher using yfinance
│   ├── stock_analyzer.py          # Analyzer for Chinese A-shares
│   ├── stock_fetcher.py           # Data fetcher using akshare/tushare
│   ├── technical_analysis.py      # Shared indicators (MA, MACD, RSI, Bollinger, KDJ)
│   └── visualization.py           # Plotting functions
├── pyproject.toml                 # Project config + CLI definition
├── requirements.txt               # Dependencies (fallback)
├── example.py                     # Example usage with mock data
├── test_skill.py                  # Basic integration test
├── SKILL.md                       # Documentation and usage guide
└── uv.lock                        # Dependency lock file
```

## Naming Conventions & Style Patterns

- **File Names**: Snake case, descriptive, often prefixed by target (`us_stock_`, `stock_`)
- **Classes**: PascalCase (`StockAnalyzer`, `TechnicalAnalyzer`)
- **Functions**: snake_case (`analyze_stock`, `calculate_macd`)
- **Constants**: UPPERCASE (`BUY`, `SELL`)
- **Logging/Output**: Mixed English and Chinese; prefer UTF-8 encoding
- **Delays**: Always include `time.sleep(1)` when looping over multiple stocks to avoid API throttling

## Testing Approach

- Ad-hoc testing via `test_skill.py`:
  - First tests internal logic with mock data
  - Then tries real data via `akshare` (optional)
- No formal test runner (e.g., `pytest`, `unittest`) configured in `pyproject.toml`
- Assertions are manual prints and condition checks
- Expected to run interactively during development

## Important Gotchas

- **Two Analyzers Exist**: Be careful not to mix up `stock_analyzer.py` (China) and `us_stock_analyzer.py` (US)
- **Primary CLI Points to US Version**:
  ```toml
  [project.scripts]
  stock-analyzer = "scripts.us_stock_analyzer:main"
  ```
- **API Rate Limits**: Yahoo Finance and AKShare impose rate limits — always add delays in loops
- **Data Source Flexibility**:
  - Default: simulated/mock data
  - Real data: specify `data_source='akshare'` or `'tushare'`
  - Tushare requires API key
- **Encoding Issues Possible**: Especially on Windows; ensure console uses UTF-8 (`chcp 65001`)
- **Confidence Scoring**: Based on dominance of buy/sell signals in last 10 events (range: 50%–100%)

## Project-Specific Context

From `SKILL.md`:
- Signal types: BUY, SELL, HOLD, WAIT
- Indicators used: MA, MACD, RSI, Bollinger Bands, KDJ
- Recommendation engine weighs signal counts and consistency
- Visualization scripts available but not auto-invoked
- Performance tip: Avoid analysis periods < 30 days

## Recommendations for Agents

- Always start with `uv sync` unless instructed otherwise
- Prefer `scripts/us_stock_analyzer.py` unless working specifically with Chinese markets
- When extending, follow existing pattern: new indicator → method in `TechnicalAnalyzer` → update signal logic
- Add `time.sleep()` in bulk operations
- Check return value `result['success']` before accessing fields
- Never assume real data is available — handle failures gracefully