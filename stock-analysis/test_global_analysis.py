#!/usr/bin/env python3
"""
全球股票分析测试脚本
测试Yahoo Finance全球股票数据获取功能
"""

import sys
import os
from datetime import datetime, timedelta

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.stock_fetcher import GlobalStockDataFetcher
from scripts.stock_analyzer import GlobalStockAnalyzer


def test_global_stock_fetcher():
    """测试全球股票数据获取器"""
    print("=" * 60)
    print("测试全球股票数据获取器")
    print("=" * 60)
    
    fetcher = GlobalStockDataFetcher()
    
    # 测试股票代码列表
    test_symbols = [
        ('美股', 'AAPL'),
        ('中国上海', '000001.SS'),
        ('中国深圳', '000001.SZ'),
        ('香港', '0700.HK'),
        ('日本', '7203.T'),
        ('德国', 'SAP.DE'),
        ('法国', 'MC.PA'),
        ('英国', 'HSBA.L'),
    ]
    
    print("获取支持的交易所信息:")
    exchanges = fetcher.get_supported_exchanges()
    for market, info in exchanges.items():
        print(f"  {market}: {info['description']}")
        print(f"    示例: {', '.join(info['examples'][:2])}")
    
    print("\n" + "-" * 60)
    print("测试股票代码验证:")
    print("-" * 60)
    
    for market, symbol in test_symbols:
        print(f"\n验证 {market} 股票 {symbol}:")
        validation = fetcher.validate_symbol(symbol, check_trading_data=False)
        
        if validation['is_valid']:
            print(f"  ✓ 有效股票: {validation['company_name']}")
            print(f"    市场: {validation['market']}")
            print(f"    行业: {validation['industry']}")
            print(f"    货币: {validation['currency']}")
            if validation['current_price']:
                print(f"    当前价格: {validation['current_price']:.2f}")
        else:
            print(f"  ✗ 无效股票: {validation['error']}")
    
    print("\n" + "-" * 60)
    print("测试数据获取:")
    print("-" * 60)
    
    # 测试部分股票的数据获取
    test_data_symbols = ['AAPL', '000001.SS', '0700.HK']
    
    for symbol in test_data_symbols:
        print(f"\n获取 {symbol} 的历史数据:")
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            df = fetcher.get_stock_data(symbol, start_date, end_date)
            
            if not df.empty:
                print(f"  ✓ 成功获取到 {len(df)} 条交易数据")
                print(f"    数据日期范围: {df['date'].min().strftime('%Y-%m-%d')} 到 {df['date'].max().strftime('%Y-%m-%d')}")
                print(f"    最新价格: {df['close'].iloc[-1]:.2f}")
                print(f"    涨跌幅: {((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0] * 100):+.2f}%")
            else:
                print(f"  ✗ 未获取到数据")
                
        except Exception as e:
            print(f"  ✗ 获取数据失败: {e}")
        
        # 添加延迟避免请求过快
        import time
        time.sleep(2)
    
    print("\n" + "-" * 60)
    print("测试股票推荐信息:")
    print("-" * 60)
    
    for symbol in test_data_symbols[:2]:  # 只测试前两个避免过多请求
        print(f"\n获取 {symbol} 的分析师推荐:")
        recommendations = fetcher.get_stock_recommendations(symbol)
        
        if recommendations['has_recommendations']:
            print(f"  ✓ 有分析师推荐")
            print(f"    日期: {recommendations['date']}")
            print(f"    分析师数量: {recommendations['total_analysts']}")
            print(f"    买入: {recommendations['buy_count']} ({recommendations['buy_percent']:.1f}%)")
            print(f"    持有: {recommendations['hold_count']} ({recommendations['hold_percent']:.1f}%)")
            print(f"    卖出: {recommendations['sell_count']} ({recommendations['sell_percent']:.1f}%)")
            print(f"    平均评分: {recommendations['average_rating']}/5")
        else:
            print(f"  ✗ 无分析师推荐: {recommendations.get('error', 'No data available')}")
        
        # 添加延迟
        time.sleep(2)


def test_global_stock_analyzer():
    """测试全球股票分析器"""
    print("\n" + "=" * 60)
    print("测试全球股票分析器")
    print("=" * 60)
    
    analyzer = GlobalStockAnalyzer()
    
    # 测试不同市场的股票
    test_stocks = [
        ('美股', 'AAPL'),
        ('中国上海', '600519.SS'),  # 贵州茅台
        ('中国深圳', '000001.SZ'),  # 平安银行
        ('香港', '0700.HK'),        # 腾讯
    ]
    
    for market, symbol in test_stocks:
        print(f"\n{'=' * 60}")
        print(f"分析 {market} 股票 {symbol}")
        print(f"{'=' * 60}")
        
        try:
            # 分析股票
            result = analyzer.analyze_global_stock(symbol, days_back=90)
            
            if result['success']:
                print(f"✓ 分析成功")
                print(f"  当前价格: {result['current_price']:.2f}")
                print(f"  涨跌幅: {result['price_change']:+.2f} ({result['price_change_pct']:+.2f}%)")
                print(f"  交易日数: {result['data_range']['trading_days']}")
                
                # 信号汇总
                analysis = result['analysis']
                summary = analysis['summary']
                print(f"\n信号汇总:")
                print(f"  总信号数: {summary['total_signals']}")
                print(f"  买入信号: {summary['buy_signals']}")
                print(f"  卖出信号: {summary['sell_signals']}")
                print(f"  持有信号: {summary['hold_signals']}")
                
                # 综合建议
                recommendation = result['recommendation']
                action_map = {
                    'BUY': '买入',
                    'SELL': '卖出',
                    'HOLD': '持有',
                    'WAIT': '观望'
                }
                print(f"\n综合建议:")
                print(f"  操作: {action_map.get(recommendation['action'], recommendation['action'])}")
                print(f"  置信度: {recommendation['confidence']:.1%}")
                print(f"  原因: {recommendation['reason']}")
                
            else:
                print(f"✗ 分析失败: {result['error']}")
                
        except Exception as e:
            print(f"✗ 分析过程中出现错误: {e}")
        
        # 添加延迟避免请求过快
        import time
        time.sleep(3)


def main():
    """主测试函数"""
    print("全球股票分析技能测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 测试数据获取器
        test_global_stock_fetcher()
        
        # 测试股票分析器
        test_global_stock_analyzer()
        
        print("\n" + "=" * 60)
        print("测试完成!")
        print("注意: 以上分析基于技术指标，仅供参考，不构成投资建议")
        print("实际投资请结合基本面分析和风险评估")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()