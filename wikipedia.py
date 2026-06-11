import sys
from collections import deque

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


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal): # bfsを使う
        #------------------------#
        # Write your code here!  #
        #------------------------#
        queue = deque() # キューをセット
        visited = {} # 訪れた場所をここに記録、値は一つ前のキーにする。でも実際は値は何でもいい？
        rev_titles = {v:k for k,v in self.titles.items()} # タイトルからidを抜き出すために、self.titlesの辞書のキーと値が逆転した辞書を作成
        start_id = rev_titles[start] # タイトルがstartのidを返す
        goal_id = rev_titles[goal] # タイトルがgoalのidを返す
        ans_id = [] # 答えのpathのidを記録
        visited[start_id] = None # startの値をNoneにしておく
        queue.append(start_id) # キューにstart_idを入れておく
        
        while queue: # キューが空になるまで # 先に見たものよりも短くなることはない
            node = queue.popleft() # キューからnodeを1つとる
            if node == goal_id: # 一番最初に見たノードが目的のノードだったら、このへんまとめられそう(と思ったけれど分けた方が簡単かも...?)
                return start + "->" + goal
            for child_id in self.links[node]:
                if child_id == goal_id : # 次のノードが目的のノード、またはstartとgoalが同じだったら
                    # 以下、道順を返すためのリストを作成 
                    prev = node
                    ans_id.append(child_id) # 次のノードを答えのリストに入れておく
                    while prev != None: # startにたどり着くまで
                        ans_id.append(prev) # 一個前に訪れたノードを答えに追加
                        prev = visited[prev] # prevの一個前のノードをprevにする            
                    ans_titles = [self.titles[k] for k in ans_id] # 答えとなるタイトルのリストを作る
                    return "->".join(reversed(ans_titles)) # 矢印でつなげて出力
                if child_id not in visited: # 次のノードがまだ訪れたことがない場所ならば
                    visited[child_id] = node # 次のノードの一個前が今見ているノード(visitedに登録)
                    queue.append(child_id) # キューに次のノードを入れる。

        return "Not_found"        

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])
        visited = {}
        for node in path:
            assert(node not in visited)
            visited[node] = True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    #wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()
    # Homework #1
    print(f"shortest_path : {wikipedia.find_shortest_path("A","F")}")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    #wikipedia.find_longest_path("渋谷", "池袋")


"""
(.venv) mchacha5041@localhost:~/c_program/google/week4$ python3 wikipedia.py pages_small.txt links_small.txt
Finished reading pages_small.txt
Finished reading links_small.txt

The most linked pages are:
B 3

shortest_path : A->B->C->F

(.venv) mchacha5041@localhost:~/c_program/google/week4$ python3 wikipedia.py pages_medium.txt links_medium.txt
Finished reading pages_medium.txt
Finished reading links_medium.txt

The most linked pages are:
ISBN 52641

shortest_path : 渋谷->ギャルサー_(テレビドラマ)->小野妹子

"""