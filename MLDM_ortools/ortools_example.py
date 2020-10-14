from pprint import pprint

from ortools.sat.python import cp_model, cp_model_helper


class SolutionCallback(cp_model.CpSolverSolutionCallback):

    def __init__(self, var_x, var_y, limit=10):
        super(SolutionCallback, self).__init__()
        self.var_x = var_x
        self.var_y = var_y
        self.limit = limit
        self.solutions = []
    
    def on_solution_callback(self):
        if len(self.solutions) >= self.limit:
            self.StopSearch()
            return
        val_x = self.Value(self.var_x)
        val_y = self.Value(self.var_y)
        self.solutions.append((val_x, val_y))

if __name__ == '__main__':
    model = cp_model.CpModel()
    var_x = model.NewIntVar(3, cp_model_helper.INT32_MAX, 'x')
    var_y = model.NewIntVar(cp_model_helper.INT32_MIN, 4, 'y')
    model.Add(2*var_x+var_y == 100)

    solver = cp_model.CpSolver()
    callback = SolutionCallback(var_x, var_y)
    status = solver.SearchForAllSolutions(model, callback)
    pprint(f'status: {solver.StatusName(status)}')
    pprint(callback.solutions)
