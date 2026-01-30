#!/usr/bin/env python3
"""
Stock Visualization Script
股票数据可视化脚本
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
import sys
import os

# 添加scripts目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class StockVisualizer:
    """股票可视化器"""
    
    def __init__(self):
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置风格
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8')
    
    def plot_price_chart(self, df: pd.DataFrame, stock_code: str, save_path: str = None):
        """
        绘制价格走势图
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle(f'{stock_code} 股票价格走势', fontsize=16, fontweight='bold')
        
        # 确保使用正确的列名
        date_col = 'trade_date' if 'trade_date' in df.columns else 'date'
        
        # 价格走势图
        ax1.plot(df[date_col], df['close'], label='收盘价', color='blue', linewidth=2)
        ax1.plot(df[date_col], df['open'], label='开盘价', color='orange', alpha=0.7)
        ax1.fill_between(df[date_col], df['low'], df['high'], alpha=0.3, color='gray', label='价格区间')
        
        # 添加移动平均线
        if 'MA5' in df.columns:
            ax1.plot(df[date_col], df['MA5'], label='MA5', color='red', alpha=0.8)
        if 'MA20' in df.columns:
            ax1.plot(df[date_col], df['MA20'], label='MA20', color='green', alpha=0.8)
        
        ax1.set_title('价格走势')
        ax1.set_xlabel('日期')
        ax1.set_ylabel('价格 (¥)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 成交量图
        vol_col = 'vol' if 'vol' in df.columns else 'volume'
        ax2.bar(df[date_col], df[vol_col], alpha=0.7, color='purple')
        ax2.set_title('成交量')
        ax2.set_xlabel('日期')
        ax2.set_ylabel('成交量')
        ax2.grid(True, alpha=0.3)
        
        # 格式化日期
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"图表已保存到: {save_path}")
        
        plt.show()
    
    def plot_technical_indicators(self, df: pd.DataFrame, stock_code: str, save_path: str = None):
        """
        绘制技术指标图
        """
        fig, axes = plt.subplots(3, 1, figsize=(12, 15))
        fig.suptitle(f'{stock_code} 技术指标分析', fontsize=16, fontweight='bold')
        
        # 确保使用正确的列名
        date_col = 'trade_date' if 'trade_date' in df.columns else 'date'
        
        # MACD
        ax1 = axes[0]
        if 'MACD' in df.columns and 'MACD_signal' in df.columns:
            ax1.plot(df[date_col], df['MACD'], label='MACD', color='blue', linewidth=1.5)
            ax1.plot(df[date_col], df['MACD_signal'], label='Signal', color='red', linewidth=1.5)
            ax1.bar(df[date_col], df['MACD_histogram'], label='Histogram', alpha=0.3, color='gray')
            ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            ax1.set_title('MACD指标')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # RSI
        ax2 = axes[1]
        if 'RSI14' in df.columns:
            ax2.plot(df[date_col], df['RSI14'], label='RSI', color='purple', linewidth=2)
            ax2.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='超买线')
            ax2.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='超卖线')
            ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='中线')
            ax2.set_title('RSI指标')
            ax2.set_ylabel('RSI值')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim(0, 100)
        
        # KDJ
        ax3 = axes[2]
        if 'K' in df.columns and 'D' in df.columns and 'J' in df.columns:
            ax3.plot(df[date_col], df['K'], label='K线', color='blue', linewidth=1.5)
            ax3.plot(df[date_col], df['D'], label='D线', color='red', linewidth=1.5)
            ax3.plot(df[date_col], df['J'], label='J线', color='green', linewidth=1.5)
            ax3.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='超买线')
            ax3.axhline(y=20, color='green', linestyle='--', alpha=0.7, label='超卖线')
            ax3.set_title('KDJ指标')
            ax3.set_ylabel('KDJ值')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            ax3.set_ylim(0, 100)
        
        # 格式化日期
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"技术指标图已保存到: {save_path}")
        
        plt.show()
    
    def plot_bollinger_bands(self, df: pd.DataFrame, stock_code: str, save_path: str = None):
        """
        绘制布林带图
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle(f'{stock_code} 布林带分析', fontsize=16, fontweight='bold')
        
        # 确保使用正确的列名
        date_col = 'trade_date' if 'trade_date' in df.columns else 'date'
        
        if 'BB_upper' in df.columns and 'BB_lower' in df.columns and 'BB_middle' in df.columns:
            # 价格线
            ax.plot(df[date_col], df['close'], label='收盘价', color='blue', linewidth=2)
            
            # 布林带
            ax.plot(df[date_col], df['BB_upper'], label='上轨', color='red', alpha=0.8)
            ax.plot(df[date_col], df['BB_middle'], label='中轨', color='gray', alpha=0.8)
            ax.plot(df[date_col], df['BB_lower'], label='下轨', color='green', alpha=0.8)
            
            # 填充区域
            ax.fill_between(df[date_col], df['BB_upper'], df['BB_lower'], 
                          alpha=0.2, color='gray', label='布林带区域')
            
            ax.set_title('布林带')
            ax.set_xlabel('日期')
            ax.set_ylabel('价格 (¥)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # 格式化日期
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"布林带图已保存到: {save_path}")
            
            plt.show()
    
    def plot_candlestick_chart(self, df: pd.DataFrame, stock_code: str, save_path: str = None):
        """
        绘制K线图
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.suptitle(f'{stock_code} K线图', fontsize=16, fontweight='bold')
        
        # 确保使用正确的列名
        date_col = 'trade_date' if 'trade_date' in df.columns else 'date'
        
        # 准备K线数据
        df_plot = df.copy()
        df_plot['date_num'] = mdates.date2num(df_plot[date_col])
        
        # 绘制K线
        width = 0.6
        width2 = 0.1
        
        for i, (date_num, row) in enumerate(zip(df_plot['date_num'], df_plot.itertuples())):
            color = 'red' if row.close >= row.open else 'green'
            
            # 绘制实体
            ax.bar(date_num, row.close - row.open, width, bottom=row.open, color=color, alpha=0.8)
            
            # 绘制上下影线
            ax.vlines(date_num, row.low, row.high, color=color, linewidth=1)
        
        ax.set_title('K线图')
        ax.set_xlabel('日期')
        ax.set_ylabel('价格 (¥)')
        ax.grid(True, alpha=0.3)
        
        # 格式化日期
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"K线图已保存到: {save_path}")
        
        plt.show()

def main():
    """测试脚本"""
    visualizer = StockVisualizer()
    
    # 这里应该从分析结果获取数据，现在使用示例数据
    print("可视化脚本已准备就绪")
    print("使用方法: visualizer.plot_xxx(df, stock_code, save_path)")

if __name__ == "__main__":
    main()