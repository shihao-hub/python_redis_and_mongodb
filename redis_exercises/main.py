import redis

conn = redis.StrictRedis()

conn.set("test:20240904:creator", "zsh")
print(conn.get("test:20240904:creator"))

