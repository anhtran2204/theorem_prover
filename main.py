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
    resolved_clause = list(dict.fromkeys(c1 + c2))  # Using `set` to remove duplicates right away
    
     # Find pairs of literals that are negations of each other between c1 and c2
    for l1 in c1:
        for l2 in c2:
            if isNegation(l1, l2):
                # Remove the negated pair from the resolved clause
                temp_resolved = [lit for lit in resolved_clause if lit != l1 and lit != l2]

                # Check for tautology
                if tautology_check(temp_resolved):
                    return True  # Represents a tautology, so we skip adding it

                # If the resolved clause is empty, it indicates a contradiction
                if not temp_resolved:
                    return False  # Represents a contradiction

                # Check if the resolved clause is already known
                return temp_resolved  # Return the resolved clause without tautologies or contradictions

    return True  # Return True if no resolution was possible

def print_initial_clauses(clauses, clause_number):
    for num, clause in enumerate(clauses):
        print_clause(num + clause_number, clause)

def print_clause(clause_number, clause, parent_1=None, parent_2=None, result=None):
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
    knowledge_base = []
    with open(sys.argv[1], errors='ignore') as input_file:
        for line in input_file:
            line = line.strip()
            line = line.split(" ")
            knowledge_base.append(line) 
        
    validation_clause = knowledge_base[-1]
    del knowledge_base[-1]

    validation_clause = negate(validation_clause)
    knowledge_base += [[lit] for lit in validation_clause]

    resolved_clauses = {frozenset(clause) for clause in knowledge_base}
    print_initial_clauses(knowledge_base, clause_number)
    clause_number = len(knowledge_base)
    clause_number += 1
    
    cli = 1
    while cli < clause_number - 1:
        clj = 0
        while clj < cli:
            resolved_clause = resolve(knowledge_base[cli], knowledge_base[clj])
            if resolved_clause is False:
                print_clause(clause_number, resolved_clause, cli + 1, clj + 1, "Contradiction")
                print("Valid")
                return
            elif resolved_clause is True:
                clj += 1
                continue
            elif set(resolved_clause) not in resolved_clauses:
                print_clause(clause_number, resolved_clause, cli + 1, clj + 1)
                resolved_clauses.add(frozenset(resolved_clause))
                knowledge_base.append(list(resolved_clause))
                clause_number += 1
            clj += 1
        cli += 1
    print("Fail")

if __name__ == '__main__':
    # main()
    cProfile.run('main()')
