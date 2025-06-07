import requests
from config import ALPHA_VANTAGE_API_KEY

def test_api():
    url = "https://www.alphavantage.co/query"
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': 'AAPL',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    
    print(f"🧪 Testing API with key: {ALPHA_VANTAGE_API_KEY[:8]}...")
    
    response = requests.get(url, params=params)
    print(f"📡 Response status: {response.status_code}")
    
    data = response.json()
    print(f"📊 Response data: {data}")
    
    if 'Global Quote' in data:
        quote = data['Global Quote']
        price = quote.get('05. price')
        print(f"✅ AAPL price: ${price}")
        return True
    elif 'Note' in data:
        print(f"⚠️ API Limit: {data['Note']}")
        return False
    elif 'Error Message' in data:
        print(f"❌ API Error: {data['Error Message']}")
        return False
    else:
        print("❌ Unknown response format")
        return False

if __name__ == "__main__":
    test_api()
