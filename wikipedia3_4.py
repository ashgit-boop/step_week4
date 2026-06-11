## pathの管理が微塵も上手くいっていない
# goalにたどり着くリンクだけ抽出(計算量減少)

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


    def make_sorted_links(self,link_list): # ボツ # self.linksの各キーが持つリストの中身を、その中身が持つリンク数でソート
        new_links = {}
        for link in link_list:
            new_links[link] = sorted(link_list[link],key=lambda x : len(self.links[x]), reverse=True) # 各要素であるリストの中身を、そのリストの要素が持つリンクの数でsort       
            #print(f"new_links:{new_links}")       
        return new_links   

        # 一度bfsをやってgoalから全ノードへの最短距離を出しておく？っていうよりゴールとつながっているかどうかの判定に使える？(つながっていないものを除く)

        
        
    def find_longest_path(self,start, goal): # DFS
        rev_titles = {v:k for k,v in self.titles.items()} # 逆順リストを作成
        start_id = rev_titles[start] # startのid
        goal_id = rev_titles[goal] # goalのid
        stack = deque()
        visited = {}
        #possible_links = self.make_path_to_goal_list(rev_titles,goal) # self.linksのうち、goalとつながっているものだけを抽出
        #orted_links = self.make_sorted_links(possible_links) # 各要素であるリストの中身を、そのリストの要素が持つリンクの数でsortしたリスト
        possible_links = self.can_reach_goal_links( goal)
        #sorted_links = self.make_sorted_links(possible_links)
        longest_path = [[]] # 最長のパスを格納
        path = []  # 現在までのpathを格納
        MAX_TIMES = 1000000
    
        visited[start_id] = True
        stack.append(start_id)
        #path.append(start_id)
        #print(possible_links)
        #print(sorted_links)
        cnt = 0
        while stack:
            cnt += 1

            if cnt % 100000 == 0:
                print(cnt, len(stack), len(path))
            
            if cnt == MAX_TIMES:
                print("limit reached")
                break    
                
            node = stack.pop()
            visited[node] = True
            path.append(node)
            
            if node != path[-1]:
                #print(node)
                #print(path)
                for i in range(len(path) - path.index(node)-1):
                    del visited[path[-1]] # 消す？-> 消したらおかしくなった
                    del path[-1]
                    i+= 1
                #print(path)    
            #tmp_path.append(node)
            if cnt % 100000 == 0:
                print("second")
                print(cnt, len(stack), len(path))
            if node == goal_id:
                #tmp_path.append(node)
                if len(path) > len(longest_path):
                    print(f"path:{path}")
                    longest_path = path.copy()
                    print(len(longest_path))
                    #print(path)
                #path = [start_id] 
                continue
            #for child in sorted_links[node][:5]:
            #for i in range(len(possible_links[node])*0.1):
            children_idx = random.sample(range(0,len(possible_links[node])),int(len(possible_links[node]))*0.1) # smallのときは0.1とかに絞ると全然６が出てこない(それはそう)
            for idx in children_idx:
                child = possible_links[node][idx] # これだとsmallでも6が見つかるときと見つからないときがある
                if child not in visited: # 重複なしで選ぶなら本当はこれはいらない？
                    #visited[child] = True
                    #path.append(child)
                    stack.append(child) 
                   
        print(f"longest_path:{longest_path}")          
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