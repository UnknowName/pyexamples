import redis

r = redis.Redis(host='redis-test', port=6379, db=0, password="redis.123")
r.set('foo', 'bar2')