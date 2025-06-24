from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis
import json
import uvicorn

app = FastAPI(title="Enhanced Cross-Venue Latency Arbitrage Dashboard")
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/", response_class=HTMLResponse)
async def enhanced_dashboard():

    all_symbols = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
        'META', 'NVDA', 'NFLX', 'AMD', 'CRM',
        'ORCL', 'ADBE', 'PYPL', 'INTC', 'UBER',
        'SPY', 'QQQ', 'IWM', 'GLD', 'TLT'
    ]
    

    market_data = []
    for symbol in all_symbols:
        quote_key = f"quote:{symbol}"
        quote_data = redis_client.get(quote_key)
        if quote_data:
            quote = json.loads(quote_data)
            market_data.append(quote)
    

    latency_data = []
    venues = ['NYSE', 'NASDAQ', 'BATS']
    for venue in venues:
        latency_key = f"latency:{venue}"
        latency_info = redis_client.get(latency_key)
        if latency_info:
            data = json.loads(latency_info)
            latency_data.append({'venue': venue, 'latency': data['latency_ms']})
    

    opportunities = []
    for symbol in all_symbols:
        opp_key = f"opportunity:{symbol}"
        opp_data = redis_client.get(opp_key)
        if opp_data:
            opportunities.append(json.loads(opp_data))
    

    opportunities.sort(key=lambda x: x['profit_bps'], reverse=True)
    

    total_profit = sum(opp['profit_per_share'] for opp in opportunities)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Enhanced Cross-Venue Latency Arbitrage System</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
            .container {{ max-width: 1400px; margin: 0 auto; }}
            .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .profit {{ color: #28a745; font-weight: bold; }}
            .latency {{ color: #007bff; }}
            h1 {{ color: #333; text-align: center; background: linear-gradient(45deg, #007bff, #28a745); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            h2 {{ color: #666; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .opportunity {{ border-left: 4px solid #28a745; margin: 5px 0; }}
            .stats {{ display: flex; gap: 10px; flex-wrap: wrap; }}
            .stat {{ flex: 1; text-align: center; min-width: 100px; background: #f8f9fa; padding: 10px; border-radius: 5px; }}
            .market-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }}
            .opportunities-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 10px; }}
            .total-profit {{ font-size: 24px; color: #28a745; font-weight: bold; text-align: center; padding: 20px; background: linear-gradient(45deg, #e8f5e8, #f0f8f0); border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Enhanced Cross-Venue Latency Arbitrage System</h1>
            
            <div class="card total-profit">
                💰 Total Arbitrage Profit Potential: ${total_profit:.2f} per share across {len(opportunities)} opportunities
            </div>
            
            <div class="card">
                <h2>📊 Live Market Data ({len(market_data)} Stocks)</h2>
                <div class="market-grid">
                    {' '.join([f'<div class="stat"><h4>{quote["symbol"]}</h4><div>${quote["price"]}</div></div>' for quote in market_data[:16]])}
                </div>
            </div>
            
            <div class="card">
                <h2>🌐 Venue Latency Performance</h2>
                <div class="stats">
                    {' '.join([f'<div class="stat"><h3>{data["venue"]}</h3><div class="latency">{data["latency"]:.1f}ms</div></div>' for data in latency_data])}
                </div>
            </div>
            
            <div class="card">
                <h2>💰 Live Arbitrage Opportunities ({len(opportunities)} Found)</h2>
                <div class="opportunities-grid">
                    {' '.join([f'''
                    <div class="card opportunity">
                        <h4>{opp["symbol"]} - {opp["profit_bps"]:.1f} bps</h4>
                        <p><strong>Strategy:</strong> Buy {opp["buy_venue"]} at ${opp["buy_price"]} → Sell {opp["sell_venue"]} at ${opp["sell_price"]}</p>
                        <p><strong>Profit:</strong> <span class="profit">${opp["profit_per_share"]:.3f} per share</span></p>
                    </div>
                    ''' for opp in opportunities[:12]])}
                </div>
                {f'<p style="text-align: center; color: #666;">Showing top 12 of {len(opportunities)} opportunities</p>' if len(opportunities) > 12 else ''}
            </div>
            
            <div class="card">
                <h2>📈 Enhanced System Status</h2>
                <div class="stats">
                    <div class="stat">
                        <h4>Market Data</h4>
                        <div style="color: #28a745;">✅ LIVE</div>
                        <small>{len(market_data)} stocks tracked</small>
                    </div>
                    <div class="stat">
                        <h4>Latency Monitor</h4>
                        <div style="color: #28a745;">✅ ACTIVE</div>
                        <small>3 venues monitored</small>
                    </div>
                    <div class="stat">
                        <h4>Arbitrage Detection</h4>
                        <div style="color: #28a745;">✅ SCANNING</div>
                        <small>Real-time analysis</small>
                    </div>
                    <div class="stat">
                        <h4>Opportunities</h4>
                        <div style="color: #28a745;">✅ {len(opportunities)} FOUND</div>
                        <small>${total_profit:.2f} total profit</small>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // Auto-refresh every 15 seconds
            setTimeout(() => window.location.reload(), 15000);
        </script>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    print("🌐 Starting Enhanced Dashboard at http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
