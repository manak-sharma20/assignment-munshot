import pandas as pd
import re

def extract_themes(input_file, output_file):
    df = pd.read_csv(input_file)
    if 'review_text' not in df.columns or df.empty:
        df.to_csv(output_file, index=False)
        return df

    keywords = {
        'wheels': ['wheel', 'wheels'],
        'handle': ['handle', 'handles', 'telescopic'],
        'durability': ['durable', 'durability', 'broke', 'snapped', 'beating', 'sturdy', 'build', 'flimsy', 'scratch', 'dented'],
        'design': ['design', 'looks', 'look', 'premium', 'stylish'],
        'zipper': ['zipper', 'zip', 'zips'],
        'lock': ['lock', 'jammed', 'code'],
        'value': ['value', 'price', 'money', 'worth']
    }

    def get_themes(text):
        if not isinstance(text, str):
            return ""
        text_lower = text.lower()
        found_themes = []
        for theme, words in keywords.items():
            if any(re.search(r'\b' + w + r'\b', text_lower) for w in words):
                found_themes.append(theme)
        return ", ".join(found_themes)

    df['themes'] = df['review_text'].apply(get_themes)
    
    def determine_pro_con(row):
        themes = row['themes']
        if not themes:
            return ""
        score = row.get('sentiment_score', 0)
        prefix = "PRO: " if score >= 0 else "CON: "
        return prefix + themes

    df['pros_cons'] = df.apply(determine_pro_con, axis=1)

    df.to_csv(output_file, index=False)
    return df

if __name__ == "__main__":
    extract_themes("data/processed/cleaned_reviews.csv", "data/processed/cleaned_reviews.csv")
