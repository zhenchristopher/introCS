#include <iostream>
#include <string>

using namespace std;

void permuteHelper(string permuted, string prefix);

int main(int argc, char* argv[]) {
    string permuter;
    cout << "Enter your string: ";
    cin >> permuter;
    string s = "";
    permuteHelper(permuter, s);
}

void permuteHelper(string permuted, string prefix) {
    if(permuted.size() == 0) {
        cout << prefix << endl;
    }
    else {
        for(unsigned int i = 0; i < permuted.size(); i++) {
            string newPermuted = permuted.substr(0, i) + permuted.substr(i+1, permuted.size()-i-1);
            string newPre = prefix + permuted[i];
            permuteHelper(newPermuted, newPre);
        }
    }
}