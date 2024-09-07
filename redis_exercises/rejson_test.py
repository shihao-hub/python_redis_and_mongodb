from rejson import Client, Path

# JSON.SET 是 RedisJSON 模块中的命令，
# 只有在安装了 RedisJSON 模块的情况下才能使用。你需要确保 Redis 服务器上安装了该模块。

# 创建 Redis JSON 客户端
rj = Client(host='localhost', port=6379, decode_responses=True)

# 设置 JSON 对象
rj.jsonset('user:1000', Path.rootPath(), {"username": "john_doe", "email": "john@example.com"})

# 获取 JSON 对象
user = rj.jsonget('user:1000')
print(user)  # 输出: {'username': 'john_doe', 'email': 'john@example.com'}
