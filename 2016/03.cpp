#include <fmt/core.h>
#include <string>
#include <algorithm>
#include <numeric>

#include "general.hpp"

using namespace std;
using namespace general;

bool valid(int a, int b, int c) {
    return a+b > c && a+c > b && b+c > a;
}

int main() {
    auto to_numbers = [](auto v){
        auto to_int = [](const auto &sv){
            int c;
            (void)from_chars(sv.begin(), sv.end(), c);
            return c;
        };
        return split(v, " ") | views::filter([](auto sv){return sv != "";}) | views::transform(to_int);
    };

    auto lines = split(get_input("03.data"), "\n") | views::transform(to_numbers);

    auto to_valid = [](auto l){
        return static_cast<int>(valid(*ranges::next(l.begin(), 0), *ranges::next(l.begin(), 1), *ranges::next(l.begin(), 2)));
    };

    auto tmp = lines | views::transform(to_valid);
    // accumulate didn't make it into ranges for c++20, so we have to call it explicitely. It will be added in c++23 though.
    fmt::print("{}\n",  accumulate(tmp.begin(), tmp.end(), 0));

    int count{0};
    auto line_count{distance(lines.begin(), lines.end())};
    for (int i = 0; i < line_count; i += 3) {
        auto l0 = *ranges::next(lines.begin(), i);
        auto l1 = *ranges::next(lines.begin(), i+1);
        auto l2 = *ranges::next(lines.begin(), i+2);

        count += valid(*ranges::next(l0.begin(), 0), *ranges::next(l1.begin(), 0), *ranges::next(l2.begin(), 0));
        count += valid(*ranges::next(l0.begin(), 1), *ranges::next(l1.begin(), 1), *ranges::next(l2.begin(), 1));
        count += valid(*ranges::next(l0.begin(), 2), *ranges::next(l1.begin(), 2), *ranges::next(l2.begin(), 2));
    }
    fmt::print("{}\n", count);

    return 0;
}
