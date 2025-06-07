import redis
import time

def test_redis():
    try:
        # Connect to Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        # Test connection
        r.ping()
        print("✅ Redis connected!")
        
        # Store some test data
        r.set('test_key', f'Hello from Python at {time.time()}')
        
        # Retrieve data
        value = r.get('test_key')
        print(f"✅ Stored and retrieved: {value.decode()}")
        
        # Clean up
        r.delete('test_key')
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_redis()
