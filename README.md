# Sentiment-Based Stock Trading Strategy

This project implements and backtests a quantitative trading strategy that leverages news sentiment to build and rebalance a stock portfolio. The core idea is to "buy" stocks with the most positive recent news coverage, based on the hypothesis that positive sentiment can be a precursor to upward price movement.

The entire pipeline, from data acquisition and sentiment analysis to strategy backtesting and performance visualization, is automated using Python.

## How It Works

The strategy follows a systematic, rules-based process that is executed monthly:

1. **Data Acquisition**: For a predefined universe of over 100 stocks, the script automatically scrapes recent news headlines using the `pygooglenews` library.

2. **Sentiment Analysis**: Each headline is processed using the VADER (Valence Aware Dictionary and sEntiment Reasoner) model from the NLTK library. VADER assigns a compound sentiment score from -1 (very negative) to +1 (very positive) to each headline.

3. **Monthly Signal Generation**: The daily sentiment scores are aggregated for each stock to calculate a mean sentiment score for the month.

4. **Portfolio Construction**: At the beginning of each month, all stocks in the universe are ranked by their aggregate sentiment score. The strategy takes a long-only, equal-weighted position in the **top 5 stocks** with the highest positive sentiment.

5. **Backtesting**: The historical performance of this strategy is simulated. The script downloads daily adjusted close prices for all selected stocks using `yfinance`, calculates the daily returns of the monthly portfolio, and stitches them together to create a continuous equity curve.

6. **Performance Analysis**: The strategy's cumulative return is calculated and plotted against a benchmark (e.g., the QQQ ETF) to evaluate its effectiveness.

## Technology Stack

This project is built entirely in Python and relies on the following core data science and finance libraries:

* **Data Acquisition**: `pygooglenews`, `yfinance`

* **Data Manipulation & Analysis**: `pandas`, `numpy`, `scipy`

* **Natural Language Processing (NLP)**: `nltk` (specifically the VADER sentiment model)

* **Data Visualization**: `matplotlib`

## Setup and Usage

To run this project on your local machine, follow these steps:

**1. Clone the Repository**

```
git clone https://github.com/augustocgb/sentiment-investing.git
cd sentiment-investing
```

**2. Install Dependencies**

It is recommended to use a virtual environment. All required libraries are listed in the `requirements.txt` file.

**3. Run data collection script**

Run the main Python file to 1. scrape google headlines, 2. run sentiment analysis, and 3. dump to .csv

```
python sentiment-analysis.py
```

The user will be prompted with stock symbol, time span to scrape headlines, and maximum number of headlines, so as to evenly distribute scraping headlines over the time period.

(To download all 100 stocks, type `ALL` when prompted for stock ticker. Depending on time period and number of headlines, this could take a few minutes to several hours.)

The current data in bulk_sentiment.csv contains headlines ranging from July 2022 to July 2025, with ~1000 headlines per stock symbol.

**4. Run Jupyter Notebook cells for analysis and trading**

The Jupyter notebook will import the sentiment data from the CSV file and run a trading strategy, comparing with NASDAQ 100 as a market base.

## Disclaimer

This project is for educational and research purposes only. The results of this backtest are based on historical data and are not indicative of future returns. This is not financial advice.