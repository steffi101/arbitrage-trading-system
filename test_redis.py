import redis
import time

def test_redis():
    try:

        r = redis.Redis(host='localhost', port=6379, db=0)
        

        r.ping()
        print("✅ Redis connected!")
        

        r.set('test_key', f'Hello from Python at {time.time()}')
        

        value = r.get('test_key')
        print(f"✅ Stored and retrieved: {value.decode()}")
        

        r.delete('test_key')
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_redis()
