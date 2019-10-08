import wmi


def main(ip: str, user: str, password: str, command: str = ""):
    path = r"C:\Users\zbx.ps1"
    conn = wmi.WMI(computer=ip, user=user, password=password)
    process_startup = conn.Win32_ProcessStartup.new()
    process_startup.ShowWindow = 1
    if not command:
        command = "powershell.exe {}".format(path)
    else:
        command = "powershell.exe {}".format(command)
    process_id, result = conn.Win32_Process.Create(
        CommandLine=command,
        ProcessStartupInformation=process_startup
    )
    if result == 0:
        print("Process started successfully: %d" % process_id)
    else:
        msg = "{} install failed\n".format("ip")
        with open("install.log", 'a') as log:
            log.write(msg)


if __name__ == '__main__':
    import time
    import json
    with open("host.txt", encoding="gbk") as f:
        hosts = json.loads(f.read())
    for host in hosts:
        for k, v in host.items():
            cmd = r"copy-item \\211.69.132.71\zabbix_agent\zbx.ps1 C:\zbx.ps1"
            main(v.get("ip"), v.get("username"), v.get("password"), "copy-item ")
            time.sleep(5)
            main(v.get("ip"), v.get("username"), v.get("password"))
            time.sleep(5)