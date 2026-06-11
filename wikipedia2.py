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
        
        while queue: # キューが空になるまで
            node = queue.popleft() # キューからnodeを1つとる
            if node == goal_id: # 一番最初に見たノードが目的のノードだったら、このへんまとめられそう(と思ったけれど分けた方が簡単かも...?)
                return start + "->" + goal
            for child_id in self.links[node]:
                if child_id == goal_id : # 次のノードが目的のノード、またはstartとgoalが同じだったら
                    # 以下、道順を返すためのリストを作成 # prevを作らなくても一個前のキーを返し続ければいいのでは
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
        print("find_most_popular_pages")
        rank_dic = defaultdict(list) # 各idのrankを格納 {..., id:[old_rank , new_rank], ...}という形
        for id in self.links:
            rank_dic[id].append(1.0) # 最初は各idに１ずつ分配
            rank_dic[id].append(0)
        ave = 1 # aveは全体のabs(old_rank - new_rank)の平均値
        while ave > 0.01:
            total_dif = 0 # ave = total_dif / len(self.links)
            #total = 0
            distribute_whole = 0 # 全体に分配するランクの総量
            
            for id in self.links.keys():
                if len(self.links[id]) == 0: # どのリンクも指していなければ
                    distribute_whole += rank_dic[id][0] # 持っているランクをすべて全体に分配する方へ回す
                    continue
                distribute_whole += rank_dic[id][0]*0.15 # そうでなければ持っているランクの１５％を全体に分配する方へ回す。(二重for文対策)
                for child in self.links[id]:                                                 
                    rank_dic[child][1] += (rank_dic[id][0]*0.85) / len(self.links[id]) # 子ノードに85%配分            
            for id in self.links:
                 rank_dic[id][1] += distribute_whole / len(self.links)   # 全ノードに15%配分   # 最後の足りなかったものを無理やりどこかにたす
                  
            #total = sum(rank_dic[id][1] for id in self.links)
            #cnt = sum(1 for id in self.links if len(self.links[id]) == 0)
            #print(cnt)
            #print(len(self.links))
            #print(total)
            #assert total == len(self.links)   # デバッグ用だが、一度小数にしている関係で合計しても微妙に合わない。
                  
            for id in self.links:
                total_dif += abs(rank_dic[id][1]-rank_dic[id][0]) # 差分の合計を計算 
                #平均をとるんじゃなくて差分を二乗した和の条件を考えるとより速く(早く)収束して結果も若干変わるかも
                rank_dic[id][0] = rank_dic[id][1] # 古いランクを新しい計算したほうのランクに更新
                rank_dic[id][1] = 0 # 上書きしたほうのランクは０にする
            ave = total_dif / len(self.links) # 全体の差分の平均値を出す。
            
            print(f"ave : {ave} なので",end = "")
            if ave > 0.01:
                print("さらに更新します！！")
            else:
                print("結果を出力します！！")   
                    
        # 結果の出力  
        print("結果出力！！")          
        rank_dic = dict(sorted(rank_dic.items(),key = lambda x : x[1][0],reverse = True)) # ranc_dicを持ちランクの大きい順に整列
        #print(rank_dic)
        cnt = 0
        top_titles = [] # 出力するトップ１０のタイトルを格納
        for id in rank_dic.keys():
            top_titles.append(self.titles[id])
            print(f"{top_titles[cnt]} : {rank_dic[id][0]}")
            cnt += 1
            if cnt == 10:
                break
        return top_titles

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
    #wikipedia.find_most_linked_pages()
    # Homework #1
    #print(f"shortest_path : {wikipedia.find_shortest_path("渋谷","パレートの法則")}\n")
    # Homework #2
    print(f"wikipedia.find_most_popular_pages() : {wikipedia.find_most_popular_pages()}")
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")



""""
mchacha5041@localhost:~/c_program/google/week4$ python3 wikipedia2.py pages_medium.txt links_medium.txt
Finished reading pages_medium.txt
Finished reading links_medium.txt

find_most_popular_pages
ave : 1.0199660560903578 なのでさらに更新します！！
ave : 0.3756659355407342 なのでさらに更新します！！
ave : 0.11362063034301548 なのでさらに更新します！！
ave : 0.04831133054655497 なのでさらに更新します！！
ave : 0.025926086253307397 なのでさらに更新します！！
ave : 0.015517883686183873 なのでさらに更新します！！
ave : 0.009864337292830615 なので結果を出力します！！
結果出力！！
英語 : 1485.489729269668
ISBN : 950.9637892418593
2006年 : 533.9501983481542
2005年 : 509.5838071441827
2007年 : 498.91792629695027
東京都 : 485.8884796174678
昭和 : 465.49369995276186
2004年 : 451.52856357468374
2003年 : 410.3661794345326
2000年 : 407.19310442174464
wikipedia.find_most_popular_pages() : ['英語', 'ISBN', '2006年', '2005年', '2007年', '東京都', '昭和', '2004年', '2003年', '2000年']

mchacha5041@localhost:~/c_program/google/week4$ python3 wikipedia2.py pages_large.txt links_large.txt
Finished reading pages_large.txt
Finished reading links_large.txt

find_most_popular_pages
ave : 1.0997270144568414 なのでさらに更新します！！
ave : 0.4196897661404544 なのでさらに更新します！！
ave : 0.13272080118060442 なのでさらに更新します！！
ave : 0.05308500217912525 なのでさらに更新します！！
ave : 0.02715915353266803 なのでさらに更新します！！
ave : 0.01602797309195186 なのでさらに更新します！！
ave : 0.010224945740646592 なのでさらに更新します！！
ave : 0.006775697166436004 なので結果を出力します！！
結果出力！！
日本 : 4600.305177215388
英語 : 4526.123369997155
VIAF_(識別子) : 3801.9793309014435
バーチャル国際典拠ファイル : 3312.772971022837
アメリカ合衆国 : 2716.541402384344
ISBN : 2690.8833814817494
ISNI_(識別子) : 2054.9767898627774
国際標準名称識別子 : 1856.47878447651
地理座標系 : 1830.7305123763012
SUDOC_(識別子) : 1507.6802921659144
wikipedia.find_most_popular_pages() : ['日本', '英語', 'VIAF_(識別子)', 'バーチャル国際典拠ファイル', 'アメリカ合衆国', 'ISBN', 'ISNI_(識別子)', '国際標準名称識別子', '地理座標系', 'SUDOC_(識別子)']
"""