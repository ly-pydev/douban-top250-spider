import requests

url = 'https://movie.douban.com/top250?'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
pages = int(input('请输入页码：'))
for i in range(pages):
    params = {
        'start':i*25
    }
    response = requests.get(url, headers=headers, params=params)
    with open(f'{i+1}.html','w',encoding='utf-8') as f:
        f.write(response.text)
