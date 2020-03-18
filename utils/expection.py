class MyException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info

# 请求失败
class RequestFailException(MyException):
    def __init__(self, error_info):
        super().__init__(error_info)

# 请求的粉丝页没有粉丝，到最后一页
class NoFansException(MyException):
    def __init__(self, error_info):
        super().__init__(error_info)


if __name__ == '__main__':
    r = RequestFailException('请求失败')
    n = NoFansException('没有粉丝了')
    try:
        raise r
    except RequestFailException as e:
        print(e)

    try:
        raise n
    except NoFansException as e:
        print(e)

