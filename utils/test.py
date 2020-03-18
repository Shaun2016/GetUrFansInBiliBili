class A(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a)

if __name__ == '__main__':
    c1 = A(4, 2)
    c2 = A(2, 3)
    c3 = A(3, 4)
    l = [c1, c2, c3]
    l.sort(key=lambda one: one.a, reverse=True)
    for i in l:
        print(i)