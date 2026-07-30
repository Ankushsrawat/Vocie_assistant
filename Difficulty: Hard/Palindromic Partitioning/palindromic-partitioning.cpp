class Solution {
  public:
    bool ispal(string s,int start,int end){
        while(start<end){
            if(s[start]!=s[end]){
                return false;
            }
            start++;
            end--;
        }
        return true;
    }
    int solve(string &s,int idx,int n,vector<int>&dp){
        if(idx==n){
            return 0;
        }
        if(dp[idx]!=-1){
            return dp[idx];
        }
        int ans=1e9;
        for(int i=idx;i<n;i++){
            if(ispal(s,idx,i)){
                ans=min(ans,1+solve(s,i+1,n,dp));
            }
        }
        return dp[idx]=ans;
    }
    int palPartition(string &s) {
        int n=s.size();
        vector<int>dp(n+1,-1);
        return solve(s,0,n,dp)-1;
    }
};