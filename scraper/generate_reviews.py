import csv
import random
from datetime import datetime, timedelta

def load_products(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def generate_random_date(start_days_ago=365):
    d = datetime.now() - timedelta(days=random.randint(0, start_days_ago))
    return d.strftime('%Y-%m-%d')

def get_review_templates():
    return {
        "positive": [
            "Great {brand} luggage, very durable and the wheels are extremely smooth.",
            "I love the design! Zippers feel premium and the handle is sturdy.",
            "Value for money. The material took a beating on my last flight but still looks good.",
            "Excellent capacity and lightweight. Best purchase from {brand}.",
            "Good quality trolley, wheels rotate 360 smoothly, and the lock works perfectly.",
            "Spacious and scratch-resistant. Highly recommended for frequent travelers."
        ],
        "neutral": [
            "It's decent for the price. The handle wobbles a bit but gets the job done.",
            "Average quality. Scratches easily but wheels are alright.",
            "Looks good but the zipper could be smoother. Expected slightly better from {brand}.",
            "Okay product. Fits in cabin but the build feels a bit flimsy."
        ],
        "negative": [
            "Wheel broke after the first trip. Very disappointed with {brand}.",
            "Zipper got stuck immediately. Poor quality check.",
            "Handle snapped while lifting. Not durable at all.",
            "Terrible material, got dented during transit. Bad value for money.",
            "The lock got jammed completely. Had to break it to open."
        ]
    }

def generate_reviews(products, num_reviews_per_product=30):
    reviews = []
    templates = get_review_templates()
    
    for idx, prod in enumerate(products):
        # We use idx as a proxy for product_id
        brand = prod.get('brand', 'this brand')
        
        # Decide an overall rating bias for this product (between 3 and 4.8)
        rating_bias = random.uniform(3.0, 4.8)
        
        for _ in range(num_reviews_per_product):
            rating = round(random.gauss(rating_bias, 1.0))
            rating = max(1, min(5, rating))
            
            if rating >= 4:
                text = random.choice(templates['positive']).format(brand=brand)
            elif rating == 3:
                text = random.choice(templates['neutral']).format(brand=brand)
            else:
                text = random.choice(templates['negative']).format(brand=brand)
                
            reviews.append({
                "product_id": idx,
                "title": prod.get("title", ""),
                "brand": brand,
                "rating": rating,
                "review_text": text,
                "review_date": generate_random_date()
            })
            
    return reviews

def main():
    products = load_products("data/raw/products.csv")
    reviews = generate_reviews(products, num_reviews_per_product=30)
    
    if not reviews:
        print("No reviews created.")
        return
        
    keys = reviews[0].keys()
    with open("data/raw/reviews.csv", 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(reviews)
        
    print(f"Generated {len(reviews)} mock reviews.")

if __name__ == "__main__":
    main()
