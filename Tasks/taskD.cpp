#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

// Глобальные переменные
int n;
int a[20];
int target_m;

// Мемоизация: для каждого m используется отдельная карта
unordered_map<ll, bool> memo;

// Функция для кодирования состояния в одно число
ll encode_state(int l, int r, ll sum_mask, int turn) {
    // l: 0-19 (5 бит)
    // r: 0-19 (5 бит)
    // sum_mask: 0-49 (50 бит)
    // turn: 0 или 1 (1 бит)
    // Общая длина: 5 + 5 + 50 + 1 = 61 бит
    // Распределение бит:
    // [60] - turn
    // [59-10] - sum_mask
    // [9-5] - r
    // [4-0] - l
    return ((ll)turn << 60) | ((ll)sum_mask << 10) | ((ll)r << 5) | (ll)l;
}

// Рекурсивная функция для проверки достижимости m
bool can_win(int l, int r, ll sum_mask, int turn) {
    // Если все монеты взяты
    if (l > r) {
        return (sum_mask & (1ULL << target_m)) != 0;
    }

    // Кодируем текущее состояние
    ll key = encode_state(l, r, sum_mask, turn);

    // Проверяем мемоизацию
    if (memo.find(key) != memo.end()) {
        return memo[key];
    }

    if (turn == 0) { // Ход игрока
        // Игрок может выбрать взять слева или справа
        // Если хотя бы один выбор гарантирует достижение m независимо от выбора автомата, возвращаем true
        // Выбор слева
        int new_l = l + 1;
        int new_r = r;
        ll new_sum_mask = sum_mask;
        if (a[l] <= target_m) {
            new_sum_mask = (sum_mask | (sum_mask << a[l]) | (1ULL << a[l])) & ((1ULL << (target_m + 1)) - 1);
        }
        // Переход к ходу автомата
        bool take_left = can_win(new_l, new_r, new_sum_mask, 1);
        if (take_left) {
            memo[key] = true;
            return true;
        }

        // Выбор справа
        new_l = l;
        new_r = r - 1;
        new_sum_mask = sum_mask;
        if (a[r] <= target_m) {
            new_sum_mask = (sum_mask | (sum_mask << a[r]) | (1ULL << a[r])) & ((1ULL << (target_m + 1)) - 1);
        }
        // Переход к ходу автомата
        bool take_right = can_win(new_l, new_r, new_sum_mask, 1);
        if (take_right) {
            memo[key] = true;
            return true;
        }

        // Если ни один выбор не гарантирует достижение m, возвращаем false
        memo[key] = false;
        return false;
    }
    else { // Ход автомата
        // Автомат может выбрать взять слева или справа
        // Если автомат может сделать выбор, при котором игрок не сможет достичь m, то игрок не может гарантировать успех
        // Выбор слева
        int new_l = l + 1;
        int new_r = r;
        ll new_sum_mask = sum_mask;
        // При ходу автомата маска игрока не изменяется
        bool machine_take_left = can_win(new_l, new_r, new_sum_mask, 0);
        if (!machine_take_left) {
            memo[key] = false;
            return false;
        }

        // Выбор справа
        new_l = l;
        new_r = r - 1;
        // Маска остается той же
        bool machine_take_right = can_win(new_l, new_r, new_sum_mask, 0);
        if (!machine_take_right) {
            memo[key] = false;
            return false;
        }

        // Если для обоих выборов автомата игрок все еще может достичь m
        memo[key] = true;
        return true;
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    cin >> n;
    for(int i=0;i<n;i++) cin >> a[i];
    vector<int> achievable_m;
    // Перебираем все m от 1 до 49
    for(int m=1; m<50; m++){
        target_m = m;
        memo.clear();
        bool possible = can_win(0, n-1, 0, 0);
        if(possible){
            achievable_m.push_back(m);
        }
    }
    // Выводим результат
    for(int i=0;i<achievable_m.size();i++){
        if(i > 0) cout << ' ';
        cout << achievable_m[i];
    }
    return 0;
}
