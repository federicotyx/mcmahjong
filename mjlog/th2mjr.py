#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from xml.etree import ElementTree as ET
from lxml import etree as ET
import os

def th2txt(thvalue):
	i = thvalue // 4
	if i < 9:
		i = i + 1
		tag = 'p'
		if i == 5 and thvalue % 4 == 0:
			tag = 'P'
	elif i < 18:
		i = i - 8
		tag = 'm'
		if i == 5 and thvalue % 4 == 0:
			tag = 'M'
	elif i < 27:
		i = i - 17
		tag = 's'
		if i == 5 and thvalue % 4 == 0:
			tag = 'S'
	else:
		i = i - 26
		tag = 'z'
	return str(i)+tag

kyoku_all=0

mjr = open('t1.mjr', 'w')
root=ET.Element('mjr')

file='t1.xml'
xmllog = ET.parse(file)

for item in xmllog.getroot():
	if item.tag == 'SHUFFLE':
		continue
	elif item.tag == 'GO':
		continue
	elif item.tag == 'UN':
		if item.get('dan') != None:
			honba = 0
			kyotaku = 0
			oya = 0
			ryuukyo = 0
			kyoku = 0
			kyoku_abs = 0
			ten = [250, 250, 250, 250]
			dan = item.get('dan').split(',')
			rate = item.get('rate').split(',')

			info=ET.SubElement(root, "info")
			info.set("id", '0')
			info.set("name", item.get('n0'))
			info.set("dan", dan[0])
			info.set("rate", rate[0])
			info=ET.SubElement(root, "info")
			info.set("id", '1')
			info.set("name", item.get('n1'))
			info.set("dan", dan[1])
			info.set("rate", rate[1])
			info=ET.SubElement(root, "info")
			info.set("id", '2')
			info.set("name", item.get('n2'))
			info.set("dan", dan[2])
			info.set("rate", rate[2])
			info=ET.SubElement(root, "info")
			info.set("id", '3')
			info.set("name", item.get('n3'))
			info.set("dan", dan[3])
			info.set("rate", rate[3])
		continue
	elif item.tag == 'TAIKYOKU':
		continue
	elif item.tag == 'INIT':
		kyoku_all = kyoku_all + 1
		if ryuukyo == 0 and int(item.get('oya')) != oya:
			honba = 0
		else:
			honba = honba + 1
		kyoku_abs = kyoku_abs + 1
		if int(item.get('oya')) != oya:
			kyoku = kyoku + 1
		w = oya = int(item.get('oya'))
		junme = [0, 0, 0, 0]
		shanten = [100, 100, 100, 100]
		win = [0, 0, 0, 0]
		naki = [[],[],[],[]]
		tp = [False, False, False, False]
		ura = []

		hai = []
		hai.append(sorted([int(n) for n in item.get('hai0').split(',')]))
		hai.append(sorted([int(n) for n in item.get('hai1').split(',')]))
		hai.append(sorted([int(n) for n in item.get('hai2').split(',')]))
		hai.append(sorted([int(n) for n in item.get('hai3').split(',')]))

		obtain = []
		play = []
		typo_obtain = []
		typo_play = []

		get_seed = item.get('seed').split(',')
		dora=[get_seed[-1]]

		game=ET.SubElement(root,"game")
		game.set('kyoku',str(get_seed[0]))
		game.set('honba',str(get_seed[1]))
		game.set('kyotaku',str(get_seed[2]))
		game.set('oya',item.get('oya'))
		score=ET.SubElement(game,"score")
		score.text=' '.join([x for x in item.get('ten').split(',')])
		init=ET.SubElement(game,"init")
		init.set('id','0')
		init.text=''.join([th2txt(x) for x in hai[0]])
		init=ET.SubElement(game,"init")
		init.set('id','1')
		init.text=''.join([th2txt(x) for x in hai[1]])
		init=ET.SubElement(game,"init")
		init.set('id','2')
		init.text=''.join([th2txt(x) for x in hai[2]])
		init=ET.SubElement(game,"init")
		init.set('id','3')
		init.text=''.join([th2txt(x) for x in hai[3]])
		indicator=ET.SubElement(game,"indicator")
		indicator.text=str(th2txt(int(get_seed[-1])))

		continue
	elif item.tag == 'REACH':
		w = int(item.get('who'))
		if int(item.get('step')) == 2:
			rch = ET.SubElement(game, "riichi2")
			kyotaku = kyotaku + 1
			ten[w] = ten[w] - 10
			ctmp = [0, 0, 0, 0]
			ctmp[w] = -10
			change = ET.SubElement(game, "change")
			change.text = ' '.join([str(x) for x in ctmp])
		elif int(item.get('step')) == 1:
			rch = ET.SubElement(game, "riichi1")
			flag_rch = True
		continue
	elif item.tag == 'BYE':
		continue
	elif item.tag == 'AGARI':
		get_who = int(item.get('who'))
		get_fwho = int(item.get('fromWho'))
		get_sc = [int(n) for n in item.get('sc').split(',')]
		ryuukyo = 0
		kyotaku = 0
		win[0] = get_sc[1]
		win[1] = get_sc[3]
		win[2] = get_sc[5]
		win[3] = get_sc[7]

		hu = ET.SubElement(game, "hu")
		hu.set("from", str(get_fwho))
		hu.set("id", str(get_who))

		end=ET.SubElement(game, "end")
		hu = ET.SubElement(game, "hu")
		hu.set("from", str(get_fwho))
		hu.set("id", str(get_who))
		hu.set("score", item.get("ten").split(",")[1])
		change = ET.SubElement(hu, "change")
		change.text = " ".join([str(x) for x in win])
		continue
	elif item.tag == 'RYUUKYOKU':
		get_sc = [int(n) for n in item.get('sc').split(',')]
		ten[0] = ten[0] + get_sc[1]
		ten[1] = ten[1] + get_sc[3]
		ten[2] = ten[2] + get_sc[5]
		ten[3] = ten[3] + get_sc[7]
		win[0] = get_sc[1]
		win[1] = get_sc[3]
		win[2] = get_sc[5]
		win[3] = get_sc[7]
		ryuukyo = 1
		end=ET.SubElement(game, "end")
		ryuukyouku = ET.SubElement(game, "ryuukyoku")
		change = ET.SubElement(ryuukyouku, "change")
		change.text = " ".join([str(x) for x in win])

		continue
	elif item.tag == 'N':
		fwho = w
		w = int(item.get('who'))
		m = int(item.get('m'))
		if (m - (fwho - w) % 4) % 8 == 4:
			#---チー---#
			junme[w] = junme[w] + 1
			hai[w].append(lasthai)
			n0 = m // 3072
			n1 = (m % 3072) // 1024
			n2 = (m % (32 * 4**n1)) // (8 * 4**n1)
			hai0 = n0 // 7 * 36 + n0 % 7 * 4 + n1 * 4 + n2
			hai1 = [n0 // 7 * 36 + n0 % 7 * 4 + x * 4 + (m % (32 * 4**x)) // (8 * 4**x) for x in [0, 1, 2]]
			p=th2txt(hai0)
			ph=[th2txt(x) for x in hai1]
			ph.remove(p)
			chi=ET.SubElement(game, "chi")
			chi.text=''.join(ph)

		elif (m - (fwho - w) % 4) % 8 == 0:
			if m % 256 == 0:
				## 暗槓 ##
				hai0 = (m - (fwho - w) % 4) // 256
				hai1 = [hai0 - hai0 % 4 + x for x in [0, 1, 2 ,3]]

				angang=ET.SubElement(game, "angang")
				angang.text=str(th2txt(hai0 % 64))

			elif (m - (fwho - w) % 4) % 256 == 0:
				## 大明槓 ##
				hai[w].append(lasthai)
				hai0 = (m - (fwho - w) % 4) // 256
				hai1 = [hai0 - hai0 % 4 + x for x in [0, 1, 2 ,3]]

				daminggang=ET.SubElement(game, "angang")
				daminggang.set("id", str(w))

			elif (m - (fwho - w) % 4) % 32 == 8:
				## ポン ##
				junme[w] = junme[w] + 1
				hai[w].append(lasthai)
				n0 = m // 1536
				n1 = (m % 1536) // 512
				n2 = (m % (512)) // 32
				hai0 = n0 * 4 + n1 + (n2 <= n1)
				hai1 = [n0 * 4 + x + (n2 <= x) for x in [0, 1, 2]]

				p=th2txt(hai0)
				ph=[th2txt(x) for x in hai1]
				ph.remove(p)
				peng=ET.SubElement(game, "peng")
				peng.text=''.join(ph)

		elif (m - (fwho - w) % 4) % 8 == 1 or (m - (fwho - w) % 4) % 8 == 2 or (m - (fwho - w) % 4) % 8 == 3:
			## 加槓 ##
			n0 = m // 1536
			n1 = (m % 1536) // 512
			n2 = (m % 512) // 32
			hai0 = n0 * 4 + n2

			jiagang=ET.SubElement(game, "jiagang")
			jiagang.text=str(th2txt(hai0 % 64))
		continue
	elif item.tag == 'DORA':
		indicator=ET.SubElement(game,"indicator")
		indicator.text=str(th2txt(int(item.get('hai'))))
		continue
	else:
		if item.tag[0] == 'T':
			w = 0
			lasthai = int(item.tag[1:])
			draw = ET.SubElement(game, "draw")
			draw.text=th2txt(int(item.tag[1:]))
		elif item.tag[0] == 'U':
			w = 1
			lasthai = int(item.tag[1:])
			draw = ET.SubElement(game, "draw")
			draw.text=th2txt(int(item.tag[1:]))
		elif item.tag[0] == 'V':
			w = 2
			lasthai = int(item.tag[1:])
			draw = ET.SubElement(game, "draw")
			draw.text=th2txt(int(item.tag[1:]))
		elif item.tag[0] == 'W':
			w = 3
			lasthai = int(item.tag[1:])
			draw = ET.SubElement(game, "draw")
			draw.text=th2txt(int(item.tag[1:]))
		elif item.tag[0] == 'D':
			w = 0
			if int(item.tag[1:])==lasthai:
				discard2 = ET.SubElement(game, "discard2")
				discard2.text=th2txt(int(item.tag[1:]))
			else:
				discard1 = ET.SubElement(game, "discard1")
				discard1.text=th2txt(int(item.tag[1:]))
			lasthai = int(item.tag[1:])
		elif item.tag[0] == 'E':
			w = 1
			if int(item.tag[1:])==lasthai:
				discard2 = ET.SubElement(game, "discard2")
				discard2.text=th2txt(int(item.tag[1:]))
			else:
				discard1 = ET.SubElement(game, "discard1")
				discard1.text=th2txt(int(item.tag[1:]))
			lasthai = int(item.tag[1:])
		elif item.tag[0] == 'F':
			w = 2
			if int(item.tag[1:])==lasthai:
				discard2 = ET.SubElement(game, "discard2")
				discard2.text=th2txt(int(item.tag[1:]))
			else:
				discard1 = ET.SubElement(game, "discard1")
				discard1.text=th2txt(int(item.tag[1:]))
			lasthai = int(item.tag[1:])
		elif item.tag[0] == 'G':
			w = 3
			if int(item.tag[1:])==lasthai:
				discard2 = ET.SubElement(game, "discard2")
				discard2.text=th2txt(int(item.tag[1:]))
			else:
				discard1 = ET.SubElement(game, "discard1")
				discard1.text=th2txt(int(item.tag[1:]))
			lasthai = int(item.tag[1:])
		continue
mjr.writelines(ET.tostringlist(root,encoding="utf-8",pretty_print=True))
mjr.writelines('</mjlog>')
mjr.close

