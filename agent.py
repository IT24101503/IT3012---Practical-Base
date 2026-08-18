# agent.py
from collections import deque
import heapq
from random import random

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SearchAgent:
    def bfs_search(percept: dict):
        visited = set()
        queue = deque([percept['agent_pos']])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for i,j in [(0,1), (0,-1), (1,0), (-1,0)]:
                neighbor = (current[0]+i, current[1]+j)

                if neighbor[0] < 0 or neighbor[0] >= percept['grid_size'][0] or neighbor[1] < 0 or neighbor[1] >= percept['grid_size'][1]:
                    continue

                if neighbor not in visited and neighbor not in percept['walls']:
                    queue.append(neighbor)

                if neighbor in percept['all_food_positions']:
                    return neighbor
        return None

    def dfs_search(percept: dict):
        visited = set()
        stack = [percept['agent_pos']]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            for i,j in [(0,1), (0,-1), (1,0), (-1,0)]:
                neighbor = (current[0]+i, current[1]+j)

                if neighbor[0] < 0 or neighbor[0] >= percept['grid_size'][0] or neighbor[1] < 0 or neighbor[1] >= percept['grid_size'][1]:
                    continue

                if neighbor not in visited and neighbor not in percept['walls']:
                    stack.append(neighbor)

                if neighbor in percept['all_food_positions']:
                    return neighbor
        return None


    def ucs_search(percept: dict):
        visited = set()
        queue = [(0, percept['agent_pos'])]
        while queue:
            cost, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            for i,j in [(0,1), (0,-1), (1,0), (-1,0)]:
                neighbor = (current[0]+i, current[1]+j)

                if neighbor[0] < 0 or neighbor[0] >= percept['grid_size'][0] or neighbor[1] < 0 or neighbor[1] >= percept['grid_size'][1]:
                    continue

                if neighbor not in visited and neighbor not in percept['walls']:
                    heapq.heappush(queue, (cost + 1, neighbor))

                if neighbor in percept['all_food_positions']:
                    return neighbor
        return None