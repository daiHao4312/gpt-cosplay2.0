# 使用sqlite3数据库

import sqlite3

import config


# 创建数据库
def createDatabase():
    config_database_path = config.Config().database_path
    conn = sqlite3.connect(config_database_path)
    print("数据库连接成功")
    return conn




