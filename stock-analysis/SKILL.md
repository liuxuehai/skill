# Stock Analysis Skill

## Overview
This skill provides comprehensive global stock data analysis capabilities using Yahoo Finance API, supporting stocks from multiple markets including US, China, Hong Kong, Japan, Europe, and more. It includes data fetching, technical indicator calculation, and buy/sell signal generation for global markets.

## Quick Start

### Basic Usage

```python
from scripts.stock_analyzer import GlobalStockAnalyzer
from scripts.stock_fetcher import GlobalStockDataFetcher

# 创建分析器
analyzer = GlobalStockAnalyzer()

# 分析全球股票
result = analyzer.analyze_global_stock('AAPL', days_back=90)
analyzer.print_global_stock_report(result)

# 验证股票代码
fetcher = GlobalStockDataFetcher()
validation = fetcher.validate_symbol('000001.SS', check_trading_data=True)
print(f"股票验证结果: {validation}")

# 获取支持的交易所信息
exchanges = fetcher.get_supported_exchanges()
for market, info in exchanges.items():
    print(f"{market}: {info['description']} - {info['examples']}")

# 获取股票推荐信息
recommendations = fetcher.get_stock_recommendations('AAPL')
print(f"股票推荐: {recommendations}")
```

## Supported Markets

### 1. US Markets (NYSE, NASDAQ)
- **Format**: Direct stock codes (e.g., 'AAPL', 'MSFT', 'GOOGL', 'TSLA')
- **Examples**: 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA'
- **Notes**: No suffix required

### 2. China Shanghai Stock Exchange (SSE)
- **Format**: 6-digit codes with '.SS' suffix
- **Examples**: '000001.SS', '600000.SS', '600519.SS' (Ping An Bank, SPDB, Kweichow Moutai)
- **Notes**: '.SS' indicates Shanghai Stock Exchange

### 3. China Shenzhen Stock Exchange (SZSE)
- **Format**: 6-digit codes with '.SZ' suffix
- **Examples**: '000001.SZ', '002415.SZ', '300750.SZ' (Ping An Bank, Hikvision, CATL)
- **Notes**: '.SZ' indicates Shenzhen Stock Exchange

### 4. Hong Kong Stock Exchange (HKEX)
- **Format**: 4-5 digit codes with '.HK' suffix
- **Examples**: '0700.HK', '0941.HK', '0998.HK' (Tencent, China Mobile, CITIC)
- **Notes**: '.HK' indicates Hong Kong Stock Exchange

### 5. Tokyo Stock Exchange (TSE)
- **Format**: 4-digit codes with '.T' suffix
- **Examples**: '7203.T', '9984.T', '6758.T' (Toyota, SoftBank, Sony)
- **Notes**: '.T' indicates Tokyo Stock Exchange

### 6. German Stock Exchange (Xetra)
- **Format**: Company codes with '.DE' suffix
- **Examples**: 'SAP.DE', 'BMW.DE', 'VOW3.DE' (SAP, BMW, Volkswagen)
- **Notes**: '.DE' indicates German Stock Exchange

