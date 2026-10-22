def read_binary():
    with open('output.bin', 'rb') as file:
        byte = file.read(1)
        result = ""
        while byte:
            result += format(ord(byte), '08b')
            byte = file.read(1)
    return result

def read_bits():
    stream = read_binary()
    n = int(stream[:8], 2)
    m = int(stream[8:16], 2)
    padding = int(stream[16:24], 2)

    base_dict = {}
    i = 24
    for _ in range(n):
        asc = int(stream[i:i+8],2)
        char = chr(asc)

        code_len = int(stream[i+8 : i+12], 2)
        code = stream[i+12 : i+12+code_len]

        base_dict[char] = code
        i += 12 + code_len
    
    o_prefix_len = len(base_dict['~'])
    fixed_code_len = (n+m-1).bit_length()
    others_code_length = o_prefix_len + fixed_code_len

    for _ in range(m):
        asc = int(stream[i:i+8],2) 
        char = chr(asc)
        code = stream[i+8 : i+8 + others_code_length]
        base_dict[char] = code
        i += 8 + others_code_length

    compStream = stream[i :(len(stream)-padding)]

    return base_dict, compStream

def decompress():
    base_dict, comp_stream = read_bits()

    reverse = {code: char for char, code in base_dict.items() if char != '~'}

    result = []
    cur = ''
    for bit in comp_stream:
        cur += bit
        if cur in reverse:
            result.append(reverse[cur])
            cur = ''
    return ''.join(result)