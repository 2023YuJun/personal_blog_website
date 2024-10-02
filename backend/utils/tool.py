import socket
import requests
import random
import string


def random_nickname(prefix="", random_length=8):
    # 随机生成昵称
    name = prefix
    for _ in range(random_length):
        # 随机选择字母或数字
        char = random.choice(string.ascii_letters + string.digits)
        name += char
    return name


def get_ip_address():
    try:
        # 获取本机IP地址
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        return str(e)


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        if response.status_code == 200:
            return response.text
    except Exception as e:
        return str(e)
    return ""


def get_current_type_name(type):
    if type == 1:
        return "文章"
    elif type == 2:
        return "说说"
    elif type == 3:
        return "留言"
    return 0


def is_valid_url(url):
    return url.startswith('http') or url.startswith('https')


# 示例调用
if __name__ == "__main__":
    print(random_nickname("user_"))
    print(get_ip_address())
    print(get_public_ip())