### 7. French Stock Exchange (Euronext Paris)
- **Format**: Company codes with '.PA' suffix
- **Examples**: 'MC.PA', 'SAN.PA', 'OR.PA' (LVMH, Sanofi, L'Oréal)
- **Notes**: '.PA' indicates Euronext Paris

### 8. London Stock Exchange (LSE)
- **Format**: Company codes with '.L' suffix
- **Examples**: 'HSBA.L', 'BARC.L', 'RIO.L' (HSBC, Barclays, Rio Tinto)
- **Notes**: '.L' indicates London Stock Exchange

## Core Components

### 1. GlobalStockDataFetcher (`scripts/stock_fetcher.py`)

Fetches stock data from Yahoo Finance API with global market support:

```python
from scripts.stock_fetcher import GlobalStockDataFetcher

fetcher = GlobalStockDataFetcher()

# 获取股票数据
df = fetcher.get_stock_data('000001.SS', '2024-01-01', '2024-12-31')

# 验证股票代码
validation = fetcher.validate_symbol('AAPL', check_trading_data=True)
print(f"股票验证: {validation}")

# 获取公司信息
company_info = fetcher.get_company_info('AAPL')
print(f"公司信息: {company_info}")

# 获取股票推荐
recommendations = fetcher.get_stock_recommendations('AAPL')
print(f"分析师推荐: {recommendations}")

# 获取支持的交易所
exchanges = fetcher.get_supported_exchanges()
for market, info in exchanges.items():
    print(f"{market}: {info['description']}")
```

**Features:**
- Global market support (US, China, HK, Japan, Europe)
- Automatic symbol formatting for different exchanges
- Retry logic with exponential backoff
- Comprehensive error handling
- Symbol validation with trading data check

**Supported Markets:**
- US Markets (NYSE, NASDAQ)
- China Shanghai/Shenzhen Stock Exchanges
- Hong Kong Stock Exchange
- Tokyo Stock Exchange
- German Stock Exchange (Xetra)
- French Stock Exchange (Euronext Paris)
- London Stock Exchange
- And more global markets

### 2. TechnicalAnalyzer (`scripts/technical_analysis.py`)

Calculates technical indicators and generates trading signals:

**Technical Indicators:**
- Moving Averages (MA): 5, 10, 20, 60 periods
- Exponential Moving Averages (EMA): 12, 26 periods
- MACD (Moving Average Convergence Divergence)
- RSI (Relative Strength Index): 14 periods
- Bollinger Bands: 20 periods, 2 standard deviations
- KDJ: 9 periods
- Volume indicators

**Signal Generation:**
- Golden/Death Cross signals (MA5 vs MA20)
- MACD crossover signals
- RSI overbought/oversold signals
- Bollinger Band bounce signals
- KDJ extreme signals

```python
from scripts.technical_analysis import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()
analysis_result = analyzer.analyze_stock(df)
```

### 3. GlobalStockAnalyzer (`scripts/stock_analyzer.py`)

Main interface combining data fetching and analysis for global markets:

```python
from scripts.stock_analyzer import GlobalStockAnalyzer

analyzer = GlobalStockAnalyzer()
result = analyzer.analyze_global_stock('AAPL', days_back=180)
analyzer.print_global_stock_report(result)
```

**Features:**
- Global market support
- Comprehensive error handling
- Automatic date range calculation
- Multi-indicator signal generation
- Confidence scoring
- Detailed reporting

### 4. StockVisualizer (`scripts/visualization.py`)

Creates visualizations for global stock data:

```python
from scripts.visualization import StockVisualizer

visualizer = StockVisualizer()
visualizer.plot_price_chart(df, 'AAPL')
visualizer.plot_technical_indicators(df, 'AAPL')
visualizer.plot_bollinger_bands(df, 'AAPL')
visualizer.plot_candlestick_chart(df, 'AAPL')
```

## Usage Examples

### Example 1: Quick Global Analysis

```python
from scripts.stock_analyzer import GlobalStockAnalyzer

analyzer = GlobalStockAnalyzer()

# 分析美国股票
result = analyzer.analyze_global_stock('AAPL', days_back=90)
analyzer.print_global_stock_report(result)

# 分析中国股票
result = analyzer.analyze_global_stock('000001.SS', days_back=180)
analyzer.print_global_stock_report(result)

# 分析香港股票
result = analyzer.analyze_global_stock('0700.HK', days_back=90)
analyzer.print_global_stock_report(result)
```

### Example 2: Custom Date Range and Validation

```python
from scripts.stock_fetcher import GlobalStockDataFetcher

# 验证股票代码
fetcher = GlobalStockDataFetcher()
validation = fetcher.validate_symbol('000001.SS', check_trading_data=True)
print(f"股票验证: {validation}")

# 自定义日期范围分析
result = analyzer.analyze_global_stock(
    stock_code='600519.SS',
    start_date='2024-06-01',
    end_date='2024-12-31'
)
analyzer.print_global_stock_report(result)
```

### Example 3: Multiple Global Markets Analysis

```python
# 分析多个市场的股票
global_stocks = [
    'AAPL',        # 美国苹果
    '000001.SS',   # 中国平安银行
    '0700.HK',     # 香港腾讯
    '7203.T',      # 日本丰田
    'SAP.DE',      # 德国SAP
    'MC.PA'        # 法国LVMH
]

for symbol in global_stocks:
    print(f"\n分析 {symbol}...")
    result = analyzer.analyze_global_stock(symbol, days_back=90)
    if result['success']:
        print(f"当前价格: {result['current_price']:.2f}")
        print(f"涨跌幅: {result['price_change_pct']:+.2f}%")
    else:
        print(f"分析失败: {result['error']}")
    
    # 避免请求过快
    import time
    time.sleep(1)
```

### Example 4: Market Information Retrieval

```python
from scripts.stock_fetcher import GlobalStockDataFetcher

fetcher = GlobalStockDataFetcher()

# 获取支持的交易所信息
exchanges = fetcher.get_supported_exchanges()
print("支持的交易所:")
for market, info in exchanges.items():
    print(f"  {market}: {info['description']}")
    print(f"  示例: {', '.join(info['examples'][:3])}")

# 获取股票推荐信息
recommendations = fetcher.get_stock_recommendations('AAPL')
if recommendations['has_recommendations']:
    print(f"\n{recommendations['symbol']} 分析师推荐:")
    print(f"  日期: {recommendations['date']}")
    print(f"  分析师数量: {recommendations['total_analysts']}")
    print(f"  买入: {recommendations['buy_count']} ({recommendations['buy_percent']:.1f}%)")
    print(f"  持有: {recommendations['hold_count']} ({recommendations['hold_percent']:.1f}%)")
    print(f"  卖出: {recommendations['sell_count']} ({recommendations['sell_percent']:.1f}%)")
    print(f"  平均评分: {recommendations['average_rating']}/5")
```

### Example 5: Error Handling and Validation

```python
from scripts.stock_fetcher import GlobalStockDataFetcher

fetcher = GlobalStockDataFetcher()

# 测试不同格式的股票代码
test_symbols = [
    'AAPL',           # 美国股票
    '000001.SS',      # 中国上海股票
    '000001.SZ',      # 中国深圳股票
    '0700.HK',        # 香港股票
    '7203.T',         # 日本股票
    'INVALID',        # 无效代码
    'NONEXISTENT'     # 不存在的股票
]

for symbol in test_symbols:
    print(f"\n验证 {symbol}:")
    validation = fetcher.validate_symbol(symbol)
    
    if validation['is_valid']:
        print(f"  ✓ 有效股票: {validation['company_name']}")
        print(f"  市场: {validation['market']}")
        print(f"  行业: {validation['industry']}")
        if validation['current_price']:
            print(f"  当前价格: {validation['current_price']}")
    else:
        print(f"  ✗ 无效股票: {validation['error']}")
```

## Installation

### Using uv (recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -r requirements.txt
```

Required packages:
- pandas>=2.0.0
- numpy>=1.24.0
- requests>=2.28.0
- yfinance>=0.2.0  # Primary data source for global markets
- matplotlib>=3.7.0
- seaborn>=0.12.0

Optional packages:
- akshare>=1.12.0 (for alternative Chinese stock data)
- tushare>=1.2.89 (for professional Chinese stock data)

## Data Sources

### 1. Yahoo Finance (Primary)
- **Global coverage**: Supports stocks from US, China, Hong Kong, Japan, Europe, and more
- **Real-time data**: Live price data and historical data
- **Company information**: Detailed company profiles, financials, and analyst recommendations
- **No API key required**: Free access with rate limits

### 2. Symbol Format Support
- **US Markets**: Direct codes (AAPL, MSFT, TSLA)
- **China Shanghai**: 6-digit + .SS suffix (000001.SS, 600519.SS)
- **China Shenzhen**: 6-digit + .SZ suffix (000001.SZ, 002415.SZ)
- **Hong Kong**: 4-5 digit + .HK suffix (0700.HK, 0941.HK)
- **Japan**: 4-digit + .T suffix (7203.T, 9984.T)
- **Europe**: Company codes + country suffix (SAP.DE, MC.PA, HSBA.L)

### 3. Data Features
- **Historical prices**: Open, High, Low, Close, Volume
- **Technical indicators**: Built-in calculation functions
- **Company fundamentals**: Financial statements, ratios, and metrics
- **Analyst recommendations**: Buy/sell/hold ratings from multiple analysts
- **Market data**: Market cap, P/E ratio, dividend yield, etc.
- Free Chinese stock data API
- Requires `pip install akshare`
- Works with A-share codes (e.g., '000001', '600000')

### 3. Tushare
- Professional stock data API
- Requires API token
- More comprehensive data coverage
- Requires `pip install tushare`

## Signal Types

- **BUY**: Strong buy signal from multiple indicators
- **SELL**: Strong sell signal from multiple indicators  
- **HOLD**: Balanced signals, suggest holding position
- **WAIT**: Insufficient signals or conflicting signals

## Confidence Levels

Signals include confidence scores based on:
- Indicator reliability
- Signal consistency
- Market conditions
- Volume confirmation

## Output Format

Analysis results include:
- Current price and price changes
- Technical indicator values
- Trading signals with timestamps
- Confidence levels
- Buy/sell recommendations
- Summary statistics

## Error Handling

The skill handles various error conditions:
- Network connectivity issues
- Invalid stock codes
- Missing data dependencies
- API rate limits

## Customization

### Adding New Indicators

Extend the `TechnicalAnalyzer` class:

```python
class TechnicalAnalyzer:
    def calculate_custom_indicator(self, df: pd.DataFrame) -> pd.DataFrame:
        # Implement custom indicator logic
        return df
    
    def generate_custom_signals(self, df: pd.DataFrame) -> List[TradingSignal]:
        # Implement custom signal logic
        return []
```

### Custom Visualization

Create custom charts using matplotlib/seaborn:

```python
def create_custom_chart(df: pd.DataFrame, save_path: str = None):
    # Implement custom visualization
    pass
```

## Best Practices

1. **Data Quality**: Use reliable data sources for production
2. **Signal Confirmation**: Combine multiple indicators for better accuracy
3. **Risk Management**: Always consider stop-loss levels
4. **Market Context**: Consider overall market conditions
5. **Regular Updates**: Keep analysis current with fresh data

## Troubleshooting

### Common Issues

1. **Module not found**: Install required dependencies
2. **API limits**: Use mock data or add delays between requests
3. **Invalid dates**: Ensure date format is 'YYYY-MM-DD'
4. **Empty data**: Check stock code format and data source availability

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## References

- [AKShare Documentation](https://akshare.readthedocs.io/)
- [Tushare Documentation](https://tushare.pro/document/2)
- [Technical Analysis](https://www.investopedia.com/terms/t/technicalanalysis.asp)