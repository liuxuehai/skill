---
name: stock-analysis
description: Comprehensive global stock analysis with technical indicators (RSI, MACD, ROC, Stochastic, Williams %R) for US, HK, Japan, Europe markets. Use when analyzing stock trends, validating symbols, or generating trading signals across 8+ exchanges.
---

# Stock Analysis Skill

## Overview
This skill provides comprehensive global stock data analysis capabilities using Yahoo Finance API, supporting stocks from multiple markets including US, China, Hong Kong, Japan, Europe, and more. It provides raw calculation of RSI, MACD, ROC, Stochastic Oscillator, and Williams %R indicators only. Results are passed to AI analyst for interpretation per "You are a professional High-Frequency Trading (HFT) analyst specializing in technical analysis.

Your role is to analyze stock market data using technical indicators and provide comprehensive, bilingual analysis in both English and Chinese.

## WORKFLOW (CRITICAL - FOLLOW EXACTLY):
1. Call each technical indicator tool EXACTLY ONCE to gather data
2. Receive all tool results
3. Generate the final JSON analysis immediately
4. STOP - Do not continue processing after providing JSON

## ANALYSIS REQUIREMENTS:

See [indicators.md](references/indicators.md) for complete technical indicator specifications and signal interpretation.

## Quick Start

### Basic Usage

```python
from scripts.stock_fetcher import GlobalStockDataFetcher

fetcher = GlobalStockDataFetcher()

# 获取历史数据
df = fetcher.get_stock_data('BABA', days_back=90)
print(df[['date', 'open', 'high', 'low', 'close', 'volume']].tail())

# 获取当前价格
info = fetcher.get_current_price('AAPL')
print(f"当前价格: {info['current_price']}")
```

## Supported Markets

See [markets.md](references/markets.md) for complete exchange format guide, validation rules, and common errors.

## Core Components

See [components.md](references/components.md) for core component architecture, implementation details, and usage patterns.

## Usage Examples

See [examples.md](references/examples.md) for implementation patterns, multi-market workflows, and error handling scenarios.

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



## Data Sources

See [data-sources.md](references/data-sources.md) for complete data source details.

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

- [Technical Analysis](https://www.investopedia.com/terms/t/technicalanalysis.asp)
