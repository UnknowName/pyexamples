import time
from threading import Thread


class TestThread(Thread):
    def __init__(self, command: str):
        super(TestThread, self).__init__()
        self.command = command

    def run(self) -> None:
        """
        重写run()方法，而不是start()方法。
        但主线程中调用start()方法
        :return:
        """
        print("Start TestThread")
        time.sleep(10)
        print(self.command)
        print("End TestThread")


if __name__ == '__main__':
    """
    start()主线程不等待子线程继续执行
    run()主线程等待子线程执行完成后继续
    """
    print("MainThread start")
    t = TestThread("echo")
    t.start()
    # t.run()
    print("End MainThread")
