#!/usr/bin/env python3
"""
全球股票数据获取模块
使用Yahoo Finance API获取全球股票原始数据
模型负责所有技术分析和解读
"""

from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf


class GlobalStockDataFetcher:
    """全球股票数据获取器 - 只提供原始数据，分析由AI模型完成"""

    def get_stock_data(self, symbol: str, days_back: int = 90) -> pd.DataFrame:
        """
        获取股票历史数据

        Args:
            symbol: 股票代码 (如 'BABA', 'AAPL', '0700.HK')
            days_back: 获取多少天的数据

        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        ticker = yf.Ticker(symbol)
        df = ticker.history(
            start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d")
        )

        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()
        df.columns = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "dividends",
            "stock_splits",
        ]
        df = df.drop(["dividends", "stock_splits"], axis=1, errors="ignore")
        df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

        return df.sort_values("date").reset_index(drop=True)

    def get_current_price(self, symbol: str) -> dict:
        """获取当前价格和基本信息"""
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1d")

        if hist.empty:
            return {"error": f"无法获取 {symbol} 的数据"}

        return {
            "symbol": symbol,
            "current_price": hist["Close"].iloc[-1],
            "company_name": info.get("shortName", info.get("longName", "Unknown")),
            "market": info.get("market", "Unknown"),
            "currency": info.get("currency", "USD"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


def main():
    """示例用法"""
    fetcher = GlobalStockDataFetcher()

    # 获取BABA数据
    df = fetcher.get_stock_data("BABA", days_back=90)
    print(f"获取到 {len(df)} 条数据")
    print(df.tail())

    # 获取当前价格
    info = fetcher.get_current_price("BABA")
    print(f"\n当前价格: {info['current_price']}")


if __name__ == "__main__":
    main()
