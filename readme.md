# Benders Decomposition Example

This repository contains two simple implementations of the Benders Decomposition example that is presented by Dr. Ray
Jian
Zhang. The YouTube video can be found here: [Youtube video](https://www.youtube.com/watch?v=vQzpydNOWDY).

Wikipedia page Benders Decomposition: [Wikipedia](https://en.wikipedia.org/wiki/Benders_decomposition)

A more extensive explanation of Benders Decomposition (in the context of Stochastic Programming) can be found in the
book "Introduction to Stochastic Programming" by Birge and
Louveaux: [Springer](https://link.springer.com/book/10.1007/978-1-4614-0237-4).

### 1. Installation

The example is implemented in Python and Gurobi, only requiring the Gurobipy-module. See also requirements.txt.

### 2. Code Execution

The code can be executed by either running the `benders.py` or `benders_no_model_rebuild.py` file, both leading to the
same solution.

In the first approach, the master problem is rebuilt from scratch in every iteration. The second approach reuses the
current state of the optimization model, therefore avoiding computational overhead when rebuilding and solving the
model. In both approaches, the generated linear programs of each iteration are stored as `.lp`-files in the root folder
of the project.