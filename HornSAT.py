def check_horn_satisfiability(clauses):
    assignment = set()  # Set of variables assigned to True
    
    def propagate():
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                if all(lit in assignment if not lit.startswith('not ') else lit[4:] not in assignment 
                       for lit in clause[:-1]):
                    if clause[-1].startswith('not '):
                        if clause[-1][4:] in assignment:
                            return False  # Contradiction found
                    elif clause[-1] not in assignment:
                        assignment.add(clause[-1])
                        changed = True
        return True

    # First, set all unit clauses to True
    for clause in clauses:
        if len(clause) == 1:
            if clause[0].startswith('not '):
                if clause[0][4:] in assignment:
                    return False  # Contradiction in unit clauses
            else:
                assignment.add(clause[0])

    # Then propagate implications
    return propagate()

def parse_clause(clause_str):
    return clause_str.replace(',', ' ').split()

def get_clauses_from_user():
    print("Enter Horn clauses, one per line. Use 'not' for negation.")
    print("Enter an empty line to finish.")
    
    clauses = []
    while True:
        clause_str = input("Enter clause (or empty line to finish): ").strip()
        if not clause_str:
            break
        clauses.append(parse_clause(clause_str))
    return clauses

def main():
    while True:
        clauses = get_clauses_from_user()
        if not clauses:
            print("No clauses entered. Exiting.")
            break
        
        print("\nClauses entered:")
        for clause in clauses:
            print(clause)
        
        is_satisfiable = check_horn_satisfiability(clauses)
        print(f"\nResult: The Horn formula is {'satisfiable' if is_satisfiable else 'unsatisfiable'}.")
        
        again = input("\nDo you want to check another formula? (yes/no): ").strip().lower()
        if again != 'yes':
            break

    print("Fin")

if __name__ == "__main__":
    main()