import time
import json
import redis
import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class Trade:
    id: str
    symbol: str
    strategy: str
    profit: float
    timestamp: float
    status: str

class PaperTradingEngine:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.total_pnl = 0.0
        self.trades_executed = 0
        self.success_rate = 0.95  # 95% success rate
        print("✅ Paper Trading Engine initialized")
    
    def execute_opportunity(self, opportunity):
        """Execute an arbitrage opportunity (simulated)"""
        try:
            trade_id = f"trade_{int(time.time() * 1000)}"
            

            success = random.random() < self.success_rate
            
            if success:

                slippage = random.uniform(0.001, 0.003)
                actual_profit = opportunity['profit_per_share'] - slippage
                
                trade = Trade(
                    id=trade_id,
                    symbol=opportunity['symbol'],
                    strategy=f"{opportunity['buy_venue']} → {opportunity['sell_venue']}",
                    profit=actual_profit,
                    timestamp=time.time(),
                    status="SUCCESS"
                )
                
                self.total_pnl += actual_profit
                self.trades_executed += 1
                
                print(f"✅ EXECUTED: {trade.symbol} | Profit: ${actual_profit:.3f}")
                
            else:
                trade = Trade(
                    id=trade_id,
                    symbol=opportunity['symbol'],
                    strategy=f"{opportunity['buy_venue']} → {opportunity['sell_venue']}",
                    profit=0.0,
                    timestamp=time.time(),
                    status="FAILED"
                )
                print(f"❌ FAILED: {trade.symbol} | Execution failed")
            

            self.store_trade(trade)
            return trade
            
        except Exception as e:
            print(f"❌ Error executing trade: {e}")
            return None
    
    def store_trade(self, trade):
        """Store trade in Redis"""
        trade_data = {
            'id': trade.id,
            'symbol': trade.symbol,
            'strategy': trade.strategy,
            'profit': trade.profit,
            'timestamp': trade.timestamp,
            'status': trade.status
        }
        

        self.redis.lpush('executed_trades', json.dumps(trade_data))
        self.redis.ltrim('executed_trades', 0, 99)  # Keep last 100 trades
        

        performance = {
            'total_pnl': self.total_pnl,
            'trades_executed': self.trades_executed,
            'success_rate': (self.trades_executed - self.get_failed_trades()) / max(1, self.trades_executed),
            'last_updated': time.time()
        }
        
        self.redis.hset('trading_performance', mapping=performance)
    
    def get_failed_trades(self):
        """Count failed trades"""
        trades_data = self.redis.lrange('executed_trades', 0, -1)
        failed_count = 0
        
        for trade_data in trades_data:
            trade = json.loads(trade_data)
            if trade['status'] == 'FAILED':
                failed_count += 1
        
        return failed_count
    
    def auto_execute_best_opportunities(self, min_profit_bps=20):
        """Automatically execute the best opportunities"""
        print(f"🎯 Scanning for opportunities > {min_profit_bps} bps...")

        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'CRM']
        
        executed_count = 0
        
        for symbol in symbols:
            opp_key = f"opportunity:{symbol}"
            opp_data = self.redis.get(opp_key)
            
            if opp_data:
                opportunity = json.loads(opp_data)
                

                if opportunity['profit_bps'] > min_profit_bps:
                    trade = self.execute_opportunity(opportunity)
                    if trade and trade.status == "SUCCESS":
                        executed_count += 1
                    
                    time.sleep(0.5)  
        
        print(f"\n📊 Execution Summary:")
        print(f"✅ Trades executed: {executed_count}")
        print(f"💰 Total P&L: ${self.total_pnl:.3f}")
        print(f"📈 Success rate: {((self.trades_executed - self.get_failed_trades()) / max(1, self.trades_executed)) * 100:.1f}%")
        
        return executed_count

if __name__ == "__main__":
    engine = PaperTradingEngine()
    
    print("🚀 Starting automated paper trading...")
    print("Will execute opportunities with >20 basis points profit")
    
    executed = engine.auto_execute_best_opportunities(min_profit_bps=20)
    
    if executed > 0:
        print(f"\n🎉 Successfully executed {executed} trades!")
        print("Check the dashboard to see trading performance!")
    else:
        print("\n📊 No high-profit opportunities available right now")
        print("Try lowering the minimum profit threshold or wait for better opportunities")
