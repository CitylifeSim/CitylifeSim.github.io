import random

class Map:
    def __init__(self, graph= None, directed=False):
        self.directed = directed
        self.waypoint_list = []
        if graph:
          self.graph = graph
        else:
          self.graph = dict()   
	
    def add_edge(self, node1, node2, weight=1):       
        if not node1 in self.graph:
          self.graph[node1] = set()
        self.graph[node1].add((node2, weight))

        if not self.directed:
          if not node2 in self.graph:
            self.graph[node2] = set()
          self.graph[node2].add((node1, weight))
    
    def get_neighbors(self, node):
        return self.graph[node]

    def get_neighbor_random(self, node, weighted=True):
        neighborList = []
        #weightList = [1] * len(self.graph[node])
        weightList = []
        for idx, n in enumerate(self.graph[node]):
          if len(self.waypoint_list) > 1:
            if self.waypoint_list[-2] != n[0]:
              neighborList.append(n[0])
              if weighted:
                weightList.append(1)
          else:
            neighborList.append(n[0])
            if weighted:
              weightList.append(1)         

        rand_neighbor = random.choices( neighborList, weights=weightList, k=1)
        print(rand_neighbor[0])
        return rand_neighbor[0]  

    def random_traverse(self, start_node, num_waypoints=5):
        self.waypoint_list.clear()
        self.waypoint_list.append(start_node)
        for i in range(num_waypoints):
          next_node = self.get_neighbor_random(start_node)
          self.waypoint_list.append(next_node)
          start_node = next_node
        #print(waypoint_list)
        return self.waypoint_list  

    # heuristic function for A* algorithm
    def init_heuristic_func(self, h_dic=None):
        if h_dic:
          self.HeuristicDic =h_dic
        else:
          self.HeuristicDic = dict()
          for key in self.graph.keys():
            self.HeuristicDic[key] = 1

    def eval_heuristic_val(self, node):
      return self.HeuristicDic[node]

    def find_path_a_star(self, start_node, stop_node):
        self.init_heuristic_func()
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = set([start_node])
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start_node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n == None or g[v] + self.eval_heuristic_val(v) < g[n] + self.eval_heuristic_val(n):
                    n = v;

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def get_all_nodes(self):
      nodes_list = []
      for key in self.graph.keys():
        nodes_list.append(key)
      return nodes_list   

    def print_map(self):
        for key in self.graph.keys():
            print("node", key, ": ", self.graph[key])