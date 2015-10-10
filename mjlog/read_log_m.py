# -*- coding: utf-8 -*-

from xml.dom import minidom
import os
from calc_shanten import calc_shanten_hai

hai_dictionary = dict([(0, 1), (1, 1), (2, 1), (3, 1), (4, 2), (5, 2), (6, 2), (7, 2), (8, 3), (9, 3), (10, 3), (11, 3), (12, 4), (13, 4), (14, 4), (15, 4), (16, 5), (17, 5), (18, 5), (19, 5), (20, 6), (21, 6), (22, 6), (23, 6), (24, 7), (25, 7), (26, 7), (27, 7), (28, 8), (29, 8), (30, 8), (31, 8), (32, 9), (33, 9), (34, 9), (35, 9), (36, 12), (37, 12), (38, 12), (39, 12), (40, 13), (41, 13), (42, 13), (43, 13), (44, 14), (45, 14), (46, 14), (47, 14), (48, 15), (49, 15), (50, 15), (51, 15), (52, 16), (53, 16), (54, 16), (55, 16), (56, 17), (57, 17), (58, 17), (59, 17), (60, 18), (61, 18), (62, 18), (63, 18), (64, 19), (65, 19), (66, 19), (67, 19), (68, 20), (69, 20), (70, 20), (71, 20), (72, 23), (73, 23), (74, 23), (75, 23), (76, 24), (77, 24), (78, 24), (79, 24), (80, 25), (81, 25), (82, 25), (83, 25), (84, 26), (85, 26), (86, 26), (87, 26), (88, 27), (89, 27), (90, 27), (91, 27), (92, 28), (93, 28), (94, 28), (95, 28), (96, 29), (97, 29), (98, 29), (99, 29), (100, 30), (101, 30), (102, 30), (103, 30), (104, 31), (105, 31), (106, 31), (107, 31), (108, 34), (109, 34), (110, 34), (111, 34), (112, 37), (113, 37), (114, 37), (115, 37), (116, 40), (117, 40), (118, 40), (119, 40), (120, 43), (121, 43), (122, 43), (123, 43), (124, 46), (125, 46), (126, 46), (127, 46), (128, 49), (129, 49), (130, 49), (131, 49), (132, 52), (133, 52), (134, 52), (135, 52)])

c = 0
reachlog = open('reachlog', 'w')
reachlog.writelines(
    "kyoku, zaseki, dan, honba, kyootaku, ten0, ten1, ten2, ten3, junme, pai0, pai1, pai2, pai3, pai4, pai5, pai6, pai7, pai8, pai9, pai10, pai11, pai12, pai13, pai14, pai15, pai16, pai17, pai18, pai19, pai20, pai21, pai22, pai23, pai24, pai25, pai26, pai27, pai28, pai29, pai30, pai31, pai32, pai33, pai34, pai35, pai36, pai37, pai38, pai39, pai40, pai41, pai42, pai43, pai44, pai45, pai46, pai47, pai48, pai49, pai50, pai51, pai52, pai53, pai54, pai55, pai56, pai57, pai58, pai59, pai60, pai61, pai62, pai63, pai64, pai65, pai66, pai67, pai68, pai69, pai70, pai71, pai72, pai73, pai74, pai75, pai76, pai77, pai78, pai79, pai80, pai81, pai82, pai83, pai84, pai85, pai86, pai87, pai88, pai89, pai90, pai91, pai92, pai93, pai94, pai95, pai96, pai97, pai98, pai99, pai100, pai101, pai102, pai103, pai104, pai105, pai106, pai107, pai108, pai109, pai110, pai111, pai112, pai113, pai114, pai115, pai116, pai117, pai118, pai119, pai120, pai121, pai122, pai123, pai124, pai125, pai126, pai127, pai128, pai129, pai130, pai131, pai132, pai133, pai134, pai135, ron, ron_ten, ron_pai" + "\n")

