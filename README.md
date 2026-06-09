# STEP_Week4_HomeWork
STEP_WEEK4_HomeWork

## HomeWork1 (Wikipedia.py)
### Objective:
Return the shortest path from the start to the goal in Wikipedia. If the start and the goal is not connected, return "Not_found".
### Function:
  - def find_shortest_path (self, start, goal): Find and return the shortest path from the start to the goal in Wikipedia.
      - Using BFS.
      - Repeat enqueue and dequeue until the queue is empty. If the goal was found(If the node popped out from the queue was the goal), make a list of titles that make up the path.
      - Join the titles with '->', and return the path. 
### Variables:
  - queue = deque() # Set queue
  - visited = {} # Store nodes that was popped from the queue as a key. The value is the previous key.
  - rev_titles = {v:k for k,v in self.titles.items()} # Set keys and values as follows; key : title, value : id to get an ID from a title.
  - start_id = rev_titles[start] # An ID whose title is start.
  - goal_id = rev_titles[goal] # An ID whose title is goal.
  - ans_id = [] # Store IDs that make up the answer path.      
   
## Homework2 (wikipedia2.py)
### Objective:

### Function:

