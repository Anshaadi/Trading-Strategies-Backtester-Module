"""
    This is a copyrighted content of Anshul Shrivastava©️.
    
    Testing strategies on a data and placing orders.
"""



#import libraries
import pandas as pd
import numpy as np
import price_action



#import data
df = pd.read_csv("./testing data/data.csv")
df.head()


#checking for a doji pattern
doji_df = price_action.doji(df)
doji_df.head(100)

#checking for a hammer pattern
hammer_df = price_action.hammer(df)
hammer_df.head(5)

#checking for a shooting star pattern
sstar_df = price_action.shooting_star(df)
sstar_df["sstar"] == True


#checking for a maru bozu pattern
maru_bozu_df = price_action.maru_bozu(df)
maru_bozu_df.maru_bozu.head()


#checking for a MACD technical indicator
MACD_df = price_action.MACD(df)
MACD_df.head()

#checking for a Bollinger Band technical indicator
bollinger_band_df = price_action.bollinger_band(df)
bollinger_band_df.head()

#checking for a ATR technical indicator
ATR_df = price_action.ATR(df)
ATR_df.head(25)



