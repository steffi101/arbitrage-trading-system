from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis
import json
import uvicorn

app = FastAPI(title="Cross-Venue Arbitrage System")
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/", response_class=HTMLResponse)
async def minimal_dashboard():
    # Get ALL symbols
    all_symbols = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
        'META', 'NVDA', 'NFLX', 'AMD', 'CRM',
        'ORCL', 'ADBE', 'PYPL', 'INTC', 'UBER',
        'SPY', 'QQQ', 'IWM', 'GLD', 'TLT'
    ]
    
    # Get market data
    market_data = []
    for symbol in all_symbols:
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
            latency_data.append({'venue': venue, 'latency': data['latency_ms']})
    
    # Get opportunities
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
        <title>Cross-Venue Arbitrage System</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: #0a0a0a;
                color: #ffffff;
                line-height: 1.5;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 24px;
            }}
            
            h1 {{
                font-size: 2rem;
                font-weight: 600;
                text-align: center;
                color: #ffffff;
                margin-bottom: 32px;
                letter-spacing: -0.5px;
            }}
            
            .card {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 24px;
                backdrop-filter: blur(10px);
                transition: all 0.2s ease;
            }}
            
            .card:hover {{
                border-color: rgba(255, 255, 255, 0.2);
                background: rgba(255, 255, 255, 0.08);
            }}
            
            h2 {{
                font-size: 1.25rem;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 20px;
                opacity: 0.9;
            }}
            
            .profit-summary {{
                text-align: center;
                padding: 32px;
                background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(16, 185, 129, 0.1));
                border: 1px solid rgba(34, 197, 94, 0.3);
                border-radius: 16px;
                margin-bottom: 32px;
            }}
            
            .profit-amount {{
                font-size: 2.5rem;
                font-weight: 700;
                color: #22c55e;
                margin-bottom: 8px;
            }}
            
            .profit-subtitle {{
                font-size: 1rem;
                color: rgba(255, 255, 255, 0.7);
            }}
            
            .grid-2 {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 24px;
            }}
            
            .grid-3 {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 16px;
            }}
            
            .grid-4 {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 16px;
            }}
            
            .grid-opportunities {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 16px;
            }}
            
            .stock-item {{
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 16px;
                text-align: center;
                transition: all 0.2s ease;
            }}
            
            .stock-item:hover {{
                border-color: rgba(59, 130, 246, 0.4);
                background: rgba(59, 130, 246, 0.05);
            }}
            
            .stock-symbol {{
                font-size: 0.875rem;
                font-weight: 600;
                color: #3b82f6;
                margin-bottom: 4px;
            }}
            
            .stock-price {{
                font-size: 1.125rem;
                font-weight: 600;
                color: #ffffff;
            }}
            
            .venue-item {{
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                transition: all 0.2s ease;
            }}
            
            .venue-item:hover {{
                border-color: rgba(249, 115, 22, 0.4);
                background: rgba(249, 115, 22, 0.05);
            }}
            
            .venue-name {{
                font-size: 0.875rem;
                font-weight: 600;
                color: #f97316;
                margin-bottom: 8px;
            }}
            
            .venue-latency {{
                font-size: 1.5rem;
                font-weight: 700;
                color: #ffffff;
            }}
            
            .opportunity-item {{
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 20px;
                transition: all 0.2s ease;
            }}
            
            .opportunity-item:hover {{
                border-color: rgba(34, 197, 94, 0.4);
                background: rgba(34, 197, 94, 0.05);
            }}
            
            .opp-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }}
            
            .opp-symbol {{
                font-size: 1.125rem;
                font-weight: 600;
                color: #ffffff;
            }}
            
            .opp-bps {{
                font-size: 0.875rem;
                font-weight: 600;
                color: #22c55e;
                background: rgba(34, 197, 94, 0.1);
                padding: 4px 8px;
                border-radius: 4px;
            }}
            
            .opp-strategy {{
                font-size: 0.875rem;
                color: rgba(255, 255, 255, 0.7);
                margin-bottom: 8px;
                line-height: 1.4;
            }}
            
            .opp-profit {{
                font-size: 1rem;
                font-weight: 600;
                color: #22c55e;
            }}
            
            .status-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
            }}
            
            .status-item {{
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 20px;
                text-align: center;
            }}
            
            .status-title {{
                font-size: 0.875rem;
                font-weight: 500;
                color: rgba(255, 255, 255, 0.7);
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .status-value {{
                font-size: 1.25rem;
                font-weight: 600;
                color: #22c55e;
                margin-bottom: 4px;
            }}
            
            .status-detail {{
                font-size: 0.75rem;
                color: rgba(255, 255, 255, 0.5);
            }}
            
            .no-data {{
                text-align: center;
                color: rgba(255, 255, 255, 0.5);
                font-style: italic;
                padding: 20px;
            }}
            
            @media (max-width: 768px) {{
                .grid-2 {{ grid-template-columns: 1fr; }}
                .grid-3 {{ grid-template-columns: 1fr; }}
                .grid-4 {{ grid-template-columns: repeat(2, 1fr); }}
                .container {{ padding: 16px; }}
                h1 {{ font-size: 1.75rem; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Cross-Venue Arbitrage System</h1>
            
            <div class="profit-summary">
                <div class="profit-amount">${total_profit:.2f}</div>
                <div class="profit-subtitle">Total profit potential across {len(opportunities)} opportunities</div>
            </div>
            
            <div class="grid-2">
                <div class="card">
                    <h2>Market Data</h2>
                    <div class="grid-4">
                        {' '.join([f'''
                        <div class="stock-item">
                            <div class="stock-symbol">{quote["symbol"]}</div>
                            <div class="stock-price">${quote["price"]}</div>
                        </div>
                        ''' for quote in market_data])}
                    </div>
                    {f'<div class="no-data">No market data available</div>' if not market_data else ''}
                </div>
                
                <div class="card">
                    <h2>Venue Latency</h2>
                    <div class="grid-3">
                        {' '.join([f'''
                        <div class="venue-item">
                            <div class="venue-name">{data["venue"]}</div>
                            <div class="venue-latency">{data["latency"]:.1f}ms</div>
                        </div>
                        ''' for data in latency_data])}
                    </div>
                    {f'<div class="no-data">No latency data available - run test_latency.py to populate</div>' if not latency_data else ''}
                </div>
            </div>
            
            <div class="card">
                <h2>Arbitrage Opportunities</h2>
                <div class="grid-opportunities">
                    {' '.join([f'''
                    <div class="opportunity-item">
                        <div class="opp-header">
                            <div class="opp-symbol">{opp["symbol"]}</div>
                            <div class="opp-bps">{opp["profit_bps"]:.1f} bps</div>
                        </div>
                        <div class="opp-strategy">Buy {opp["buy_venue"]} at ${opp["buy_price"]} → Sell {opp["sell_venue"]} at ${opp["sell_price"]}</div>
                        <div class="opp-profit">Profit: ${opp["profit_per_share"]:.3f} per share</div>
                    </div>
                    ''' for opp in opportunities])}
                </div>
                {f'<div class="no-data">No opportunities available</div>' if not opportunities else ''}
            </div>
            
            <div class="card">
                <h2>System Status</h2>
                <div class="status-grid">
                    <div class="status-item">
                        <div class="status-title">Market Data</div>
                        <div class="status-value">{'LIVE' if market_data else 'OFFLINE'}</div>
                        <div class="status-detail">{len(market_data)} stocks tracked</div>
                    </div>
                    <div class="status-item">
                        <div class="status-title">Latency Monitor</div>
                        <div class="status-value">{'ACTIVE' if latency_data else 'OFFLINE'}</div>
                        <div class="status-detail">{len(latency_data)} venues monitored</div>
                    </div>
                    <div class="status-item">
                        <div class="status-title">Arbitrage Engine</div>
                        <div class="status-value">{'SCANNING' if opportunities else 'IDLE'}</div>
                        <div class="status-detail">Real-time analysis</div>
                    </div>
                    <div class="status-item">
                        <div class="status-title">Opportunities</div>
                        <div class="status-value">{len(opportunities)} FOUND</div>
                        <div class="status-detail">${total_profit:.2f} total profit</div>
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
    print("Starting dashboard at http://localhost:8003")
    uvicorn.run(app, host="0.0.0.0", port=8003)
