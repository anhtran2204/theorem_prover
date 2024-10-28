import sys

def negate(l1, l2):
    if l1 == ('~' + l2) or l2 == ('~' + l1):
        return True
    else:
        return False

def resolve():
    pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file>")
        sys.exit(1)

    

if __name__ == '__main__':
    main()

