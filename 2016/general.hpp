#ifndef AOC_GENERAL
#define AOC_GENERAL

#include <filesystem>
#include <fstream>
#include <ranges>
#include <charconv>

using namespace std;

namespace general {

string get_input(string path) {
    ifstream f(path, ios::in | ios::binary);
    const auto size = filesystem::file_size(path);
    string buf(size, '\0');
    f.read(buf.data(), size);
    return buf;
}

// returns a range of string_views
auto split(string_view str, string_view delim) {
    return str | ranges::views::split(delim) | ranges::views::transform([](auto &&rng) {
        return string_view(&*rng.begin(), ranges::distance(rng));
    });
}

}

#endif // AOC_GENERAL
