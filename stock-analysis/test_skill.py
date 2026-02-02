#!/usr/bin/env python3
"""
测试股票分析技能
"""

import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.stock_analyzer import GlobalStockAnalyzer


def test_skill():
    """测试技能功能"""
    print("正在测试股票分析技能...")

    # 创建分析器
    analyzer = GlobalStockAnalyzer()

    # 测试美股数据
    print("\n1. 测试美股数据 (AAPL)...")
    result = analyzer.analyze_global_stock("AAPL", days_back=90)

    if result["success"]:
        print("美股数据获取成功")
        print(f"数据条数: {result['data_range']['trading_days']}")
        print(f"当前价格: {result['current_price']:.2f}")
        print(f"涨跌幅: {result['price_change_pct']:+.2f}%")
    else:
        print("美股数据获取失败")
        return False

    # 测试中国A股数据
    print("\n2. 测试中国A股数据 (000001.SS)...")
    try:
        result_cn = analyzer.analyze_global_stock("000001.SS", days_back=30)
        if result_cn["success"]:
            print("中国A股数据获取成功")
            print(f"当前价格: {result_cn['current_price']:.2f}")
        else:
            print("中国A股数据获取失败")
    except Exception as e:
        print(f"中国A股测试失败: {e}")

    # 打印示例报告
    print("\n3. 示例分析报告:")
    print("-" * 50)
    try:
        analyzer.print_global_stock_report(result)
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
