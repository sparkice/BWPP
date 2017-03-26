from urllib import parse
import http.client
import random

def send_sms(apikey, text, mobile):
	# 服务地址
	sms_host = "sms.yunpian.com"
	# 端口号
	port = 443
	# 版本号
	version = "v2"
	# 智能匹配模板短信接口的URI
	sms_send_uri = "/" + version + "/sms/single_send.json"
	params = parse.urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
	conn.request("POST", sms_send_uri, params, headers)
	response = conn.getresponse()
	response_str = response.read()
	conn.close()
	return response_str


def createPhoneCode():
	chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
	verifyCode = "".join(x)
	return verifyCode

