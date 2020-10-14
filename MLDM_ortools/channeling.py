from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = model.NewIntVar(0, 10, 'x')
y = model.NewIntVar(0, 10, 'y')
b = model.NewBoolVar('b')

# if x > 5 then y == 3 otherwise y == 2
model.Add(x > 5).OnlyEnforceIf(b)
model.Add(x <= 5).OnlyEnforceIf(b.Not())
model.Add(y == 3).OnlyEnforceIf(b)
model.Add(y == 2).OnlyEnforceIf(b.Not())


model.Maximize(x + y)
solver = cp_model.CpSolver()
status = solver.Solve(model)
print(f'status: {solver.StatusName(status)}')
print(solver.Value(x), solver.Value(y))
