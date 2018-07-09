#coding=utf-8
import scrapy
import re


global START_YEAR, END_YEAR, CSV_PATH_PLAYER_RANK
START_YEAR = 2015
END_YEAR = 2017
CSV_PATH_PLAYER_RANK = '/Users/llx/PyProjects/BettingDog/Data/Game Data/西甲球员排行.csv'


class BettingDog2_Spider(scrapy.Spider):
	name = 'betting_dog2'

	# 生成爬取路径
	start_urls = []

	for yymm_start in range(START_YEAR, END_YEAR + 1):
		yymm_end = yymm_start + 1
		url = 'http://zq.win007.com/cn/TechList/%s-%s/31.html' % (yymm_start, yymm_end)
		print(url)
		start_urls.append(url)


	def parse(self, response):
		baseUrl = 'http://zq.win007.com'

		# 得到js data路径
		# /jsData/Count/2017-2018/playerTech_31.js
		js_path = re.search(r'src="(?P<js>/jsData/Count/.*?)"\>', response.body.decode('utf-8')).groupdict()
		js_data = js_path['js']
		print('*'*60)
		print(js_path)
		print(js_data)
		print(baseUrl+js_data)

		# -- 传当前赛季到crawl_info()
		season = js_data.split('/')[3]

		print('Now crawling season %s ... ' % season)

		# 反爬虫处理机制
		#seconds = random.randint(3, 10)
		#for i in range(1, seconds+1):
		#	print('%s seconds to crawl ...' % (seconds+1 - i))
		#	time.sleep(1)

		request  = scrapy.Request(baseUrl+js_data, callback=self.crawl_info, meta = {'season':season})
		yield request

	# 解析js data
	def crawl_info(self, response):
		season = response.meta['season'] # 赛季
		print('Crawling Data of Season: ' + season)

		techCout_Player = {}
		crawl_info = re.findall(r'(techCout_Player.*?};)', response.body.decode('utf-8'))[0].replace('techCout_Player', 'techCout_Player["a"]')

		exec(crawl_info) # exec直接生成techCout_Player

		# 得到球员id
		players = {}
		players = techCout_Player['a']['Pid']
		#print(players)

		# 得到球员数据
		values_total = {}
		values_total = techCout_Player['a']['Total']['value']

		all_players_list = []

		#print(values_total)

		for player_value in values_total:
			player_id = player_value[0]
			player_name = players.get(str(player_id))[0][0] #球员
			game_num = player_value[1] #出场
			sub_num = player_value[2] #替补
			game_time = player_value[3] #出场时间
			goals = player_value[4] #运动战进球
			penalty = player_value[5] #点球
			total_goals = goals + penalty #总进球
			shoots = player_value[6] #射门
			on_target = player_value[7] #射正
			vialated_num = player_value[8] #被侵犯次数
			mvp_num = player_value[9] #最佳
			score = player_value[10] #评分

			player_list = []
			player_list.append(str(season))
			player_list.append(str(player_id))
			player_list.append(str(player_name))
			player_list.append(str(game_num))
			player_list.append(str(sub_num))
			player_list.append(str(game_time))
			player_list.append(str(goals))
			player_list.append(str(penalty))
			player_list.append(str(total_goals))
			player_list.append(str(shoots))
			player_list.append(str(on_target))
			player_list.append(str(vialated_num))
			player_list.append(str(mvp_num))
			player_list.append(str(score))

			if player_list[0] in ('梅西', 'C.罗纳尔多'):
				print(player_list)

			all_players_list.append(player_list)


		with open(CSV_PATH_PLAYER_RANK,'ab+') as f:
			title = ['赛季','球员ID','球员','出场','替补','出场总时长','运动战进球','点球','总进球数','射门','射正','被侵犯次数', '最佳球员次数','评分']
			f.write(bytes(",".join(title)+"\n",encoding="utf-8"))
			for player_list in all_players_list:
				f.write(bytes(",".join(player_list) + "\n",encoding="utf-8"))