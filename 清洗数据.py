from lxml import html
for i in range(1,11):
    with open(f'{i}.html','r',encoding='utf-8') as f:
        html_text = f.read()
        doc = html.fromstring(html_text)

        items = doc.xpath('//ol[@class="grid_view"]/li')

        for item in items:
            # 排名
            rank_res= item.xpath('.//div[@class="pic"]/em/text()')
            rank = rank_res[0].strip()
            # 电影名称
            title_res = item.xpath('.//span[@class="title"]/text()')
            title = title_res[0].strip().replace('\xa0','') if title_res else ''
            title1 = title_res[1].strip().replace('\xa0', '') if len(title_res)>=2 else ''
            # 别名
            other_res = item.xpath('.//span[@class="other"]/text()')
            other = other_res[0].strip().replace('\xa0', '') if other_res else ''
            # 电影详情
            bd_res = item.xpath('.//div[@class="bd"]/p/text()')
            # bd = item.xpath('.//div[@class="bd"]/p/text()')
            bd = bd_res[0].strip().replace('\xa0','') if bd_res else ''
            bd1 = bd_res[1].strip().replace('\xa0', '') if len(bd_res)>=2 else ''

            #评分

            store_res = item.xpath('.//div[@class="bd"]/div/span/text()')
            store = store_res[0].strip().replace('\xa0','') if store_res else ''
            store1 = store_res[1].strip().replace('\xa0', '') if store_res else ''

            print(f'排名 {rank} | 名称 {title}{title1}{other}')
            print(f'详情 {bd} | {bd1}')
            print(f'评分 {store} | {store1}')
            print('-'*60)
    print('='*80)