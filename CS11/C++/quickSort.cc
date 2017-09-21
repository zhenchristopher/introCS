#include <vector>
#include <iostream>
#include <string>

using namespace std;

int main();
void quickSort(vector<int>& list, int start, int end);
void swap(vector<int>& list, int index1, int index2);

int main() {
    int mylist[] = {2, 4, 5, 1, 3, 7, 10, 8, 4, 3, 1};
    vector<int> myVec (mylist, mylist + sizeof(mylist)/sizeof(mylist[0]));
    quickSort(myVec, 0, myVec.size()-1);
    for(unsigned i = 0; i < myVec.size(); i++) {
        cout << myVec[i] << " ";
    }
}

void quickSort(vector<int>& list, int start, int end) {
    if(end <= start) {
        //do nothing
    }
    else {
        int pivot = list[end];
        int iter1 = start-1;
        for(int iter2 = start; iter2 < end; iter2++) {
            if(list[iter2] < pivot) {
                iter1++;
                swap(list, iter1, iter2);
            }
        }
        swap(list, iter1+1, end);
        quickSort(list, start, iter1); quickSort(list, iter1 + 2, end);
    }
}

void swap(vector<int>& list, int index1, int index2) {
    int temp = list[index1];
    list[index1] = list[index2];
    list[index2] = temp;
}