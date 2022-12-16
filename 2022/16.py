#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

Valve = recordtype("Valve", "flow_rate is_open tunnels")
State = recordtype("State", "score open_valves v minutes history")

def bfs(valves, max_minutes):
    best = State(0, None, "", 0, "")
    queue = [State(0, set(), "AA", 0, "AA")]
    #heapify(queue)
    heapq._heapify_max(queue)

    cache = dict()

    while len(queue) > 0:
        #state = heappop(queue)
        state = heapq._heappop_max(queue) # pop from maxheap
        #state = queue.pop()


        if state.minutes >= max_minutes:
            if state.score > best.score:
                best = state
                print(best.score, best.history)
            continue



        new_score = state.score + sum([v.flow_rate for k,v in valves.items() if k in state.open_valves])
        #state.pressure_release.append(sum([v.flow_rate for k,v in valves.items() if k in state.open_valves]))
        #state.score += sum([v.flow_rate for k,v in valves.items() if k in state.open_valves])

        # we don't pop from the queue so this element has high priority next round!
        if valves[state.v].flow_rate > 0 and not state.v in state.open_valves:
            #score = sum(state.pressure_release)
            #history = state.history+f" [{state.v}]"
            next_state = State(new_score, state.open_valves.union({state.v}), state.v, state.minutes+1, "")
            heappush(queue, next_state)
            #queue.append(next_state)
            continue

        #print(state.v, list(sorted(valves[state.v].tunnels, key=lambda x: valves[x].flow_rate, reverse=True)))
        for v in sorted(valves[state.v].tunnels, key=lambda x: valves[x].flow_rate, reverse=False):
            #score = sum(state.pressure_release)
            history = state.history+" -> "+v
            next_state = State(new_score, state.open_valves.copy(), v, state.minutes+1, "")
            heappush(queue, next_state)
            #queue.append(next_state)

    return best


cache = dict()

def try_valve2(valves, open_valves, current, minutes, score, history):

    key = (open_valves, current, minutes)
    if key in cache:
        return cache[key]

    if minutes >= 30:
        return score, history


    best = (0, "")
    for open_valve in [True, False]:
        # open valve, if closed
        tmp_history = history
        tmp_open_valves = open_valves
        tmp_minutes = minutes
        tmp_score = score

        ok = not open_valve
        if open_valve and valves[current].flow_rate > 0 and current not in tmp_open_valves:
            tmp_history += f" [{current}]"
            tmp_open_valves += current
            tmp_minutes += 1
            tmp_score += (30-tmp_minutes) * valves[current].flow_rate
            ok = True

        if ok:
            for new_valve in valves[current].tunnels:
                s, p = try_valve2(valves, tmp_open_valves, new_valve, tmp_minutes+1, tmp_score, tmp_history+f" -> {new_valve}")
                if s > best[0]:
                    best = (s, p)

    key = (open_valves, current, minutes)
    cache[key] = best
    return best



def main():

    lines = open_data("16.data")

    valves = dict()

    for line in lines:
        l = line.split(" ")
        v = l[1]
        flow_rate = ints(line)[0]
        vs = line.split(" to ")[1].replace(",", "").split(" ")[1:]
        #print(f"{v} --> {valves}")
        # (flow_rate, is_open, tunnels)
        valves[v] = Valve(flow_rate, False, vs)


    #pressure_release = 0
    #print(try_valve(valves, "AA", 1, pressure_release, 30, "AA "))

    print(try_valve2(valves, "", "AA", 0, 0, "AA"))

    #pressure_release = []
    #
    #r = bfs(valves, 30)
    #print(r)
    #
    #print(sum(r.pressure_release))












if __name__ == "__main__":
    main()

# year 2022
# solution for 16.01: ? < 3303, < 2412, not 2263
# solution for 16.02: ?
