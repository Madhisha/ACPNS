class DSU:
    def __init__(self, n):
        self.parent = [i for i in range(n + 1)]  # Parent array
        self.size = [1] * (n + 1)               # Size array for subtree sizes

    def find(self, x):
        # Path compression heuristic
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def merge(self, a, b):
        # Find the roots of both components
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return 0  # Already in the same component, no change needed

        # Union by size: attach smaller tree under the larger tree
        if self.size[b] > self.size[a]:
            a, b = b, a

        # Update size and parent
        ret = self.size[a] * self.size[b]  # Contribution of this edge
        self.size[a] += self.size[b]
        self.parent[b] = a
        return ret

    def solve(self, N, edges):
        # Sort edges by weight (ascending)
        edges.sort(key=lambda x: x[2])  # x[2] is the weight of the edge

        ans = 0
        for u, v, w in edges:
            # Merge the two components connected by this edge and calculate the contribution
            contribution = self.merge(u, v)
            ans += contribution * w  # Contribution of this edge to the total sum

        return ans


# Input parsing and function call
if __name__ == "__main__":
    # N = 5
    # edges = [
    #     (1, 2, 4),  # Edge between node 1 and node 2 with weight 4
    #     (2, 3, 1),  # Edge between node 2 and node 3 with weight 1
    #     (1, 4, 6),  # Edge between node 1 and node 4 with weight 6
    #     (4, 5, 12)  # Edge between node 4 and node 5 with weight 12
    # ]

    N = 3
    edges = [
        (1, 2, 10),  # Edge between node 1 and node 2 with weight 10
        (1, 3, 2)    # Edge between node 1 and node 3 with weight 2
    ]

    # Create a DSU instance
    dsu = DSU(N)

    # Call the solve function on the DSU instance
    result = dsu.solve(N, edges)

    print(result)  # Output the result




class DSU:
    def _init_(self, n):
        self.representative = [i for i in range(n + 1)]
        self.subtree_size = [1] * (n + 1)

    def find(self, element):
        if self.representative[element] != element:
            self.representative[element] = self.find(self.representative[element])
        return self.representative[element]

    def merge(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return 0

        if self.subtree_size[root_y] > self.subtree_size[root_x]:
            root_x, root_y = root_y, root_x

        merged_size = self.subtree_size[root_x] * self.subtree_size[root_y]
        self.subtree_size[root_x] += self.subtree_size[root_y]
        self.representative[root_y] = root_x
        return merged_size

    def solve(self, n, edges):
        edges.sort(key=lambda edge: edge[2])
        total_weight = 0
        for start, end, weight in edges:
            contribution = self.merge(start, end)
            total_weight += contribution * weight
        return total_weight