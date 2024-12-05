#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define IOS ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0);
const ll N=1e4+1;
const ll K=1e2+1;
const ll INF=-1e18;
ll cache[N][K][2],vis[N][K][2],n,k,a[N];
ll dp(ll idx1,ll idx2,ll idx3)
{
    if(idx1==n+1)
    {
        if(!idx3 && idx2==(k+1))return 0;
        else
        return -1e18;
    }
    if(idx2>k)return -1e18;
    ll &ans=cache[idx1][idx2][idx3];
    if(vis[idx1][idx2][idx3])return ans;
    ans=-1e18;
    if(idx2&1)
    ans=-a[idx1]+max(dp(idx1+1,idx2,1ll),dp(idx1+1,idx2+1,0ll));
    else
    ans= a[idx1]+max(dp(idx1+1,idx2,1ll),dp(idx1+1,idx2+1,0ll));
    vis[idx1][idx2][idx3]=1;
    return ans;
}
int32_t main()
{
    IOS;
    int t;
    cin>>t;
    assert(t>=1 && t<=10);
    while (t--)
    {
        cin>>n;
        assert(n>=1 && n<=1e4);
        for(ll i=1;i<=n;i++)
        {
            cin>>a[i];
            assert(a[i]>=-1e9 && a[i]<=1e9);
        }
        cin>>k;
        ll z=1e2,x=min(z,n);
        assert(k>=1 && k<=x);
        for(ll i=0;i<n+1;i++)
        {
            for(ll j=0;j<k+1;j++)
            vis[i][j][0]=0,vis[i][j][1]=0;
        }
        ll ans=dp(1ll,1ll,0ll);
        cout<<ans<<endl;
    }
    return 0;
}