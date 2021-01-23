import os
import platform

def xitong():
	pd = platform.system()
	return pd



def lyzf_main(zt):
	if zt:
		print("=========正在关闭转发=========")
		if xitong() == "Windows":
			os.system('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters /v IPEnableRouter /D 0 /f')
			os.system('net stop remoteaccess')
			print("=========转发已关闭=========")
		if xitong() == "Linux":
			os.system("echo 0 >> /proc/sys/net/ipv4/ip_forward")
			os.system("sysctl net.ipv4.ip_forward")
			print("=========转发已关闭=========")
		return False
	else:
		print("=========正在开启转发=========")
		if xitong() == "Windows":
			os.system('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters /v IPEnableRouter /D 1 /f')
			os.system('net start remoteaccess')
			print("=========转发已开启=========")
		if xitong() == "Linux":
			os.system("echo 1 >> /proc/sys/net/ipv4/ip_forward")
			os.system("sysctl net.ipv4.ip_forward")
			print("=========转发已开启=========")
		return True
