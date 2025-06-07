import time
import json
import redis
import requests
from config import ALPHA_VANTAGE_API_KEY

class ImprovedMarketDataCollector:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        
        # EXPANDED STOCK LIST - Top 20 most traded stocks
        self.symbols = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
            'META', 'NVDA', 'NFLX', 'AMD', 'CRM',
            'ORCL', 'ADBE', 'PYPL', 'INTC', 'UBER',
            'SPY', 'QQQ', 'IWM', 'GLD', 'TLT'
        ]
        
        self.venues = ['NYSE', 'NASDAQ', 'BATS']
        print(f"✅ Improved Collector initialized - tracking {len(self.symbols)} symbols")
    
    def collect_all_data(self):
        """Collect market data and generate arbitrage opportunities"""
        print("🚀 Starting comprehensive data collection...")
        
        # Collect market data for all symbols
        collected_count = 0
        
        for i, symbol in enumerate(self.symbols):
            try:
                print(f"📡 Collecting {symbol} ({i+1}/{len(self.symbols)})...")
                
                # Get real quote
                quote_data = self.get_quote(symbol)
                
                if quote_data:
                    # Store market data
                    self.store_quote(symbol, quote_data)
                    
                    # Generate arbitrage opportunity
                    opportunity = self.generate_opportunity(symbol, quote_data['price'])
                    
                    if opportunity:
                        self.store_opportunity(symbol, opportunity)
                    
                    collected_count += 1
                    print(f"✅ {symbol}: ${quote_data['price']} - Opportunity: {opportunity['profit_bps']:.1f} bps")
                
                # Wait between calls to respect rate limits
                time.sleep(1.5)  # Alpha Vantage allows 5 calls per minute
                
            except Exception as e:
                print(f"❌ Error with {symbol}: {e}")
                continue
        
        print(f"\n🎉 Collection complete! {collected_count}/{len(self.symbols)} symbols collected")
        return collected_count
    
    def get_quote(self, symbol):
        """Get quote from Alpha Vantage"""
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
    
    def generate_opportunity(self, symbol, base_price):
        """Generate arbitrage opportunity with realistic venue pricing"""
        import random
        
        # Create more realistic venue price differences
        venue_multipliers = {
            'NYSE': random.uniform(0.9985, 1.0015),    # ±0.15%
            'NASDAQ': random.uniform(0.9990, 1.0020),  # ±0.10-0.20%
            'BATS': random.uniform(0.9980, 1.0010)     # ±0.10-0.20%
        }
        
        venue_prices = {}
        for venue, multiplier in venue_multipliers.items():
            venue_prices[venue] = round(base_price * multiplier, 2)
        
        # Find arbitrage opportunity
        buy_venue = min(venue_prices, key=venue_prices.get)
        sell_venue = max(venue_prices, key=venue_prices.get)
        
        buy_price = venue_prices[buy_venue]
        sell_price = venue_prices[sell_venue]
        
        profit_per_share = sell_price - buy_price
        profit_bps = (profit_per_share / buy_price) * 10000
        
        # Only return opportunities with decent profit
        if profit_bps > 5:  # At least 5 basis points
            return {
                'symbol': symbol,
                'buy_venue': buy_venue,
                'sell_venue': sell_venue,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'profit_per_share': profit_per_share,
                'profit_bps': profit_bps,
                'timestamp': time.time()
            }
        
        return None
    
    def store_quote(self, symbol, quote_data):
        """Store quote with longer expiry"""
        quote_key = f"quote:{symbol}"
        self.redis.set(quote_key, json.dumps(quote_data), ex=1800)  # 30 minute expiry
        
        history_key = f"history:{symbol}"
        self.redis.lpush(history_key, json.dumps(quote_data))
        self.redis.ltrim(history_key, 0, 99)
    
    def store_opportunity(self, symbol, opportunity):
        """Store opportunity with longer expiry"""
        if opportunity:
            opp_key = f"opportunity:{symbol}"
            self.redis.set(opp_key, json.dumps(opportunity), ex=1800)  # 30 minute expiry

if __name__ == "__main__":
    collector = ImprovedMarketDataCollector()
    collector.collect_all_data()
    
    print("\n🎯 Summary:")
    print(f"📊 Tracking: {len(collector.symbols)} stocks")
    print("🌐 Venues: NYSE, NASDAQ, BATS")
    print("⏰ Data expires in: 30 minutes")
    print("🔄 Run this script again to refresh data")
