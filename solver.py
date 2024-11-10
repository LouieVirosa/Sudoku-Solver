from datetime import datetime

import constraint

from puzzle import initial_puzzle

problem = constraint.Problem()

# Create initial 81 variables, each with domain of ints 1-9 unless we have an initial value
init_vals = {}
for row_count, row in enumerate(initial_puzzle, start=1):
    for col_count, val in enumerate(row, start=1):
        if val != 0:
            init_vals[(row_count, col_count)] = val

for row in range(1, 10):
    for col in range(1, 10):
        init_val = init_vals.get((row, col))
        if init_val:
            problem.addVariable((row, col), [init_val])
        else:
            problem.addVariable((row, col), range(1, 10))

# ==================== Sudoku general constraints =================================================
# All rows must have different integers in every variable
for row in range(1, 10):
    print("Adding a row constraint...")
    problem.addConstraint(constraint.AllDifferentConstraint(), [(row, col) for col in range(1, 10)])
    # TODO: Find out why the fuck this is so much slower:
    # problem.addConstraint(lambda *args: len(set(args)) == 9, [(row, col) for col in range(1, 10)])

# All cols must have different integers in every variable
for col in range(1, 10):
    print("Adding a column constraint...")
    problem.addConstraint(constraint.AllDifferentConstraint(), [(row, col) for row in range(1, 10)])

# All 3x3 matrices must have different integers in every variable
for matrix_row in range(1, 10, 3):
    for matrix_col in range(1, 10, 3):
        var_list = []
        for row in range(3):
            for col in range(3):
                var_list.append((matrix_row + row, matrix_col + col))
        print("Adding a 3x3 matrix constraint...")
        problem.addConstraint(constraint.AllDifferentConstraint(), var_list)


start_time = datetime.now()
print(f"Starting at {start_time} seconds...")
solution = problem.getSolution()
end_time = datetime.now()
print(f"Starting at {end_time} seconds...")
print(f"(Took {(end_time - start_time)} seconds)")

# Print results (solutions are not in sorted order otherwise)
for row in range(1, 10):
    line = ""
    for col in range(1, 10):
        line += f"{solution[(row, col)]}"
    print(line)

