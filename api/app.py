from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the whole app

def fetch_stock_price(stock_url):
    response = requests.get(stock_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    value_element = soup.select_one('.kf1m0 > .fxKbKc')

    if value_element:
        value = round(float(value_element.text.strip().replace("₹", "").replace(",", "")), 2)
        return value
    else:
        return None  

@app.route('/stocks', methods=['GET'])
def get_stock_prices():
    urls = {
        "ARE&M": "https://www.google.com/finance/quote/ARE%26M:NSE",
        "TATAMOTORS": "https://www.google.com/finance/quote/TATAMOTORS:NSE"
    }

    stock_prices = {}

    for stock_name, url in urls.items():
        price = fetch_stock_price(url)
        if price is not None:
            stock_prices[stock_name] = price
        else:
            stock_prices[stock_name] = "Price not found"

    return jsonify(stock_prices)

if __name__ == '__main__':
    app.run()
