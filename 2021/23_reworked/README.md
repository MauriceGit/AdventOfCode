
# AOC day 23 reworked

## Motivation
After the initial (and very rough) solution in Python during last years AdventOfCode, I felt quite unhappy with the
not so good runtime of ~60s (don't ask :D).

So I implemented day 23 again from scratch in Go with some proper types and some optimizations.

## Solution and timings
Both parts of my own input now run in 81ms combined. With part 1 in 25ms and part 2 in 56ms.

Additionally I created a list of all possible inputs that have a valid solution (2139 inputs for both parts -- see all_solutions.txt).

On my computer I get the following results overall:

| | Average runtime | Min runtime | Max runtime |
| :--   | :--  | --:  | :-:  |
Part 1  | 12ms | 0ms  | 36ms |
Part 2  | 49ms | 23ms | 72ms |
Overall | 30ms | 0ms  | 72ms |

## Hardware
All tests were run under Linux Mint on a desktop computer with a 9th generation Intel i3 with multiple processes running in the background (browers, IDEs, ...).

## Implemented list of optimizations

- The hall is compressed into an int64 with 3bits each place (a, b, c, d, empty, x)
- The rooms are also combined and compressed into an int64 (3bits per place)
- So each game state is represented in only three int64 (cost, hall, rooms)
- Dijkstra for shortest path (surprisingly, for A* it takes longer to calculate even a rough heuristic than it takes to just evaluate >30k nodes on top)
- Some calculations (is it possible to move up within the room) can be reduced to a single expression (with bit-operations on the int64)
- Deadlock detection: Two pods are in a hall and would need to pass each other to reach their destination room (state can be discarded!)
- Divide-and-Conquer approach: If a pod is in the hall, only the side to the destination room matters until the pod reached its room. If that is not possible, the situation can't be solved anyway.

## Run

> go run .

This will run my own input. For all possible input, change the "if false {" to true in the main function.

## Calculate average runtimes

To get the numbers above, run this program with all inputs (change the if in the main function to true) and replace the "all_solutions.txt" file with the output.

Then run
> eval_all_solutions.py
to get the min/max/avg runtimes.
