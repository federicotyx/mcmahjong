# -*- coding: utf-8 -*-

from xml.etree import ElementTree as etree
import os
from calc_shanten import calc_shanten

path = './mjlogdb'
obtain=['T','U','V','W']
play=['D','E','F','G']

c=0
flag = False
writelog = open('anal_tenpai','w')
writelog.writelines('kyoku, oya, junme, issuji, waijing, kuajing, xuanyanwai, xuanyankua, who\n')
for file in os.listdir(path):
    if file != '.DS_Store':
        xmllog = etree.iterparse(path+ '/' + file)
        for _, element in xmllog:
            c=c+1
            # if c == 1000:
                # break
            # print(element.tag)
            if element.tag == 'INIT':
                kyoku = element.get('kyoku')
                oya = element.get('oya')
                t=['']*4
            elif element.tag == 'AGARI':
                continue
            elif element.tag == 'RYUUKYOKU':
                continue
            elif element.tag == 'REACH':
                get_who = int(element.get('who'))
                get_junme = int(element.get('junme'))
                if element.get('machi_hai') == "":
                    continue
                else:
                    get_machi = [int(x) for x in element.get('machi_hai').split(',')]
                t[get_who] = ('R',get_junme,get_machi)
            elif element.tag == 'DAMA':
                continue
            elif element.tag == 'TENPAI':
                continue
            elif element.tag == 'GET':
                obtain_seq = element.get('seq').split(',')
                obtain_hai = element.get('hai').split(',')
            elif element.tag == 'PLAY':
                for w in range(0,4):
                    if t[w] != '':
                        play_seq = element.get('seq').split(',')
                        play_hai = [int(x)//4 for x in element.get('hai').split(',')]
                        a = [x[0] for x in enumerate(play_seq) if x[1][0] == play[w]]
                        # print('a = ' + str(a))
                        # print(t[w])
                        kawa = [play_hai[x] for x in a[0:t[w][1]]]
                        suji = []
                        for hai in t[w][2]:
                            suji.extend([x for x in [hai-3, hai+3] if x//9 == hai//9])
                        suji = sorted(set(suji)&set(t[w][2]))
                        # print(t[w])
                        # print(suji)
                        out_suji_id = 'NA'
                        in_suji_id = 'NA'
                        if suji:
                            out_suji = set([x-1 for x in suji[0:-1] if x//9 == (x-1)//9] + [x+1 for x in suji[1:] if x//9 == (x+1)//9])
                            in_suji = set([x+1 for x in suji[0:-1] if x//9 == (x+1)//9] + [x-1 for x in suji[1:] if x//9 == (x-1)//9])
                            for i in range(len(kawa)-1,-1,-1):
                                if kawa[i] in out_suji:
                                    out_suji_id = i
                                if kawa[i] in in_suji:
                                    in_suji_id = i
                        # print(kawa, t[w], a)
                        writelog.writelines(kyoku + ',' + oya + ',' + str(t[w][1]) + ',' + str(suji!=[]) + ',' + str(out_suji_id) + ',' + str(in_suji_id) + ',' + str(kawa[-1] in out_suji) + ',' + str(kawa[-1] in in_suji) + ',' + str(w) + '\n')
writelog.close()
