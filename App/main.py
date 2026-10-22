import compression as comp
import decompression as decomp

def compress(txt, thrs, save):
    comp_stream = comp.Modified_Huffman(txt, thrs)
    if save:
        comp.save_binary(comp_stream)
    return comp_stream

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
            comp_stream = compress(txt, thrs, True)
            print(f"Compressed Stream: {comp_stream}")
            print("Compressed Stream saved in a binary file successfully...")
        else:
            comp_stream = compress(txt, thrs, False)
            print(f"Compressed Stream: {comp_stream}")

menu()