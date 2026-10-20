from collections import Counter

class Node:
    def __init__(self, sym, freq):
        self.left = None
        self.right = None
        self.sym = sym 
        self.freq = freq


def gen_codes(root, sym, dic, code = ''):
    if root == None:
        code = code[:-1]
        dic[sym] = code
        return

    sym = root.sym
    code += '0' 
    gen_codes(root.left, sym, dic, code)
    code = code[:-1]
    code += '1'
    gen_codes(root.right, sym, dic, code)
    code = code[:-1]

 
def Modified_Huffman(txt, threshold):
    len_txt = len(txt)

    char_freq = Counter(txt)
    dic = {}
    others = []
    others_freq = 0

    for char, freq in char_freq.most_common():
        if (freq / len_txt) <= threshold:
            others.append(char)
            others_freq += char_freq[char]
        else:
            dic[char] = char_freq[char]

    dic['or'] = others_freq
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

    i = len(dic) - 1
    val= codes_dic["or"]
    bit_len= len(char_freq).bit_length()
    others.sort()
    for char in others:
        codes_dic[char]  = val + format(i , f"0{bit_len}b")
        i += 1

    print(codes_dic)

    return codes_dic


Modified_Huffman("abcazdafcqdadcuabapd", 0.05)

# Output the compressed stream using the codes table
# Think about What you need to use in the decompression
