from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import redis
import json
import uvicorn

app = FastAPI(title="Cross-Venue Latency Arbitrage Dashboard")

# Initialize Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard page"""
    
    # Get market data
    market_data = []
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    
    for symbol in symbols:
        quote_key = f"quote:{symbol}"
        quote_data = redis_client.get(quote_key)
        
        if quote_data:
            quote = json.loads(quote_data)
            market_data.append(quote)
    
    # Get latency data
    latency_data = []
    venues = ['NYSE', 'NASDAQ', 'BATS']
    
    for venue in venues:
        latency_key = f"latency:{venue}"
        latency_info = redis_client.get(latency_key)
        
        if latency_info:
            data = json.loads(latency_info)
            latency_data.append({
                'venue': venue,
                'latency': data['latency_ms']
            })
    
    # Get arbitrage opportunities
    opportunities = []
    for symbol in symbols:
        opp_key = f"opportunity:{symbol}"
        opp_data = redis_client.get(opp_key)
        
        if opp_data:
            opportunities.append(json.loads(opp_data))
    
    # Sort opportunities by profit
    opportunities.sort(key=lambda x: x['profit_bps'], reverse=True)
    
    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cross-Venue Latency Arbitrage System</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .profit {{ color: #28a745; font-weight: bold; }}
            .latency {{ color: #007bff; }}
            h1 {{ color: #333; text-align: center; }}
            h2 {{ color: #666; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .opportunity {{ border-left: 4px solid #28a745; }}
            .stats {{ display: flex; gap: 20px; }}
            .stat {{ flex: 1; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Cross-Venue Latency Arbitrage System</h1>
            
            <div class="card">
                <h2>📊 Live Market Data</h2>
                <div class="stats">
                    {' '.join([f'<div class="stat"><h3>{quote["symbol"]}</h3><div>${quote["price"]}</div></div>' for quote in market_data])}
                </div>
            </div>
            
            <div class="card">
                <h2>🌐 Venue Latency Performance</h2>
                <div class="stats">
                    {' '.join([f'<div class="stat"><h3>{data["venue"]}</h3><div class="latency">{data["latency"]:.1f}ms</div></div>' for data in latency_data])}
                </div>
            </div>
            
            <div class="card">
                <h2>💰 Live Arbitrage Opportunities</h2>
                {' '.join([f'''
                <div class="card opportunity">
                    <h3>{opp["symbol"]}</h3>
                    <p><strong>Strategy:</strong> Buy {opp["buy_venue"]} at ${opp["buy_price"]} → Sell {opp["sell_venue"]} at ${opp["sell_price"]}</p>
                    <p><strong>Profit:</strong> <span class="profit">${opp["profit_per_share"]:.3f} per share ({opp["profit_bps"]:.1f} basis points)</span></p>
                </div>
                ''' for opp in opportunities])}
            </div>
            
            <div class="card">
                <h2>📈 System Status</h2>
                <p>✅ Market Data: <strong>LIVE</strong></p>
                <p>✅ Latency Monitor: <strong>ACTIVE</strong></p>
                <p>✅ Arbitrage Detection: <strong>SCANNING</strong></p>
                <p>✅ Opportunities Found: <strong>{len(opportunities)}</strong></p>
            </div>
        </div>
        
        <script>
            // Auto-refresh every 10 seconds
            setTimeout(() => window.location.reload(), 10000);
        </script>
    </body>
    </html>
    """
    
    return html

if __name__ == "__main__":
    print("🌐 Starting dashboard at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
