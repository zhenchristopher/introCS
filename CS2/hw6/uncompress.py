# Christopher Zhen
# February 14, 2017
# uncompress.py

# This file has all the necessary classes and functions to run Huffman 
# decompression given a Huffman Key file and the compressed Huffmann file

def main():
    ''' Main file for uncompression '''
    file = str(input("Enter a file to uncompress: "))
    if file[len(file)-8:] != ".HUFFMAN":
        raise ValueError("file doesn't end in .HUFFMAN")
    finalCode = buildCode(file + '.KEY')
    decoded = decode(file, finalCode)
    finalFile = open(file + ".DECODED", 'w')
    finalFile.write(decoded)
    finalFile.close()

def buildCode(file):
    ''' Build the Huffman key from the file '''
    f = open(file, 'r')
    code = f.read().splitlines()
    finalCode = {}
    i = 2
    while i < len(code):
        if code[i] == '':
            #special case where symbol is \n
            i += 1
            finalCode[code[i]] = "\n"
        else:
            finalCode[code[i][1:]] = code[i][0]
        i += 1
    return finalCode

def decode(file, finalCode):
    f = open(file, 'rb')
    readBytes = f.read()
    f.close()
    listOfBytes = list(readBytes)
    bitString = ''
    for byte in listOfBytes:
        #convert byte to bits and append to string
        bitString += (bin(byte)[2:]).zfill(8)
    huffByte = ''
    decoded = ''
    for bit in bitString:
        huffByte += bit
        if huffByte in finalCode:
            #add decoded bit to string
            decoded += finalCode[huffByte]
            huffByte = ''
    return decoded

if __name__ == '__main__':
    main()