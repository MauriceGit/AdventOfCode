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

bool valid(auto &r) {
    int a[3]{};
    int i{0};
    for (const auto &tmp : r) {
        a[i++] = tmp;
    }
    return a[0]+a[1] > a[2] && a[0]+a[2] > a[1] && a[1]+a[2] > a[0];
}

int main() {

    auto input = split(get_input("03.data"), "\n");

    int sum{0};
    for (int ii = 0; ii < 1; ii++) {
        auto to_numbers = [](auto v){
            auto to_int = [](const auto &sv){
                int c;
                (void)from_chars(sv.begin(), sv.end(), c);
                return c;
            };
            return split(v, " ") | views::filter([](auto sv){return sv != "";}) | views::transform(to_int);
        };

        auto lines = input | views::transform(to_numbers);

        auto to_valid = [](auto l){
            return static_cast<int>(valid(l));
        };

        auto tmp = lines | views::transform(to_valid);
        // accumulate didn't make it into ranges for c++20, so we have to call it explicitely. It will be added in c++23 though.
        fmt::print("{}\n",  accumulate(tmp.begin(), tmp.end(), 0));
        //sum += accumulate(tmp.begin(), tmp.end(), 0);

        int count{0};
        auto line{0};
        int d[3][3]{};

        for (auto l : lines) {
            int i{0};
            for (const auto &tmp : l) {
                d[i++][line%3] = tmp;
            }
            if (line%3 == 2) {
                count += valid(d[0][0], d[0][1], d[0][2]);
                count += valid(d[1][0], d[1][1], d[1][2]);
                count += valid(d[2][0], d[2][1], d[2][2]);
            }
            line++;
        }
        fmt::print("{}\n", count);
        //sum += count;
    }
    //fmt::print("{}\n", sum);

    return 0;
}

// year 2016
// solution for 03.01: 983
// solution for 03.02: 1836
