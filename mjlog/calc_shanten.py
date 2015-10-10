# !--v.1.0--

class hai_tree:

    nodes = []
    candidates = []
    pending_list = []
    part = []
    last_div = []

    def __init__(self, hai_left, parent=[]):
        hai_tree.nodes.append(self)
        self.hai_left = sorted(hai_left)
        self.children = []
        self.parents = parent
        if hai_left != []:
            hai_tree.pending_list.append(self)

    def grow_tree(self):
        hai_n = [(n // 4) % 9 for n in self.hai_left]
        if hai_n.count(hai_n[0]) >= 3:  # 111
            new_part = [0, 1, 2]
            self.add_child(new_part)
        if hai_n.count(hai_n[0] + 1) > 0 and hai_n.count(hai_n[0] + 2) > 0: # 123
            new_part = [0, hai_n.index(hai_n[0] + 1), hai_n.index(hai_n[0] + 2)]
            self.add_child(new_part)
        elif hai_n.count(hai_n[0] + 2) > 0:  # 13
            new_part = [0, hai_n.index(hai_n[0] + 2)]
            self.add_child(new_part)
        if hai_n.count(hai_n[0]) > 1:  # 11
            new_part = [0, 1]
            self.add_child(new_part)
        else:  # 1
            new_part = [0]
            self.add_child(new_part)
        if hai_n.count(hai_n[0] + 1) > 0:  # 12
            new_part = [0, hai_n.index(hai_n[0] + 1)]
            self.add_child(new_part)
        hai_tree.pending_list.remove(self)

    def add_child(self, new_part):
        flag = 0
        new_left = self.hai_left[:]
        for x in sorted(new_part, reverse=True):
            new_left.pop(x)
        for node in hai_tree.nodes:
            if node.hai_left == new_left:
                node.parents.append(self)
                self.children.append(node)
                flag = 1
        if flag == 0:
            self.children.append(hai_tree(new_left, [self]))

    def search_candidates(self, depth=0):
        if depth == 0:
            hai_tree.candidates = []
            hai_tree.last_div = []
            hai_tree.part = []
        hai_tree.last_div.append(depth)
        for node in self.children:
            # attach part to candidates
            hai_tree.part.append(
                sorted(list(set(self.hai_left) - set(node.hai_left))))
            if node == self.children[-1]:
                hai_tree.last_div.pop()
            if node.hai_left != []:
                node.search_candidates(depth + 1)
            else:
                hai_tree.candidates.append(hai_tree.part[:])
                if hai_tree.last_div:
                    hai_tree.part[hai_tree.last_div[-1]:] = []
        return hai_tree.candidates

    def reset(self):
        hai_tree.nodes = []
        hai_tree.candidates = []
        hai_tree.pending_list = []
        hai_tree.part = []
        hai_tree.last_div = []

def trans_format(input_format):
    table = dict([('m', 0), ('p', 36), ('s', 72), ('z', 108)])

    if isinstance(input_format,str):
        output_format = []
        temp_str = []
        for char in input_format:
            if char == "m" or char == "p" or char == "s" or char == "z":
                cont = table[char]
                for x in temp_str:
                    output_format.extend([int(x) * 4 - 4 + cont])
                temp_str = []
            else:
                if char == '0':
                    temp_str.extend('5')
                else:
                    temp_str.extend(char)
        for i in range(len(output_format)):
            output_format[i] = output_format[i] + output_format.count(output_format[i]) - 1
        output_format = sorted(output_format)
    else:
        output_format = ''
        input_format = sorted(input_format)
        if len([str(x) for x in input_format if x < 36]):
            output_format += ''.join([str(x//4%9 + 1) for x in input_format if x < 36] + ['m'])
        if len([str(x) for x in input_format if x < 72 and x >= 36]):
            output_format += ''.join([str(x//4%9 + 1) for x in input_format if x < 72 and x >= 36] + ['p'])
        if len([str(x) for x in input_format if x < 108 and x >= 72]):
            output_format += ''.join([str(x//4%9 + 1) for x in input_format if x < 108 and x >= 72] + ['s'])
        if len([str(x) for x in input_format if x >= 108]):
            output_format += ''.join([str(x//4%9 + 1) for x in input_format if x >= 108] + ['z'])

    return output_format

def calc_shanten(te_hai, naku_hai):
    if isinstance(te_hai, str):
        te_hai = trans_format(te_hai)
    if isinstance(naku_hai, str):
        naku_hai = trans_format(naku_hai)
    if len(te_hai) + len(naku_hai)*3 != 13:
        print('error')
        return None

    hai_m = sorted([x for x in te_hai if x < 36])
    hai_p = sorted([x for x in te_hai if x >= 36 and x < 72])
    hai_s = sorted([x for x in te_hai if x >= 72 and x < 108])
    hai_z = sorted([(x, x // 4) for x in te_hai if x >= 108], key=lambda y: y[0])

    if hai_m:
        root_m = hai_tree(hai_m)
        root_m.grow_tree()
        while hai_tree.pending_list != []:
            hai_tree.pending_list[0].grow_tree()
        candidates_m = root_m.search_candidates()
    else:
        candidates_m = [[]]
    if hai_p:
        root_p = hai_tree(hai_p)
        root_p.grow_tree()
        while hai_tree.pending_list != []:
            hai_tree.pending_list[0].grow_tree()
        candidates_p = root_p.search_candidates()
    else:
        candidates_p = [[]]
    if hai_s:
        root_s = hai_tree(hai_s)
        root_s.grow_tree()
        while hai_tree.pending_list != []:
            hai_tree.pending_list[0].grow_tree()
        candidates_s = root_s.search_candidates()
    else:
        candidates_s = [[]]
    if hai_z:
        candidates_z = []
        for n in sorted(set([x[1] for x in hai_z])):
            candidates_z.append([x[0] for x in hai_z if x[1] == n])
    else:
        candidates_z = []
    candidates_hai = []
    for x in candidates_m:
        for y in candidates_p:
            for z in candidates_s:
                candidates_hai.append(x + y + z + candidates_z)
    # shanten
    shanten_candidates = []
    for part in candidates_hai:
        mentsu = len([1 for x in part if len(x) == 3]) + len(naku_hai)
        tatsu = len([1 for x in part if len(x) == 2])
        toitsu = len(
            [1 for x in part if len(x) == 2 and x[0] // 4 == x[1] // 4])
        shanten_candidates.append((min(tatsu, 4 - mentsu) + max(4 - mentsu - tatsu, 0) * 2 + (
            toitsu == 0 or (mentsu + tatsu) <= 4) - 1, part, mentsu, tatsu, toitsu))
    te_hai_n = [x // 4 for x in te_hai]
    for x in set(te_hai_n):
        te_hai_n.remove(x)
    shanten_chitoi = 6 - len(set(te_hai_n)) + 100 * len(naku_hai)
    gokushi_hai = [x // 4 for x in te_hai if x //
                   4 in [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]]
    shanten_gokushi = 13 - \
        len(set(gokushi_hai)) - \
        (len(gokushi_hai) > len(set(gokushi_hai))) + 100 * len(naku_hai)
    shanten_min = min(
        [x[0] for x in shanten_candidates] + [shanten_chitoi] + [shanten_gokushi])
    if hai_tree.nodes:
        hai_tree.reset(hai_tree.nodes[0])
    # machihai
    machi = []
    for sugata in shanten_candidates:
        if sugata[0] == shanten_min:
            if 4 - sugata[2] > 0:
                 # lack of mentsu
                for div in sugata[1]:
                    if len(div) == 2:
                        # not lack of toitsu
                        if div[0] // 4 == div[1] // 4 and sugata[4] >= 2:
                            machi.append(div[0] // 4)
                        elif div[1] // 4 - div[0] // 4 == 1:
                            machi.extend([x for x in [div[0] // 4 - 1, div[1] // 4 + 1] if x in
                                range(min(div[1] // 36, 2) * 9, min(div[1] // 36, 2) * 9 + 9)])
                        elif div[1] // 4 - div[0] // 4 == 2:
                            machi.append(div[0] // 4 + 1)
            if 4 - sugata[2] - sugata[3] + min(sugata[4], 1) > 0:
                # lack of tatsu/toisu
                for div in sugata[1]:
                    if len(div) == 1:
                        machi.append(div[0] // 4)
                        machi.extend([x for x in [div[0] // 4 - 2, div[0] // 4 - 1, div[0] // 4 + 1,
                            div[0] // 4 + 2] if x in range(min(div[0] // 36, 2) * 9, min(div[0] // 36, 2) * 9 + 9)])
            elif 4 - sugata[2] - sugata[3] == 0:
                # not lack of tatsu but lack of toitsu
                for div in sugata[1]:
                    if len(div) == 1:
                        machi.append(div[0] // 4)
            elif 4 - sugata[2] - sugata[3] < 0 and sugata[4] == 0:
                # too many tatsu but lack of toitsu
                for div in sugata[1]:
                    if len(div) == 1:
                        machi.append(div[0] // 4)
                    elif len(div) == 2:
                        machi.extend([div[0] // 4, div[1] // 4])
    if shanten_chitoi == shanten_min:
        machi.extend(set([x // 4 for x in te_hai]) - set(te_hai_n))
    if shanten_gokushi == shanten_min:
        if len(gokushi_hai) > len(set(gokushi_hai)):
            machi.extend(
                set([0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]) - set(gokushi_hai))
        else:
            machi.extend([0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33])
    machi = sorted(set(machi))
    return [shanten_min, machi]
