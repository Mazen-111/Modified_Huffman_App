from collections import Counter

class Node:
    def __init__(self, sym, freq):
        self.left = None
        self.right = None
        self.sym = sym 
        self.freq = freq

def gen_codes(root, sym, dic, code = ''):
    if root.left is None and root.right is None:
        dic[root.sym] = code
        return

    sym = root.sym
    gen_codes(root.left, sym, dic, code+'0')
    gen_codes(root.right, sym, dic, code+'1')

def Modified_Huffman(txt, threshold):
    len_txt = len(txt)

    char_freq = Counter(txt).most_common()
    dic = dict(char_freq)
    
    if threshold >= char_freq[0][1] / len_txt:
        return None
    
    if threshold >= char_freq[-2][1] / len_txt:
        others = []
        others_freq = 0
        
        for char, freq in char_freq:
            if (freq / len_txt) <= threshold:
                others.append(char)
                others_freq += char_freq[char]
                dic.pop(char)
            else:
                dic[char] = char_freq[char]
        
        dic['~'] = others_freq
        dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))

    nodes = []
    for key in dic:
        node = Node(key, dic[key])
        nodes.append(node)

    i = len(nodes)
    while i > 2:
        first_min = nodes.pop()
        second_min = nodes.pop()
        parent_freq = first_min.freq + second_min.freq

        parent = Node(None, parent_freq)
        parent.left = first_min
        parent.right = second_min

        pos = 0
        for item in nodes:
            if(item.freq > parent_freq):
                pos += 1
                continue
            else:
                nodes.insert(pos, parent)
                break
        i -= 1

    
    root = Node(None, len_txt)
    root.left = nodes.pop()
    root.right = nodes.pop()

    codes_dic = {}
    gen_codes(root, 'temp',  codes_dic)
    print(codes_dic)

    if dic.get('~'):
        i = len(dic) - 1
        val= codes_dic["~"]
        bit_len= len(char_freq).bit_length()
        others.sort()
        others_codes = {}
        for char in others:
            value = val + format(i, f"0{bit_len}b")
            others_codes[char] = value
            i += 1

    encoded_txt = encode(txt, codes_dic, (others_codes if dic.get('~') else {}))
    comp_stream = adding_overhead(codes_dic, (others_codes if dic.get('~') else {}), encoded_txt)
    return comp_stream

def encode(txt, huff_codes, others_codes):
    total_codes = huff_codes | others_codes
    result = ""
    for char in txt:
        result += f"{total_codes[char]}"
    return result

def adding_overhead(huff_codes, others_codes, txt_bin):
    n = len(huff_codes)
    m = len(others_codes)

    dics = ""
        
    for key in huff_codes:
        dics += format(ord(key), '08b') + format(len(huff_codes[key]), f'04b') + huff_codes[key]

    for key in others_codes:
        dics += format(ord(key), '08b') + others_codes[key]


    result = dics + txt_bin
    result_len = len(result)

    padding = (8-(result_len) % 8) % 8
    
    result = format(padding, "08b") + result
    result = format(m, '08b') + result
    result = format(n, '08b') + result

    result += padding * '0'
    
    return result

def save_binary(comp_stream):
    comp_len = len(comp_stream)
    with open('output.bin', 'wb') as file:
        for i in range(0,comp_len, 8):
            byte = int(comp_stream[i:i+8], 2)
            file.write(bytes([byte]))

#    n        m        p        char     codelen  code                   ochar   code
# ******** ******** ******** ( ********   ****    ??   ) => n times  (  ********  ???  ) => m times