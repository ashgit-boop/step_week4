## pathの管理が微塵も上手くいっていない ->　でもstackにidと一緒にpathも積むとメモリが爆発しそう
# goalにたどり着くリンクだけ抽出(けど計算量多すぎ)
# そのあとさらに各リンクが持っているリンクたちの多さ順にソートするのも考えたがあまり意味なさそう...?
# beamで探索幅を固定で前から何個のリンク~という風に絞る（でもこれだと永遠に終わらない可能性がある）
# ランダムに何個かのリンクを選んでいくのが一番楽しく終わるかも


import sys
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
        
        
    def find_shortest_path2(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        queue = deque()
        visited = {}
        rev_titles = {v:k for k,v in self.titles.items()}
        start_id = rev_titles[start]
        goal_id = rev_titles[goal]
        ans_id = []
        visited[start_id] = None
        queue.append(start_id)
        
        while queue:
            node = queue.popleft()
            if node == goal_id: # このへんまとめられそう
                return [start_id ,goal_id]
            for child_id in self.links[node]:
                if child_id == goal_id:
                    #prev = node
                    #ans_id.append(child_id)
                    #while prev != None:
                        #ans_id.append(prev)
                        #prev = visited[prev]           
                    #ans_titles = [self.titles[k] for k in ans_id]
                    return True #len(ans_titles)
                if child_id not in visited:
                    visited[child_id] = node
                    queue.append(child_id)

        return "Not_found"        
    


    def make_sorted_links(self,link_list): # ボツ # self.linksの各キーが持つリストの中身を、その中身が持つリンク数でソート
        new_links = {}
        for link in link_list:
            new_links[link] = sorted(link_list[link],key=lambda x : len(self.links[x]), reverse=True) # 各要素であるリストの中身を、そのリストの要素が持つリンクの数でsort       
            #print(f"new_links:{new_links}")       
        return new_links   

        # 一度bfsをやってgoalから全ノードへの最短距離を出しておく？っていうよりゴールとつながっているかどうかの判定に使える？(つながっていないものを除く)
    def make_path_to_goal_list(self,rev_list,goal): # ゴールとつながっているものだけを抽出 # ただこれは計算量が大きいからgoalから逆算していくべき
        path_links = {}
        
        for start in self.titles.values():
            start_id = rev_list[start]
            ret = self.find_shortest_path2(start,goal) # startとgoalがつながっているかをチェック
            if ret == True: # goalとつながっていないものはさよなら
                path_links[start_id] = self.links[start_id] # goalとつながっているものだけを追加
        return path_links   # self.linksのgoalとつながっているidのものだけを抽出した版
        
        
    def find_longest_path(self,start, goal): # DFS
        rev_titles = {v:k for k,v in self.titles.items()} # 逆順リストを作成
        start_id = rev_titles[start] # startのid
        goal_id = rev_titles[goal] # goalのid
        stack = deque()
        visited = {}
        possible_links = self.make_path_to_goal_list(rev_titles,goal) # self.linksのうち、goalとつながっているものだけを抽出
        #sorted_links = self.make_sorted_links(possible_links) # 各要素であるリストの中身を、そのリストの要素が持つリンクの数でsortしたリスト
        longest_path = [[]] # 最長のパスを格納
        path = []  # 現在までのpathを格納
        MAX_TIMES = 1000000
        cnt = 0
        beam = 3
    
        visited[start_id] = True
        stack.append(start_id)
        #path.append(start_id)
        #print(possible_links)
        #print(sorted_links)
    
        while stack:
            node = stack.pop()
            path.append(node)
            cnt += 1

            if cnt % 100000 == 0:
                print(cnt, len(stack), len(path))
            
            if cnt == MAX_TIMES:
                print("limit reached")
                break    
                

                #print(path)    
            #tmp_path.append(node)
            #if cnt % 100000 == 0:
                #print("second")
                #print(cnt, len(stack), len(path))
                
            if node != path[-1]:
                #print(f"node:{node}")
                #print(f"path_before:{path}")
                for i in range(len(path) - path.index(node)-1):
                    del visited[path[-1]]
                    del path[-1]
                    i+= 1
                #print(f"path_after:{path}")    
            #tmp_path.append(node)
            if node == goal_id:
                #tmp_path.append(node)
                if len(path) > len(longest_path):
                    longest_path = path.copy()
                    print(f"update len(longest_path) : {len(longest_path)}")
                    print(f"path : {path}, longest_path : {longest_path}")
                #path = [start_id] 
                #del path[-1]
                continue
            
            for child in possible_links[node][:beam]:
                #print(path)
                if child not in visited:
                    visited[child] = True
                    #path.append(child)
                    stack.append(child) 
                    
            if cnt >= 500000:
                print(f"cnt : {cnt}",end="")
                stack.append(goal_id)
                path.append(goal_id)        
                    
        #print(f"longest_path:{longest_path}")  
        if longest_path == [[]]:
            return "Not_found"  
        print("final answer : ",end = "")      
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
    print(wikipedia.find_longest_path("A", "F"))