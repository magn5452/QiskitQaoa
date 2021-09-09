from matplotlib import pyplot as plt

from VehicleRouting.standard.Problem import Problem
from VehicleRouting.standard.QuantumProgram import QuantumProgram
from VehicleRouting.standard.factories.Experiment1ProblemFactory import Experiment1ProblemFactory

problem_factory = Experiment1ProblemFactory()
problem = Problem(problem_factory)
program = QuantumProgram(problem)
program.run()

plt.show()
