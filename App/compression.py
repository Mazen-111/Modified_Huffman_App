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

    i = len(dic) - 1
    val= codes_dic["~"]
    bit_len= len(char_freq).bit_length()
    others.sort()
    others_codes = {}
    for char in others:
        value = val + format(i, f"0{bit_len}b")
        others_codes[char] = value
        i += 1

    print(codes_dic)

    return codes_dic, others_codes

def results(txt, codes_dic):
    result = ""
    for char in txt:
        result += f"{codes_dic[char]}"
    return result

codes1, codes2 = Modified_Huffman("abcazdafcqdadcuabapd", 0.05)

def results_bin(codes1, codes2, txt_bin):
    result = ""
    n = len(codes1)
    m = len(codes2)
    
    huffcodes_bits = n.bit_length()
    otherscodes_bits = n.bit_length() + (n-1+m).bit_length()
    
    for key in codes1:
        result += format(ord(key), '08b') + str((huffcodes_bits-len(codes1[key]))*'0' + codes1[key])
    
    for key in codes2:
        result += format(ord(key), '08b') + str((otherscodes_bits-len(codes2[key]))*'0' + codes2[key])
    
    result += txt_bin
    lenlen = len(result)
    padding = (8-(lenlen) % 8) % 8
    
    result += padding*'0'
    result = format(padding, f"0{3}b") + result

    result = format(m, f"0{7}b")  + result
    result = format(n, f"0{7}b") + result
    
    
    
    return result
#header: len of the char in the first table => n in byte 
#        len of char of the others => m in byte            (n).bit_length + (n-1+m).bit_length
#        byte for num of padding
#        byte for every char and num of bits constant we it by the log n => num of bits n times
#        and byte for every char in other and num of bits we know it by sum of num of bits and log n m
#        read a byte and then num of bits   

#headr:   
total_codes = codes1 | codes2
resultts = results("abcazdafcqdadcuabapd", total_codes)
print(resultts)

resultts_bin = results_bin(codes1, codes2, resultts)
print(resultts_bin)
# Output the compressed stream using the codes table
# Think about What you need to use in the decompression

def read_bin(stream):
    n = int(stream[:7], 2)
    m = int(stream[7:14], 2)
    
    padding = int(stream[14:17], 2)
    
    HuffCodes_bits = n.bit_length()
    othersCodes_bits = n.bit_length() + (n-1+m).bit_length()
    
    endOfft = n*8 + n*HuffCodes_bits + 17
    endOfSt = m*8 + m*othersCodes_bits + endOfft
    
    base_dict = {}
    for i in range(17, endOfft, (8+HuffCodes_bits)):
        asc = int(stream[i:i+8],2)
        char = chr(asc)
        code = stream[i+8:i+8+HuffCodes_bits]
        base_dict[char] = code
    
    for i in range(endOfft, endOfSt, (8+othersCodes_bits)):
        asc = int(stream[i:i+8],2)
        char = chr(asc)
        code = stream[i+8:i+8+othersCodes_bits]
        base_dict[char] = code

    compStream = stream[endOfSt:(len(stream)-padding)]

    print(compStream)

    
        
    print(base_dict)

read_bin(resultts_bin)