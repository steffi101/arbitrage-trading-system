from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis
import json
import uvicorn

app = FastAPI(title="🚀 EPIC Cross-Venue Arbitrage System")
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/", response_class=HTMLResponse)
async def epic_dashboard():

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
        <title>🚀 EPIC Cross-Venue Arbitrage System</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Rajdhani', sans-serif;
                background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%);
                color: #ffffff;
                overflow-x: hidden;
                animation: backgroundShift 20s ease-in-out infinite;
            }}
            
            @keyframes backgroundShift {{
                0%, 100% {{ background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%); }}
                50% {{ background: linear-gradient(135deg, #000000 0%, #0f0f23 25%, #16213e 50%, #1a1a2e 75%, #0c0c0c 100%); }}
            }}
            
            .container {{
                max-width: 1600px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            h1 {{
                font-family: 'Orbitron', monospace;
                font-size: 3.5rem;
                font-weight: 900;
                text-align: center;
                background: linear-gradient(45deg, #00ff88, #00ccff, #ff0088, #ffaa00);
                background-size: 400% 400%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradientShift 3s ease-in-out infinite;
                text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
                margin-bottom: 30px;
            }}
            
            @keyframes gradientShift {{
                0%, 100% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
            }}
            
            .cyber-card {{
                background: rgba(0, 255, 136, 0.1);
                border: 2px solid #00ff88;
                border-radius: 15px;
                padding: 25px;
                margin: 20px 0;
                box-shadow: 0 0 30px rgba(0, 255, 136, 0.3), inset 0 0 20px rgba(0, 255, 136, 0.1);
                backdrop-filter: blur(10px);
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
            }}
            
            .cyber-card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 20px 50px rgba(0, 255, 136, 0.4), inset 0 0 30px rgba(0, 255, 136, 0.2);
                border-color: #00ccff;
            }}
            
            .cyber-card::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(0, 255, 136, 0.1), transparent);
                animation: scan 4s linear infinite;
            }}
            
            @keyframes scan {{
                0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
                100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
            }}
            
            .profit-banner {{
                font-family: 'Orbitron', monospace;
                font-size: 2.5rem;
                font-weight: 700;
                text-align: center;
                background: linear-gradient(45deg, #00ff88, #ffaa00);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                padding: 30px;
                border-radius: 20px;
                background-color: rgba(0, 255, 136, 0.1);
                border: 3px solid #00ff88;
                box-shadow: 0 0 50px rgba(0, 255, 136, 0.5);
                animation: pulse 2s ease-in-out infinite;
                margin-bottom: 30px;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
            }}
            
            h2 {{
                font-family: 'Orbitron', monospace;
                font-size: 1.8rem;
                color: #00ff88;
                text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
                margin-bottom: 20px;
                position: relative;
                z-index: 2;
            }}
            
            .market-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }}
            
            .stock-card {{
                background: linear-gradient(145deg, rgba(0, 204, 255, 0.1), rgba(255, 0, 136, 0.1));
                border: 1px solid #00ccff;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                transition: all 0.3s ease;
                box-shadow: 0 5px 20px rgba(0, 204, 255, 0.2);
                position: relative;
                overflow: hidden;
            }}
            
            .stock-card:hover {{
                transform: scale(1.1) rotateY(5deg);
                border-color: #ff0088;
                box-shadow: 0 15px 40px rgba(255, 0, 136, 0.4);
            }}
            
            .stock-symbol {{
                font-family: 'Orbitron', monospace;
                font-size: 1.4rem;
                font-weight: 700;
                color: #00ccff;
                margin-bottom: 10px;
            }}
            
            .stock-price {{
                font-size: 1.6rem;
                font-weight: 600;
                color: #00ff88;
                text-shadow: 0 0 10px rgba(0, 255, 136, 0.6);
            }}
            
            .latency-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin: 20px 0;
            }}
            
            .venue-card {{
                background: linear-gradient(145deg, rgba(255, 170, 0, 0.1), rgba(0, 255, 136, 0.1));
                border: 2px solid #ffaa00;
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                transition: all 0.3s ease;
                position: relative;
            }}
            
            .venue-card:hover {{
                transform: rotateX(10deg);
                box-shadow: 0 20px 40px rgba(255, 170, 0, 0.3);
            }}
            
            .venue-name {{
                font-family: 'Orbitron', monospace;
                font-size: 1.5rem;
                font-weight: 700;
                color: #ffaa00;
                margin-bottom: 10px;
            }}
            
            .venue-latency {{
                font-size: 2rem;
                font-weight: 700;
                color: #00ccff;
                text-shadow: 0 0 15px rgba(0, 204, 255, 0.8);
            }}
            
            .opportunities-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            
            .opportunity-card {{
                background: linear-gradient(145deg, rgba(255, 0, 136, 0.1), rgba(0, 255, 136, 0.1));
                border: 2px solid #ff0088;
                border-radius: 15px;
                padding: 20px;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            
            .opportunity-card:hover {{
                transform: translateX(10px) rotateZ(2deg);
                border-color: #00ff88;
                box-shadow: 0 15px 50px rgba(0, 255, 136, 0.4);
            }}
            
            .opp-symbol {{
                font-family: 'Orbitron', monospace;
                font-size: 1.8rem;
                font-weight: 700;
                color: #ff0088;
                margin-bottom: 10px;
            }}
            
            .opp-strategy {{
                font-size: 1.1rem;
                color: #00ccff;
                margin: 10px 0;
                line-height: 1.4;
            }}
            
            .opp-profit {{
                font-size: 1.4rem;
                font-weight: 700;
                color: #00ff88;
                text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
            }}
            
            .status-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            
            .status-card {{
                background: rgba(0, 255, 136, 0.1);
                border: 2px solid #00ff88;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                transition: all 0.3s ease;
            }}
            
            .status-card:hover {{
                transform: scale(1.05);
                box-shadow: 0 10px 30px rgba(0, 255, 136, 0.4);
            }}
            
            .status-title {{
                font-family: 'Orbitron', monospace;
                font-size: 1.2rem;
                color: #00ccff;
                margin-bottom: 10px;
            }}
            
            .status-value {{
                font-size: 1.5rem;
                font-weight: 700;
                color: #00ff88;
                margin-bottom: 5px;
            }}
            
            .status-detail {{
                font-size: 0.9rem;
                color: #ffffff;
                opacity: 0.8;
            }}
            
            .floating-particles {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: -1;
            }}
            
            .particle {{
                position: absolute;
                width: 4px;
                height: 4px;
                background: #00ff88;
                border-radius: 50%;
                animation: float 6s ease-in-out infinite;
                opacity: 0.6;
            }}
            
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px) translateX(0px); }}
                50% {{ transform: translateY(-20px) translateX(10px); }}
            }}
        </style>
    </head>
    <body>
        <div class="floating-particles">
            <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
            <div class="particle" style="left: 20%; animation-delay: 1s;"></div>
            <div class="particle" style="left: 30%; animation-delay: 2s;"></div>
            <div class="particle" style="left: 40%; animation-delay: 3s;"></div>
            <div class="particle" style="left: 50%; animation-delay: 4s;"></div>
            <div class="particle" style="left: 60%; animation-delay: 5s;"></div>
            <div class="particle" style="left: 70%; animation-delay: 2s;"></div>
            <div class="particle" style="left: 80%; animation-delay: 3s;"></div>
            <div class="particle" style="left: 90%; animation-delay: 1s;"></div>
        </div>
        
        <div class="container">
            <h1>🚀 EPIC CROSS-VENUE ARBITRAGE SYSTEM 💰</h1>
            
            <div class="profit-banner">
                💎 TOTAL PROFIT POTENTIAL: ${total_profit:.2f} 💎<br>
                🎯 {len(opportunities)} LIVE OPPORTUNITIES 🎯
            </div>
            
            <div class="cyber-card">
                <h2>📊 LIVE MARKET DATA ({len(market_data)} STOCKS)</h2>
                <div class="market-grid">
                    {' '.join([f'''
                    <div class="stock-card">
                        <div class="stock-symbol">{quote["symbol"]}</div>
                        <div class="stock-price">${quote["price"]}</div>
                    </div>
                    ''' for quote in market_data])}
                </div>
            </div>
            
            <div class="cyber-card">
                <h2>🌐 VENUE LATENCY PERFORMANCE</h2>
                <div class="latency-grid">
                    {' '.join([f'''
                    <div class="venue-card">
                        <div class="venue-name">{data["venue"]}</div>
                        <div class="venue-latency">{data["latency"]:.1f}ms</div>
                    </div>
                    ''' for data in latency_data])}
                </div>
            </div>
            
            <div class="cyber-card">
                <h2>💰 LIVE ARBITRAGE OPPORTUNITIES ({len(opportunities)} FOUND)</h2>
                <div class="opportunities-grid">
                    {' '.join([f'''
                    <div class="opportunity-card">
                        <div class="opp-symbol">{opp["symbol"]} - {opp["profit_bps"]:.1f} BPS</div>
                        <div class="opp-strategy">🎯 Buy {opp["buy_venue"]} at ${opp["buy_price"]} → Sell {opp["sell_venue"]} at ${opp["sell_price"]}</div>
                        <div class="opp-profit">💵 PROFIT: ${opp["profit_per_share"]:.3f} per share</div>
                    </div>
                    ''' for opp in opportunities])}
                </div>
            </div>
            
            <div class="cyber-card">
                <h2>📈 SYSTEM STATUS</h2>
                <div class="status-grid">
                    <div class="status-card">
                        <div class="status-title">MARKET DATA</div>
                        <div class="status-value">🟢 LIVE</div>
                        <div class="status-detail">{len(market_data)} stocks tracked</div>
                    </div>
                    <div class="status-card">
                        <div class="status-title">LATENCY MONITOR</div>
                        <div class="status-value">🟢 ACTIVE</div>
                        <div class="status-detail">3 venues monitored</div>
                    </div>
                    <div class="status-card">
                        <div class="status-title">ARBITRAGE ENGINE</div>
                        <div class="status-value">🟢 SCANNING</div>
                        <div class="status-detail">Real-time analysis</div>
                    </div>
                    <div class="status-card">
                        <div class="status-title">OPPORTUNITIES</div>
                        <div class="status-value">🟢 {len(opportunities)} FOUND</div>
                        <div class="status-detail">${total_profit:.2f} total profit</div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // Auto-refresh every 15 seconds
            setTimeout(() => window.location.reload(), 15000);
            
            // Add some interactive effects
            document.addEventListener('mousemove', (e) => {{
                const particles = document.querySelectorAll('.particle');
                particles.forEach((particle, index) => {{
                    const speed = (index + 1) * 0.01;
                    const x = e.clientX * speed;
                    const y = e.clientY * speed;
                    particle.style.transform = `translate(${{x}}px, ${{y}}px)`;
                }});
            }});
        </script>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    print("🚀 Starting EPIC Dashboard at http://localhost:8002")
    uvicorn.run(app, host="0.0.0.0", port=8002)
