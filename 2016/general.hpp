#ifndef AOC_GENERAL
#define AOC_GENERAL

#include <filesystem>
#include <fstream>
#include <ranges>
#include <charconv>
#include <vector>

using namespace std;

namespace general {

vector<string> get_lines(string path) {
    vector<string> lines{};
    ifstream ifs;
    string tmp;
    ifs.open(path, ios::in);
    if(ifs) {
        while (!ifs.eof()) {
            string tmp;
            getline(ifs, tmp);
            lines.push_back(tmp);
        }
        ifs.close();
    }
    return lines;
}

// returns a range of string_views
auto split(string_view str, string_view delim) {
    return str | ranges::views::split(delim) | ranges::views::transform([](auto &&rng) {
        return string_view(&*rng.begin(), ranges::distance(rng));
    });
}

vector<string_view> split2(string_view str, string_view delim) {
    vector<string_view> r{};
    ranges::copy(split(str, delim), back_inserter(r));
    return r;
}

}

#endif // AOC_GENERAL
