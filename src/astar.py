from heapq import *

def heuristic(x, y):
	return (y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2


# A* pathfinding algorithm
def find_path(grid, start, goal):
	# Possible directional moves (horizontal and vertical)
	possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

	# Data storage
	closed_set = set()
	came_from = {}
	cost_from_start = {start: 0}
	cost = {start: heuristic(start, goal)}
	heap = []

	heappush(heap, (cost[start], start))

	while heap:
		current = heappop(heap)[1]

		if current == goal:
			# Path found. Add to list and return it
			data = []
			while current in came_from:
				data.append(current)
				current = came_from[current]
			return data

		closed_set.add(current)
		for i, j in possible_moves:
			child = current[0] + i, current[1] + j
			unconfirmed_cost_from_start = cost_from_start[current] + heuristic(current, child)

			# If out of bounds or a wall, continue to next iteration
			if 0 <= child[0] < grid.shape[0]:
				if 0 <= child[1] < grid.shape[1]:
					if grid[child[0]][child[1]] == 1:
						continue
				else:
					continue
			else:
				continue

			# If cost is too high, continue to next iteration
			if child in closed_set and unconfirmed_cost_from_start >= cost_from_start.get(child, 0):
				continue

			# Path is still cheap enough
			if unconfirmed_cost_from_start < cost_from_start.get(child, 0) or child not in [i[1] for i in heap]:
				came_from[child] = current
				cost_from_start[child] = unconfirmed_cost_from_start
				cost[child] = unconfirmed_cost_from_start + heuristic(child, goal)
				heappush(heap, (cost[child], child))

	return False  # Unable to find a path
