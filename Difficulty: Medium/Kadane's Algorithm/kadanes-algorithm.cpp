class Solution {
  public:
    int maxSubarraySum(vector<int> &arr) {
        // Code here
        int cursum=0;
        int maxsum=INT_MIN;
        for(int i=0;i<arr.size();i++){
            cursum=cursum+arr[i];
            maxsum=max(maxsum,cursum);
            if(cursum<0){
                cursum=0;
            }
        }
        return maxsum;
    }
};