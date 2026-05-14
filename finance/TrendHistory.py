import requests
import json
import time
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from finance.YahooFinance import YahooFinance

class TrendHistory:
	def __init__(self, asset: YahooFinance):
		asset.records = asset.records[-500:]
		self.asset = asset
		asset_timestamps = [records.timestamp for records in self.asset.records]
		self.asset_quotes = [records.close for records in self.asset.records]
		self.dates = [datetime.fromtimestamp(timestamp) for timestamp in asset_timestamps]
		self.df = pd.DataFrame({
			'Date': self.dates,
			'asset': self.asset_quotes
		})
	def getMean(self, size: int):
		return self.df['asset'].rolling(window=size).mean()
	def getlastDividend(self):
		if len(self.asset.events["dividends"]) > 0:
			last_dividend_date = list(self.asset.events["dividends"].keys())[-1]
			last_dividend_value = self.asset.events["dividends"][last_dividend_date]
			return last_dividend_value
		return None
	def daysBetweenDividends(self):
		if len(self.asset.events["dividends"]) > 0:
			dates = [datetime.fromtimestamp(int(dividend)) for dividend in self.asset.events["dividends"]]
			dates.sort()
			differences = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
			average_days = sum(differences) / len(differences)
			if average_days > 365:
				average_days = 365
			return average_days
		return None
	def daysSinceLastDividend(self):
		last_dividend_value = self.getlastDividend()
		timestamp_date = datetime.fromtimestamp(last_dividend_value["date"])
		now = datetime.now()
		difference = now - timestamp_date
		days_between = difference.days
		return days_between
	def check_trends(self):
		#asset_timestamps = get_tenth(asset_timestamps, 3)
		#asset_quotes = get_tenth(asset_quotes, 3)

		timestamps = []
		long_average = self.getMean(200)
		short_average = self.getMean(50)
		very_short_average = self.getMean(20)


		quote = 0
		trend_ratios = []
		while quote < len(self.asset_quotes):
			if not math.isnan(short_average[quote]) and not math.isnan(long_average[quote]):
				trend_ratios.append(short_average[quote] / long_average[quote])
			else:
				trend_ratios.append(0)
			quote = quote + 1
		colors = []
		isTrends = []

		i = 0
		latest_50_ratios = []
		while i < len(trend_ratios):
			trend_ratio = trend_ratios[i]
			if trend_ratio:
				if (len(latest_50_ratios)) == 50:
					latest_20_ratios = latest_50_ratios[-20:]
					latest_5_ratios = latest_50_ratios[-5:]
					
					latest_5_ratio_growth = [latest_5_ratios[i+1] / latest_5_ratios[i] for i in range(len(latest_5_ratios) - 1)]
					
					std50 = np.std(latest_50_ratios)
					mean50 = np.mean(latest_50_ratios)
					std20 = np.std(latest_20_ratios)
					mean20 = np.mean(latest_20_ratios)
					std5 = np.std(latest_5_ratios)
					mean5 = np.mean(latest_5_ratios)
					cv50 = 100.0 * std50 / mean50
					cv20 = 100.0 * std20 / mean20
					cv5 = 100.0 * std5 / mean5
					distance_from_short_average = 100 * abs(1 - (self.asset_quotes[i] / short_average[i]))
					mean5_growth = 100 * (np.mean(latest_5_ratio_growth) - 1)
					#mean_growth = abs(mean_growth)
		#			print(str(trend_ratio) + " str : " + str(cv))
		#			if mean50 > 1.1 and cv50 < 1 and cv5 < 1 and distance_from_short_average < 5:
		#			if mean50 > 1.05 and cv50 < 2.3 and cv20 < 1.4:
					asset_height = (self.asset_quotes[i]-long_average[i])/(short_average[i] - long_average[i])
		#				if trend_ratio > 1.05 and mean5_growth > -0.05 and cv50 < 2.3 and asset_height < 2 and asset_height > 0.75:
					if trend_ratio > 1 and asset_height > 0.75 and mean5_growth > -0.05:
						if 1 and cv50 < 5: # maybe should increase comparator when the growth is high
							isTrends.append(2)
							colors.append('green')
						else:
							isTrends.append(2)
							colors.append('orange')
					else:
						isTrends.append(0)
						colors.append('black')
					latest_50_ratios = latest_50_ratios[1:]
				else:
					isTrends.append(0)
					colors.append('black')
				latest_50_ratios.append(trend_ratio)
			else:
				isTrends.append(0)
				colors.append('black')
			i = i + 1
		return isTrends	