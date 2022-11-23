#include <fmt/core.h>
#include <set>

#include "general.hpp"

using namespace std;
using namespace general;

int main() {
    string data = get_input("01.data");
    const auto lines = split(data, "\n");

    pair<int, int> pos{0, 0};
    pair<int, int> dir{0, 1};

    set<pair<int, int>> positions{};
    positions.insert(pos);

    int first_double = -1;

    for (auto s : split(*lines.begin(), ", ")) {
        int c;
        // string_view to int - no errors possible (for aoc specifically)
        (void)from_chars(s.begin()+1, s.end(), c);
        dir = s[0] == 'R' ? make_pair(get<1>(dir), -get<0>(dir)) : make_pair(-get<1>(dir), get<0>(dir));

        for (int i = 1; i <= c && first_double < 0; i++) {
            pair<int, int> tmp = {get<0>(pos)+i*get<0>(dir), get<1>(pos)+i*get<1>(dir)};
            if (first_double < 0 && positions.contains(tmp)) {
                first_double = abs(get<0>(tmp))+abs(get<1>(tmp));
                break;
            }
            positions.insert(tmp);
        }
        pos = {get<0>(pos)+c*get<0>(dir), get<1>(pos)+c*get<1>(dir)};
    }
    fmt::print("{}\n", abs(get<0>(pos))+abs(get<1>(pos)));
    fmt::print("{}\n", first_double);
    return 0;
}

// year 2016
// solution for 01.01: 300
// solution for 01.02: 159
