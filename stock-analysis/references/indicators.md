# Technical Indicators Reference

## Calculation Methods

### Moving Averages (MA)
```python
def calculate_ma(df, period=20):
    return df['Close'].rolling(window=period).mean()
```

### Exponential Moving Averages (EMA)
```python
def calculate_ema(df, period=12):
    return df['Close'].ewm(span=period, adjust=False).mean()
```

### MACD (Moving Average Convergence Divergence)
```python
# Standard (12,26,9) MACD
def calculate_macd(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram
```

### RSI (Relative Strength Index)
```python
# 14-period RSI calculation
def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
```

### Bollinger Bands
```python
def calculate_bollinger(df, period=20, num_std=2):
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    return upper, lower, sma
```

### KDJ
```python
def calculate_kdj(df, period=9):
    low_min = df['Low'].rolling(window=period).min()
    high_max = df['High'].rolling(window=period).max()
    rsv = (df['Close'] - low_min) / (high_max - low_min) * 100
    k = rsv.ewm(span=3, adjust=False).mean()
    d = k.ewm(span=3, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j
```

### Volume Indicators
```python
def calculate_volume_ma(df, period=20):
    return df['Volume'].rolling(window=period).mean()
```

## Signal Generation

| Indicator | Bullish Signal | Bearish Signal | Neutral Zone |
|-----------|----------------|----------------|--------------|
| MA Golden/Death Cross | MA5 > MA20 | MA5 < MA20 | MA5 = MA20 |
| MACD Crossover | MACD > Signal | MACD < Signal | Histogram near 0 |
| RSI Overbought/Oversold | RSI < 30 | RSI > 70 | 30-70 |
| Bollinger Band Bounce | Price touches lower band | Price touches upper band | Price between bands |
| KDJ Extreme | K > 80, D > 80 | K < 20, D < 20 | 20-80 |

## Implementation Notes
1. Always use 14-period for RSI unless specified
2. MACD histogram width indicates momentum strength
3. Combine indicators for confirmation (e.g., RSI + MACD)
4. Volume confirmation increases signal reliability

## Common Errors
- ❌ Using different periods across indicators
- ❌ Ignoring market context (bull/bear market)
- ❌ Over-relying on single indicator signals

## Implementation Notes
1. Always use 14-period for RSI unless specified
2. MACD histogram width indicates momentum strength
3. Combine indicators for confirmation (e.g., RSI + MACD)
4. Volume confirmation increases signal reliability

## Common Errors
- ❌ Using different periods across indicators
- ❌ Ignoring market context (bull/bear market)
- ❌ Over-relying on single indicator signals