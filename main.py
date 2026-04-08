import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

all_books = []

# Extraction Phase (Looping through 50 pages)
for i in range(1, 51):
    url = f"https://toscrape.com{i}.html"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price_text = book.find("p", class_="price_color").text

            # Transformation Phase (Cleaning price data)
            clean_price = float(price_text.replace('£', '').replace('Â', ''))

            all_books.append((title, clean_price))

        print(f"Successfully scraped page: {i}")

    except Exception as e:
        print(f"Error on page {i}: {e}")

# Loading Phase (Storing data into SQL Database)
conn = sqlite3.connect('books_data.db')
cursor = conn.cursor()

# Create Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL
    )
''')

# Insert Data
cursor.executemany('INSERT INTO books (title, price) VALUES (?, ?)', all_books)

conn.commit()
conn.close()

# Optional: Export to Excel as a secondary backup
df = pd.DataFrame(all_books, columns=["Title", "Price_GBP"])
df.to_excel("final_books_report.xlsx", index=False)

print("Process Completed: 1000 books saved to SQL and Excel.")
