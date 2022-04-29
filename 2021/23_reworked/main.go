// 23_reworked project main.go
package main

import (
	"container/heap"
	"fmt"
	"time"
)

const (
	HALL_LENGTH = 11
)

var gFinalRooms string
var gRoomHeight int
var gRoomX = []int{2, 4, 6, 8}
var gCheckedNodes int

var gStepCost = map[rune]int{'a': 1, 'b': 10, 'c': 100, 'd': 1000}

type RoomState struct {
	cost          int
	heuristicCost int
	hall          string
	rooms         string
}

type PriorityQueue []RoomState

// Sort interface
func (s PriorityQueue) Len() int {
	return len(s)
}
func (s PriorityQueue) Less(i, j int) bool {
	return s[i].cost+s[i].heuristicCost < s[j].cost+s[j].heuristicCost
}
func (s PriorityQueue) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}

// Heap interface
func (s *PriorityQueue) Push(x any) {
	*s = append(*s, x.(RoomState))
}
func (s *PriorityQueue) Pop() any {
	old := *s
	n := len(old)
	x := old[n-1]
	*s = old[0 : n-1]
	return x
}

func isInFinalPosition(c rune, col, yPos int, rooms string) bool {
	// The final column is: a->0, b->1, c->2, d->3. So ascii-97.
	if int(c)-97 != col {
		return false
	}

	// If there is anything underneath the column that is not the same (correct) character, than the final position is not reached yet!
	for p := yPos + 1; p < gRoomHeight; p++ {
		if rune(rooms[col*gRoomHeight+p]) != c {
			return false
		}
	}
	return true
}

func canMoveUp(col, yPos int, rooms string) bool {
	for p := 0; p < yPos; p++ {
		if rooms[col*gRoomHeight+p] != ' ' {
			return false
		}
	}
	return true
}

// Calculates a rough heuristic of remaining costs based on the manhatten distance of remaining characters
// Results: It explores ~36000 fewer nodes but takes ~50ms longer because calculating the heuristic takes longer than just
// trying some more nodes...
func heuristic(s RoomState) (cost int) {

	return

	for i, c := range s.rooms {
		if c != ' ' && int(c)-97 != int(i/gRoomHeight) {
			cost += (i % gRoomHeight)
		}
	}
	for _, c := range s.hall {
		if c != ' ' && c != 'x' {
			dstCol := int(c) - 97
			dstHallPos := dstCol*2 + 2

			tmp := dstHallPos - dstCol
			if tmp < 0 {
				tmp *= -1
			}
			cost += tmp
		}
	}

	return
}

func moveRoomToHall(rPos, hPos, roomSteps, hallSteps int, c rune, s RoomState) RoomState {
	// TODO: don't use strings at all and switch to []rune/[]byte in general for performance reasons, to avoid the conversions?
	tmpRooms := []rune(s.rooms)
	tmpRooms[rPos] = ' '

	tmpHall := []rune(s.hall)
	tmpHall[hPos] = c

	cost := (hallSteps + roomSteps + 1) * gStepCost[c]

	return RoomState{s.cost + cost, heuristic(s), string(tmpHall), string(tmpRooms)}
}

func moveHallToRoom(hPos, rPos, roomSteps, hallSteps int, c rune, s RoomState) RoomState {
	tmpHall := []rune(s.hall)
	tmpHall[hPos] = ' '

	tmpRooms := []rune(s.rooms)
	tmpRooms[rPos] = c

	cost := (hallSteps + roomSteps + 1) * gStepCost[c]

	return RoomState{s.cost + cost, heuristic(s), string(tmpHall), string(tmpRooms)}
}

// Does not check the start position and does not check the end position!
// Both are OK, as you can't stand above a room and it should not check the start position anyway!
func checkHallUntil(start, end, incr int, hall string) bool {
	// Check, if the hall is empty until dstHallPos
	for p := start + incr; p != end; p += incr {
		h := hall[p]
		if h == 'x' {
			continue
		}
		if h != ' ' {
			return false
		}
	}
	return true
}

