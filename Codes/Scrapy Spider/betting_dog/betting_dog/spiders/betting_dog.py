#coding=utf-8
import scrapy
import re


global START_YEAR, END_YEAR, CSV_PATH_EVENTS, CSV_PATH_SCORE, CSV_PATH_SCORE_HOME, CSV_PATH_SCORE_AWAY
START_YEAR = 2003
END_YEAR = 2017
CSV_PATH_EVENTS = '/Users/llx/PyProjects/BettingDog/Data/Game Data/西甲比赛明细.csv'
CSV_PATH_SCORE = '/Users/llx/PyProjects/BettingDog/Data/Game Data/西甲总积分榜.csv'
CSV_PATH_SCORE_HOME = '/Users/llx/PyProjects/BettingDog/Data/Game Data/西甲主场积分榜.csv'
CSV_PATH_SCORE_AWAY = '/Users/llx/PyProjects/BettingDog/Data/Game Data/西甲客场积分榜.csv'


class BettingDogSpider(scrapy.Spider):
	name = 'betting_dog'

	# 生成爬取路径
	start_urls = []

	for yymm_start in range(START_YEAR, END_YEAR + 1):
		yymm_end = yymm_start + 1
		url = 'http://zq.win007.com/cn/League/%s-%s/31.html' % (yymm_start, yymm_end)
		print(url)
		start_urls.append(url)


	def parse(self, response):
		baseUrl = 'http://zq.win007.com'

		# 得到js data路径
		js_path = re.search(r'src="(?P<js>/jsData/matchResult/.*?)"\>', response.body.decode('utf-8')).groupdict()
		js_data = js_path['js']
		print('*'*60)
		print(js_path)
		print(js_data)
		print(baseUrl+js_data)

		# -- 传当前赛季到cral_info()
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

		# 得到队伍名称
		teams = {}
		arrTeam = {}

		crawl_teams = re.findall(r'(arrTeam.*?;)', response.body.decode('utf-8'))[0].replace('arrTeam','arrTeam["a"]')

		exec(crawl_teams) # exec直接生成arrTeam

		for team in arrTeam['a']:
			teams[team[0]] = team[1]

		# 得到轮次数据
		crawl_round = re.findall(r'(jh.*?;)', response.body.decode('utf-8'))
		jh = {}
		for item in crawl_round:
			exec(item.replace(',,', ",'',").replace(',,', ",'',"))

		all_round_list = [] #存储全部轮次比赛结果
		for rnd in jh:
			round_num = rnd[2:] #轮次
			round_list = [] # 存储当前轮次全部比赛结果

			for match in jh[rnd]:
				time = match[3] #时间
				home_red = match[18] #主队红牌
				home_team =  teams.get(match[4])#主队名称
				home_rank = match[8] #主队名次
				score = match[6] #比分
				score_half = match[7] #半场比分
				away_red = match[19] #客队红牌
				away_team =  teams.get(match[5]) #客队名称
				away_rank = match[9] #客队名次

				tmp = []
				tmp.append(str(season))
				tmp.append(str(round_num))
				tmp.append(str(time))
				tmp.append(str(home_red))
				tmp.append(str(home_team))
				tmp.append(str(home_rank))
				tmp.append(str(score))
				tmp.append(str(score_half))
				tmp.append(str(away_red))
				tmp.append(str(away_team))
				tmp.append(str(away_rank))

				round_list.append(tmp)
			all_round_list.append(round_list)

		with open(CSV_PATH_EVENTS,'ab+') as f:
			title = ['赛季','轮次','时间','主队红牌数','主队名称','主队上轮名次','比分','半场比分','客队红牌数','客队名称','客队上轮名次']
			f.write(bytes(",".join(title)+"\n",encoding="utf-8"))
			for rnd in all_round_list:
				for match in rnd:
					f.write(bytes(",".join(match) + "\n",encoding="utf-8"))

		# 得到总积分榜
		crawl_total_score = re.findall(r'(totalScore.*?;)', response.body.decode('utf-8'))[0].replace('totalScore','totalScore["a"]')

		totalScore = {}
		exec(crawl_total_score) # exec直接生成arrTeam

		all_score_list = []
		for team in totalScore['a']:
			rank = team[1] # 排名
			team_name = teams.get(team[2]) # 球队名称
			red_card = team[3] # 红牌数量
			games = team[4] # 比赛数量
			games_win = team[5] # 胜场数
			games_draw = team[6] # 平场数
			games_lost = team[7] # 负场数
			goals = team[8] # 进球数
			goals_concede = team[9] # 丢球数
			goals_diff = team[10] # 净胜球
			rate_win = round(float(team[11]) / 100, 4) # 胜率
			rate_draw = round(float(team[12]) / 100, 4) # 平率
			rate_lost = round(float(team[13]) / 100, 4) # 负率
			goal_avg = team[14] # 场均进球
			goal_concede_avg = team[15] # 场均丢球
			score = team[16] # 积分

			score_list = []
			score_list.append(str(season))
			score_list.append(str(rank))
			score_list.append(str(team_name))
			score_list.append(str(red_card))
			score_list.append(str(games))
			score_list.append(str(games_win))
			score_list.append(str(games_draw))
			score_list.append(str(games_lost))
			score_list.append(str(goals))
			score_list.append(str(goals_concede))
			score_list.append(str(goals_diff))
			score_list.append(str(rate_win))
			score_list.append(str(rate_draw))
			score_list.append(str(rate_lost))
			score_list.append(str(goal_avg))
			score_list.append(str(goal_concede_avg))
			score_list.append(str(score))

			all_score_list.append(score_list)

		with open(CSV_PATH_SCORE,'ab+') as f:
			title = ['赛季','排名','球队名称','红牌数量','比赛数量','胜场数','平场数','负场数','进球数','丢球数','净胜球', '胜率', '平率', '负率', '场均进球', '场均丢球', '积分']
			f.write(bytes(",".join(title)+"\n",encoding="utf-8"))
			for team_score in all_score_list:
				f.write(bytes(",".join(team_score) + "\n",encoding="utf-8"))

		# 得到主场积分榜
		crawl_home_score = re.findall(r'(homeScore.*?;)', response.body.decode('utf-8'))[0].replace('homeScore','homeScore["a"]')

		homeScore = {}
		exec(crawl_home_score) # exec直接生成homeScore

		#print('*' * 66)
		#print(homeScore['a'])

		all_score_list = []
		for team in homeScore['a']:
			rank = team[0] # 排名
			team_name = teams.get(team[1]) # 球队名称
			games = team[2] # 比赛数量
			games_win = team[3] # 胜场数
			games_draw = team[4] # 平场数
			games_lost = team[5] # 负场数
			goals = team[6] # 进球数
			goals_concede = team[7] # 丢球数
			goals_diff = team[8] # 净胜球
			rate_win = round(float(team[9]) / 100, 4) # 胜率
			rate_draw = round(float(team[10]) / 100, 4) # 平率
			rate_lost = round(float(team[11]) / 100, 4) # 负率
			goal_avg = team[12] # 场均进球
			goal_concede_avg = team[13] # 场均丢球
			score = team[14] # 积分

			score_list = []
			score_list.append(str(season))
			score_list.append(str(rank))
			score_list.append(str(team_name))
			score_list.append(str(games))
			score_list.append(str(games_win))
			score_list.append(str(games_draw))
			score_list.append(str(games_lost))
			score_list.append(str(goals))
			score_list.append(str(goals_concede))
			score_list.append(str(goals_diff))
			score_list.append(str(rate_win))
			score_list.append(str(rate_draw))
			score_list.append(str(rate_lost))
			score_list.append(str(goal_avg))
			score_list.append(str(goal_concede_avg))
			score_list.append(str(score))

			all_score_list.append(score_list)

		with open(CSV_PATH_SCORE_HOME,'ab+') as f:
			title = ['赛季','排名','球队名称','比赛数量','胜场数','平场数','负场数','进球数','丢球数','净胜球', '胜率', '平率', '负率', '场均进球', '场均丢球', '积分']
			f.write(bytes(",".join(title)+"\n",encoding="utf-8"))
			for team_score in all_score_list:
				f.write(bytes(",".join(team_score) + "\n",encoding="utf-8"))

		# 得到主场积分榜
		crawl_away_score = re.findall(r'(guestScore.*?;)', response.body.decode('utf-8'))[0].replace('guestScore','guestScore["a"]')

		guestScore = {}
		exec(crawl_away_score) # exec直接生成guestScore

		#print('*' * 66)
		#print(guestScore['a'])

		all_score_list = []
		for team in guestScore['a']:
			rank = team[0] # 排名
			team_name = teams.get(team[1]) # 球队名称
			games = team[2] # 比赛数量
			games_win = team[3] # 胜场数
			games_draw = team[4] # 平场数
			games_lost = team[5] # 负场数
			goals = team[6] # 进球数
			goals_concede = team[7] # 丢球数
			goals_diff = team[8] # 净胜球
			rate_win = round(float(team[9]) / 100, 4) # 胜率
			rate_draw = round(float(team[10]) / 100, 4) # 平率
			rate_lost = round(float(team[11]) / 100, 4) # 负率
			goal_avg = team[12] # 场均进球
			goal_concede_avg = team[13] # 场均丢球
			score = team[14] # 积分

			score_list = []
			score_list.append(str(season))
			score_list.append(str(rank))
			score_list.append(str(team_name))
			score_list.append(str(games))
			score_list.append(str(games_win))
			score_list.append(str(games_draw))
			score_list.append(str(games_lost))
			score_list.append(str(goals))
			score_list.append(str(goals_concede))
			score_list.append(str(goals_diff))
			score_list.append(str(rate_win))
			score_list.append(str(rate_draw))
			score_list.append(str(rate_lost))
			score_list.append(str(goal_avg))
			score_list.append(str(goal_concede_avg))
			score_list.append(str(score))

			all_score_list.append(score_list)

		with open(CSV_PATH_SCORE_AWAY,'ab+') as f:
			title = ['赛季','排名','球队名称','比赛数量','胜场数','平场数','负场数','进球数','丢球数','净胜球', '胜率', '平率', '负率', '场均进球', '场均丢球', '积分']
			f.write(bytes(",".join(title)+"\n",encoding="utf-8"))
			for team_score in all_score_list:
				f.write(bytes(",".join(team_score) + "\n",encoding="utf-8"))

