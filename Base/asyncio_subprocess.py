import asyncio


async def run(cmd: str) -> None:
    """
    Shell，直接通过当前进程的Shell环境中执行命令，可以带参数
    :param cmd:
    :return:
    """
    process = await asyncio.subprocess.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if not stderr:
        print("cmd success,output is {}".format(stdout.decode()))
    else:
        print("Error,{}".format(stderr.decode()))


async def exec(cmd: str, *args) -> None:
    """
    Exec: 启动一个新进程，新进程执行名为cmd的可执行文件。args是命令的相关参数
    :param cmd:
    :param args:
    :return:
    """
    process = await asyncio.subprocess.create_subprocess_exec(
        cmd,
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    # wait subprocess execute over
    await process.wait()
    stdout, stderr = await process.communicate()
    print(stdout, stderr)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [run("sleep 2&&echo test"), exec("df")]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
