import time
import json
import redis
import requests
from config import ALPHA_VANTAGE_API_KEY

class BasicMarketDataCollector:
    def __init__(self):
        # Connect to Redis
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        
        # Test symbols
        self.symbols = ['AAPL', 'MSFT', 'GOOGL']
        
        print("✅ Market Data Collector initialized")
    
    def collect_quotes(self):
        """Collect quotes for all symbols"""
        print("📡 Collecting market data...")
        
        for symbol in self.symbols:
            try:
                # Get quote from Alpha Vantage
                quote_data = self.get_quote(symbol)
                
                if quote_data:
                    # Store in Redis
                    self.store_quote(symbol, quote_data)
                    print(f"✅ {symbol}: ${quote_data['price']}")
                
                # Wait 1 second between calls (rate limit)
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error getting {symbol}: {e}")
    
    def get_quote(self, symbol):
        """Get quote from Alpha Vantage API"""
        url = "https://www.alphavantage.co/query"
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'symbol': symbol,
                    'price': float(quote.get('05. price', 0)),
                    'change': quote.get('09. change', '0'),
                    'timestamp': time.time()
                }
        
        return None
    
    def store_quote(self, symbol, quote_data):
        """Store quote in Redis"""
        # Store latest quote
        quote_key = f"quote:{symbol}"
        self.redis.set(quote_key, json.dumps(quote_data), ex=300)  # 5 min expiry
        
        # Add to history list
        history_key = f"history:{symbol}"
        self.redis.lpush(history_key, json.dumps(quote_data))
        self.redis.ltrim(history_key, 0, 99)  # Keep last 100 quotes
    
    def get_latest_quote(self, symbol):
        """Get latest quote from Redis"""
        quote_key = f"quote:{symbol}"
        quote_data = self.redis.get(quote_key)
        
        if quote_data:
            return json.loads(quote_data)
        return None

if __name__ == "__main__":
    # Test the collector
    collector = BasicMarketDataCollector()
    collector.collect_quotes()
    
    # Show what we collected
    print("\n📊 Latest quotes in Redis:")
    for symbol in collector.symbols:
        quote = collector.get_latest_quote(symbol)
        if quote:
            print(f"{symbol}: ${quote['price']} (stored at {quote['timestamp']})")
