
"""
Complete Cross-Venue Latency Arbitrage System
This script runs the entire system end-to-end
"""

import time
import subprocess
import sys

def run_command(command, description):
    """Run a command and show progress"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def main():
    print("=" * 60)
    print("🎯 CROSS-VENUE LATENCY ARBITRAGE SYSTEM")
    print("🏦 Ready to pitch to Goldman Sachs, Jump Trading, etc.")
    print("=" * 60)
    print()
    

    print("PHASE 1: Data Collection")
    success1 = run_command("python improved_collector.py", "Collecting market data for 20 stocks")
    time.sleep(2)
    

    print("\nPHASE 2: Latency Monitoring")
    success2 = run_command("python test_latency.py", "Measuring venue latencies")
    time.sleep(1)
    

    print("\nPHASE 3: Paper Trading Execution")
    success3 = run_command("python paper_trading.py", "Executing profitable arbitrage trades")
    time.sleep(1)
    

    print("\n" + "=" * 60)
    print("📊 SYSTEM STATUS SUMMARY")
    print("=" * 60)
    
    print(f"📈 Market Data Collection: {'✅ SUCCESS' if success1 else '❌ FAILED'}")
    print(f"🌐 Latency Monitoring: {'✅ SUCCESS' if success2 else '❌ FAILED'}")
    print(f"💰 Paper Trading: {'✅ SUCCESS' if success3 else '❌ FAILED'}")
    
    if success1 and success2 and success3:
        print("\n🎉 COMPLETE SYSTEM OPERATIONAL!")
        print("🚀 Dashboard available at: http://localhost:8004")
        print("💎 System ready for institutional presentation!")
        
        print("\n📋 WHAT YOU'VE BUILT:")
        print("• Real-time market data collection (20+ stocks)")
        print("• Multi-venue latency monitoring (NYSE, NASDAQ, BATS)")
        print("• ML-powered arbitrage opportunity detection")
        print("• Automated paper trading execution")
        print("• Professional web dashboard")
        print("• Complete performance analytics")
        
        print("\n🏆 BUSINESS VALUE:")
        print("• Identifies profitable trading opportunities in real-time")
        print("• Monitors execution costs via latency tracking")
        print("• Automates high-frequency trading strategies")
        print("• Provides institutional-grade performance metrics")
        print("• Scalable to thousands of stocks and venues")
        
        return True
    else:
        print("\n⚠️  Some components failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
