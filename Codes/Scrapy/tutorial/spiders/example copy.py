# -*- coding: utf-8 -*-
import scrapy
import re

class ExampleSpider(scrapy.Spider):
	name = 'example'
	start_urls = []
	for yymm in range(2013, 2018):
		yymm2 = yymm + 1
		start_urls.append('http://zq.win007.com/cn/League/%s-%s/31.html' % (yymm, yymm2))

	def parse(self, response):
		baseUrl = 'http://zq.win007.com'

		# 得到js data路径
		s = re.search(r'src="(?P<js>/jsData/matchResult/.*?)"\>', response.body.decode('utf-8')).groupdict()
		jsFile = s['js']
		print('*'*60)
		print(s)
		print(jsFile)
		print(baseUrl+jsFile)
		request  = scrapy.Request(baseUrl+jsFile, callback=self.my_callback)
		yield request

	# 解析js data
	def my_callback(self, response):
		arrTeam = {}
		s = re.findall(r'(arrTeam.*?;)', response.body.decode('utf-8'))

		for item in s:
			item = item.replace('arrTeam','arrTeam["a"]')
			exec(item)

		# 得到队伍名称
		name = {}
		for item in arrTeam["a"]:
			name[item[0]] = item[1]

		s = re.findall(r'(jh.*?;)', response.body.decode('utf-8'))
		jh = {}
		for item in s:
			exec(item)

		# 得到结果
		result = []
		for item in jh:
			rou = item[2:] #轮次
			t = []
			for j in jh[item]:
				time = j[3] #时间
				a_red = j[18] #主队红牌
				a_name =  name.get(j[4])#主队名称
				a_ran = j[8] #主队名次
				score = j[6] #比分
				score_half = j[7] #半场比分
				b_red = j[19] #主队红牌
				b_name =  name.get(j[5])#主队名称
				b_ran = j[9] #主队名次
				legGoal = self.getLetGoal(j[10]) # 全场让球
				legGoal = self.getLetGoal(j[11]) # 半场让球
				size = j[12] #全场大小
				size_half = j[13] #半场大小
				tmp = []
				tmp.append(str(rou))
				tmp.append(str(time))
				tmp.append(str(a_red))
				tmp.append(str(a_name))
				tmp.append(str(a_ran))
				tmp.append(str(score))
				tmp.append(str(score_half))
				tmp.append(str(b_red))
				tmp.append(str(b_name))
				tmp.append(str(b_ran))
				tmp.append(str(legGoal))
				tmp.append(str(legGoal))
				tmp.append(str(size))
				tmp.append(str(size_half))
				t.append(tmp)
			result.append(t)

		with open('/Users/llx/PyProjects/BettingDog/Data/Game Data/test.csv',"ab+") as f:
			title = ['轮次','时间','主队红牌','主队名称','主队名次','比分','半场比分','主队红牌','主队名称','主队名次','全场让球','半场让球','全场大小','半场大小']
			f.write(bytes(",".join(title)+"\n",encoding="gb2312"))
			for i in result:
				for j in i:
					f.write(bytes(",".join(j) + "\n",encoding="gb2312"))

	def getLetGoal(self, goal):
		GoalCn = ["平手", "平/半", "半球", "半/一", "一球", "一/球半", "球半", "半/二", "二球", "二/半", "二球半", "半/三", "三球", "三/半", "三球半", "半/四", "四球", "四/半", "四球半", "半/五", "五球", "五/半", "五球半", "五球半/六球", "六球", "六球/六球半", "六球半", "六球半/七球", "七球", "七球/七球半", "七球半", "七球半/八球", "八球", "八球/八球半", "八球半", "八球半/九球", "九球", "九球/九球半", "九球半", "九球半/十球", "十球"]
		goalKind = abs(int(float(goal) * 4.0))
		return GoalCn[goalKind]
