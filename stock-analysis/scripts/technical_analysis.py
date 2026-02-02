#!/usr/bin/env python3
"""
Technical Analysis Script
技术指标分析和买卖信号识别
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SignalType(Enum):
    """信号类型"""
    BUY = "买入"
    SELL = "卖出"
    HOLD = "持有"
    WAIT = "观望"

@dataclass
class TradingSignal:
    """交易信号"""
    signal_type: SignalType
    price: float
    date: pd.Timestamp
    indicator_name: str
    confidence: float
    reason: str

class TechnicalAnalyzer:
    """技术指标分析器"""
    
    def __init__(self):
        self.indicators = {}
    
    def calculate_ma(self, df: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> pd.DataFrame:
        """
        计算移动平均线
        """
        df = df.copy()
        for period in periods:
            df[f'MA{period}'] = df['close'].rolling(window=period).mean()
        return df
    
    def calculate_ema(self, df: pd.DataFrame, periods: List[int] = [12, 26]) -> pd.DataFrame:
        """
        计算指数移动平均线
        """
        df = df.copy()
        for period in periods:
            df[f'EMA{period}'] = df['close'].ewm(span=period, adjust=False).mean()
        return df
    
    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        计算MACD指标
        """
        df = df.copy()
        
        # 计算快速和慢速EMA
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
        
        # 计算MACD线
        df['MACD'] = ema_fast - ema_slow
        df['MACD_signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
        df['MACD_histogram'] = df['MACD'] - df['MACD_signal']
        
        return df
    
    def calculate_rsi(self, df: pd.DataFrame, periods: List[int] = [14]) -> pd.DataFrame:
        """
        计算RSI指标
        """
        df = df.copy()
        
        for period in periods:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            df[f'RSI{period}'] = 100 - (100 / (1 + rs))
        
        return df
    
    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std_dev: float = 2) -> pd.DataFrame:
        """
        计算布林带
        """
        df = df.copy()
        
        # 计算中轨（简单移动平均）
        df['BB_middle'] = df['close'].rolling(window=period).mean()
        
        # 计算标准差
        df['BB_std'] = df['close'].rolling(window=period).std()
        
        # 计算上轨和下轨
        df['BB_upper'] = df['BB_middle'] + (df['BB_std'] * std_dev)
        df['BB_lower'] = df['BB_middle'] - (df['BB_std'] * std_dev)
        
        # 计算带宽
        df['BB_bandwidth'] = (df['BB_upper'] - df['BB_lower']) / df['BB_middle']
        
        return df
    
    def calculate_kdj(self, df: pd.DataFrame, period: int = 9) -> pd.DataFrame:
        """
        计算KDJ指标
        """
        df = df.copy()
        
        # 计算RSV (未成熟随机值)
        low_min = df['low'].rolling(window=period).min()
        high_max = df['high'].rolling(window=period).max()
        df['RSV'] = (df['close'] - low_min) / (high_max - low_min) * 100
        
        # 计算K、D、J值
        df['K'] = df['RSV'].ewm(com=2, adjust=False).mean()
        df['D'] = df['K'].ewm(com=2, adjust=False).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']
        
        return df
    
    def calculate_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算成交量指标
        """
        df = df.copy()
        
        # 确保使用正确的列名
        volume_col = 'vol' if 'vol' in df.columns else 'volume'
        
        # 成交量移动平均
        df['VOL_MA5'] = df[volume_col].rolling(window=5).mean()
        df['VOL_MA10'] = df[volume_col].rolling(window=10).mean()
        
        # 成交量变化率
        df['VOL_change'] = df[volume_col].pct_change() * 100
        
        # 量比
        df['VOL_ratio'] = df[volume_col] / df['VOL_MA5']
        
        return df
    
    def generate_ma_signals(self, df: pd.DataFrame) -> List[TradingSignal]:
        """
        基于移动平均线的交易信号
        """
        signals = []
        
        # 计算MA
        df_ma = self.calculate_ma(df)
        
        # 确保使用正确的列名
        date_col = 'trade_date' if 'trade_date' in df_ma.columns else 'date'
        
        # 寻找金叉和死叉
        for i in range(1, len(df_ma)):
            prev_row = df_ma.iloc[i-1]
            curr_row = df_ma.iloc[i]
            
            # MA5上穿MA20 - 金叉
            if (prev_row['MA5'] <= prev_row['MA20'] and 
                curr_row['MA5'] > curr_row['MA20'] and 
                not pd.isna(curr_row['MA5']) and not pd.isna(curr_row['MA20'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.BUY,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="MA金叉",
                    confidence=0.7,
                    reason="MA5上穿MA20，形成金叉信号"
                ))
            
            # MA5下穿MA20 - 死叉
            elif (prev_row['MA5'] >= prev_row['MA20'] and 
                  curr_row['MA5'] < curr_row['MA20'] and 
                  not pd.isna(curr_row['MA5']) and not pd.isna(curr_row['MA20'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.SELL,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="MA死叉",
                    confidence=0.7,
                    reason="MA5下穿MA20，形成死叉信号"
                ))
        
        return signals
    
    def generate_macd_signals(self, df: pd.DataFrame) -> List[TradingSignal]:
        """
        基于MACD的交易信号
        """
        signals = []
        
        # 计算MACD
        df_macd = self.calculate_macd(df)
        
        for i in range(1, len(df_macd)):
            prev_row = df_macd.iloc[i-1]
            curr_row = df_macd.iloc[i]

            date_col = 'trade_date' if 'trade_date' in df_macd.columns else 'date'

            # MACD上穿信号线
            if (prev_row['MACD'] <= prev_row['MACD_signal'] and 
                curr_row['MACD'] > curr_row['MACD_signal'] and
                not pd.isna(curr_row['MACD']) and not pd.isna(curr_row['MACD_signal'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.BUY,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="MACD金叉",
                    confidence=0.8,
                    reason="MACD上穿信号线，形成买入信号"
                ))
            
            # MACD下穿信号线
            elif (prev_row['MACD'] >= prev_row['MACD_signal'] and 
                  curr_row['MACD'] < curr_row['MACD_signal'] and
                  not pd.isna(curr_row['MACD']) and not pd.isna(curr_row['MACD_signal'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.SELL,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="MACD死叉",
                    confidence=0.8,
                    reason="MACD下穿信号线，形成卖出信号"
                ))
        
        return signals
    
    def generate_rsi_signals(self, df: pd.DataFrame, oversold: int = 30, overbought: int = 70) -> List[TradingSignal]:
        """
        基于RSI的交易信号
        """
        signals = []
        
        # 计算RSI
        df_rsi = self.calculate_rsi(df)
        
        for i in range(1, len(df_rsi)):
            prev_row = df_rsi.iloc[i-1]
            curr_row = df_rsi.iloc[i]

            date_col = 'trade_date' if 'trade_date' in df_rsi.columns else 'date'

            # RSI从超卖区域反弹
            if (prev_row['RSI14'] <= oversold and 
                curr_row['RSI14'] > oversold and
                not pd.isna(curr_row['RSI14'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.BUY,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="RSI反弹",
                    confidence=0.6,
                    reason=f"RSI从超卖区域({oversold})反弹"
                ))
            
            # RSI从超买区域回落
            elif (prev_row['RSI14'] >= overbought and 
                  curr_row['RSI14'] < overbought and
                  not pd.isna(curr_row['RSI14'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.SELL,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="RSI回落",
                    confidence=0.6,
                    reason=f"RSI从超买区域({overbought})回落"
                ))
        
        return signals
    
    def generate_bollinger_signals(self, df: pd.DataFrame) -> List[TradingSignal]:
        """
        基于布林带的交易信号
        """
        signals = []
        
        # 计算布林带
        df_bb = self.calculate_bollinger_bands(df)
        
        for i in range(1, len(df_bb)):
            prev_row = df_bb.iloc[i-1]
            curr_row = df_bb.iloc[i]

            date_col = 'trade_date' if 'trade_date' in df_bb.columns else 'date'

            # 价格从下轨反弹
            if (prev_row['close'] <= prev_row['BB_lower'] and 
                curr_row['close'] > prev_row['BB_lower'] and
                not pd.isna(curr_row['BB_lower'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.BUY,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="布林带反弹",
                    confidence=0.6,
                    reason="价格从布林带下轨反弹"
                ))
            
            # 价格触及上轨
            elif (curr_row['close'] >= curr_row['BB_upper'] and
                  not pd.isna(curr_row['BB_upper'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.SELL,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="布林带超买",
                    confidence=0.5,
                    reason="价格触及布林带上轨，可能超买"
                ))
        
        return signals
    
    def generate_kdj_signals(self, df: pd.DataFrame) -> List[TradingSignal]:
        """
        基于KDJ的交易信号
        """
        signals = []
        
        # 计算KDJ
        df_kdj = self.calculate_kdj(df)
        
        for i in range(1, len(df_kdj)):
            prev_row = df_kdj.iloc[i-1]
            curr_row = df_kdj.iloc[i]

            date_col = 'trade_date' if 'trade_date' in df_kdj.columns else 'date'

            # K线从超卖区域反弹
            if (prev_row['K'] <= 20 and curr_row['K'] > 20 and
                not pd.isna(curr_row['K'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.BUY,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="KDJ反弹",
                    confidence=0.6,
                    reason="K线从超卖区域(20以下)反弹"
                ))
            
            # K线从超买区域回落
            elif (prev_row['K'] >= 80 and curr_row['K'] < 80 and
                not pd.isna(curr_row['K'])):
                
                signals.append(TradingSignal(
                    signal_type=SignalType.SELL,
                    price=curr_row['close'],
                    date=curr_row[date_col],
                    indicator_name="KDJ回落",
                    confidence=0.6,
                    reason="K线从超买区域(80以上)回落"
                ))
        
        return signals
    
    def analyze_stock(self, df: pd.DataFrame) -> Dict:
        """
        综合分析股票并生成交易信号
        """
        # 计算所有技术指标
        df_analysis = df.copy()
        df_analysis = self.calculate_ma(df_analysis)
        df_analysis = self.calculate_macd(df_analysis)
        df_analysis = self.calculate_rsi(df_analysis)
        df_analysis = self.calculate_bollinger_bands(df_analysis)
        df_analysis = self.calculate_kdj(df_analysis)
        df_analysis = self.calculate_volume_indicators(df_analysis)
        
        # 生成各种信号
        ma_signals = self.generate_ma_signals(df_analysis)
        macd_signals = self.generate_macd_signals(df_analysis)
        rsi_signals = self.generate_rsi_signals(df_analysis)
        bb_signals = self.generate_bollinger_signals(df_analysis)
        kdj_signals = self.generate_kdj_signals(df_analysis)
        
        # 合并所有信号
        all_signals = ma_signals + macd_signals + rsi_signals + bb_signals + kdj_signals
        
        # 按日期排序
        all_signals.sort(key=lambda x: x.date, reverse=True)
        
        return {
            'data': df_analysis,
            'signals': all_signals,
            'latest_signals': all_signals[:10] if all_signals else [],  # 最近10个信号
            'summary': {
                'total_signals': len(all_signals),
                'buy_signals': len([s for s in all_signals if s.signal_type == SignalType.BUY]),
                'sell_signals': len([s for s in all_signals if s.signal_type == SignalType.SELL]),
                'hold_signals': len([s for s in all_signals if s.signal_type == SignalType.HOLD]),
            }
        }

def main():
    """测试脚本"""
    # 这里应该从文件或API获取数据，现在使用测试数据
    pass

if __name__ == "__main__":
    main()