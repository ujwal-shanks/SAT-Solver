from typing import List, Tuple, Set, Dict

def parse_2cnf(formula: str) -> List[Tuple[int, int]]:
    clauses = []
    for clause in formula.split('&'):
        literals = clause.strip()[1:-1].split('v')
        clauses.append((int(literals[0]), int(literals[1])))
    return clauses

def resolve(clause1: Tuple[int, int], clause2: Tuple[int, int]) -> Tuple[int, int] | None:
    if clause1[0] == -clause2[0]:
        return (clause1[1], clause2[1])
    if clause1[0] == -clause2[1]:
        return (clause1[1], clause2[0])
    if clause1[1] == -clause2[0]:
        return (clause1[0], clause2[1])
    if clause1[1] == -clause2[1]:
        return (clause1[0], clause2[0])
    return None

def resolution(clauses: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    result = set(clauses)
    changed = True
    while changed:
        changed = False
        new_clauses = set()
        for c1 in result:
            for c2 in result:
                if c1 != c2:
                    resolved = resolve(c1, c2)
                    if resolved and resolved not in result:
                        new_clauses.add(resolved)
                        changed = True
        result.update(new_clauses)
    return result

def check_sat(formula: str) -> Tuple[bool, Dict[int, bool] | None]:
    clauses = parse_2cnf(formula)
    resolved_clauses = resolution(clauses)
    
    # Check for contradictions
    for clause in resolved_clauses:
        if clause[0] == -clause[1]:
            return False, None  # Unsatisfiable
    
    # If no contradictions, the formula is satisfiable
    # We can now construct a satisfying assignment
    assignment = {}
    for clause in resolved_clauses:
        if clause[0] not in assignment and -clause[0] not in assignment:
            assignment[clause[0]] = True
        if clause[1] not in assignment and -clause[1] not in assignment:
            assignment[clause[1]] = True
    
    # Convert negative literals to their positive counterparts
    final_assignment = {abs(k): v for k, v in assignment.items()}
    
    return True, final_assignment

# Example usage
formula = "(1v2) & (-1v3) & (-2v-3)"
is_satisfiable, assignment = check_sat(formula)

print(f"Formula: {formula}")
print(f"Is satisfiable: {is_satisfiable}")
if is_satisfiable:
    print("Satisfying assignment:")
    for var, value in assignment.items():
        print(f"  {var}: {value}")
else:
    print("The formula is unsatisfiable.")
