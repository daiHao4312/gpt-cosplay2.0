from entity.chatModel import Chat
from util.dbUtil import createDatabase


def createChatTable(chat: Chat):
    """
    创建对话表
    :param chat: 对话实体
    :return: 返回表的描述信息
    """

    conn = None
    try:
        conn = createDatabase()
        cursor = conn.cursor()
        sql = f'''
        create table if not exists  {chat.chatTableName}(
            id integer primary key autoincrement,
            roles varchar(20) not null,
            contents varchar(1024) not null
        )
        '''
        cursor.execute(sql)
        conn.commit()
        print("创建表成功")
        return cursor.description
    except Exception as e:
        print(e)
        print("创建表失败")
        return 1
    finally:
        conn.close()


def addChatData(chat: Chat):
    """
    插入数据
    :param chat: 对话实体
    :return: 返回执行的条数
    """

    conn = None
    try:
        conn = createDatabase()
        cursor = conn.cursor()
        cursor.execute(f'insert into {chat.chatTableName} values(NULL,"{chat.roles}","{chat.contents}")')
        conn.commit()
        print("插入数据成功")
        return cursor.rowcount
    except Exception as e:
        print(e)
        print("插入数据失败")
        return 0
    finally:
        conn.close()

def showAllTables():
    """
    查看所有表
    :return: 返回所有表的名称
    """

    conn = None
    try:
        conn = createDatabase()
        cursor = conn.cursor()
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        conn.rollback()
        print(e)
        return None
    finally:
        conn.close()

def showChatData(chatTableName: str):
    """
    查看对话数据
    :param chatTableName: 对话表名
    :return:返回查询到的对话列表（集合）
    """

    conn = None
    try:
        conn = createDatabase()
        cursor = conn.cursor()
        sql = f'select * from "{chatTableName}"'
        cursor.execute(sql)
        return cursor.fetchall()  # 返回查询到的对话列表（集合）
    except Exception as e:
        conn.rollback()
        print(e)
        return None
    finally:
        conn.close()

def deleteChatTable(chatTableName: str):
    """
    删除对话表
    :param chatTableName: 对话表名
    :return: 返回执行的条数
    """

    conn = None
    try:
        conn = createDatabase()
        cursor = conn.cursor()
        sql = f'drop table "{chatTableName}"'
        cursor.execute(sql)
        conn.commit()
        print("删除表成功")
        return cursor.rowcount
    except Exception as e:
        print(e)
        print("删除表失败")
        return 0
    finally:
        conn.close()


if __name__ == '__main__':
    chat = Chat("chat1", "user", "你好")
    # a=createChatTable(chat)
    b = addChatData(chat)
    # print(a)
    print(b)
    c = showChatData("chat")
    print(c)
    d = showAllTables()
    print(d)