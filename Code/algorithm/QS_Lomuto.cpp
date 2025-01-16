#include<iostream>
#include<vector>
using namespace std;
int partition(vector<int>& a,int l,int r){//10 7 8 3 5 1 6
    int pivot=a[r];
     int i=l-1;
    for(int j=l;j<r;j++){
        if(a[j]<pivot){
            ++i;
           swap(a[i],a[j]);
        }
    }
    swap(a[i+1],a[r]);
 return i+1;
}
 void quickSort (vector<int>& a,int l,int r){
    if(l<r){
    int pi=partition(a,l, r);
     quickSort(a,l,pi-1);
     quickSort(a,pi+1,r);
    }
 }
int main(){
    vector<int> a={10, 7, 8 ,3 ,5 ,1, 6};
    int n=a.size();
    quickSort(a,0,n-1);
    for(auto i=0;i<a.size();i++){
   cout<<a[i]<<" ";
    }
    return 0;
}