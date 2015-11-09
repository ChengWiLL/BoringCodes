#include<vector>
using namespace std;
class Solution
{
public:
	vector<int>::iterator My_unique(vector<int> &nums)
	{
		vector<int>::iterator Iter=nums.begin();
		vector<int>::iterator flag=nums.begin();
		int tag=0;
		for(;Iter!=nums.end()-1;++Iter)
		{
			if(*Iter==*(Iter+1)&&tag==0)
			{
				flag=Iter+1;
				tag++;
			}
			if(*Iter!=*(Iter+1)&&tag!=0)
			{
				*flag=*(Iter+1);
				flag++;
			}
		}
		return flag;
	}
};
