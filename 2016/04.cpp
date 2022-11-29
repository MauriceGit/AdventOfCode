#include <fmt/core.h>
#include <string>
#include <algorithm>
#include <numeric>
#include <iostream>
#include "general.hpp"
#include <unordered_map>

using namespace std;
using namespace general;


int main() {

    auto lines = get_lines("04.data");

    int real_room_id_count{0};
    int north_pole_obj_id{0};

    for (const auto &line : lines) {
        if (line != "") {
            auto s = split2(line, "-");
            auto ends = split2(s[s.size()-1], "[");
            int id;
            (void)from_chars(ends[0].begin(), ends[0].end(), id);

            unordered_map<char, int> count{};
            for (const char &c : s | views::take(s.size()-1) | views::join) {
                count[c]++;
            }

            // to vector for sorting...
            vector<pair<char, int>> v{};
            copy(count.begin(), count.end(), back_inserter(v));
            sort(v.begin(), v.end(), [](auto a, auto b){
                return get<1>(a) > get<1>(b) || get<1>(a) == get<1>(b) && get<0>(a) < get<0>(b);
            });

            auto extract = [](const auto a) -> string {return string{get<0>(a)};};
            auto res = v | views::take(5) | views::transform(extract) | views::join | views::common;
            real_room_id_count += ends[1].starts_with(string(res.begin(), res.end()))*id;

            string unencrypted{};
            for (const auto &tmpS : s | views::take(s.size()-1)) {
                auto tmp = tmpS | views::transform([id](const char &c) -> char {return (c-'a'+id)%26+'a';});
                unencrypted += string(tmp.begin(), tmp.end());
            }
            if (unencrypted.starts_with("northpole")) {
                north_pole_obj_id = id;
            }
        }
    }

    fmt::print("{}\n{}\n", real_room_id_count, north_pole_obj_id);

    return 0;
}

// year 2016
// solution for 04.01: 185371
// solution for 04.02: 984
