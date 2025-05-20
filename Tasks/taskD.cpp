#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <unordered_map>
#include <cinttypes>

using namespace std;

int_fast32_t n;
int_fast32_t a[20];
int_fast32_t target_m;

unordered_map<int_fast64_t, bool> memo;

int_fast64_t encode_state(int_fast32_t l, int_fast32_t r, int_fast64_t sum_mask, int_fast32_t turn) {
    return ((int_fast64_t)turn << 60) | ((int_fast64_t)sum_mask << 10) | ((int_fast64_t)r << 5) | (int_fast64_t)l;
}

bool can_win(int_fast32_t l, int_fast32_t r, int_fast64_t sum_mask, int_fast32_t turn) {
    if (l > r) {
        return (sum_mask & (1ULL << target_m)) != 0;
    }

    int_fast64_t key = encode_state(l, r, sum_mask, turn);

    if (memo.find(key) != memo.end()) {
        return memo[key];
    }

    if (turn == 0) {
        int_fast32_t new_l = l + 1;
        int_fast32_t new_r = r;
        int_fast64_t new_sum_mask = sum_mask;
        if (a[l] <= target_m) {
            new_sum_mask = (sum_mask | (sum_mask << a[l]) | (1ULL << a[l])) & ((1ULL << (target_m + 1)) - 1);
        }
        bool take_left = can_win(new_l, new_r, new_sum_mask, 1);
        if (take_left) {
            memo[key] = true;
            return true;
        }

        new_l = l;
        new_r = r - 1;
        new_sum_mask = sum_mask;
        if (a[r] <= target_m) {
            new_sum_mask = (sum_mask | (sum_mask << a[r]) | (1ULL << a[r])) & ((1ULL << (target_m + 1)) - 1);
        }
        bool take_right = can_win(new_l, new_r, new_sum_mask, 1);
        if (take_right) {
            memo[key] = true;
            return true;
        }

        memo[key] = false;
        return false;
    }
    else {
        int_fast32_t new_l = l + 1;
        int_fast32_t new_r = r;
        int_fast64_t new_sum_mask = sum_mask;
        bool machine_take_left = can_win(new_l, new_r, new_sum_mask, 0);
        if (!machine_take_left) {
            memo[key] = false;
            return false;
        }

        new_l = l;
        new_r = r - 1;
        bool machine_take_right = can_win(new_l, new_r, new_sum_mask, 0);
        if (!machine_take_right) {
            memo[key] = false;
            return false;
        }

        memo[key] = true;
        return true;
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    for(int_fast32_t i=0;i<n;i++) cin >> a[i];
    vector<int_fast32_t> achievable_m;
    for(int_fast32_t m=1; m<50; m++){
        target_m = m;
        memo.clear();
        bool possible = can_win(0, n-1, 0, 0);
        if(possible){
            achievable_m.push_back(m);
        }
    }
    for(int_fast32_t i=0;i<achievable_m.size();i++){
        if(i > 0) cout << ' ';
        cout << achievable_m[i];
    }
    return 0;
}
