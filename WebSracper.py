import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Target URL (demo site like 'books.toscrape.com' which is safe for scraping)
url = "http://books.toscrape.com/catalogue/category/books_1/index.html"

product_names = []
product_prices = []

# Loop through pages (optional)
for page in range(1, 3):  # Scrape first 2 pages
    page_url = url.replace("index.html", f"page-{page}.html") if page > 1 else url
    response = requests.get(page_url)
    
    if response.status_code != 200:
        print(f"Failed to load page {page}")
        continue
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    products = soup.find_all("article", class_="product_pod")
    
    for product in products:
        name = product.h3.a['title']
        price = product.find("p", class_="price_color").text
        product_names.append(name)
        product_prices.append(price)
    
    time.sleep(1)  # polite pause

# Save to Excel
df = pd.DataFrame({
    "Product Name": product_names,
    "Price": product_prices
})

df.to_excel("products.xlsx", index=False)
print("Scraping complete! Saved to products.xlsx")