func roomPlacementPossible(col int, c rune, rooms string) (int, bool) {

	lastIndex := 0
	for i := 0; i < gRoomHeight; i++ {
		p := rune(rooms[col*gRoomHeight+i])

		if p == ' ' {
			lastIndex = i
		} else {
			if p != c {
				return 0, false
			}
		}
	}

	return lastIndex, true
}

func calcNextSteps(s RoomState) []RoomState {

	var nextSteps []RoomState

	// Move from room to hall
	for i, c := range s.rooms {
		if c == ' ' {
			continue
		}

		yPos := i % gRoomHeight
		roomCol := int(i / gRoomHeight)
		hallCol := roomCol*2 + 2

		// Don't move, if already in destination room all the way down
		if isInFinalPosition(c, roomCol, yPos, s.rooms) {
			continue
		}

		// Don't move, if something is in the way within the room
		if !canMoveUp(roomCol, yPos, s.rooms) {
			continue
		}

		// Check open positions to the left and break if one is not empty
		for p := hallCol - 1; p >= 0; p-- {
			h := s.hall[p]
			if h == 'x' {
				continue
			}
			if h != ' ' {
				break
			}
			nextSteps = append(nextSteps, moveRoomToHall(i, p, yPos, hallCol-p, c, s))
		}
		// Check open positions to the right and break if one is not empty
		for p := hallCol + 1; p < HALL_LENGTH; p++ {
			h := s.hall[p]
			if h == 'x' {
				continue
			}
			if h != ' ' {
				break
			}
			nextSteps = append(nextSteps, moveRoomToHall(i, p, yPos, p-hallCol, c, s))
		}
	}

	// Move from hall to destination room!
	for i, c := range s.hall {
		if c == ' ' || c == 'x' {
			continue
		}

		dstCol := int(c) - 97
		dstHallPos := dstCol*2 + 2

		hallDir := dstHallPos - i
		if hallDir > 0 {
			hallDir = 1
		} else {
			hallDir = -1
		}

		// Check, if the hall is empty until dstHallPos
		if checkHallUntil(i, dstHallPos, hallDir, s.hall) {

			// Check, if there are only correct things in the final room!
			if index, ok := roomPlacementPossible(dstCol, c, s.rooms); ok {

				nextSteps = append(nextSteps, moveHallToRoom(i, dstCol*gRoomHeight+index, index, (dstHallPos-i)*hallDir, c, s))
			}
		}

	}

	return nextSteps
}

func aStar(state RoomState) int {
	priorityQueue := &PriorityQueue{}
	heap.Init(priorityQueue)

	heap.Push(priorityQueue, state)

	visited := make(map[string]bool)

	for priorityQueue.Len() > 0 {
		var s = heap.Pop(priorityQueue).(RoomState)

		gCheckedNodes++

		if s.rooms == gFinalRooms {
			return s.cost
		}

		if _, ok := visited[s.hall+s.rooms]; ok {
			continue
		}
		visited[s.hall+s.rooms] = true

		nextSteps := calcNextSteps(s)

		for _, nextStep := range nextSteps {
			heap.Push(priorityQueue, nextStep)
		}
	}

	return 0
}

func elapsed() func() {
	start := time.Now()
	return func() {
		fmt.Printf("Runtime: %v\n", time.Since(start))
	}
}

func main() {

	parts := []struct {
		finalRoom  string
		roomHeight int
		hall       string
		rooms      string
	}{{"aabbccdd", 2, "  x x x x  ", "bcadbdca"}, {"aaaabbbbccccdddd", 4, "  x x x x  ", "bddcacbdbbadcaca"}}

	var timings [2]int64

	for i, part := range parts {
		gFinalRooms = part.finalRoom
		gRoomHeight = part.roomHeight

		start := time.Now()
		score := aStar(RoomState{0, 0, part.hall, part.rooms})
		timings[i] = time.Since(start).Milliseconds()

		fmt.Printf("Part %v: %v in %vms\n", i+1, score, timings[i])
	}

	fmt.Printf("Total runtime: %vms\n", timings[0]+timings[1])
	fmt.Printf("Checked nodes: %v\n", gCheckedNodes)
}
