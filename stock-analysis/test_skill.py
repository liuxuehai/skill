#!/usr/bin/env python3
"""
测试股票分析技能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.stock_analyzer import StockAnalyzer

def test_skill():
    """测试技能功能"""
    print("正在测试股票分析技能...")
    
    # 创建分析器
    analyzer = StockAnalyzer()
    
    # 测试模拟数据
    print("\n1. 测试模拟数据...")
    result = analyzer.analyze_stock('000001', days_back=90)
    
    if result['success']:
        print("模拟数据获取成功")
        print(f"数据条数: {result['data_range']['trading_days']}")
        print(f"当前价格: {result['current_price']:.2f}")
        print(f"涨跌幅: {result['price_change_pct']:+.2f}%")
    else:
        print("模拟数据获取失败")
        return False
    
    # 测试AKShare（如果可用）
    print("\n2. 测试AKShare数据...")
    try:
        result_ak = analyzer.analyze_stock('000001', days_back=30, data_source='akshare')
        if result_ak['success']:
            print("AKShare数据获取成功")
        else:
            print("AKShare数据获取失败（可能需要安装或网络问题）")
    except Exception as e:
        print(f"AKShare测试失败: {e}")
    
    # 打印示例报告
    print("\n3. 示例分析报告:")
    print("-" * 50)
    try:
        analyzer.print_analysis_report(result)
    except UnicodeEncodeError:
        print("编码错误，跳过详细报告打印")
        print(f"分析结果: {result['success']}")
        print(f"股票代码: {result['stock_code']}")
        print(f"当前价格: {result['current_price']:.2f}")
        print(f"建议操作: {result['recommendation']['action']}")
    
    print("\n技能测试完成!")
    return True

if __name__ == "__main__":
    test_skill()