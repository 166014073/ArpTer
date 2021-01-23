import re

wgip = "193.18.101.1"

pdip = re.findall("^\d+?\.\d+?\.\d+?\.\d+?$",wgip)
if pdip:
	print("yes!")
else:
	print("no!")