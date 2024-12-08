Hierarchical Task Network (HTN) planning has proven to be
an effective approach for addressing complex planning prob-
lems, particularly in dynamic and uncertain environments.
By breaking down tasks into hierarchically structured sub-
tasks, HTN planners provide a natural and computationally
efficient way to address planning challenges.
This project integrates GTPyhop, a Python-based HTN
planner, with the Cliff Walking domain from OpenAI’s
ToyText Gym environment. The primary goal is to eval-
uate GTPyhop’s performance in solving planning problems
as the complexity of the environment increases. Specifically,
the project aims to investigate how search time and task suc-
cess rate are affected by changes in environmental parame-
ters, such as grid size and obstacle density.
There are 2 different implementations, deterministic and non-deterministic, each of which is implemented using gtpyhop environment.
deterministic.py -> deterministic implementation and test cases
non-deterministic.py -> non-deterministic domain and test cases
the txt files are some of the results
plot.py plot the result written in text file
