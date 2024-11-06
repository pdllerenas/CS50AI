import sys

class Node():
  def __init__(self, state, parent, action, cost = 1, heuristic = 0):
    self.state = state
    self.parent = parent
    self.action = action
    self.cost = cost
    self.heuristic = heuristic

class StackFrontier():
  def __init__(self):
    self.frontier = []

  def add(self, node):
    self.frontier.append(node)

  def contains_state(self, state):
    return any(node.state == state for node in self.frontier)

  def empty(self):
    return len(self.frontier) == 0

  def remove(self):
    if len(self.frontier) == 0:
      raise Exception("empty frontier")
    else:
      return self.frontier.pop()

class QueueFrontier(StackFrontier):
  def remove(self):
    if len(self.frontier) == 0:
      raise Exception("empty frontier")
    else:
      return self.frontier.pop(0)
    
class Maze():
  def __init__(self, filename):
    self.maze = []
    with open(filename) as f:
      for line in f:
        row = [int(x) for x in line.strip()]
        self.maze.append(row)

    self.start = None
    self.goal = None

    for i in range(len(self.maze)):
      for j in range(len(self.maze[0])):
        if self.maze[i][j] == 2:
          self.start = (i, j)
        elif self.maze[i][j] == 3:
          self.goal = (i, j)
        elif self.maze[i][j] == 0:
          self.maze[i][j] = 10

    self.maze[self.start[0]][self.start[1]] = 2
    self.maze[self.goal[0]][self.goal[1]] = 3

  def __str__(self):
    output = ""
    for row in self.maze: 
      for cell in row:
        if cell == 10:
          output += " "
        elif cell == 2:
          output += "S"
        elif cell == 3:
          output += "G"
        else:
          output += str(cell)
      output += "\n"
    return output

  def successors(self, state):
    successors = [] 
    i, j = state
    if i > 0 and self.maze[i - 1][j] != 0:
      successors.append((i - 1, j))
    if i < len(self.maze) - 1 and self.maze[i + 1][j] != 0:
      successors.append((i + 1, j))
    if j > 0 and self.maze[i][j - 1] != 0:  
      successors.append((i, j - 1))
    if j < len(self.maze[0]) - 1 and self.maze[i][j + 1] != 0:
      successors.append((i, j + 1))
    return successors

  def goal_test(self, state):
    return state == self.goal
  
  def heuristic(self, state):
    return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])
  
  def path(self):
    path = []
    state = self.goal
    while state != self.start:
      path.append(state)
      state = self.maze[state[0]][state[1]]
    path.append(self.start)
    path.reverse()
    return path
  
  def solve(self):
    start = Node(self.start, None, None)
    frontier = StackFrontier()
    frontier.add(start)
    explored = []
    while not frontier.empty():
      node = frontier.remove()
      if node.state == self.goal:
        path = self.path()
        return path
      explored.append(node.state)
      for child in self.successors(node.state):
        if child not in explored and child not in frontier.frontier:
          child_node = Node(child, node, node.action)
          frontier.add(child_node)
    return None
  
  