from pygooglenews import GoogleNews
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import csv

nltk.download('vader_lexicon')

def get_stock_news(ticker, period='1d'):
    """
    Fetches news headlines for a given stock ticker.
    """

    gn = GoogleNews()
    search = gn.search(f'{ticker} stock', when=period)
    headlines = [entry['title'] for entry in search['entries']]
    
    return headlines

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
        fieldnames = ['Headline', 'Sentiment Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(headlines_data)

    print(f"Successfully saved headlines and scores to {filename}")

if __name__ == "__main__":
    stock_ticker = input("Enter a stock ticker (e.g., GOOGL, TSLA): ").upper()
    period = input("Enter the period for news (e.g., 1d, 7d, 30d): ").strip() or '1d'
    news_headlines = get_stock_news(stock_ticker, period)

    if news_headlines:

        scored_headlines = []
        sia = SentimentIntensityAnalyzer()

        for i, headline in enumerate(news_headlines):
            score = sia.polarity_scores(headline)['compound']
            
            scored_headlines.append({'Headline': headline, 'Sentiment Score': score})
            
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