#!/usr/bin/env python3
"""
股票分析技能使用示例
"""

import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.stock_analyzer import GlobalStockAnalyzer


def main():
    """主函数"""
    print("=== 股票分析技能使用示例 ===")

    # 创建分析器
    analyzer = GlobalStockAnalyzer()

    # 示例股票列表
    stock_examples = ["BABA"]

    for stock_code in stock_examples:
        print(f"\n{'=' * 60}")
        print(f"分析股票: {stock_code}")
        print(f"{'=' * 60}")

        try:
            # 分析股票（使用真实数据）
            result = analyzer.analyze_global_stock(stock_code, days_back=180)

            if result["success"]:
                # 打印基本信息
                print(f"当前价格: {result['current_price']:.2f}")
                print(
                    f"涨跌幅: {result['price_change']:+.2f} ({result['price_change_pct']:+.2f}%)"
                )
                print(f"数据条数: {result['data_range']['trading_days']}")

                # 打印分析摘要
                analysis = result["analysis"]
                summary = analysis["summary"]
                print(f"\n信号汇总:")
                print(f"总信号数: {summary['total_signals']}")
                print(f"买入信号: {summary['buy_signals']}")
                print(f"卖出信号: {summary['sell_signals']}")
                print(f"持有信号: {summary['hold_signals']}")

                # 打印综合建议
                recommendation = result["recommendation"]
                action_map = {
                    "BUY": "买入",
                    "SELL": "卖出",
                    "HOLD": "持有",
                    "WAIT": "观望",
                }
                print(
                    f"\n综合建议: {action_map.get(recommendation['action'], recommendation['action'])}"
                )
                print(f"置信度: {recommendation['confidence']:.1%}")
                print(f"建议理由: {recommendation['reason']}")

                # 打印最近的信号
                print(f"\n最近交易信号:")
                for i, signal in enumerate(analysis["latest_signals"][:3], 1):
                    action_map = {
                        "BUY": "买入",
                        "SELL": "卖出",
                        "HOLD": "持有",
                        "WAIT": "观望",
                    }
                    print(
                        f"{i}. {signal.date.strftime('%Y-%m-%d')} - "
                        f"{action_map.get(signal.signal_type.value, signal.signal_type.value)} "
                        f"{signal.price:.2f} "
                        f"({signal.indicator_name}: {signal.confidence:.1%})"
                    )

            else:
                print(f"分析失败: {result['error']}")

        except Exception as e:
            print(f"分析过程中出现错误: {e}")

        # 避免请求过快
        import time

        time.sleep(1)

    print(f"\n{'=' * 60}")
    print("分析完成!")
    print("注意: 以上分析基于技术指标，仅供参考，不构成投资建议")
    print("实际投资请结合基本面分析和风险评估")
    print("{'='*60}")


if __name__ == "__main__":
    main()
