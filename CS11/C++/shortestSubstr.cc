#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main();
string shortestSubstr(string parentStr);
vector<int> subDict(string parentStr, int start, int end);

int main() {
    string parstr, substr;
    cout << "Input string" << endl;
    cin >> parstr;
    substr = shortestSubstr(parstr);
    cout << substr << endl;
}

string shortestSubstr(string parentStr) {
    int charAt = parentStr[0];
    int maxLength, maxIndex = 1;
    vector<int> repeats(256, -1);
    vector<int> maxSubstr(parentStr.size(), 0);
    repeats[charAt] = 0;
    for(int i = 1; i < parentStr.size(); i++) {
        charAt = parentStr[i];
        if(repeats[charAt] == -1) {
            repeats[charAt] = i;
            maxSubstr[i] = maxSubstr[i-1];
            if(i - maxSubstr[i] > maxLength) {
                maxIndex = i;
                maxLength = i - maxSubstr[i] + 1;
            }
        }
        else {
            maxSubstr[i] = repeats[charAt] + 1;
            repeats = subDict(parentStr, repeats[charAt] + 1, i);
        }
    }
    for(int i = 0; i < maxSubstr.size(); i++) {
        cout << maxSubstr[i] << endl;
    }
    return parentStr.substr(maxSubstr[maxIndex], maxLength);
}

vector<int> subDict(string parentStr, int start, int end) {
    vector<int> repeats(256, -1);
    for(int i = start; i <= end; i++) {
        repeats[(int)parentStr[i]] = i;
    }
    return repeats;
}