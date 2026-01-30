#!/usr/bin/env python3
"""
全球股票数据获取脚本
使用Yahoo Finance获取全球股票数据
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import yfinance as yf
from datetime import datetime, timedelta

class GlobalStockDataFetcher:
    """全球股票数据获取器 - 使用Yahoo Finance获取全球股票数据"""
    
    def __init__(self):
        """初始化数据获取器"""
        self.session = None
        
    def format_symbol(self, symbol: str) -> str:
        """
        格式化股票代码以适配Yahoo Finance
        
        Args:
            symbol: 原始股票代码
        
        Returns:
            格式化后的股票代码
        """
        # 如果已经是格式化的代码，直接返回
        if '.' in symbol:
            return symbol
        
        # 中国股票代码映射
        china_symbol_map = {
            # 上海证券交易所 (.SS)
            '000001': '000001.SS',  # 平安银行
            '000002': '000002.SS',  # 万科A
            '600000': '600000.SS',  # 浦发银行
            '600036': '600036.SS',  # 招商银行
            '600519': '600519.SS',  # 贵州茅台
            '600887': '600887.SS',  # 伊利股份
            '600958': '600958.SS',  # 东方财富
            '000858': '000858.SS',  # 五粮液
            '000895': '000895.SS',  # 双汇发展
            '000001.SS': '000001.SS',
            '000002.SS': '000002.SS',
            '600000.SS': '600000.SS',
            '600036.SS': '600036.SS',
            '600519.SS': '600519.SS',
            '600887.SS': '600887.SS',
            '600958.SS': '600958.SS',
            '000858.SS': '000858.SS',
            '000895.SS': '000895.SS',
            # 深圳证券交易所 (.SZ)
            '000001.SZ': '000001.SZ',  # 平安银行
            '000002.SZ': '000002.SZ',  # 万科A
            '002415.SZ': '002415.SK',  # 海康威视
            '300750.SZ': '300750.SZ',  # 宁德时代
            '000858.SZ': '000858.SZ',  # 五粮液
            '000895.SZ': '000895.SZ',  # 双汇发展
            '002594.SZ': '002594.SZ',  # 比亚迪
            '000858.SZ': '000858.SZ',
            '000895.SZ': '000895.SZ',
        }
        
        # 香港股票代码映射
        hk_symbol_map = {
            '0700': '0700.HK',      # 腾讯控股
            '0941': '0941.HK',      # 中国移动
            '0998': '0998.HK',      # 中信股份
            '1398': '1398.HK',      # 工商银行
            '3988': '3988.HK',      # 中国银行
            '0001': '0001.HK',      # 友邦保险
            '0012': '0012.HK',      # 恒生银行
            '0023': '0023.HK',      # 中银香港
            '0038': '0038.HK',      # 香港交易所
            '0094': '0094.HK',      # 东方海外国际
            '00941': '0941.HK',     # 中国移动
            '00998': '0998.HK',     # 中信股份
            '01398': '1398.HK',     # 工商银行
            '03988': '3988.HK',     # 中国银行
            '00700': '0700.HK',     # 腾讯控股
            '09988': '9988.HK',     # 阿里巴巴-SW
            '09988.HK': '09988.HK',
            '0700.HK': '0700.HK',
            '0941.HK': '0941.HK',
            '0998.HK': '0998.HK',
            '1398.HK': '1398.HK',
            '3988.HK': '3988.HK',
            '0001.HK': '0001.HK',
        }
        
        # 日本股票代码映射
        japan_symbol_map = {
            '7203': '7203.T',      # 丰田汽车
            '9984': '9984.T',      # SoftBank Group
            '4502': '4502.T',      # 武田制药
            '6758': '6758.T',      # 索尼
            '4568': '4568.T',      # 夏普
            '8306': '8306.T',      # 三菱UFJ金融集团
            '8766': '8766.T',      # 三井不动产
            '4503': '4503.T',      # KDDI
            '9432': '9432.T',      # Kao
            '4501': '4501.T',      # KDDI
            '7203.T': '7203.T',
            '9984.T': '9984.T',
            '4502.T': '4502.T',
            '6758.T': '6758.T',
            '4568.T': '4568.T',
            '8306.T': '8306.T',
            '8766.T': '8766.T',
            '4503.T': '4503.T',
            '9432.T': '9432.T',
            '4501.T': '4501.T',
        }
        
        # 欧洲股票代码映射
        europe_symbol_map = {
            # 德国
            'SAP': 'SAP.DE',        # SAP
            'BAS': 'BAS.DE',        # 巴斯夫
            'VOW3': 'VOW3.DE',      # 大众汽车
            'BMW': 'BMW.DE',        # 宝马
            'DAI': 'DAI.DE',        # 戴姆勒
            'SIE': 'SIE.DE',        # 西门子
            'ALV': 'ALV.DE',        # 安联保险
            'BAYN': 'BAYN.DE',      # 拜耳
            'BMW.DE': 'BMW.DE',
            'VOW3.DE': 'VOW3.DE',
            'SAP.DE': 'SAP.DE',
            'BAS.DE': 'BAS.DE',
            'DAI.DE': 'DAI.DE',
            'SIE.DE': 'SIE.DE',
            'ALV.DE': 'ALV.DE',
            'BAYN.DE': 'BAYN.DE',
            # 法国
            'MC': 'MC.PA',          # LVMH
            'SAN': 'SAN.PA',        # 赛诺菲
            'OR': 'OR.PA',          # 欧莱雅
            'AI': 'AI.PA',          # Air Liquide
            'BNP': 'BNP.PA',        # 法国巴黎银行
            'MC.PA': 'MC.PA',
            'SAN.PA': 'SAN.PA',
            'OR.PA': 'OR.PA',
            'AI.PA': 'AI.PA',
            'BNP.PA': 'BNP.PA',
            # 英国
            'HSBA': 'HSBA.L',       # 汇丰银行
            'BARC': 'BARC.L',       # 巴克莱银行
            'RIO': 'RIO.L',         # 力拓集团
            'GSK': 'GSK.L',         # 葛兰素史克
            'SHEL': 'SHEL.L',       # 壳牌
            'HSBA.L': 'HSBA.L',
            'BARC.L': 'BARC.L',
            'RIO.L': 'RIO.L',
            'GSK.L': 'GSK.L',
            'SHEL.L': 'SHEL.L',
        }
        
        # 如果在中国股票映射中，返回对应的Yahoo Finance代码
        if symbol in china_symbol_map:
            return china_symbol_map[symbol]
        # 如果在香港股票映射中，返回对应的Yahoo Finance代码
        elif symbol in hk_symbol_map:
            return hk_symbol_map[symbol]
        # 如果在日本股票映射中，返回对应的Yahoo Finance代码
        elif symbol in japan_symbol_map:
            return japan_symbol_map[symbol]
        # 如果在欧洲股票映射中，返回对应的Yahoo Finance代码
        elif symbol in europe_symbol_map:
            return europe_symbol_map[symbol]
        
        # 默认返回原始代码（Yahoo Finance可以处理大部分全球代码）
        return symbol
        
    def get_stock_data(self, symbol: str, start_date: str, end_date: str, max_retries: int = 3) -> pd.DataFrame:
        """
        使用Yahoo Finance获取全球股票数据
        
        Args:
            symbol: 股票代码 (如 'BABA', 'AAPL', 'TSLA', '000001.SS', '000001.SZ', '700.HK')
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            max_retries: 最大重试次数
        
        Returns:
            股票数据DataFrame
        """
        import time
        
        # 格式化股票代码
        formatted_symbol = self.format_symbol(symbol)
        
        print(f"正在获取股票 {formatted_symbol} 的数据...")
        print(f"数据范围: {start_date} 到 {end_date}")
        
        for attempt in range(max_retries):
            try:
                # 创建Yahoo Finance ticker对象
                ticker = yf.Ticker(formatted_symbol)
                
                # 获取历史数据
                df = ticker.history(start=start_date, end=end_date)
                
                if df.empty:
                    print(f"第{attempt + 1}次尝试: 未找到股票 {formatted_symbol} 的数据")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # 指数退避
                        # 尝试使用原始代码
                        ticker = yf.Ticker(symbol)
                        df = ticker.history(start=start_date, end=end_date)
                        
                        if df.empty:
                            print(f"第{attempt + 1}次尝试: 仍未找到股票数据: {symbol}")
                            continue
                        else:
                            print(f"第{attempt + 1}次尝试: 使用原始代码 {symbol} 获取到数据")
                            break
                    else:
                        print(f"所有尝试均失败: {symbol}")
                        return pd.DataFrame()
                
                # 重命名列以符合标准格式
                df = df.reset_index()
                df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'stock_splits']
                
                # 确保日期格式正确
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                
                # 删除不需要的列
                df = df.drop(['dividends', 'stock_splits'], axis=1, errors='ignore')
                
                print(f"成功获取到 {len(df)} 条交易数据")
                return df
                
            except Exception as e:
                print(f"第{attempt + 1}次尝试获取股票 {formatted_symbol} 数据时出错: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                else:
                    print(f"所有重试均失败: {symbol}")
                    return pd.DataFrame()
        
        return pd.DataFrame()
    
    def validate_symbol(self, symbol: str, check_trading_data: bool = False) -> Dict:
        """
        验证股票代码是否有效
        
        Args:
            symbol: 股票代码
            check_trading_data: 是否检查实际的交易数据
        
        Returns:
            验证结果字典
        """
        try:
            # 格式化股票代码
            formatted_symbol = self.format_symbol(symbol)
            
            # 尝试获取基本信息
            ticker = yf.Ticker(formatted_symbol)
            info = ticker.info
            
            # 检查是否为有效的股票信息
            is_valid = bool(info.get('symbol') or info.get('shortName') or info.get('longName'))
            
            result = {
                'symbol': symbol,
                'formatted_symbol': formatted_symbol,
                'is_valid': is_valid,
                'company_name': info.get('shortName') or info.get('longName') or 'Unknown',
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market': info.get('market', 'Unknown'),
                'currency': info.get('currency', 'Unknown'),
                'market_cap': info.get('marketCap'),
                'current_price': info.get('currentPrice'),
                'error': None
            }
            
            # 如果需要检查交易数据
            if check_trading_data and is_valid:
                try:
                    # 获取最近一天的交易数据
                    end_date = datetime.now().strftime('%Y-%m-%d')
                    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                    
                    df = ticker.history(start=start_date, end=end_date)
                    
                    if not df.empty:
                        result['has_trading_data'] = True
                        result['latest_price'] = df['close'].iloc[-1]
                        result['trading_days'] = len(df)
                    else:
                        result['has_trading_data'] = False
                        result['error'] = 'No trading data available'
                        
                except Exception as e:
                    result['has_trading_data'] = False
                    result['error'] = f'Error fetching trading data: {e}'
            
            return result
            
        except Exception as e:
            return {
                'symbol': symbol,
                'formatted_symbol': formatted_symbol,
                'is_valid': False,
                'company_name': 'Unknown',
                'sector': 'Unknown',
                'industry': 'Unknown',
                'market': 'Unknown',
                'currency': 'Unknown',
                'market_cap': None,
                'current_price': None,
                'error': str(e)
            }
    
    def get_company_info(self, symbol: str) -> Dict:
        """
        获取公司信息
        
        Args:
            symbol: 股票代码
        
        Returns:
            公司信息字典
        """
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info
        except Exception as e:
            print(f"获取公司信息时出错: {e}")
            return {}
    
    def get_supported_exchanges(self) -> Dict:
        """
        获取支持的交易所和股票代码格式
        
        Returns:
            支持的交易所信息字典
        """
        return {
            'US': {
                'description': '美国股市',
                'suffix': '',
                'examples': ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN'],
                'notes': '直接使用股票代码，不需要后缀'
            },
            'China_SH': {
                'description': '上海证券交易所',
                'suffix': '.SS',
                'examples': ['000001.SS', '600000.SS', '600519.SS'],
                'notes': '以.SS结尾，6位数字代码'
            },
            'China_SZ': {
                'description': '深圳证券交易所',
                'suffix': '.SZ',
                'examples': ['000001.SZ', '002415.SZ', '300750.SZ'],
                'notes': '以.SZ结尾，6位数字代码'
            },
            'Hong_Kong': {
                'description': '香港交易所',
                'suffix': '.HK',
                'examples': ['0700.HK', '0941.HK', '0998.HK'],
                'notes': '以.HK结尾，4-5位数字代码'
            },
            'Japan': {
                'description': '东京证券交易所',
                'suffix': '.T',
                'examples': ['7203.T', '9984.T', '6758.T'],
                'notes': '以.T结尾，4位数字代码'
            },
            'Germany': {
                'description': '德国股市',
                'suffix': '.DE',
                'examples': ['SAP.DE', 'BMW.DE', 'VOW3.DE'],
                'notes': '以.DE结尾，公司股票代码'
            },
            'France': {
                'description': '法国股市',
                'suffix': '.PA',
                'examples': ['MC.PA', 'SAN.PA', 'OR.PA'],
                'notes': '以.PA结尾，公司股票代码'
            },
            'UK': {
                'description': '英国股市',
                'suffix': '.L',
                'examples': ['HSBA.L', 'BARC.L', 'RIO.L'],
                'notes': '以.L结尾，公司股票代码'
            }
        }
    
    def get_stock_recommendations(self, symbol: str) -> Dict:
        """
        获取股票推荐信息
        
        Args:
            symbol: 股票代码
        
        Returns:
            推荐信息字典
        """
        try:
            ticker = yf.Ticker(symbol)
            recommendations = ticker.recommendations
            
            if recommendations.empty:
                return {
                    'symbol': symbol,
                    'has_recommendations': False,
                    'error': 'No recommendation data available'
                }
            
            # 计算最近的推荐统计
            latest_rec = recommendations.iloc[-1]
            total_analysts = latest_rec.get('To Grade', 0)
            
            buy_count = latest_rec.get('Buy', 0)
            hold_count = latest_rec.get('Hold', 0)
            sell_count = latest_rec.get('Sell', 0)
            
            if total_analysts > 0:
                buy_percent = (buy_count / total_analysts) * 100
                hold_percent = (hold_count / total_analysts) * 100
                sell_percent = (sell_count / total_analysts) * 100
            else:
                buy_percent = hold_percent = sell_percent = 0
            
            return {
                'symbol': symbol,
                'has_recommendations': True,
                'date': recommendations.index[-1].strftime('%Y-%m-%d'),
                'total_analysts': total_analysts,
                'buy_count': buy_count,
                'hold_count': hold_count,
                'sell_count': sell_count,
                'buy_percent': buy_percent,
                'hold_percent': hold_percent,
                'sell_percent': sell_percent,
                'average_rating': self._calculate_rating(buy_count, hold_count, sell_count)
            }
            
        except Exception as e:
            return {
                'symbol': symbol,
                'has_recommendations': False,
                'error': str(e)
            }
    
    def _calculate_rating(self, buy_count: int, hold_count: int, sell_count: int) -> float:
        """
        计算平均评分 (1-5, 5=强烈买入, 1=强烈卖出)
        
        Args:
            buy_count: 买入分析师数量
            hold_count: 持有分析师数量
            sell_count: 卖出分析师数量
        
        Returns:
            平均评分
        """
        total = buy_count + hold_count + sell_count
        if total == 0:
            return 3.0  # 中性
        
        # 权重: 买入=5, 持有=3, 卖出=1
        weighted_score = (buy_count * 5 + hold_count * 3 + sell_count * 1) / total
        return round(weighted_score, 2)