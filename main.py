import sys
import cProfile

# negate a clause
def negate(clause):
    negated_clause = clause.copy()
    for lit in range(len(negated_clause)):
        if '~' in negated_clause[lit]:
            negated_clause[lit] = negated_clause[lit].replace('~', '')
        else:
            negated_clause[lit] = '~' + negated_clause[lit]
    return negated_clause

def isNegation(l1, l2):
    if l1 == ('~' + l2) or l2 == ('~' + l1):
        return True
    return False
    
# check if the clause is trivially true
def tautology_check(resolved):
    for l1 in resolved:
        for l2 in resolved:
            if isNegation(l1, l2):
                return True
    return False

# resolve clauses using resolution principle
def resolve(c1, c2):
    resolved_clause = c1 + c2
    resolved_clause = list(dict.fromkeys(resolved_clause))  # Using `set` to remove duplicates right away
    ors = resolved_clause.copy()  # Copy for comparison later

    # Identify and remove negated pairs
    for l1 in c1:
        for l2 in c2:
            if isNegation(l1, l2):
                resolved = [literal for literal in resolved_clause if literal != l1 and literal != l2]
                
                # Check for contradiction
                if len(resolved) == 0:
                    return False
                # Check if the clause is trivially true
                elif tautology_check(resolved):
                    return True
                # Check for redundancy
                else:
                    return resolved  # Return new clause if it's informative

    # Final check to return True if no changes were made to `resolved`
    if resolved_clause == ors:
        return True

def print_initial_clauses(clauses):
    start = 1
    for num, clause in enumerate(clauses):
        print_clause(num + start, clause)

def print_clause(clause_number, clause, result=None, parent_1=None, parent_2=None):
    if parent_1 and parent_2:
        if result:
            print(f"{clause_number}. {result} {{{parent_1}, {parent_2}}}")
        else:
            print(f"{clause_number}. {' '.join(clause)} {{{parent_1}, {parent_2}}}")
    else:
        print(f"{clause_number}. {' '.join(clause)} {{}}")

# main function
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

    validation_clause = negate(validation_clause)
    clauses += [[lit] for lit in validation_clause]

    clause_number = len(clauses)
    print_initial_clauses(clauses)
    clause_number += 1
    
    cli = 1
    while cli < clause_number - 1:
        clj = 0
        while clj < cli:
            resolved_clause = resolve(clauses[cli], clauses[clj])
            if resolved_clause is False:
                print_clause(clause_number, resolved_clause, "Contradiction", cli + 1, clj + 1)
                print("Valid")
                return
            elif resolved_clause is True:
                clj += 1
                continue
            else:
                print_clause(clause_number, resolved_clause, cli + 1, clj + 1)
                clauses.append(list(resolved_clause))
                clause_number += 1
            clj += 1
        cli += 1
    print("Fail")
    # cli = 1
    # while cli < clause_number - 1:
    #     clj = 0
    #     while clj < cli:
    #         #print("testing",cli, clj)
    #         result = resolve(clauses, clauses[cli], clauses[clj])
    #         if result is False:
    #             print(clause_number, ". ","Contradiction", ' {', cli + 1, ", ", clj + 1, '}', sep='')
    #             clause_number += 1
    #             print("Valid")
    #             sys.exit(0)
    #         elif result is True:
    #             clj += 1
    #             continue
    #         else:
    #             print(clause_number, ". ",' '.join(result), ' {', cli + 1, ", ", clj + 1, '}', sep='')
    #             clauses.append(result)
    #             clause_number += 1
    #         clj += 1
    #     cli += 1
    # print('Fail')

if __name__ == '__main__':
    # main()
    cProfile.run('main()')
