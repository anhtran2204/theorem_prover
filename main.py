import sys

def negate(l1, l2):
    if l1 == ('~' + l2) or l2 == ('~' + l1):
        return True
    else:
        return False

def resolve():
    pass

def print_resolution(clauses, p1=None, p2=None):
    num = 1
    for clause in clauses:
        if len(clause) > 1: 
            if p1 != None and p2 != None:
                print(f"{num}. {' '.join(clause)} {{p1, p2}}")
            else:
                print(f"{num}. {' '.join(clause)} {{}}")
        else:
            if p1 != None and p2 != None:
                print(f"{num}. {clause} {{p1, p2}}")
            else:
                print(f"{num}. {clause} {{}}")
        num += 1

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file>")
        sys.exit(1)

    clauses = []
    with open(sys.argv[1], errors='ignore') as input_file:
        for line in input_file:
            line = line.strip()
            line = line.split(" ")
            clauses.append(line) 
        
    validation_clause = clauses[-1]
    del clauses[-1]
    
    print_resolution(clauses)

if __name__ == '__main__':
    main()

