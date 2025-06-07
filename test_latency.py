import time
import subprocess
import json
import redis

class SimpleLatencyMonitor:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.venues = {
            'NYSE': '8.8.8.8',
            'NASDAQ': '1.1.1.1', 
            'BATS': '8.8.4.4'
        }
        print("✅ Latency Monitor initialized")
    
    def measure_latency(self, venue, ip):
        try:
            result = subprocess.run(['ping', '-c', '1', ip], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'time=' in line:
                        latency_str = line.split('time=')[1].split(' ')[0]
                        return float(latency_str)
            return None
        except Exception as e:
            return None
    
    def monitor_all_venues(self):
        print("🌐 Measuring venue latencies...")
        results = {}
        
        for venue, ip in self.venues.items():
            latency = self.measure_latency(venue, ip)
            if latency:
                results[venue] = {'latency_ms': latency, 'timestamp': time.time()}
                latency_key = f"latency:{venue}"
                self.redis.set(latency_key, json.dumps(results[venue]), ex=300)
                print(f"✅ {venue}: {latency:.1f}ms")
            else:
                print(f"❌ {venue}: Failed")
        return results

if __name__ == "__main__":
    monitor = SimpleLatencyMonitor()
    monitor.monitor_all_venues()
