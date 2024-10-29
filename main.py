import sys

def negate(l1, l2):
    if l1 == ('~' + l2) or l2 == ('~' + l1):
        return True
    else:
        return False
    
def tautology_check(resolved):
    for r1 in resolved:
        for r2 in resolved:
            if negate(r1, r2):
                return True
    return False

def redundant_check(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

def resolve(clauses, c1, c2):
    # Combine c1 and c2 and use list comprehension to remove duplicates
    resolved = list(set(c1 + c2))  # Using `set` to remove duplicates right away
    ors = resolved.copy()  # Copy for comparison later

    # Identify and remove negated pairs
    for l1 in c1:
        for l2 in c2:
            if negate(l1, l2):
                resolved = [literal for literal in resolved if literal != l1 and literal != l2]
                
                # Check for contradiction
                if len(resolved) == 0:
                    return False
                # Check if the clause is trivially true
                elif tautology_check(resolved):
                    return True
                # Check for redundancy
                else:
                    for cl in clauses:
                        if redundant_check(resolved, cl) == []:
                            return True
                    return resolved  # Return new clause if it's informative

    # Final check to return True if no changes were made to `resolved`
    if resolved == ors:
        return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file>")
        sys.exit(1)

    clause_number = 1
    clauses = []
    with open(sys.argv[1], errors='ignore') as input_file:
        for line in input_file:
            line = line.strip()
            line = line.split(" ")
            clauses.append(line) 
        
    validation_clause = clauses[-1]
    del clauses[-1]

    for clause in clauses:
        print(clause_number, ". ", ' '.join(clause), " {}", sep='')
        clause_number += 1

    for clause in range(len(validation_clause)):
        if '~' in validation_clause[clause]:
            validation_clause[clause] = validation_clause[clause].replace('~', '')
        else:
            validation_clause[clause] = '~' + validation_clause[clause]

    for clause in validation_clause:
        clauses.append([clause])
        print(clause_number, ". ", ' '.join([clause]), " {}", sep='')
        clause_number += 1

    cli = 1
    while cli < clause_number - 1:
        clj = 0
        while clj < cli:
            #print("testing",cli, clj)
            result = resolve(clauses, clauses[cli], clauses[clj])
            if result is False:
                print(clause_number, ". ","Contradiction", ' {', cli + 1, ", ", clj + 1, '}', sep='')
                clause_number += 1
                print("Valid")
                sys.exit(0)
            elif result is True:
                clj += 1
                continue
            else:
                print(clause_number, ". ",' '.join(result), ' {', cli + 1, ", ", clj + 1, '}', sep='')
                clause_number += 1
                clauses.append(result)
            clj += 1
        cli += 1
    print('Not Valid')

if __name__ == '__main__':
    main()
