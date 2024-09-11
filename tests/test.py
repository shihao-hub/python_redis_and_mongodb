from datetime import datetime
import pytz

# 原始日期时间字符串
date_str = '2024-07-12T00:58:04.000+0800'

# 使用 strptime 解析字符串
dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')

# 输出结果
print("转换后的 datetime 对象:", dt.strftime("%Y-%m-%d %H:%M:%S"))

# 如果需要转换为其他时区，可以使用 pytz
# 例如，将其转换为 UTC
dt_utc = dt.astimezone(pytz.utc)
print("转换为 UTC 的 datetime 对象:", dt_utc)
