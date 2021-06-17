from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from websocket import create_connection
import threading
import json
load_dotenv()

app = Flask(__name__)

cryptos = [
    {
        "symbol": "ETH",
        "price": 0 
    },
    {
        "symbol": "BTC",
        "price": 0 
    }
]

def startingThread():
    ws = create_connection("wss://stream.binance.com/ws/ethusdt@ticker/btcusdt@ticker")
    while True:
        data = json.loads(ws.recv())
        for crypto in cryptos:
            if crypto["symbol"] in data["s"]:
                crypto["price"] = data["c"]

@app.route("/")
def handlerIndex():
    driver = webdriver.Chrome(executable_path='./driver/chromedriver')
    driver.get('https://www.google.com/search?q=usd+to+cop&oq=usd+to+cop&aqs=chrome..69i57.1749j0j4&sourceid=chrome&ie=UTF-8')
    driver.implicitly_wait(10)
    priceusdtocop = driver.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').text
    driver.close()
    return jsonify({
        "priceusdtocop": priceusdtocop,
        "cryptos": cryptos
    })

if __name__ == "__main__":
    t = threading.Thread(name='binance-websocket', target=startingThread)
    t.start()
    app.run(debug=True)