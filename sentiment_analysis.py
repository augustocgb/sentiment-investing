from pygooglenews import GoogleNews
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import csv
import pandas as pd
from datetime import date, timedelta

nltk.download('vader_lexicon')

def get_stock_news(ticker, period='1d', start_date=None, end_date=None, max_results=100):
    """
    Fetches news headlines for a given stock ticker.
    """

    if (end_date is not None):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        return get_historical_news(ticker, start_date, end_date, max_results)

    gn = GoogleNews()
    search = gn.search(f'{ticker} stock', when=period)
    
    return search['entries']

def get_historical_news(ticker, start_date, end_date, max_results):
    """
    Fetches news headlines for a ticker over a given date range.
    """

    gn = GoogleNews()
    all_entries = set()
    
    current_date = start_date

    num_results = 0

    while current_date <= end_date:
        start_date_str = current_date.strftime('%Y-%m-%d')
        end_date_str = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"Fetching news for {start_date_str}...")

        try:
            search = gn.search(f'{ticker} stock', from_=start_date_str, to_=end_date_str)
        except Exception as e:
            print(f"Error fetching news for {start_date_str}: {e}")
            current_date += timedelta(days=1)
            continue

        for entry in search['entries']:

            if num_results >= max_results:
                return list(all_entries)

            num_results += 1
            all_entries.add(entry)

        current_date += timedelta(days=1)
    
    print(f"Fetched {len(all_entries)} unique headlines from {start_date} to {end_date}.")
    return list(all_entries)

def period_to_days(period: str) -> int:
    """
    Converts a period string to the equivalent number of days.
    """

    period = period.lower().strip()

    multipliers = {'d': 1, 'm': 30, 'y': 365, 'yr': 365}
    
    if period.endswith('yr'):
        unit = 'yr'
        numeric_str = period[:-2]
    elif period[-1] in multipliers:
        unit = period[-1]
        numeric_str = period[:-1]
    else:
        raise ValueError(f"Invalid time unit in '{period}'. Use 'd', 'm', 'y', or 'yr'.")

    try:
        num = int(numeric_str)
        return num * multipliers[unit]
    except ValueError:
        raise ValueError(f"Invalid number format in '{period}'.")

def analyze_sentiment(headline):
    """
    Analyzes the sentiment of a single headline.
    """

    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(headline)

    return score['compound']

def analyze_sentiment_list(headlines):
    """
    Analyzes the sentiment of a list of headlines.
    """

    sia = SentimentIntensityAnalyzer()

    sentiment_scores = [sia.polarity_scores(headline)['compound'] for headline in headlines]

    if sentiment_scores:
        return sum(sentiment_scores) / len(sentiment_scores)
    else:
        return 0

def save_to_csv(ticker, headlines_data):
    """
    Saves a list of headlines and their scores to a CSV file.
    """

    filename = f"{ticker}_headlines.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Date', 'Headline', 'Sentiment Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(headlines_data)

    print(f"Successfully saved headlines and scores to {filename}")

if __name__ == "__main__":
    stock_ticker = input("Enter a stock ticker (e.g., GOOGL, TSLA): ").upper()
    period = input("Enter the period for news (e.g., 1d, 7d, 30d): ").strip() or '1d'
    max_headlines = input("Enter the maximum number of headlines to fetch (default is 100): ").strip() or '100'

    end = date.today()
    start = end - timedelta(days=period_to_days(period))

    news = get_stock_news(stock_ticker, period, start_date=start, end_date=end, max_results=int(max_headlines))

    if news:
        scored_headlines = []
        sia = SentimentIntensityAnalyzer()
        news_headlines = [entry.title for entry in news]
        news_dates = [entry.published for entry in news]

        for i, headline in enumerate(news_headlines):

            score = sia.polarity_scores(headline)['compound']
            date = pd.to_datetime(news_dates[i])
            scored_headlines.append({'Date': date, 'Headline': headline, 'Sentiment Score': score})
            
            print(f"{i+1}. {headline} (Score: {score:.2f})")
        
        save_to_csv(stock_ticker, scored_headlines)

        avg_sentiment = analyze_sentiment_list(news_headlines)
        print(f"Average Sentiment Score: {avg_sentiment:.2f}")

        if avg_sentiment > 0.05:
            print("Overall sentiment is Positive")
        elif avg_sentiment < -0.05:
            print("Overall sentiment is Negative")
        else:
            print("Overall sentiment is Neutral")
    else:
        print(f"No recent news found for {stock_ticker}.")