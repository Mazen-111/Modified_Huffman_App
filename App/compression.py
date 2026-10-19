from collections import Counter

class Parent:
    def __init__(self, code, right, left):
        self.code = code
        self.right = right
        self.left = left
        pass

class Leaf:
    def __init__(self, code, char):
        self.code = code
        self.char = char
        pass

txt = input("Enter the text to be compressed: ")
thrs = input("Enter the 'Others' group threshold: ")

others = []
parents = []
min_pairs = []
new_dict = {}
other_prob = 0
probs = dict(Counter(txt))

for char in probs:
    if probs[char] <= int(thrs):
        others.append(char)
        others_prob += probs[char]
    else:
        new_dict[char] = probs[char]
new_dict['others'] = others_prob
temp_dict = new_dict

for i in range(len(probs) - 1):
    min1 = min(temp_dict, key=temp_dict.get)
    temp_dict.popitem(min1)
    min2 = min(temp_dict, key=temp_dict.get)
    temp_dict.popitem(min2)
    temp_dict[min1 + min2] = new_dict[min1] + new_dict[min2]
    min_pairs.insert(0, (min1, min2))

for pair in min_pairs:
    if pair[0] in new_dict and pair[1] in new_dict:
        parents.append(Parent(None, Leaf(None, pair[0]), Leaf(None, pair[1])))
    elif pair[0] in new_dict:
        parents.append(Parent(None, Leaf(None, pair[0]), pair[1]))
    elif pair[1] in new_dict:
        parents.append(Parent(None, pair[0], Leaf(None, pair[1])))
    else:
        parents.append(Parent(None, pair[0], pair[1]))