import pandas as pd

def clean_products(input_path, output_path):
    df = pd.read_csv(input_path)
    if df.empty:
        df.to_csv(output_path, index=False)
        return df
        
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['mrp'] = pd.to_numeric(df['mrp'], errors='coerce')
    df['discount_pct'] = pd.to_numeric(df['discount_pct'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
    
    df = df.dropna(subset=['title', 'price'])
    
    df.to_csv(output_path, index=False)
    return df

def clean_reviews(input_path, output_path):
    df = pd.read_csv(input_path)
    if df.empty:
        df.to_csv(output_path, index=False)
        return df
        
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['review_text', 'rating'])
    
    df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    clean_products("data/raw/products.csv", "data/processed/cleaned_products.csv")
    clean_reviews("data/raw/reviews.csv", "data/processed/cleaned_reviews.csv")
