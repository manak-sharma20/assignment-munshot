import csv
import re
from playwright.sync_api import sync_playwright

def clean_price(text):
    if not text:
        return None
    return text.replace(',', '').replace('₹', '').strip()

def scrape_search_results(brands):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        for brand in brands:
            search_url = f"https://www.amazon.in/s?k={brand}+luggage"
            try:
                page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(3000)
                print(f"Title for {brand}: {page.title()}")
                
                items = page.locator("div[data-component-type='s-search-result']").all()
                print(f"Found {len(items)} items for {brand}")
                
                if len(items) > 0 and brand == "Safari":
                    print(f"First item HTML: {items[0].inner_html()[:2000]}")
                    
                for item in items:
                    try:
                        title_el = item.locator("h2")
                        title = title_el.first.text_content().strip() if title_el.count() > 0 else None
                        if not title:
                            continue
                            
                        link_el = item.locator("h2 a")
                        product_link = "https://www.amazon.in" + link_el.get_attribute("href") if link_el.count() > 0 else None
                        
                        price_el = item.locator("span.a-price-whole")
                        price = clean_price(price_el.first.text_content()) if price_el.count() > 0 else None
                        
                        mrp_el = item.locator("span.a-text-price span[aria-hidden='true']")
                        mrp = clean_price(mrp_el.first.text_content()) if mrp_el.count() > 0 else None
                        
                        rating_text = None
                        rating_el_alt = item.locator("span[aria-label*='out of 5 stars']")
                        if rating_el_alt.count() > 0:
                            rating_text = rating_el_alt.first.get_attribute("aria-label")
                            
                        rating = rating_text.split(" ")[0] if rating_text else None
                        
                        count_el = item.locator("span[aria-label*='ratings']")
                        if count_el.count() == 0:
                            count_el = item.locator("span[aria-label*='reviews']")
                            
                        review_count = None
                        if count_el.count() > 0:
                            aria_label = count_el.first.get_attribute("aria-label")
                            if aria_label:
                                review_count = aria_label.split(' ')[0].replace(',', '')
                        
                        discount = None
                        if price and mrp:
                            try:
                                p_val = float(price)
                                m_val = float(mrp)
                                if m_val > 0:
                                    discount = round(((m_val - p_val) / m_val) * 100, 2)
                            except ValueError:
                                pass
                        
                        results.append({
                            "brand": brand,
                            "title": title,
                            "price": price,
                            "mrp": mrp,
                            "discount_pct": discount,
                            "rating": rating,
                            "review_count": review_count,
                            "product_link": product_link
                        })
                    except Exception as e:
                        import traceback
                        print(f"Inner error: {e}\n{traceback.format_exc()}")
                        continue
            except Exception as e:
                print(f"Error scraping {brand}: {e}")
                
        browser.close()
    return results

def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Saved {len(data)} items to {filename}")

if __name__ == "__main__":
    brands_to_scrape = ["Safari", "Skybags", "VIP", "American Tourister"]
    data = scrape_search_results(brands_to_scrape)
    save_to_csv(data, "data/raw/products.csv")
