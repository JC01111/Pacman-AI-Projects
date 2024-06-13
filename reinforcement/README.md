# Reinforcement Learning

In this project, the Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. The value iteration and Q-learning of Reinforcement Learning techniques will be applied to pacman scenarios for pacman to have different routes and behaviors to collect dots and the costs.

Click on the [implemented]() (example) to look at specific function.

<br>

Files of main algorithms:

| File                     | Description                                                       |
|--------------------------|-------------------------------------------------------------------|
| `valueIterationAgents.py`| A value iteration agent for solving known MDPs.                   |
| `qlearningAgents.py`     | Q-learning agents for Gridworld, Crawler and Pacman.              |
| `analysis.py`            | A file to put your answers to questions given in the project.     |

Files you might want to look at:

| File                     | Description                                                                                         |
|--------------------------|-----------------------------------------------------------------------------------------------------|
| `mdp.py`                 | Defines methods on general MDPs.                                                                    |
| `learningAgents.py`      | Defines the base classes `ValueEstimationAgent` and `QLearningAgent`, which your agents will extend.|
| `util.py`                | Utilities, including `util.Counter`, which is particularly useful for Q-learners.                   |
| `gridWorld.py`           | The Gridworld implementation.                                                                       |
| `featureExtractors.py`   | Classes for extracting features on (state, action) pairs. Used for the approximate Q-learning agent (in `qlearningAgents.py`).|

Supporting files you can ignore:

| File                      | Description                                                                                        |
|---------------------------|----------------------------------------------------------------------------------------------------|
| `environment.py`          | Abstract class for general reinforcement learning environments. Used by `gridWorld.py`.            |
| `graphicsGridworldDisplay.py`| Gridworld graphical display.                                                                   |
| `graphicsUtils.py`        | Graphics utilities.                                                                               |
| `textGridworldDisplay.py` | Plug-in for the Gridworld text interface.                                                         |
| `crawler.py`              | The crawler code and test harness. You will run this but not edit it.                              |
| `graphicsCrawlerDisplay.py`| GUI for the crawler robot.                                                                        |
| `autograder.py`           | Project autograder.                                                                               |
| `testParser.py`           | Parses autograder test and solution files.                                                        |
| `testClasses.py`          | General autograding test classes.                                                                 |
| `test_cases/`             | Directory containing the test cases for each question.                                            |
| `reinforcementTestClasses.py`| Project 3 specific autograding test classes.                                                   |

<br>

## 1. Value Iteration

The Bellman equation for value iteration state update is given by:

$$ V_{k+1}(s) \leftarrow \max_{a} \sum_{s'} T(s, a, s') \left[ R(s, a, s') + \gamma V_k(s') \right] $$

I first [wrote](https://github.com/JC01111/Pacman-AI-Projects/blob/d5a9f975cb093dc2b435a2e908bd685593748900/reinforcement/valueIterationAgents.py#L62) a value iteration agent in `ValueIterationAgent`, this is an offline planner, not a reinforcement learning agent. `ValueIterationAgent` takes an MDP on construction and runs value iteration for the specified number of iterations before the constructor returns.

Value iteration computes _k_-step estimates of the optimal values, $V_k$. In addition to `runValueIteration`, I also implemented the following methods for `ValueIterationAgent` using $V_k$:

- [`computeActionFromValues(state)`](https://github.com/JC01111/Pacman-AI-Projects/blob/d5a9f975cb093dc2b435a2e908bd685593748900/reinforcement/valueIterationAgents.py#L97) computes the best action according to the value function given by `self.values`.
- [`computeQValueFromValues(state, action)`](https://github.com/JC01111/Pacman-AI-Projects/blob/d5a9f975cb093dc2b435a2e908bd685593748900/reinforcement/valueIterationAgents.py#L85) returns the Q-value of the (state, action) pair given by the value function given by `self.values`.

We can test the implementation by:
```python
python gridworld.py -a value -i 100 -k 10
python gridworld.py -a value -i 5
```

<img src="../images/rl_1.png" width=450>

```
EPISODE 1 COMPLETE: RETURN WAS 0.47829690000000014

AVERAGE RETURNS FROM START STATE: 0.47829690000000014
```

## 2. Policies
Now we have a `DiscountGrid` layout, shown below.  This grid has two terminal states with positive payoff (in the middle row), a close exit with payoff +1 and a distant exit with payoff +10. The bottom row of the grid consists of terminal states with negative payoff (shown in red); each state in this “cliff” region has payoff -10. The starting state is the yellow square. We distinguish between two types of paths: (1) paths that “risk the cliff” and travel near the bottom row of the grid; these paths are shorter but risk earning a large negative payoff, and are represented by the red arrow in the figure below. (2) paths that “avoid the cliff” and travel along the top edge of the grid. These paths are longer but are less likely to incur huge negative payoffs. These paths are represented by the green arrow in the figure below.

<img src="../images/rl_2_1.png" width=420>

<br>

Now we want to choose settings of the __discount, noise, and living reward__ parameters for this MDP to produce optimal policies of several different types. The setting of the parameter values for each part should have the property that, if the agent followed its optimal policy without being subject to any noise, it would exhibit the given behavior. If a particular behavior is not achieved for any setting of the parameters, assert that the policy is impossible by returning the string 'NOT POSSIBLE'.

1. Prefer the close exit (+1), risking the cliff (-10): <br>
    discount = 0.4, noise = 0.01, livingReward = -0.8
    
    Which can be tested by running:
   ```python
   python gridworld.py -g DiscountGrid -a value --discount 0.4 --noise 0.01 --livingReward -0.8
   ```

    <img src="../images/rl_2_2.gif" width=400>

3. Prefer the close exit (+1), but avoiding the cliff (-10): <br>
    discount = 0.01, noise = 0.01, livingReward = 0.9
    
    Which can be tested by running:
   ```python
   python gridworld.py -g DiscountGrid -a value --discount 0.01 --noise 0.01 --livingReward 0.9
   ```

    <img src="../images/rl_2_3.gif" width=400>

5. Prefer the distant exit (+10), risking the cliff (-10): <br>
    discount = 0.8, noise = 0.01, livingReward = -0.8
    
    Which can be tested by running:
   ```python
   python gridworld.py -g DiscountGrid -a value --discount 0.8 --noise 0.01 --livingReward -0.8
   ```

    <img src="../images/rl_2_4.gif" width=400>

7. Prefer the distant exit (+10), avoiding the cliff (-10): <br>
    discount = 0.9, noise = 0.2, livingReward = 0.9
    
    Which can be tested by running:
    ```python
   python gridworld.py -g DiscountGrid -a value --discount 0.9 --noise 0.2 --livingReward 0.9
    ```

   <img src="../images/rl_2_5.gif" width=400> 

9. Avoid both exits and the cliff (so an episode should never terminate): <br>
    discount = 1, noise = 0.8, livingReward = 0.9 
    
    Which can be tested by running:
   ```python
   python gridworld.py -g DiscountGrid -a value --discount 1 --noise 0.8 --livingReward 0.9
   ```

    <img src="../images/rl_2_6.gif" width=400>

The lower discount means short-sighted, higher discount focuses more on future (go further).
Lower noise means more deterministic, higher noise will lead to more random moves.
Negative livingReward discourages to live longer (takes shorter steps), but higher livingReward encourages live long, take longer action.

## 3. Prioritized Sweeping Value Iteration
