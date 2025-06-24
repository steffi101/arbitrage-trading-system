import requests
from config import ALPHA_VANTAGE_API_KEY

def test_api():
    try:

        url = "https://www.alphavantage.co/query"
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': 'AAPL',
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        
        print("Testing Alpha Vantage API...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {response.status_code}")
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                price = quote.get('05. price', 'N/A')
                symbol = quote.get('01. symbol', 'N/A')
                print(f"✅ API working! {symbol} price: ${price}")
            else:
                print(f"⚠️  Response structure: {data}")
                
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
