#include <fmt/core.h>
#include <set>

#include "general.hpp"

using namespace std;
using namespace general;

template<int X, int Y>
struct field {
    int x{X/2};
    int y{Y/2};
    char f[Y][X];

    field(initializer_list<char> l) {
        copy(l.begin(), l.end(), &**f);
    }
};

string run(auto &f, const auto &lines) {
    string res{};

    for (const auto &l : lines) {
        for (const auto &c : l) {
            switch (c) {
                case 'R':
                    f.x = !f.f[f.y][f.x+1] ? f.x : f.x+1;
                    break;
                case 'L':
                    f.x = !f.f[f.y][f.x-1] ? f.x : f.x-1;
                    break;
                case 'U':
                    f.y = !f.f[f.y-1][f.x] ? f.y : f.y-1;
                    break;
                case 'D':
                    f.y = !f.f[f.y+1][f.x] ? f.y : f.y+1;
                    break;
            }
        }
        res += f.f[f.y][f.x];
    }
    return res;
}

int main() {
    const auto lines = split(get_input("02.data"), "\n");

    field<5, 5> f1{0, 0,  0,  0, 0,
                   0,'1','2','3',0,
                   0,'4','5','6',0,
                   0,'7','8','9',0,
                   0, 0,  0,  0, 0};
    fmt::print("{}\n", run(f1, lines));

    field<7, 7> f2{0, 0,  0,  0,  0, 0,  0,
                   0, 0,  0, '1', 0, 0,  0,
                   0, 0, '2','3','4',0,  0,
                   0,'5','6','7','8','9',0,
                   0, 0, 'A','B','C',0,  0,
                   0, 0,  0, 'D', 0, 0,  0,
                   0, 0,  0,  0,  0, 0,  0};
    fmt::print("{}\n", run(f2, lines));

    return 0;
}
