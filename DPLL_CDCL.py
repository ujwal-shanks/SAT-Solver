from typing import List, Dict, Tuple, Optional
from collections import deque

class CDCLSolver:
    def __init__(self, clauses: List[List[str]]):
        self.clauses = clauses
        self.variables = set(abs(lit.replace('-', '')) for clause in clauses for lit in clause)
        self.assignment = {}
        self.level = 0
        self.decision_level = {}
        self.implication_graph = {}
        self.learned_clauses = []
        self.watches = {lit: [] for clause in clauses for lit in clause}
        for i, clause in enumerate(clauses):
            self.watches[clause[0]].append(i)
            self.watches[clause[1]].append(i)

    def solve(self) -> bool:
        while True:
            conflict = self.unit_propagate()
            if conflict:
                if self.level == 0:
                    return False
                backtrack_level = self.analyze_conflict(conflict)
                self.backtrack(backtrack_level)
            elif len(self.assignment) == len(self.variables):
                return True
            else:
                self.decide()

    def unit_propagate(self) -> Optional[List[str]]:
        propagation_queue = deque(self.assignment.keys())
        while propagation_queue:
            lit = propagation_queue.popleft()
            for clause_idx in self.watches[-lit]:
                clause = self.clauses[clause_idx]
                if self.clause_is_sat(clause):
                    continue
                unassigned = self.find_unassigned(clause)
                if not unassigned:
                    return clause
                if len(unassigned) == 1:
                    new_lit = unassigned[0]
                    self.assign(new_lit, clause)
                    propagation_queue.append(new_lit)
                else:
                    self.update_watch(clause_idx, -lit, unassigned[0])
        return None

    def clause_is_sat(self, clause: List[str]) -> bool:
        return any(lit in self.assignment for lit in clause)

    def find_unassigned(self, clause: List[str]) -> List[str]:
        return [lit for lit in clause if lit not in self.assignment and '-' + lit not in self.assignment]

    def update_watch(self, clause_idx: int, old_lit: str, new_lit: str):
        self.watches[old_lit].remove(clause_idx)
        self.watches[new_lit].append(clause_idx)
        clause = self.clauses[clause_idx]
        clause[clause.index(old_lit)] = new_lit

    def assign(self, lit: str, reason: Optional[List[str]] = None):
        self.assignment[lit] = True
        self.decision_level[lit.replace('-', '')] = self.level
        self.implication_graph[lit.replace('-', '')] = reason if reason else []

    def decide(self):
        self.level += 1
        for var in self.variables:
            if var not in self.assignment and '-' + var not in self.assignment:
                self.assign(var)
                return

    def analyze_conflict(self, conflict: List[str]) -> int:
        learned_clause = set(conflict)
        seen = set()
        current_level_count = 0
        while True:
            for lit in learned_clause:
                if lit.replace('-', '') not in seen:
                    seen.add(lit.replace('-', ''))
                    if self.decision_level[lit.replace('-', '')] == self.level:
                        current_level_count += 1
                    elif self.decision_level[lit.replace('-', '')] > 0:
                        learned_clause.update(self.implication_graph[lit.replace('-', '')])
            if current_level_count <= 1:
                break
            learned_clause = self.resolve(learned_clause)
            current_level_count -= 1
        self.learned_clauses.append(list(learned_clause))
        return max(self.decision_level[lit.replace('-', '')] for lit in learned_clause if self.decision_level[lit.replace('-', '')] < self.level)

    def resolve(self, clause: set) -> set:
        for lit in clause:
            if '-' + lit.replace('-', '') in self.implication_graph[lit.replace('-', '')]:
                return (clause | set(self.implication_graph[lit.replace('-', '')])) - {lit, '-' + lit.replace('-', '')}
        return clause

    def backtrack(self, level: int):
        self.level = level
        self.assignment = {lit: val for lit, val in self.assignment.items() if self.decision_level[lit.replace('-', '')] <= level}

def solve_sat(clauses: List[List[str]]) -> Optional[Dict[str, bool]]:
    solver = CDCLSolver(clauses)
    if solver.solve():
        return {var: (var in solver.assignment) for var in solver.variables}
    return None


clauses = [["A","B"], ["-A","B"]]
solve_sat(clauses)