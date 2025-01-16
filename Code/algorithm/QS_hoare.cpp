#include<iostream>
#include<vector>
using namespace std;

int heart(vector<int>& a,int l,int r){
    int piv=a[l];
    int i=l-1,j=r+1;
    while(1){
      do{
         ++i;
      } while(a[i]<piv);
      do{
        --j;
      } while(a[j]>piv);
      if(i>=j) { return j;}
      swap(a[i],a[j]);
       
    }                                                                                                                                                
}
void quickSort(vector<int>& a,int l,int r){
    if(l<r){
        int pi=heart(a,l,r);
        quickSort(a,l,pi);
        quickSort(a,pi+1,r);
    }
}
