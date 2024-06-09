import sys
import collections
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
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
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
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
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


    # Find the most linked pages.
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
        
    def pagename_to_id(self, pagename):
        id = None
        for page_id, title in self.titles.items():
            if title == pagename:
                id = page_id
                return id
        print("そんなページはありません")
        return -1


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = self.pagename_to_id(start)
        goal_id = self.pagename_to_id(goal)
        visited = set()
        queue = deque([(start_id, [start_id])])
        while queue:
            current_id, id_path = queue.popleft()
            if current_id == goal_id:
                break
            
            visited.add(current_id)
            
            for neighbor_id in self.links[current_id]:
                if neighbor_id not in visited:
                    queue.append((neighbor_id, id_path + [neighbor_id]))
        
        path = [self.titles[page_id] for page_id in id_path]
        print(f"最短path:{path}")
        
        

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        neighbor_ratio = 0.85
        # ランク初期化
        page_ranks = {}
        for page_id in self.titles.keys():
            page_ranks[page_id] = 1
            
        # ページランクの収束を確認する関数
        def check_convergence(page_ranks, new_page_ranks):
            for page_id in page_ranks.keys():
                if abs(page_ranks[page_id] - new_page_ranks[page_id]) > 0.01:
                    return False
            return True
        
        
        # 収束するまで頑張る
        convergence_flag = False
        roop_count= 0
        while(not convergence_flag):
            roop_count+= 1        
            # デバッグ用 全てのページのpointの合計が同じか確認
            # print(page_ranks)
            # total_rank_must_be = len(self.titles)
            # total_rank = 0
            # for page_id in self.titles.keys(): # total の点数同じか確認
            #     total_rank += page_ranks[page_id]
            # if total_rank_must_be - total_rank > 0.01:
            #     print(page_ranks)
            #     print(total_rank, total_rank_must_be)
            #     print("error")
            #     return -1
            
            # Random Surferモデルの実装　詳細はREADME
            
            # new_page_ranks辞書の初期化
            new_page_ranks = {}
            for page_id in self.titles.keys():
                new_page_ranks[page_id] = 0
            
            # 隣のノードにポイントあげる。全てのノードに均等に渡すページランク分は、あとでふりわける。
            total_random_giving_points = 0
            for page_id in self.titles.keys():
                if len(self.links[page_id]) == 0:
                    total_random_giving_points += page_ranks[page_id]
                    page_ranks[page_id] = 0
                
                else:
                    total_random_giving_points += page_ranks[page_id] * (1-neighbor_ratio)
                    for neighbor_id in self.links[page_id]:
                        new_page_ranks[neighbor_id] += page_ranks[page_id] * neighbor_ratio / len(self.links[page_id])

                        
            # 他のノードからrandomにとんできたpointを足す
            each_given_points = total_random_giving_points / len(self.titles)
            for page_id in self.titles.keys():
                new_page_ranks[page_id] += each_given_points
            
            # 収束したか確認
            convergence_flag = check_convergence(page_ranks, new_page_ranks)
            # page_ranksを書き換える
            page_ranks = new_page_ranks
            
        print(f"ループ{roop_count}回で収束") 
        sorted_pages = sorted(page_ranks.items(), key=lambda x: x[1], reverse=True)
        print("The most popular pages using Random Surfer Model is:")
        popular_page_id, popular_rank = sorted_pages[0]
        print(self.titles[popular_page_id], popular_rank)
        
            
        

    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    