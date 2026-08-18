# agent.py
from collections import deque
import heapq
from random import random

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        pos = percept['agent_pos']
        return random.choice(self.actions_pool)

class SearchAgent:
    def __init__(self):
        self.plan = []
        # self.active_algo = 'BFS'
        # self.active_algo = 'DFS'
        self.active_algo = 'UCS'

    def bfs_search(self, percept: dict):
        visited = set()
        agent_pos = tuple(percept['agent_pos'])
        walls = set(tuple(w) for w in percept['walls'])
        food_positions = set(tuple(f) for f in percept['all_food_positions'])
        queue = deque([(agent_pos, [agent_pos])])
        
        while queue:
            current, path = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            
            for i, j in [(0,1), (0,-1), (1,0), (-1,0)]:
                neighbor = (current[0]+i, current[1]+j)

                if neighbor[0] < 0 or neighbor[0] >= percept['grid_size'][0] or \
                   neighbor[1] < 0 or neighbor[1] >= percept['grid_size'][1]:
                    continue

                if neighbor not in visited and neighbor not in walls:
                    new_path = path + [neighbor]

                    if neighbor in food_positions:
                        self.plan = new_path
                        return

                    queue.append((neighbor, new_path))

        self.plan = []
        return

    def dfs_search(self, percept: dict):
        visited = set()
        agent_pos = tuple(percept['agent_pos'])
        walls = set(tuple(w) for w in percept['walls'])
        food_positions = set(tuple(f) for f in percept['all_food_positions'])
        stack = [(agent_pos, [agent_pos])]
        
        while stack:
            current, path = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            
            for i, j in [(0,1), (0,-1), (1,0), (-1,0)]:
                neighbor = (current[0]+i, current[1]+j)

                if neighbor[0] < 0 or neighbor[0] >= percept['grid_size'][0] or \
                   neighbor[1] < 0 or neighbor[1] >= percept['grid_size'][1]:
                    continue

                if neighbor not in visited and neighbor not in walls:
                    new_path = path + [neighbor]

                    if neighbor in food_positions:
                        self.plan = new_path
                        return

                    stack.append((neighbor, new_path))
                    
        self.plan = []
        return

    def ucs_search(self, percept: dict):
        visited = set()
        agent_pos = tuple(percept['agent_pos'])
        walls = set(tuple(w) for w in percept['walls'])
        food_positions = set(tuple(f) for f in percept['all_food_positions'])
        queue = [(0, agent_pos, [agent_pos])]
        
        while queue:
            cost, current, path = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            
            for i, j in [(0,1), (0,-1), (1,0), (-1,0)]:
                neighbor = (current[0]+i, current[1]+j)

                if neighbor[0] < 0 or neighbor[0] >= percept['grid_size'][0] or \
                   neighbor[1] < 0 or neighbor[1] >= percept['grid_size'][1]:
                    continue

                if neighbor not in visited and neighbor not in walls:
                    new_path = path + [neighbor]

                    if neighbor in food_positions:
                        self.plan = new_path
                        return

                    heapq.heappush(queue, (cost + 1, neighbor, new_path))

        self.plan = []
        return

    def sense_and_act(self, percept: dict):
        if len(self.plan) < 1:
            if self.active_algo == 'BFS':
                self.bfs_search(percept)
            elif self.active_algo == 'DFS':
                self.dfs_search(percept)
            elif self.active_algo == 'UCS':
                self.ucs_search(percept)

            return self.sense_and_act(percept)
        else:
            next_pos = self.plan[0]
            current_pos = tuple(percept['agent_pos'])
            
            if next_pos == current_pos:
                self.plan.pop(0)
                if not self.plan:
                    return self.sense_and_act(percept)
                next_pos = self.plan[0]
            
            if next_pos[1] > current_pos[1]:
                return 'Up'
            elif next_pos[1] < current_pos[1]:
                return 'Down'
            elif next_pos[0] < current_pos[0]:
                return 'Left'
            elif next_pos[0] > current_pos[0]:
                return 'Right'
