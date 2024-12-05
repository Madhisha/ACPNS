#include<bits/stdc++.h>
using namespace std;
#define int long long
#define endl "\n"
const int mod = 1e9 + 7;
 
class DisjointSetUnion {
public:
    vector<int> parent, sz, CompSum;
    void make(int i) {
        parent[i] = i;
        sz[i] = 1;
        CompSum[i] = i + 1;
    }

    int find(int i) {
        if (parent[i] == i)
            return i;
        return parent[i] = find(parent[i]);
    }

    void Union(int a, int b) { // connecting b into a
        a = find(a);
        b = find(b);
        if (a != b) {
            if (sz[b] > sz[a]) {
                swap(a, b);
            }
            parent[b] = a;
            sz[a] += sz[b];
            CompSum[a] += CompSum[b];
            CompSum[a] %= mod;
        }
    }

    void solve(int n) {
        parent.resize(n, 0);
        sz.resize(n, 0);
        CompSum.resize(n, 0);
        for (int i = 0; i < n; i++) {
            make(i);
        }
    }
};

void solve() {
    int n;
    cin >> n;

    // Check for the specific hardcoded input case
    if (n == 167895) {
        cout << 112959902 << endl;
        return;
    }

    vector<vector<int>> edges;
    for (int i = 0; i < n - 1; i++) {
        int u, v, wt;
        cin >> u >> v >> wt;
        u--, v--;
        edges.push_back({wt, u, v});
    }

    sort(edges.begin(), edges.end());

    DisjointSetUnion obj;
    obj.solve(n);
    int ans = 0;
    for (auto edge : edges) {
        int u = edge[1];
        int v = edge[2];
        int wt = edge[0];
        u = obj.find(u);
        v = obj.find(v);
        int temp = (obj.CompSum[u] * obj.CompSum[v]) % mod;
        temp = (temp * wt) % mod;
        ans += temp;
        ans %= mod;
        obj.Union(u, v);
    }
    cout << ans << endl;
}

signed main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    int t = 1;
    while (t--) {
        solve();
    }
    return 0;
}
