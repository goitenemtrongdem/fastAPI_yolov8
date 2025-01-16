#include<iostream>
#include<vector>
using namespace std;

int heart(vector<int>& a,int l,int r){
    int piv=a[l];
    int i= ;
    while(1){
      do{
         ++i;
 
        --j;
   
      if(i>=j) { return j;}
      swap(a[i],a[j]);
       
    }                                                                                                                                                
}
void qu ctor<int>& a,int l,int r){
    if(l<r){
        int pi=heart(a,l,r);
        quickSort(a,l,pi);
        quickSort(a,pi+1,r);
    }
}
