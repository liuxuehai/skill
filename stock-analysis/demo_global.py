#!/usr/bin/env python3
"""
全球股票分析使用示例
演示如何使用增强后的全球股票分析功能
"""

import sys
import os
from datetime import datetime, timedelta

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.stock_analyzer import GlobalStockAnalyzer
from scripts.stock_fetcher import GlobalStockDataFetcher


def demo_global_analysis():
    """演示全球股票分析功能"""
    print("🌍 全球股票分析技能演示")
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 创建分析器
    analyzer = GlobalStockAnalyzer()
    fetcher = GlobalStockDataFetcher()
    
    # 1. 显示支持的市场
    print("\n📊 支持的市场和交易所:")
    print("-" * 50)
    exchanges = fetcher.get_supported_exchanges()
    for market, info in exchanges.items():
        print(f"  {market}: {info['description']}")
        print(f"    示例: {', '.join(info['examples'][:3])}")
    
    # 2. 分析不同市场的股票
    demo_stocks = [
        ('🇺🇸 美国', 'AAPL', '苹果公司'),
        ('🇨🇳 中国上海', '600519.SS', '贵州茅台'),
        ('🇨🇳 中国深圳', '000001.SZ', '平安银行'),
        ('🇭🇰 香港', '0700.HK', '腾讯控股'),
        ('🇯🇵 日本', '7203.T', '丰田汽车'),
        ('🇩🇪 德国', 'SAP.DE', 'SAP公司'),
    ]
    
    print("\n📈 全球股票分析结果:")
    print("-" * 70)
    
    for i, (region, symbol, company) in enumerate(demo_stocks, 1):
        print(f"\n{i}. {region} - {company} ({symbol})")
        print("-" * 50)
        
        try:
            # 分析股票
            result = analyzer.analyze_global_stock(symbol, days_back=60)
            
            if result['success']:
                # 基本信息
                current_price = result['current_price']
                price_change_pct = result['price_change_pct']
                trading_days = result['data_range']['trading_days']
                
                print(f"  ✓ 分析成功")
                print(f"    当前价格: ${current_price:.2f}")
                print(f"    涨跌幅: {price_change_pct:+.2f}%")
                print(f"    交易日数: {trading_days}")
                
                # 技术分析结果
                analysis = result['analysis']
                summary = analysis['summary']
                
                print(f"\n    📊 技术信号:")
                print(f"      总信号数: {summary['total_signals']}")
                print(f"      买入信号: {summary['buy_signals']}")
                print(f"      卖出信号: {summary['sell_signals']}")
                print(f"      持有信号: {summary['hold_signals']}")
                
                # 综合建议
                recommendation = result['recommendation']
                action_map = {
                    'BUY': '🟢 买入',
                    'SELL': '🔴 卖出',
                    'HOLD': '🟡 持有',
                    'WAIT': '⚪ 观望'
                }
                
                print(f"\n    💡 综合建议:")
                print(f"      操作: {action_map.get(recommendation['action'], recommendation['action'])}")
                print(f"      置信度: {recommendation['confidence']:.1%}")
                print(f"      原因: {recommendation['reason']}")
                
            else:
                print(f"  ✗ 分析失败: {result['error']}")
                
        except Exception as e:
            print(f"  ✗ 分析过程中出现错误: {e}")
        
        # 添加延迟避免请求过快
        import time
        time.sleep(2)
    
    # 3. 获取股票推荐信息
    print("\n🏢 分析师推荐信息:")
    print("-" * 50)
    
    for symbol in ['AAPL', '0700.HK']:
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
            print(f"  ✗ 无分析师推荐")
        
        # 添加延迟
        time.sleep(2)
    
    # 4. 总结
    print("\n" + "=" * 70)
    print("🎯 总结")
    print("=" * 70)
    print("✅ 成功演示了全球股票分析功能")
    print("✅ 支持多个市场的股票分析")
    print("✅ 提供技术分析和综合建议")
    print("✅ 包含分析师推荐信息")
    print("\n📝 注意事项:")
    print("• 分析结果仅供参考，不构成投资建议")
    print("• 技术指标存在滞后性，请结合基本面分析")
    print("• 投资有风险，请谨慎决策")
    print("• 建议使用多个时间周期进行分析")
    print("=" * 70)


def demo_symbol_validation():
    """演示股票代码验证功能"""
    print("\n🔍 股票代码验证演示")
    print("-" * 50)
    
    fetcher = GlobalStockDataFetcher()
    
    # 测试各种格式的股票代码
    test_symbols = [
        'AAPL',           # 美国股票
        '000001.SS',      # 中国上海股票
        '000001.SZ',      # 中国深圳股票
        '0700.HK',        # 香港股票
        '7203.T',         # 日本股票
        'SAP.DE',         # 德国股票
        'MC.PA',          # 法国股票
        'HSBA.L',         # 英国股票
        'INVALID',        # 无效代码
    ]
    
    for symbol in test_symbols:
        print(f"\n验证 {symbol}:")
        validation = fetcher.validate_symbol(symbol, check_trading_data=True)
        
        if validation['is_valid']:
            print(f"  ✓ 有效股票: {validation['company_name']}")
            print(f"    市场: {validation['market']}")
            print(f"    行业: {validation['industry']}")
            print(f"    货币: {validation['currency']}")
            if validation['current_price']:
                print(f"    当前价格: {validation['current_price']:.2f}")
            if validation.get('has_trading_data'):
                print(f"    有交易数据: {validation.get('trading_days', 0)} 天")
        else:
            print(f"  ✗ 无效股票: {validation['error']}")
        
        # 短暂延迟
        import time
        time.sleep(1)


def main():
    """主函数"""
    try:
        demo_global_analysis()
        demo_symbol_validation()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断演示")
    except Exception as e:
        print(f"\n\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()