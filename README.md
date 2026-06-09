# STEP_Week4_HomeWork
STEP_WEEK4_HomeWork

## HomeWork1 (Wikipedia.py)
### Objective:
Return the shortest path from the start to the goal in Wikipedia. If the start and the goal is not connected, return "Not_found".
### Function:
  - def find_shortest_path (self, start, goal) : Find and return the shortest path from the start to the goal in Wikipedia.
      - Using BFS.
      - Repeat enqueue and dequeue until the queue is empty. If the goal was found(If the node popped out from the queue was the goal), make a list of titles that make up the path.
      - Join the titles with '->', and return the path. 
### Variables:
  - queue = deque() : Set queue
  - visited = {} : Store nodes that was popped from the queue as a key. The value is the previous key.
  - rev_titles = {v:k for k,v in self.titles.items()} : Set keys and values as follows; key : title, value : id to get an ID from a title.
  - start_id = rev_titles[start] : An ID whose title is start.
  - goal_id = rev_titles[goal] : An ID whose title is goal.
  - ans_id = [] : Store IDs that make up the answer path.  <br>    
     
## Homework2 (wikipedia2.py)
### Objective:
Return 10 pages that have the highest page ranks in wikipedia. (The most poplular pages in Wikipedia.)
### Function:
  - def find_most_popular_pages(self) : Find the most popular pages in Wikipedia and return the pages.
    - Set all of the nodes' rank 1.0.
    - If the node has links, distribute 85% of the ranks to them evenly, and 15% to the whole.
    - If the node doesn't have any link, distribute the rank to the whole evenly. (Random Surfer)
    - Update each value.
    - Repeat this flow until the whole average of difference between values before and after the update falls below 0.01.
      
### Variables:
  - rank_dic = defaultdict(list) : Store ranks of each ID as follows : {..., id:[old_rank , new_rank], ...}
  - ave : Whole average of abs(old_rank - new_rank). Initially set 1.
  - total_dif : ave = total_dif / len(self.links). Initially set 0.
  - distribute_whole : Total value to distribute to the whole.
  - top_titles = [] : Store 10 answer titles.



