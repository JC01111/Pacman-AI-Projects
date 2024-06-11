# Search Algorithms

In this project, the Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. The general search algorithms (BFS, DFS, UCS, A*, Heuristic) will be applied to Pacman scenarios.

<br>

Files of main algorithms:

| File               | Description                                                    |
|--------------------|----------------------------------------------------------------|
| `search.py`        | Where all of search algorithms will reside.               |
| `searchAgents.py`  | Where all of search-based agents will reside.             |

Files you might want to look at:

| File               | Description                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------|
| `pacman.py`        | The main file that runs Pacman games. This file describes a Pacman GameState type, which you use in this project. |
| `game.py`          | The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid. |
| `util.py`          | Useful data structures for implementing search algorithms.                                          |

Supporting files you can ignore:

| File                  | Description                           |
|-----------------------|---------------------------------------|
| `graphicsDisplay.py`  | Graphics for Pacman                   |
| `graphicsUtils.py`    | Support for Pacman graphics           |
| `textDisplay.py`      | ASCII graphics for Pacman             |
| `ghostAgents.py`      | Agents to control ghosts              |
| `keyboardAgents.py`   | Keyboard interfaces to control Pacman |
| `layout.py`           | Code for reading layout files and storing their contents |
| `autograder.py`       | Project autograder                    |
| `testParser.py`       | Parses autograder test and solution files |
| `testClasses.py`      | General autograding test classes      |
| `test_cases/`         | Directory containing the test cases for each question |
| `searchTestClasses.py`| Project specific autograding test classes |

<br>

## 1. Finding a Fixed Food Dot using Depth First Search
In `searchAgents.py`, the fully implemented `SearchAgent` plans out a path through Pacman’s world and then executes that path step-by-step.

First, test that the `SearchAgent` is working correctly by running:
```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch
```

Graph
