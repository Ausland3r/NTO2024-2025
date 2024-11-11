#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ifstream f("input.txt");
    ofstream fout("output.txt");

    int n, m;
    f >> n >> m;

    vector<vector<long long>> summer(n, vector<long long>(m + 1, 0));

    int q;
    f >> q;

    for (int i = 0; i < q; ++i) {
        int x, y, h;
        long long v;
        f >> x >> y >> h >> v;

        int rowStart = n - (y + h) + 1;
        int colStart = x - 1;

        for (int r = 0; r < h; ++r) {
            int rowIndex = rowStart + r;
            if (rowIndex < 0 || rowIndex >= n) continue;

            int colFrom = colStart;
            int colTo = colStart + r;
            if (colFrom >= m) continue;
            if (colTo >= m) colTo = m - 1;

            summer[rowIndex][colFrom] += v;
            if (colTo + 1 < m) {
                summer[rowIndex][colTo + 1] -= v;
            }
        }
    }

    for (int i = 0; i < n; ++i) {
        long long curr = 0;
        for (int j = 0; j < m; ++j) {
            curr += summer[i][j];
            summer[i][j] = curr;
        }
    }

    for (const auto& row : summer) {
        for (size_t j = 0; j < m; ++j) {
            fout << row[j];
            if (j != m - 1) fout << " ";
        }
        fout << "\n";
    }

    return 0;
}
