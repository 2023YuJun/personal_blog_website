ERRORCODE = {
    "USER": "100001",  # 用户错误码
    "AUTH": "100002",  # 用户权限不足
    "TAG": "100003",
    "CATEGORY": "100004",
    "ARTICLE": "100005",
    "UPLOAD": "100006",
    "CONFIG": "100007",
    "STATISTIC": "100008",
    "PHOTOALBUM": "100009",
    "PHOTO": "100010",
    "TALK": "100011",  # 说说
    "MESSAGE": "100012",  # 留言
    "RECOMMEND": "100012",  # 推荐
    "HEADER": "100013",  # 背景图
    "LINKS": "100014",  # 友链
    "COMMENT": "100015",  # 评论
    "AUTHTOKEN": "100016",  # 用户登录过期
    "NOTIFY": "100017",  # 消息推送
    "LIKE": "100018",  # 点赞
    "CHAT": "100019",  # 聊天
    "TIPS": "111111",  # 提示
}


def result(message, result):
    """公共返回结果方法"""
    return {
        "code": 0,
        "message": message,
        "result": result,
    }


def tips_result(message):
    """公共返回提示方法"""
    return {
        "code": 100,
        "message": message,
    }


def throw_error(code, message):
    """公共抛出错误方法"""
    return {
        "code": code,
        "message": message,
    }
