#include<bits/stdc++.h>
using namespace std ;


void selec( int a[],int n){
    for(int i=0;i<n;i++){
        int res=i;
        for(int j=i+1;j<n;j++){
            if(a[j]<a[i]){
                res=j;
            }
        }
        swap(a[i],res);
    }
}
int main(){

}