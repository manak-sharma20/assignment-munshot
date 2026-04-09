import pandas as pd

def compute_metrics(products_file, reviews_file, output_file):
    prod_df = pd.read_csv(products_file)
    rev_df = pd.read_csv(reviews_file)
    
    if prod_df.empty:
        return
        
    brand_prod = prod_df.groupby('brand').agg(
        avg_price=('price', 'mean'),
        avg_discount=('discount_pct', 'mean'),
        avg_rating=('rating', 'mean'),
        product_count=('title', 'count')
    ).reset_index()
    
    if not rev_df.empty and 'sentiment_score' in rev_df.columns:
        brand_rev = rev_df.groupby('brand').agg(
            sentiment_score=('sentiment_score', 'mean'),
            review_count=('review_text', 'count')
        ).reset_index()
        metrics = pd.merge(brand_prod, brand_rev, on='brand', how='left')
    else:
        metrics = brand_prod
        metrics['sentiment_score'] = 0.0
        metrics['review_count'] = 0
        
    metrics = metrics.round(2)
    metrics.to_csv(output_file, index=False)
    return metrics

if __name__ == "__main__":
    compute_metrics("data/processed/cleaned_products.csv", "data/processed/cleaned_reviews.csv", "data/processed/brand_metrics.csv")
