import json
import redis
import time
import random

class SimpleArbitrageDetector:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.symbols = ['AAPL', 'MSFT', 'GOOGL']
        self.venues = ['NYSE', 'NASDAQ', 'BATS']
        print("✅ Arbitrage Detector initialized")
    
    def simulate_venue_prices(self, base_price):
        """Simulate slightly different prices across venues"""
        venue_prices = {}
        
        for venue in self.venues:
            # Add small random variation (±0.5%)
            variation = random.uniform(-0.005, 0.005)
            venue_price = base_price * (1 + variation)
            venue_prices[venue] = round(venue_price, 2)
        
        return venue_prices
    
    def find_arbitrage_opportunities(self):
        """Find arbitrage opportunities across venues"""
        print("🔍 Scanning for arbitrage opportunities...")
        opportunities = []
        
        for symbol in self.symbols:
            # Get base price from our market data
            quote_key = f"quote:{symbol}"
            quote_data = self.redis.get(quote_key)
            
            if quote_data:
                quote = json.loads(quote_data)
                base_price = quote['price']
                
                # Simulate different prices across venues
                venue_prices = self.simulate_venue_prices(base_price)
                
                # Find best buy and sell venues
                buy_venue = min(venue_prices, key=venue_prices.get)  # Lowest price
                sell_venue = max(venue_prices, key=venue_prices.get) # Highest price
                
                buy_price = venue_prices[buy_venue]
                sell_price = venue_prices[sell_venue]
                
                # Calculate profit
                profit_per_share = sell_price - buy_price
                profit_bps = (profit_per_share / buy_price) * 10000  # Basis points
                
                if profit_bps > 1:  # More than 1 basis point profit
                    opportunity = {
                        'symbol': symbol,
                        'buy_venue': buy_venue,
                        'sell_venue': sell_venue,
                        'buy_price': buy_price,
                        'sell_price': sell_price,
                        'profit_per_share': profit_per_share,
                        'profit_bps': profit_bps,
                        'timestamp': time.time()
                    }
                    
                    opportunities.append(opportunity)
                    
                    # Store in Redis
                    opp_key = f"opportunity:{symbol}"
                    self.redis.set(opp_key, json.dumps(opportunity), ex=60)
                    
                    print(f"💰 {symbol}: Buy {buy_venue} ${buy_price} → Sell {sell_venue} ${sell_price}")
                    print(f"   Profit: ${profit_per_share:.3f} ({profit_bps:.1f} bps)")
        
        return opportunities
    
    def get_best_opportunities(self):
        """Get best opportunities ranked by profit"""
        print("\n🏆 Best Arbitrage Opportunities:")
        
        opportunities = []
        for symbol in self.symbols:
            opp_key = f"opportunity:{symbol}"
            opp_data = self.redis.get(opp_key)
            
            if opp_data:
                opportunities.append(json.loads(opp_data))
        
        # Sort by profit (highest first)
        opportunities.sort(key=lambda x: x['profit_bps'], reverse=True)
        
        for i, opp in enumerate(opportunities, 1):
            print(f"#{i} {opp['symbol']}: {opp['profit_bps']:.1f} bps profit")
            print(f"    {opp['buy_venue']} → {opp['sell_venue']}")
        
        return opportunities

if __name__ == "__main__":
    detector = SimpleArbitrageDetector()
    opportunities = detector.find_arbitrage_opportunities()
    
    if opportunities:
        detector.get_best_opportunities()
    else:
        print("📊 No arbitrage opportunities found right now")
