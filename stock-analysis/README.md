# 全球股票分析技能

这是一个专注于全球股票分析的技能，使用Yahoo Finance作为唯一数据源，支持美股、中国A股、港股、日股、欧股等多个市场，提供技术分析、信号生成和买卖建议。

## 功能特性

- 🌍 **全球市场支持**: 美股、中国A股、港股、日股、欧股等多个市场
- 📊 **Yahoo Finance数据**: 使用真实的全球历史数据
- 📈 **技术指标**: MA、MACD、RSI、布林带、KDJ等
- 🔔 **交易信号**: 自动识别买入、卖出、持有信号
- 🎯 **智能建议**: 基于多指标的买卖建议和置信度
- 🔍 **股票验证**: 自动验证股票代码和交易所映射
- 📋 **分析师推荐**: 获取专业分析师评级和建议

## 快速开始

### 1. 安装依赖

```bash
# 使用uv（推荐）
uv sync

# 或使用pip
pip install yfinance pandas numpy matplotlib seaborn
```

### 2. 直接运行示例

```bash
# 运行示例分析
python example.py

# 运行全球股票分析器
python scripts/us_stock_analyzer.py
```

### 3. 代码中使用

```python
from scripts.us_stock_analyzer import GlobalStockAnalyzer
from scripts.us_stock_fetcher import GlobalStockDataFetcher

# 创建分析器
analyzer = GlobalStockAnalyzer()

# 分析美股
result = analyzer.analyze_global_stock('AAPL', days_back=180)
analyzer.print_global_stock_report(result)

# 分析中国股票
result = analyzer.analyze_global_stock('000001.SS', days_back=180)
analyzer.print_global_stock_report(result)

# 分析港股
result = analyzer.analyze_global_stock('0700.HK', days_back=90)
analyzer.print_global_stock_report(result)
```

## 支持的市场和股票代码

### 美国市场 (NYSE, NASDAQ)
- **格式**: 直接股票代码
- **示例**: AAPL, MSFT, GOOGL, TSLA, AMZN, NVDA
- **说明**: 无需后缀，直接使用股票代码

### 中国上海证券交易所 (SSE)
- **格式**: 6位数字 + .SS后缀
- **示例**: 000001.SS, 600000.SS, 600519.SS
- **说明**: .SS表示上海证券交易所

### 中国深圳证券交易所 (SZSE)
- **格式**: 6位数字 + .SZ后缀
- **示例**: 000001.SZ, 002415.SZ, 300750.SZ
- **说明**: .SZ表示深圳证券交易所

### 香港交易所 (HKEX)
- **格式**: 4-5位数字 + .HK后缀
- **示例**: 0700.HK, 0941.HK, 0998.HK
- **说明**: .HK表示香港交易所

### 日本东京证券交易所 (TSE)
- **格式**: 4位数字 + .T后缀
- **示例**: 7203.T, 9984.T, 6758.T
- **说明**: .T表示东京证券交易所

### 德国股市 (Xetra)
- **格式**: 公司代码 + .DE后缀
- **示例**: SAP.DE, BMW.DE, VOW3.DE
- **说明**: .DE表示德国股票交易所

### 法国股市 (Euronext Paris)
- **格式**: 公司代码 + .PA后缀
- **示例**: MC.PA, SAN.PA, OR.PA
- **说明**: .PA表示Euronext巴黎

### 英国股市 (LSE)
- **格式**: 公司代码 + .L后缀
- **示例**: HSBA.L, BARC.L, RIO.L
- **说明**: .L表示伦敦股票交易所

## 分析报告内容

### 基本信息
- 当前价格和涨跌幅
- 分析时间
- 数据范围（交易日数量）

### 信号汇总
- 买入信号数量
- 卖出信号数量
- 持有信号数量
- 总信号数

### 综合建议
- 买卖建议（买入/卖出/持有）
- 置信度水平
- 建议理由

### 最近交易信号
- 最近5个交易信号
- 信号类型和价格
- 触发指标和置信度
- 信号原因说明

## 技术指标说明

### 移动平均线 (MA)
- MA5: 5日移动平均线
- MA10: 10日移动平均线
- MA20: 20日移动平均线
- MA60: 60日移动平均线

### MACD指标
- MACD线：快慢EMA差值
- 信号线：MACD的EMA
- 金叉：买入信号
- 死叉：卖出信号

