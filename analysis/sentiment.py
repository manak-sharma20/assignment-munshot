import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(input_file, output_file):
    df = pd.read_csv(input_file)
    if 'review_text' not in df.columns or df.empty:
        df.to_csv(output_file, index=False)
        return df

    analyzer = SentimentIntensityAnalyzer()
    
    def get_score(text):
        if not isinstance(text, str):
            return 0.0
        return analyzer.polarity_scores(text)['compound']
        
    df['sentiment_score'] = df['review_text'].apply(get_score)
    df['sentiment_label'] = pd.cut(
        df['sentiment_score'],
        bins=[-1.01, -0.05, 0.05, 1.01],
        labels=['Negative', 'Neutral', 'Positive']
    )
    
    df.to_csv(output_file, index=False)
    return df

if __name__ == "__main__":
    analyze_sentiment("data/processed/cleaned_reviews.csv", "data/processed/cleaned_reviews.csv")
