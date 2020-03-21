import time
import utils.tools as Tools


class Bar(object):
    def __init__(self, total_size, title, block_size=30, signal='#'):
        self.total_size = total_size    # 总进度数
        self.block_size = block_size        # 进度条格子数（默认为 50）
        self.process_size = min(total_size, self.block_size) # 设置进度条长度最大值
        self.title = title  # 进度条前的名称
        self.process_now = 0  # 当前进度
        self.signal = signal
        self.start_time = time.time()  # 起始时间

    def __cost_time(self):
        cost = time.time() - self.start_time
        return Tools.seconds_format(cost)

    # 剩余时间 = 总进度 / 当前速率 - 当前用时，当前速率 = 当前进度 / 当前用时
    def __left_time(self):
        time_now = (time.time() - self.start_time)
        if time_now == 0:
            return '-:-:-'
        speed = self.process_now / time_now
        left_seconds = int(self.total_size / speed - time_now)
        return Tools.seconds_format(left_seconds)

    # 用户直接传入当前进度，注：i从0开始
    def update(self, i, add=1):
        i += add
        self.process_now = i
        process = '\r \033[0;31;49m' + self.title + ' %d of %d %2d%% [%s%s]  Cost: ' + self.__cost_time() + ' Left: ' + self.__left_time() + '\033[0m'
        step = int(i / self.total_size * self.block_size)
        a = self.signal * step
        b = ' ' * (self.process_size - step)
        c = (i / self.total_size) * 100
        print(process % (i, self.total_size, c, a, b), end='')

    # 当你不方便取到当前进度时，直接将当前进度+1
    def update_once(self):
        self.update(self.process_now)

    # 当你不方便取到当前进度时，直接将当前进度 + multi
    def update_multiple(self, multi):
        self.update(self.process_now, add=multi)


if __name__ == '__main__':
    total = 1000
    bar = Bar(total, 'Progress:')
    for i in range(total):
        bar.update(i)
        time.sleep(0.01)
