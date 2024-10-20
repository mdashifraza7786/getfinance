from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch stock price
def fetch_stock_price(stock_url):
    # Send an HTTP request to the URL
    response = requests.get(stock_url)

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the value using a CSS selector
    value_element = soup.select_one('.kf1m0 > .fxKbKc')

    # Check if the element was found and extract its text
    if value_element:
        # Clean and convert the value to float
        value = round(float(value_element.text.strip().replace("₹", "").replace(",", "")), 2)
        return value
    else:
        return None  # Return None if not found

# Route to fetch stock prices
@app.route('/stocks', methods=['GET'])
def get_stock_prices():
    # URLs of the Google Finance pages
    urls = {
        "AREM": "https://www.google.com/finance/quote/ARE%26M:NSE",
        "TATAMOTORS": "https://www.google.com/finance/quote/TATAMOTORS:NSE"
    }

    # Dictionary to hold the stock prices
    stock_prices = {}

    # Fetch prices for both stocks
    for stock_name, url in urls.items():
        price = fetch_stock_price(url)
        if price is not None:
            stock_prices[stock_name] = price
        else:
            stock_prices[stock_name] = "Price not found"

    # Return the stock prices as a JSON response
    return jsonify(stock_prices)

