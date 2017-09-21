#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main();
vector<string> towerHelper(int numPegs, string source, string dest, string aux);

int main() {
    int n;
    vector<string> solution;
    cout << "How many pegs?";
    cin >> n;
    if(n < 1) {
        return 1;
    }
    solution = towerHelper(n - 1, "A", "B", "C");
    for(unsigned i = 0; i < solution.size(); i++) {
        cout << solution[i] << endl;
    }
    return 0;
}

vector<string> towerHelper(int numPegs, string source, string dest, string aux) {
    vector<string> moves, newMoves1, newMoves2;
    if(numPegs == 1) {
        moves.push_back(source + " to " + aux);
        moves.push_back(source + " to " + dest);
        moves.push_back(aux + " to " + dest);
    }
    else {
        newMoves1 = towerHelper(numPegs - 1, source, aux, dest);
        newMoves2 = towerHelper(numPegs - 1, aux, dest, source);
        moves.insert(moves.end(), newMoves1.begin(), newMoves1.end());
        moves.push_back(source + " to " + dest);
        moves.insert(moves.end(), newMoves2.begin(), newMoves2.end());
    }
    return moves;
}