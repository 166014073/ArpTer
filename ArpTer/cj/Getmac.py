from scapy.all import *



def GetMac(lip):
	liveHost = {}
	scanList = lip + '/24'
	print("===============开始获取===============")
	try:
		ans,unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=scanList),timeout=2)
	except Exception as e:
		print(e)
	else:
		for send,rcv in ans:
			addList = rcv.sprintf('%Ether.src%|%ARP.psrc%')    #格式化处理内容
			liveHost[addList.split('|')[1]] = addList.split('|')[0]  #将存活IP与mac地址保存至列表当中
	print("===============获取完毕===============")
	return liveHost

