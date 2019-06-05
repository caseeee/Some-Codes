# coding:utf-8

from city_code import city_data
import requests
from bs4 import BeautifulSoup

def get_weather(base_url, code):
	headers = {'User-agent':'user-agent:Mozilla/5.0 \
	(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
	resp = requests.get(base_url %code, headers=headers)
	resp.encoding = 'utf-8'
	soup = BeautifulSoup(resp.text, 'html.parser')
	temp_today = soup.find('p', class_='tem')
	try:
		max_temp = temp_today.span.string
	except AttributeError:
		max_temp = '当前无最高温度。'
	min_temp = temp_today.i.string
	weather = soup.find('p', class_='wea').string
	return max_temp, min_temp, weather


if __name__ == '__main__':
	while True:
		try:
			base_url = 'http://www.weather.com.cn/weather/%s.shtml'
			input_name = input('输入你想查寻天气的城市：\n>>>')
			if input_name == 'quit' or input_name == 'ｑｕｉｔ':
				print('感谢查询.....')
				break
			else:
				pass
			code = city_data.get(input_name)
			if code:
				try:
					g_w = get_weather(base_url, code)
					print('天气：  %s\n最高温度：  %s℃\n最低温度：  %s\n' %(g_w[2], g_w[0], g_w[1]))
				except Exception:
					print('\n......对不起，未找到您查找的城市天气。\n')
			else:
				print('\n......对不起，未找到您查找的城市天气。\n')
		except Exception:
			break