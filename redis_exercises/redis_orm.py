from redisorm import Model

import redis

conn = redis.StrictRedis()


# 2024-09-07：此处 gpt 的回答都有问题，之后再说吧！

# 定义模型
class User(Model):
    __database__ = conn
    username: str
    email: str

    def add_to_list(self, value):
        this = self
        conn.rpush('user_list', value)  # 将值添加到列表

    def get_list(self):
        this = self
        return conn.lrange('user_list', 0, -1)  # 获取列表的所有值

    def add_to_set(self, value):
        this = self
        conn.sadd('user_set', value)  # 添加到集合

    def get_set(self):
        this = self
        return conn.smembers('user_set')  # 获取集合的所有成员

    def add_to_zset(self, score, value):
        this = self
        conn.zadd('user_zset', {value: score})  # 添加到有序集合

    def get_zset(self):
        this = self
        return conn.zrange('user_zset', 0, -1)  # 获取有序集合的所有成员

    def save_to_hash(self):
        this = self
        conn.hset('user_hash', self.username, self.email)  # 将用户信息保存到哈希

    def get_from_hash(self):
        this = self
        return conn.hgetall('user_hash')  # 获取哈希中的所有字段


if __name__ == '__main__':
    # 创建和保存用户
    user = User(username='john_doe', email='john@example.com')
    user.save()

    # 获取用户
    retrieved_user = User.get(user.id)
    print(retrieved_user.username)  # 输出: john_doe
