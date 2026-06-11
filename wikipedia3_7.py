## AIに書いてもらったfind_longest_path(ただしstackにそれまでのパスをすべて積んでいるのでメモリ爆発すると思われます。)

import sys,random
from collections import deque,defaultdict
class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id # idが数字、titlesがアルファベット
                self.titles[id] = title
                self.links[id] = []
        #print(f"self.titles:{self.titles}")        
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        #print(f"self.links:{self.links}")
        print()
        
        
    def can_reach_goal_links(self, goal): # 
        rev_titles = {v:k for k,v in self.titles.items()}
        goal_id = rev_titles[goal]
        reverse_links = defaultdict(list)

        for src in self.links:
            for dst in self.links[src]:
                reverse_links[dst].append(src) #{dst : src}の反対向きlinks(本来はsrc->dst)

        queue = deque()
        visited = {} # goalから訪れた場所(ここに載っている場所はすべてgoalにたどり着ける)
        visited[goal_id] = True
        queue.append(goal_id)

        while queue:
            node = queue.popleft()
            for parent in reverse_links[node]: # parentはnodeへ直接つながっているリンクたち(最初のは、goalと直接つながったリンクたち)
                if parent not in visited:
                    visited[parent] = True
                    queue.append(parent)

        ans_id = {}

        for node in visited:
            ans_id[node] = []
            for child in self.links[node]:
                if child in visited:
                    ans_id[node].append(child)

        return ans_id


    def make_sorted_links(self,link_list): # ボツ関数　# self.linksの各キーが持つリストの中身を、その中身が持つリンク数でソート
        new_links = {}
        for link in link_list:
            new_links[link] = sorted(link_list[link],key=lambda x : len(self.links[x]), reverse=True) # 各要素であるリストの中身を、そのリストの要素が持つリンクの数でsort       
            #print(f"new_links:{new_links}")       
        return new_links   

        # 一度bfsをやってgoalから全ノードへの最短距離を出しておく？っていうよりゴールとつながっているかどうかの判定に使える？(つながっていないものを除く)

        
        
    def find_longest_path(self, start, goal):  
        rev_titles = {v: k for k, v in self.titles.items()}
        start_id = rev_titles[start]
        goal_id = rev_titles[goal]

        possible_links = self.can_reach_goal_links( goal)

        stack = deque()
        longest_path = []

        MAX_TIMES = 1000000
        cnt = 0

        # (node, path)
        stack.append((start_id, [start_id]))

        while stack:
            node, path = stack.pop()
            cnt += 1

            if cnt % 100000 == 0:
                print(cnt, len(stack), len(path))

            if cnt >= MAX_TIMES:
                print("limit reached")
                break

            if node == goal_id:
                if len(path) > len(longest_path):
                    longest_path = path.copy()
                    #print(f"update len(longest_path) : {len(longest_path)}")
                    #print(f"path : {path}")
                continue

            for child in possible_links[node][:3]:
                if child not in path:  # 同じ経路内での再訪問禁止
                    new_path = path + [child]
                    stack.append((child, new_path))

        if not longest_path:
            return "Not_found"

        print("final answer : ", end="")
        return len(longest_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    #wikipedia.find_longest_titles()
    # Example
    #wikipedia.find_most_linked_pages()
    # Homework #1
    #print(f"shortest_path : {wikipedia.find_shortest_path("渋谷","パレートの法則")}")
    # Homework #2
    #print(f"wikipedia.find_most_popular_pages() : {wikipedia.find_most_popular_pages()}")
    # Homework #3 (optional)
    #print(wikipedia.find_longest_path("池袋", "渋谷"))
    print(wikipedia.find_longest_path("A", "F"))