kyoku_all = 0
for file in os.listdir('./mjlogdb'):
    if file != '.DS_Store':
        print file
        c = c + 1
        # if c == 1000:
        #     break
        xmllog = minidom.parse('./mjlogdb/' + file)
        for item in xmllog.childNodes[0].childNodes:
            if item.nodeName == 'SHUFFLE':
                continue
            elif item.nodeName == 'GO':
                honba = 0
                kyotaku = 0
                oya = 0
                ryuukyo = 0
                kyoku = 0
                kyoku_abs = 0
                ten = [250, 250, 250, 250]
                continue
            elif item.nodeName == 'UN':
                if item.getAttribute('dan') != '':
                    dan = item.getAttribute('dan').split(',')
                continue
            elif item.nodeName == 'TAIKYOKU':
                continue
            elif item.nodeName == 'INIT':
                kyoku_all = kyoku_all + 1
                ## 更新托供 ##
                if ryuukyo == 0 and int(item.getAttribute('oya')) != oya:
                    honba = 0
                else:
                    honba = honba + 1
                ## 当前局数 ##
                kyoku_abs = kyoku_abs + 1
                if int(item.getAttribute('oya')) != oya:
                    kyoku = kyoku + 1
                ## 当前亲位 ##
                oya = int(item.getAttribute('oya'))
                ## 重置巡目向听 ##
                pai=[-1]*136
                junme = [1, 0, 0, 0]
                shanten = [100, 100, 100, 100]
                win = [0, 0, 0, 0]
                naki = [[],[],[],[]]
                kawa = [[],[],[],[]]
                teda=[[],[],[],[]]
                line=['','','','']
                ## 读取手牌 ##
                hai = []
                hai.append([int(n) for n in item.getAttribute('hai0').split(',')])
                hai.append([int(n) for n in item.getAttribute('hai1').split(',')])
                hai.append([int(n) for n in item.getAttribute('hai2').split(',')])
                hai.append([int(n) for n in item.getAttribute('hai3').split(',')])
                for x in item.getAttribute('hai0').split(','):
                    pai[int(x)]=0
                for x in item.getAttribute('hai1').split(','):
                    pai[int(x)]=1
                for x in item.getAttribute('hai2').split(','):
                    pai[int(x)]=2
                for x in item.getAttribute('hai3').split(','):
                    pai[int(x)]=3

                lasthai=hai[0][-1]
                ## 读取宝牌 ##
                get_seed = item.getAttribute('seed').split(',')
                dora=[int(get_seed[-1])]
                pai[int(get_seed[-1])]=9
                ura=[]
                continue
            elif item.nodeName == 'RYUUKYOKU':
                #---流局---#
                get_sc = [int(n) for n in item.getAttribute('sc').split(',')]
                ten[0] = ten[0] + get_sc[1]
                ten[1] = ten[1] + get_sc[3]
                ten[2] = ten[2] + get_sc[5]
                ten[3] = ten[3] + get_sc[7]
                ryuukyo = 1

                reachlog.writelines(line)
                continue
            elif item.nodeName == 'REACH':
                # step==1
                # step==2 then kyotaku+1
                w = int(item.getAttribute('who'))
                if int(item.getAttribute('step')) == 2:
                    kyotaku = kyotaku + 1
                    ten[w] = ten[w] - 10

                    machi=calc_shanten_hai(hai[w], naki[w])
                    misepai= kawa[0] + kawa[1] + kawa[2] + kawa[3]
                    for x in range(4):
                        try:
                            misepai.extend(naki[0][x])
                            misepai.extend(naki[1][x])
                            misepai.extend(naki[2][x])
                            misepai.extend(naki[3][x])
                        except IndexError:
                            pass
                    misepai.extend(dora)
                    for x in machi[1]:
                        for y in range(x*4,x*4+4):
                            if pai[y]==-1:
                                pai[y]=w+10
                    line[w]=str(kyoku)+","+str(w)+","+str(dan[w])+","+str(honba)+","+str(kyotaku)+","+str(ten[0])+","+str(ten[1])+","+str(ten[2])+","+str(ten[3])+","+str(junme[w])+","+str(pai)[1:-1]+","+'-1'+","+'0'+","+'-1'+"\n"
                continue
            elif item.nodeName == 'BYE':
                continue
            elif item.nodeName == 'DORA':
                dora.append(int(item.getAttribute('hai')))
                pai[int(item.getAttribute('hai'))]=9
                continue
            elif item.nodeName == 'AGARI':
                ## 和牌 ##
                try:
                    get_yaku = [int(n) for n in item.getAttribute('yaku').split(',')]
                except:
                    get_yaku = [int(n) for n in item.getAttribute('yakuman').split(',')]
                get_who = int(item.getAttribute('who'))
                get_fwho = int(item.getAttribute('fromWho'))
                ## 更新点数 ##
                get_sc = [int(n) for n in item.getAttribute('sc').split(',')]
                ten[0] = ten[0] + get_sc[1]
                ten[1] = ten[1] + get_sc[3]
                ten[2] = ten[2] + get_sc[5]
                ten[3] = ten[3] + get_sc[7]
                ## 更新流局 ##
                ryuukyo = 0
                ## 更新托供 ##
                kyotaku = 0
                win[get_who] = 1
                if get_who != get_fwho:
                    win[get_fwho] = -1

                if get_who == get_fwho:
                    hai[get_who].remove(lasthai)

                ura=item.getAttribute('doraHaiUra').split(',')
                # print hai_dictionary[lasthai]
                # print calc_shanten_hai(hai[get_who], naki[get_who])
                if line[get_who]:
                    line[get_who]=line[get_who][0:-8]+str(get_fwho)+","+str(get_sc[get_who*2+1])+","+str(lasthai)+"\n"
                reachlog.writelines(line)
                continue
            elif item.nodeName == 'N':
                #---副露---#
                fwho = w
                w = int(item.getAttribute('who'))
                m = int(item.getAttribute('m'))
                if (m - (fwho - w) % 4) % 8 == 4:
                    #---チー---#
                    junme[w] = junme[w] + 1
                    hai[w].append(lasthai)
                    n0 = m // 3072
                    n1 = (m % 3072) // 1024
                    n2 = (m % (32 * 4**n1)) // (8 * 4**n1)
                    hai0 = n0 // 7 * 36 + n0 % 7 * 4 + n1 * 4 + n2
                    hai1 = [n0 // 7 * 36 + n0 % 7 * 4 + x * 4 + (m % (32 * 4**x)) // (8 * 4**x) for x in [0, 1, 2]]
                    for x in hai1:
                        hai[w].remove(x)
                    naki[w].append(hai1)
                    for x in hai1:
                        pai[x]=w+4
                elif (m - (fwho - w) % 4) % 8 == 0:
                    if m % 256 == 0:
                        ## 暗槓 ##
                        hai0 = (m - (fwho - w) % 4) // 256
                        hai1 = [hai0 - hai0 % 4 + x for x in [0, 1, 2 ,3]]
                        for x in hai1:
                            hai[w].remove(x)
                        naki[w].append(hai1)
                        for x in hai1:
                            pai[x]=w+4
                    elif (m - (fwho - w) % 4) % 256 == 0:
                        ## 大明槓 ##
                        hai[w].append(lasthai)
                        hai0 = (m - (fwho - w) % 4) // 256
                        hai1 = [hai0 - hai0 % 4 + x for x in [0, 1, 2 ,3]]
                        for x in hai1:
                            hai[w].remove(x)
                        naki[w].append(hai1)
                        for x in hai1:
                            pai[x]=w+4
                    elif (m - (fwho - w) % 4) % 32 == 8:
                        ## ポン ##
                        junme[w] = junme[w] + 1
                        hai[w].append(lasthai)
                        n0 = m // 1536
                        n1 = (m % 1536) // 512
                        n2 = (m % (512)) // 32
                        hai0 = n0 * 4 + n1 + (n2 <= n1)
                        hai1 = [n0 * 4 + x + (n2 <= x) for x in [0, 1, 2]]
                        for x in hai1:
                            hai[w].remove(x)
                        naki[w].append(hai1)
                        for x in hai1:
                            pai[x]=w+4
                elif (m - (fwho - w) % 4) % 8 == 1 or (m - (fwho - w) % 4) % 8 == 2 or (m - (fwho - w) % 4) % 8 == 3:
                    ## 加槓 ##
                    n0 = m // 1536
                    n1 = (m % 1536) // 512
                    n2 = (m % 512) // 32
                    hai0 = n0 * 4 + n2
                    hai[w].remove(hai0)
                    for x in naki[w]:
                        if x[0]//4==hai0//4:
                            x.append(hai0)
                    pai[hai0]=w+4
                    lasthai = hai0
                continue
            else:
                if item.nodeName[0] == 'T':
                    w = 0
                    junme[w] = junme[w] + 1
                    lasthai = int(item.nodeName[1:])
                    hai[w].append(int(item.nodeName[1:]))
                    pai[int(item.nodeName[1:])]=w
                elif item.nodeName[0] == 'U':
                    w = 1
                    junme[w] = junme[w] + 1
                    lasthai = int(item.nodeName[1:])
                    hai[w].append(int(item.nodeName[1:]))
                    pai[int(item.nodeName[1:])]=w
                elif item.nodeName[0] == 'V':
                    w = 2
                    junme[w] = junme[w] + 1
                    lasthai = int(item.nodeName[1:])
                    hai[w].append(int(item.nodeName[1:]))
                    pai[int(item.nodeName[1:])]=w
                elif item.nodeName[0] == 'W':
                    w = 3
                    junme[w] = junme[w] + 1
                    lasthai = int(item.nodeName[1:])
                    hai[w].append(int(item.nodeName[1:]))
                    kawa[w].append(int(item.nodeName[1:]))
                    pai[int(item.nodeName[1:])]=w
                elif item.nodeName[0] == 'D':
                    w = 0
                    if int(item.nodeName[1:])==lasthai:
                        teda[w].append(0)
                        pai[int(item.nodeName[1:])]=w*100+junme[w]+20
                    else:
                        teda[w].append(1)
                        pai[int(item.nodeName[1:])]=w*100+junme[w]+420
                    lasthai = int(item.nodeName[1:])
                    hai[w].remove(int(item.nodeName[1:]))
                    kawa[w].append(int(item.nodeName[1:]))
                elif item.nodeName[0] == 'E':
                    w = 1
                    if int(item.nodeName[1:])==lasthai:
                        teda[w].append(0)
                        pai[int(item.nodeName[1:])]=w*100+junme[w]+20
                    else:
                        teda[w].append(1)
                        pai[int(item.nodeName[1:])]=w*100+junme[w]+420
                    lasthai = int(item.nodeName[1:])
                    hai[w].remove(int(item.nodeName[1:]))
                    kawa[w].append(int(item.nodeName[1:]))
                elif item.nodeName[0] == 'F':
                    w = 2
                    if int(item.nodeName[1:])==lasthai:
                        teda[w].append(0)
                        pai[int(item.nodeName[1:])]=w*100+junme[w]+20
                    else:
                        teda[w].append(1)
                        pai[int(item.nodeName[1:])]=w*100+junme[w]+420
                    lasthai = int(item.nodeName[1:])
                    hai[w].remove(int(item.nodeName[1:]))
                    kawa[w].append(int(item.nodeName[1:]))
                elif item.nodeName[0] == 'G':
                    w = 3
                    if int(item.nodeName[1:])==lasthai:
                        teda[w].append(0)
                        pai[int(item.nodeName[1:])]=w*100+junme[w]+20
                    else:
                        teda[w].append(1)
                        pai[int(item.nodeName[1:])]=w*100+junme[w]+420
                    lasthai = int(item.nodeName[1:])
                    hai[w].remove(int(item.nodeName[1:]))
                    kawa[w].append(int(item.nodeName[1:]))
                continue
print kyoku_all
reachlog.close
