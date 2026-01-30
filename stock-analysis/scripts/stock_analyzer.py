#!/usr/bin/env python3
"""
全球股票分析脚本
使用Yahoo Finance获取全球股票数据并进行分析
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach(), errors="replace")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach(), errors="replace")

# 添加scripts目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.stock_fetcher import GlobalStockDataFetcher
from scripts.technical_analysis import TechnicalAnalyzer, TradingSignal, SignalType

class GlobalStockAnalyzer:
    """全球股票分析器 - 使用Yahoo Finance获取全球股票数据"""
    
    def __init__(self):
        self.fetcher = GlobalStockDataFetcher()
        self.analyzer = TechnicalAnalyzer()
    
    def analyze_global_stock(self, symbol: str, 
                           start_date: Optional[str] = None, 
                           end_date: Optional[str] = None,
                           days_back: int = 365) -> Dict:
        """
        分析全球股票
        
        Args:
            symbol: 股票代码 (如 'BABA', 'AAPL', 'TSLA', '000001.SS', '000002.SZ', 'AAPL')
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            days_back: 如果没有指定日期，获取最近多少天的数据
        
        Returns:
            分析结果字典
        """
        # 设置默认日期
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        if not start_date:
            start_dt = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days_back)
            start_date = start_dt.strftime('%Y-%m-%d')
        
        print(f"正在分析全球股票 {symbol}...")
        print(f"数据范围: {start_date} 到 {end_date}")
        print("使用Yahoo Finance全球数据")
        
        # 获取股票数据
        df = self.fetcher.get_stock_data(symbol, start_date, end_date)
        
        if df.empty:
            return {
                'success': False,
                'error': '无法获取股票数据',
                'stock_code': symbol,
                'data': None,
                'signals': [],
                'summary': None
            }
        
        print("使用Yahoo Finance真实数据")
        
        # 技术分析
        analysis_result = self.analyzer.analyze_stock(df)
        
        # 生成综合建议
        recommendation = self.generate_recommendation(analysis_result)
        
        result = {
            'success': True,
            'stock_code': symbol,
            'data_range': {
                'start_date': start_date,
                'end_date': end_date,
                'trading_days': len(df)
            },
            'current_price': df['close'].iloc[-1],
            'price_change': df['close'].iloc[-1] - df['close'].iloc[0],
            'price_change_pct': ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100,
            'analysis': analysis_result,
            'recommendation': recommendation,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return result
    
    def generate_recommendation(self, analysis_result: Dict) -> Dict:
        """
        基于分析结果生成综合建议
        """
        signals = analysis_result['latest_signals']
        summary = analysis_result['summary']
        
        # 统计最近的信号
        recent_signals = signals[-10:]  # 最近10个信号
        buy_count = sum(1 for signal in recent_signals if signal.signal_type == SignalType.BUY)
        sell_count = sum(1 for signal in recent_signals if signal.signal_type == SignalType.SELL)
        
        # 计算置信度
        if buy_count + sell_count > 0:
            confidence = max(buy_count, sell_count) / (buy_count + sell_count)
        else:
            confidence = 0.5
        
        # 生成建议
        if buy_count > sell_count * 1.5:
            action = 'BUY'
            reason = f"买入信号({buy_count}个)明显多于卖出信号({sell_count}个)"
        elif sell_count > buy_count * 1.5:
            action = 'SELL'
            reason = f"卖出信号({sell_count}个)明显多于买入信号({buy_count}个)"
        else:
            action = 'HOLD'
            reason = "买卖信号相对平衡，建议观望"
        
        return {
            'action': action,
            'confidence': confidence,
            'reason': reason,
            'buy_signals': buy_count,
            'sell_signals': sell_count,
            'total_signals': len(recent_signals)
        }
    
    def print_global_stock_report(self, result: Dict):
        """
        打印全球股票分析报告
        """
        if not result['success']:
            print(f"分析失败: {result['error']}")
            return
        
        print("\n" + "="*60)
        print(f"全球股票分析报告 - {result['stock_code']}")
        print("="*60)
        print("数据来源: Yahoo Finance")
        
        # 基本信息
        print(f"当前价格: {result['current_price']:.2f}")
        print(f"涨跌幅: {result['price_change']:+.2f} ({result['price_change_pct']:+.2f}%)")
        print(f"分析时间: {result['generated_at']}")
        
        # 交易信号汇总
        analysis = result['analysis']
        summary = analysis['summary']
        
        print(f"\n信号汇总:")
        print(f"总信号数: {summary['total_signals']}")
        print(f"买入信号: {summary['buy_signals']}")
        print(f"卖出信号: {summary['sell_signals']}")
        print(f"持有信号: {summary['hold_signals']}")
        
        # 综合建议
        recommendation = result['recommendation']
        action_map = {
            'BUY': '买入',
            'SELL': '卖出',
            'HOLD': '持有',
            'WAIT': '观望'
        }
        
        print(f"\n综合建议: {action_map.get(recommendation['action'], recommendation['action'])}")
        print(f"置信度: {recommendation['confidence']:.1%}")
        print(f"建议理由: {recommendation['reason']}")
        
        # 最近信号
        print(f"\n最近交易信号:")
        for i, signal in enumerate(analysis['latest_signals'][:5], 1):
            action_map = {
                'BUY': '买入',
                'SELL': '卖出',
                'HOLD': '持有',
                'WAIT': '观望'
            }
            print(f"{i}. {signal.date.strftime('%Y-%m-%d')} - "
                  f"{action_map.get(signal.signal_type.value, signal.signal_type.value)} "
                  f"{signal.price:.2f} "
                  f"({signal.indicator_name}: {signal.confidence:.1%})")
            print(f"   原因: {signal.reason}")
        
        print("\n" + "="*60)

def main():
    """分析全球股票示例"""
    analyzer = GlobalStockAnalyzer()
    
    # 分析美股
    print("分析美国股票...")
    us_stocks = ['BABA', 'AAPL', 'TSLA', 'MSFT', 'NVDA']
    for symbol in us_stocks:
        print(f"\n分析 {symbol}...")
        result = analyzer.analyze_global_stock(symbol, days_back=180)
        analyzer.print_global_stock_report(result)
        
        # 间隔1秒避免API限制
        import time
        time.sleep(1)
    
    # 分析中国A股（通过Yahoo Finance）
    print("\n" + "="*60)
    print("分析中国A股...")
    china_stocks = ['000001.SS', '000002.SS', '000858.SS', '000895.SS']  # 上海证券交易所
    shenzhen_stocks = ['000001.SZ', '000002.SZ', '000858.SZ', '000895.SZ']  # 深圳证券交易所
    
    all_china_stocks = china_stocks + shenzhen_stocks
    
    for symbol in all_china_stocks[:3]:  # 只分析前3个避免过多请求
        print(f"\n分析 {symbol}...")
        result = analyzer.analyze_global_stock(symbol, days_back=90)
        analyzer.print_global_stock_report(result)
        
        # 间隔2秒避免API限制
        import time
        time.sleep(2)
    
    # 分析其他市场股票
    print("\n" + "="*60)
    print("分析其他市场股票...")
    other_stocks = [
        '700.HK',    # 香港交易所 - 腾讯控股
        '0700.HK',   # 香港交易所 - 腾讯控股（另一种格式）
        '9988.HK',   # 香港交易所 - 阿里巴巴
        'BABA',      # 美股 - 阿里巴巴
        'TSM',       # 美股 - 台积电
        'SIE.DE',    # 德国 - 西门子
        'SAP.DE'     # 德国 - SAP
    ]
    
    for symbol in other_stocks[:3]:  # 只分析前3个避免过多请求
        print(f"\n分析 {symbol}...")
        result = analyzer.analyze_global_stock(symbol, days_back=90)
        analyzer.print_global_stock_report(result)
        
        # 间隔2秒避免API限制
        import time
        time.sleep(2)

if __name__ == "__main__":
    main()