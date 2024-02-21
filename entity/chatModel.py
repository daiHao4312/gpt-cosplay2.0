# 对话模块实体类

class Chat:
    # 对话表格名称
    chatTableName = None

    # 对话id
    id = None

    # 对话角色
    roles = None

    # 对话内容
    contents = None

    def __init__(self, chatTableName, roles, contents):
        self.chatTableName = chatTableName
        self.roles = roles
        self.contents = contents
