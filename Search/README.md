# Search Algorithms

In this project, the Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. The general search algorithms (BFS, DFS, UCS, A*, Heuristic) will be applied to Pacman scenarios.

In `search.py` file, I implemented the __BFS, DFS, USC, A*, and Heuristic__ for pacman to have different routes and behaviors to collect dots and the costs.

<br>

Files of main algorithms:

| File               | Description                                                    |
|--------------------|----------------------------------------------------------------|
| `search.py`        | Where all of the search algorithms reside.               |
| `searchAgents.py`  | Where all of the search-based agents reside.             |

Files you might want to look at:

| File               | Description                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------|
| `pacman.py`        | The main file that runs Pacman games. This file describes a Pacman GameState type.|
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

Then, I implemented the __DFS on graph__ in `depthFirstSearch` function in `search.py`.
Now test the result by:
```python
python pacman.py -l tinyMaze -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent
```
You should see the mediumMaze for **DFS** like this:

<img src='./images/search_1.png'>

```
[SearchAgent] using function depthFirstSearch
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 130 in 0.0 seconds
Search nodes expanded: 146
Pacman emerges victorious! Score: 380
Average Score: 380.0
Scores:        380.0
Win Rate:      1/1 (1.00)
Record:        Win
```

## 2. Breadth First Search
I implemented the __BFS on graph__ in the `breadthFirstSearch` function in `search.py`. 

We can test on the same way by running:
```python
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
```

You should see the mediumMaze for **BFS** like this:

<img src='./images/search_2.png'>

```
[SearchAgent] using function bfs
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 68 in 0.0 seconds
Search nodes expanded: 269
Pacman emerges victorious! Score: 442
Average Score: 442.0
Scores:        442.0
Win Rate:      1/1 (1.00)
Record:        Win
```

## 3. Varying the Cost Function
UCS: an uninformed search that performs a search based on the loweset path cost.

While BFS will find a fewest-actions path to the goal, we might want to find paths that are “best” in other senses. Consider `mediumDottedMaze` and `mediumScaryMaze`.

By changing the cost function, we can encourage Pacman to find different paths. For example, we can charge more for dangerous steps in ghost-ridden areas or less for steps in food-rich areas, and a rational Pacman agent should adjust its behavior in response.

I implemented the __uniform-cost graph search algorithm__ in the `uniformCostSearch` function in `search.py`. The result of `UCS` is the same as `BFS`, which you can refer above.

We can run the tests by:
```python
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
```

You should see the mediumDottedMaze:

<img src='./images/search_3.png'>

which results in higher scores because we encourage pacman to eat more dots as part of our cost function.
```
Path found with total cost of 1 in 0.0 seconds
Search nodes expanded: 186
Pacman emerges victorious! Score: 646
Average Score: 646.0
Scores:        646.0
Win Rate:      1/1 (1.00)
Record:        Win
```

<br>

And the mediumScaryMaze:

<img src='./images/search_3_1.png'>

```
Path found with total cost of 68719479864 in 0.0 seconds
Search nodes expanded: 108
Pacman emerges victorious! Score: 418
Average Score: 418.0
Scores:        418.0
Win Rate:      1/1 (1.00)
Record:        Win
```

## 4. A* search
A*: an informed search f(n) = g(n) + h(n). g(n) is the cost of the path from the start node to n, and h(n) is a heuristic function that estimates the cost of the cheapest path from n to the goal.

I implemented __A* graph search__ in the empty function `aStarSearch` in `search.py`. A* takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). The `nullHeuristic` heuristic function in `search.py` is a trivial example.

You can test your A* implementation on the original problem of finding a path through a maze to a fixed position using the Manhattan distance heuristic (implemented already as `manhattanHeuristic` in `searchAgents.py`).

```python
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

<img src='./images/search_4.png' width=600>

A* finds the optimal solution slightly faster than uniform cost search (about 549 vs. 620 search nodes expanded in our implementation, but ties in priority may make your numbers differ slightly).

```
[SearchAgent] using function astar and heuristic manhattanHeuristic
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 68 in 0.0 seconds
Search nodes expanded: 221
Pacman emerges victorious! Score: 442
Average Score: 442.0
Scores:        442.0
Win Rate:      1/1 (1.00)
Record:        Win
```

## 5. Finding All the Corners
