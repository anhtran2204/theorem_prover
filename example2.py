import sys
import re

def main():

    # error if there is an invalid number of arguments
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_kb_file>")
        sys.exit(1)

    # Counter for output
    counter = 1

    # get the input from the kb file
    clauses, test_clause = kb_file()

    # Negate test clause and add each literal as a clause due to ANDs in the negation
    negated_clause = negation(test_clause)
    clauses += [[lit] for lit in negated_clause]

    # initialize known clauses as a set of frozensets (this is my method of optimizing so that accesses and comparisons are faster, also removes duplication)
    known_clauses = {frozenset(clause) for clause in clauses}
    
    # print the initial clauses
    print_clauses(clauses, counter)
    # update counter
    counter += len(clauses)

    # Resolution!
    i = 1
    # loop through clauses
    # i is 1, j is 0, iterate j to i, then increase i. this way we can test the clause with EVERY previous clause
    while i < len(clauses):
        for j in range(i):
            # get the new clause from the resolve
            new_clause = resolve_clauses(clauses[i], clauses[j])
            # if there is no clause, go to the next iteration
            if new_clause is None:
                continue
            # if the clause is an empty set, we have a contradiction, so print that
            elif new_clause == []:
                print(f"{counter}. Contradiction {{{i + 1}, {j + 1}}}")
                print("Valid")
                return
            # otherwise, we check if the clause is known, and then added it to the known clauses, printing the clause
            elif set(new_clause) not in known_clauses:
                # print clause
                print_clause(list(new_clause), counter, i + 1, j + 1)
                # add to known clauses
                # add a frozen set so that it can be hashed
                known_clauses.add(frozenset(new_clause))
                # add the clause to the clauses list
                clauses.append(list(new_clause))
                # print the clause
                counter += 1
        i += 1
    print("Fail")


# resolve two clauses
def resolve_clauses(clause1, clause2):
    # combine the clauses
    resolved_clause = clause1 + clause2
    # remove duplicates
    resolved_clause = list(dict.fromkeys(resolved_clause))
    
    # checks to see if there are any literals in the clause that have a negated version in the clause as well
    # returns the literal that has a negation
    negations = [literal for literal in resolved_clause if ('~' + literal) in resolved_clause]
    
    # if there is a negation, then we remove the negation and its negated pair
    if len(negations) == 1: 
        # remove the negated pair
        resolved_clause.remove(negations[0])
        for lit in negations:
            resolved_clause.remove('~' + lit) 
        # check if there is a tautology (i.e. ~p V p is always true)
        if not tautology_check(set(resolved_clause)):
            # if there is no tautology, return the clause
            return resolved_clause
    return None

# check if there is a tautology
def tautology_check(clause):
    return any(lit in clause and ('~' + lit) in clause for lit in clause)

# negate a clause
def negation(clause):
    return [('~' + literal if literal[0] != '~' else literal[1:]) for literal in clause]

# read the input kb file
def kb_file():
    clauses = []
    # open the file
    with open(sys.argv[1], 'r') as file:
        lines = file.read().splitlines()
        # get the clauses
        clauses = [line.split() for line in lines[:-1]]
        # extract the test clause
        test_clause = lines[-1].split()
    return clauses, test_clause

# print all of the clauses
def print_clauses(clauses, start_counter):
    # loop through every clause in clauses
    for idx, clause in enumerate(clauses):
        # print the specific clause
        print_clause(clause, start_counter + idx)

# print a clause given the clauses, the current counter, and the parent
def print_clause(clause, counter, parent_i=None, parent_j=None):
    # create a string combining all of the literals in the clause into a single string
    clause_str = " ".join(clause)
    # if there exists a parent that the clause comes from, then we print the parents in the curly brackets
    if parent_i and parent_j:
        print(f"{counter}. {clause_str} {{{parent_i}, {parent_j}}}")
    # otherwise the brackets are empty
    else:
        print(f"{counter}. {clause_str} {{}}")

if __name__ == '__main__':
    main()