### RSI指标
- RSI14: 14日相对强弱指数
- 超买线：70以上
- 超卖线：30以下
- 回落反弹：买卖时机

### 布林带
- 上轨：中轨 + 2倍标准差
- 中轨：20日移动平均
- 下轨：中轨 - 2倍标准差
- 突破上下轨：交易信号

### KDJ指标
- K值：快速随机指标
- D值：慢速随机指标
- J值：K的3倍减去D的2倍
- 超买超卖：买卖时机

## 置信度计算

置信度基于最近10个交易信号的统计：
- 买入信号数量 vs 卖出信号数量
- 优势越明显，置信度越高
- 置信度范围：50%-100%

## 使用示例

### 示例1: 分析阿里巴巴(BABA)

```bash
cd stock-analysis\n# Analyze global stocks via Yahoo Finance\n# Analyze global stocks via Yahoo Finance\npython scripts/us_stock_analyzer.py BABA
```

输出示例：
```
正在分析美股 BABA...
数据范围: 2025-08-03 到 2026-01-30
获取到 124 条交易数据
使用Yahoo Finance真实数据

============================================================
美股分析报告 - BABA
============================================================
当前价格: 174.25
涨跌幅: +56.75 (+48.30%)
分析时间: 2026-01-30 11:06:58

信号汇总:
总信号数: 43
买入信号: 15
卖出信号: 28
持有信号: 0

综合建议: 卖出
置信度: 90.0%
建议理由: 卖出信号(9个)明显多于买入信号(1个)
```

### 示例2: 批量分析多只股票

```python
from scripts.us_stock_analyzer import USStockAnalyzer

analyzer = USStockAnalyzer()
symbols = ['BABA', 'AAPL', 'TSLA', 'MSFT', 'GOOGL']

for symbol in symbols:
    print(f"\n分析 {symbol}...")
    result = analyzer.analyze_us_stock(symbol, days_back=90)
    analyzer.print_us_stock_report(result)
    import time
    time.sleep(1)  # 避免请求过快
```

## 数据获取说明

### Yahoo Finance数据源
- **实时性**: 提供实时和历史数据
- **覆盖范围**: 全球主要交易所
- **数据质量**: 高质量的官方数据
- **限制**: 免费版有请求频率限制

### 数据范围
- 默认获取最近180天数据
- 可自定义开始和结束日期
- 数据包含OHLCV（开高低收成交量）

## 注意事项

1. **投资风险**: 技术分析仅供参考，不构成投资建议
2. **延迟性**: 历史数据可能有延迟，非实时交易数据
3. **市场变化**: 市场环境变化可能影响指标有效性
4. **数据限制**: Yahoo Finance有请求频率限制
5. **代码格式**: 确保使用正确的股票代码格式

## 故障排除

### 常见错误

1. **连接错误**
   ```bash
   # 检查网络连接
   ping finance.yahoo.com
   ```

2. **数据为空**
   ```bash
   # 验证股票代码
   python -c "from scripts.us_stock_fetcher import USStockDataFetcher; print(USStockDataFetcher().validate_symbol('BABA'))"
   ```

3. **编码问题**
   ```bash
   # 确保使用UTF-8编码
   chcp 65001  # Windows
   export LANG=zh_CN.UTF-8  # Linux/Mac
   ```

### 性能优化

- 批量分析时添加延迟（建议1-2秒）
- 避免过短的分析周期（建议至少30天）
- 合理设置数据范围

## 开发说明

### 代码结构
```
stock-analysis/
├── scripts/
│   ├── us_stock_analyzer.py     # 主分析器
│   ├── us_stock_fetcher.py      # 数据获取器
│   ├── technical_analysis.py    # 技术分析
│   └── visualization.py         # 可视化
├── pyproject.toml              # 项目配置
└── README.md                   # 说明文档
```

### 扩展功能

可以轻松添加新的技术指标：
```python
# 在technical_analysis.py中添加新指标
def calculate_new_indicator(self, df: pd.DataFrame) -> pd.DataFrame:
    # 实现新指标计算逻辑
    df['NEW_INDICATOR'] = df['close'].rolling(10).mean()
    return df
```

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 免责声明

本工具仅供学习和研究使用，不构成投资建议。投资有风险，请谨慎决策。