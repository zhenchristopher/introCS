# Ran Libeskind-Hadas
# January 14, 2017
# argsDemo.py

# This file demonstrates getting input from the command line and 
# automatically invoking the main() function.

# Try this by typing the following at the terminal prompt:
# python argsDemo.py foo.png 42

import sys

def main():
    inputs = sys.argv
    print(inputs)
    columns = eval(inputs[2])
    print(columns)
    
if __name__ == '__main__': main()
