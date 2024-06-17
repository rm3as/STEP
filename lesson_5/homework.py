import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix

def nearest_neighbor_tsp(points):
    num_points = len(points)
    visited = [False] * num_points
    route = [0]
    visited[0] = True
    
    for _ in range(num_points - 1):
        last = route[-1]
        next_point = np.argmin([np.inf if visited[i] else np.linalg.norm(points[last] - points[i]) for i in range(num_points)])
        route.append(next_point)
        visited[next_point] = True
    
    route.append(0)  # 戻る
    return route

def two_opt(route, distance_matrix):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1]
                if route_length(new_route, distance_matrix) < route_length(best, distance_matrix):
                    best = new_route
                    improved = True
        route = best
    return best

def route_length(route, distance_matrix):
    length = 0
    for i in range(len(route) - 1):
        length += distance_matrix[route[i], route[i+1]]
    return length

# 与えられた点の集合
points = np.array([
    (1, 1),
    (2, 5),
    (3, 3),
    (5, 3),
    (3, 1),
    (4, 4),
    (3, 2)
])

# 最近近傍法で初期ルートを求める
initial_route = nearest_neighbor_tsp(points)

# 距離行列を計算
dist_matrix = distance_matrix(points, points)

# 2-optアルゴリズムで初期ルートを改善
optimized_route = two_opt(initial_route, dist_matrix)

# 結果を表示
print("初期ルート:", initial_route)
print("最適化されたルート:", optimized_route)
print("最適化されたルートの距離:", route_length(optimized_route, dist_matrix))

# プロット
plt.plot(points[:, 0], points[:, 1], 'o', label='Points')

# 初期ルートをプロット
initial_route_points = points[initial_route]
plt.plot(initial_route_points[:, 0], initial_route_points[:, 1], 'r--', label='Initial Route')

# 最適化されたルートをプロット
optimized_route_points = points[optimized_route]
plt.plot(optimized_route_points[:, 0], optimized_route_points[:, 1], 'g-', label='Optimized Route')

plt.legend()
plt.show()