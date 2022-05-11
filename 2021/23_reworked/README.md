
# AOC day 23 reworked

## Motivation
After the initial (and very rough) solution in Python during last years AdventOfCode, I felt quite unhappy with the
not so good runtime of ~60s (don't ask :D).

So I implemented day 23 again from scratch in Go with some proper types and some optimizations.

## Solution and timings
Both parts of my own input now run in 80ms combined. With part 1 in 25ms and part 2 in 55ms.

Additionally I created a list of all possible inputs that have a valid solution (2139 inputs for both parts -- see all_solutions.txt).

On my computer I get the following results overall:

| | Average runtime | Min runtime | Max runtime |
| :--   | :--  | --:  | :-:  |
Part 1  | 12ms | 0ms  | 36ms |
Part 2  | 49ms | 23ms | 72ms |
Overall | 30ms | 0ms  | 72ms |

## Hardware
All tests were run under Linux Mint on a desktop computer with a 9th generation Intel i3 with multiple processes running in the background (browers, IDEs, ...).
