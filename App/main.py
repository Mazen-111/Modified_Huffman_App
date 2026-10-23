import compression as comp
import decompression as decomp

def compress(txt, thrs):
    comp_stream = comp.Modified_Huffman(txt, thrs)
    return comp_stream

def save_binary(comp_stream):
    comp.save_binary(comp_stream)

def decompress_txt(txt):
    result = decomp.decompress(txt)
    return result

def decompress_bin_file(file_name):
    txt = decomp.read_binary(file_name)
    result = decomp.decompress(txt)
    return result

def menu():
    print("==================================================")
    print("|     WELCOME TO THE HUFFMAN COMPRESSION APP     |")
    print("==================================================")
    choice = input("Please select an option:\n1. Compress a text\n2. Decompress a binary stream\n")
    if choice == "1":
        txt = input("Please enter a text to compress: ")
        thrs = float(input("Enter the threshold: "))
        save = input("Would you like to save the text in a binary file? ")
        if save.lower() == "yes" or save.lower() == "y":
            comp_stream = compress(txt, thrs)
            
            if comp_stream is None:
                print("The threshold is too high, compression is not possible.")
                return
            
            print(f"Compressed Stream: {comp_stream}")
            print("Compressed Stream saved in a binary file successfully...")
        else:
            comp_stream = compress(txt, thrs)
            
            if comp_stream is None:
                print("The threshold is too high, compression is not possible.")
                return
            save_binary(comp_stream)
            print(f"Compressed Stream: {comp_stream}")
    else:
        choice = input("Would you like to decompress a normal binary text or a binary file?\n1. Binary text\n2. Binary file\n")
        if choice == "1":
            txt = input("Enter the text you want to decompress:\n")
            result = decompress_txt(txt)
            print(f"Decompressed Stream: {result}")
        else:
            file_name = input("Enter the file name you want to decompress:\n")
            result = decompress_bin_file(file_name)
            print(f"Decompressed Stream: {result}")
        

menu()