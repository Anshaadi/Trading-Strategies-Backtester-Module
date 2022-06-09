"""
    This is a copyrighted content of Anshul Shrivastava©️.
    
    Price action technical indicators and patterns.
    
    List of functions.
    
    -> Candlestick Patterns:
        1. doji candlestick pattern : doji(ohlc_df,factor=0.05)
        2. hammer candlestick pattern : hammer(ohlc_df,cndl_to_body=3,bodylwr_to_cndl=0.6,lwr_to_cndl=0.6,body_to_cndl=0.1)
        3. shooting star candlestick pattern : shooting_star(ohlc_df,cndl_to_body=3,pattern_to_cndl=0.6,body_to_cndl=0.1)
        4. maru bozu candlestick pattern : maru_bozu(ohlc_df,body_to_avg_cndl=2,wick_to_avg_cndl=0.005)
    
    -> Technical Indicators :
        I. Moving Average Convergence Divergence : MACD(ohlc_df,fast_ma=12,slow_ma=26,signal_line=9)
        II. Bollinger Band : bollinger_band(ohlc_df,period=20,std_dev=2)
        III. Average True Range : ATR(ohlc_df,period=20)
        
"""


#import libraries as needed
import pandas as pd
import numpy as np


########################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------#
########################################################################################################
########################################################################################################
########################################################################################################
################################CANDLESTICK PATTERNS####################################################
########################################################################################################
########################################################################################################
########################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------#
########################################################################################################
#1.doji candlestick pattern
def doji(ohlc_df,factor=0.05):
    #returns dataframe with doji candle column.
    df = ohlc_df.copy()
    avg_candle_size = abs(df["close"] - df["open"]).median()
    df["doji"] = abs(df["close"] - df["open"]) <= (factor * avg_candle_size)
    return df
########################################################################################################
#2.hammer candlestick pattern
def hammer(ohlc_df,cndl_to_body=3,pattern_to_cndl=0.6,body_to_cndl=0.1):
    #returns dataframe with hammer candle column
    df = ohlc_df.copy()
    #ratio of candle size to body size greater than cndl_to_body.
    ratio1 = (df["high"] - df["low"]) > cndl_to_body * (df["open"] - df["close"])
    #ratio of (body+lowerwick) size and lowerwick size to candle size greater than pattern_to_cndl.
    ratio2 = ((df["close"] - df["low"]) / (.001 + df["high"] - df["low"])) > pattern_to_cndl
    ratio3 = ((df["open"] - df["low"]) / (.001 + df["high"] - df["low"])) > pattern_to_cndl
    #ratio of body size to candle size greater than body_to_cndl to check for doji pattern.
    ratio4 = (abs(df["close"] - df["open"])) > body_to_cndl * (df["high"] - df["low"])
    df["hammer"] = ratio1 & ratio2 & ratio3 & ratio4
    return df
########################################################################################################
#3.shooting star candlestick pattern
def shooting_star(ohlc_df,cndl_to_body=3,pattern_to_cndl=0.6,body_to_cndl=0.1):
    #returns dataframe with shooting star candle column.
    df = ohlc_df.copy()
    #ratio of candle size to body size greater than cndl_to_body.
    ratio1 = (df["high"] - df["low"]) > cndl_to_body * (df["open"] - df["close"])
    #ratio of (body+upperwick) size and upperwick size to candle size greater than pattern_to_cndl.
    ratio2 = ((df["high"] - df["close"]) / (.001 + df["high"] - df["low"])) > pattern_to_cndl
    ratio3 = ((df["high"] - df["open"]) / (.001 + df["high"] - df["low"])) > pattern_to_cndl
    #ratio of body size to candle size greater than body_to_cndl to check for doji pattern.
    ratio4 = (abs(df["close"] - df["open"])) > body_to_cndl * (df["high"] - df["low"])
    df["sstar"] = ratio1 & ratio2 & ratio3 & ratio4
    return df
########################################################################################################
#4.maru bozu candlestick pattern
def maru_bozu(ohlc_df,body_to_avg_cndl=2,wick_to_avg_cndl=0.005):
    #returns dataframe with maru bozu candle column.
    df = ohlc_df.copy()
    avg_candle_size = abs(df["close"] - df["open"]).median()
    df["h-c"] = df["high"] - df["close"]
    df["l-o"] = df["low"] - df["open"]
    df["h-o"] = df["high"] - df["open"]
    df["l-c"] = df["low"] - df["close"]
    df["maru_bozu"] = np.where((df["close"] - df["open"] > body_to_avg_cndl * avg_candle_size) & \
                               (df[["h-c","l-o"]].max(axis=1) < wick_to_avg_cndl * avg_candle_size),"maru_bozu_green",
                               np.where((df["open"] - df["close"] > body_to_avg_cndl * avg_candle_size) & \
                                        (abs(df[["h-o","l-c"]]).max(axis=1) < wick_to_avg_cndl * avg_candle_size),"maru_bozu_red",False))
    df.drop(["h-c","l-o","h-o","l-c"],axis=1,inplace=True)
    return df
########################################################################################################

########################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------#
########################################################################################################
########################################################################################################
########################################################################################################
#################################TECHNICAL INDICATORS###################################################
########################################################################################################
########################################################################################################
########################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------#
########################################################################################################
#I.Moving Average Convergence Divergence
def MACD(ohlc_df,fast_ma=12,slow_ma=26,signal_line=9):
    df = ohlc_df.copy()
    df["ma_fast"] = df["close"].ewm(span=fast_ma,min_periods=fast_ma).mean()
    df["ma_slow"] = df["close"].ewm(span=slow_ma,min_periods=slow_ma).mean()
    df["MACD"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = df["MACD"].ewm(span=signal_line,min_periods=signal_line).mean()
    df.dropna(inplace=True)
    return df
########################################################################################################
#II.Bollinger Band
def bollinger_band(ohlc_df,period=20,std_dev=2):
    df = ohlc_df.copy()
    df["EMA"] = df["close"].ewm(span=period,min_periods=period).mean()
    df["BB_up"] = df["EMA"] + (std_dev * df["close"].ewm(span=period,min_periods=period).std(dd0f=0))
    df["BB_dn"] = df["EMA"] - (std_dev * df["close"].ewm(span=period,min_periods=period).std(dd0f=0))
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df
########################################################################################################
#III.Average True Range
def ATR(ohlc_df,period=20):
    #returns dataframe with average true range column
    df = ohlc_df.copy()
    df['h-l'] = abs(df['high'] - df['low'])
    df['h-pc'] = abs(df['high'] - df['close'].shift(1))
    df['l-pc'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['h-l','h-pc','l-pc']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].ewm(com=period,min_periods=period).mean()
    df.drop(["h-l","h-pc","l-pc"],axis=1,inplace=True)
    return df
########################################################################################################