// 23_reworked project main.go
package main

import (
	"container/heap"
	"fmt"
	"time"
	//"github.com/pkg/profile"
)

const (
	HALL_LENGTH      = 11
	A           byte = 0
	B           byte = 1
	C           byte = 2
	D           byte = 3
	EMPTY       byte = 4
	X           byte = 5
)

var gFinalRooms int64
var gRoomHeight int
var gRoomsArrayLength int
var gRoomX = []int{2, 4, 6, 8}

// 4*7 is the theoretical maximum of next possible steps.
// That is: All the 7 hall places are empty and each of the 4 rooms tries all different hall placements.
var gNextSteps [28]RoomState

var gStepCost = map[byte]int{A: 1, B: 10, C: 100, D: 1000}
var gMapping = map[byte]byte{'a': A, 'b': B, 'c': C, 'd': D, ' ': EMPTY, 'x': X}

type RoomState struct {
	cost int
	// 3 bit per entry. 0..3 == a..d, 4==empty, 5 == x. Corresponding to the final column!
	// 11 places == 33bit --> 64bit int
	hall int64
	// 3 bit per entry. 0..3 == a..d, 4==empty.
	// Max 16 places == 48bit --> 64bit int
	rooms int64
}

type VisitedKey struct {
	hall  int64
	rooms int64
}

type PriorityQueue []RoomState

// Sort interface
func (s PriorityQueue) Len() int {
	return len(s)
}
func (s PriorityQueue) Less(i, j int) bool {
	return s[i].cost < s[j].cost
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

//func isInFinalPosition(c byte, col, yPos int, rooms [16]byte) bool {
func isInFinalPosition(c byte, col, yPos int, rooms int64) bool {
	// c already represents its final column.
	if int(c) != col {
		return false
	}

	// If there is anything underneath the column that is not the same (correct) character, than the final position is not reached yet!
	for p := yPos + 1; p < gRoomHeight; p++ {
		if getAt(rooms, col*gRoomHeight+p) != c {
			return false
		}
	}
	return true
}

func canMoveUp(col, yPos int, rooms int64) bool {
	for p := 0; p < yPos; p++ {
		if getAt(rooms, col*gRoomHeight+p) != EMPTY {
			return false
		}
	}
	return true
}

func emptyAt(i int64, pos int) int64 {
	return i & ^(7 << (pos * 3))
}
func setAt(i int64, pos int, c byte) int64 {
	return emptyAt(i, pos) | (int64(c) << (pos * 3))
}
func getAt(i int64, pos int) byte {
	return byte((i >> (pos * 3)) & 7)
}

func moveRoomToHall(rPos, hPos, roomSteps, hallSteps int, c byte, s RoomState) RoomState {
	cost := (hallSteps + roomSteps + 1) * gStepCost[c]
	return RoomState{s.cost + cost, setAt(s.hall, hPos, c), setAt(s.rooms, rPos, EMPTY)}
}

func moveHallToRoom(hPos, rPos, roomSteps, hallSteps int, c byte, s RoomState) RoomState {
	cost := (hallSteps + roomSteps + 1) * gStepCost[c]
	return RoomState{s.cost + cost, setAt(s.hall, hPos, EMPTY), setAt(s.rooms, rPos, c)}
}

// Does not check the start position and does not check the end position!
// Both are OK, as you can't stand above a room and it should not check the start position anyway!
func checkHallUntil(start, end, incr int, hall int64) bool {
	// Check, if the hall is empty until dstHallPos
	for p := start + incr; p != end && p < HALL_LENGTH; p += incr {
		h := getAt(hall, p)
		if h == X {
			continue
		}
		if h != EMPTY {
			return false
		}
	}
	return true
}

func roomPlacementPossible(col int, c byte, rooms int64) (int, bool) {

	lastIndex := 0

	for i := 0; i < gRoomHeight; i++ {
		p := getAt(rooms, col*gRoomHeight+i)

		if p == EMPTY {
			lastIndex = i
		} else {
			if p != c {
				return 0, false
			}
		}
	}

	return lastIndex, true
}

func calcNextSteps(s RoomState) int {

	nextStepsCount := 0

	// Move from hall to destination room!
	for i := 0; i < HALL_LENGTH; i++ {
		c := getAt(s.hall, i)

		if c == EMPTY || c == X {
			continue
		}

		dstCol := int(c)
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
				gNextSteps[0] = moveHallToRoom(i, dstCol*gRoomHeight+index, index, (dstHallPos-i)*hallDir, c, s)

				// We can immediately stop right here, as this is _always_ a perfect move!
				// So we trim the search tree and consider all other moves after this one!
				return 1
			}
		}
	}

	// Move from room to hall
	for i := 0; i < gRoomsArrayLength; i++ {
		c := getAt(s.rooms, i)

		if c == EMPTY {
			continue
		}
		if i >= gRoomsArrayLength {
			break
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

			h := getAt(s.hall, p)
			if h == X {
				continue
			}
			if h != EMPTY {
				break
			}
			gNextSteps[nextStepsCount] = moveRoomToHall(i, p, yPos, hallCol-p, c, s)
			nextStepsCount++
		}
		// Check open positions to the right and break if one is not empty
		for p := hallCol + 1; p < HALL_LENGTH; p++ {
			h := getAt(s.hall, p)
			if h == X {
				continue
			}
			if h != EMPTY {
				break
			}
			gNextSteps[nextStepsCount] = moveRoomToHall(i, p, yPos, p-hallCol, c, s)
			nextStepsCount++
		}
	}

	return nextStepsCount
}

func dijkstra(state RoomState) int {
	priorityQueue := &PriorityQueue{}
	heap.Init(priorityQueue)

	heap.Push(priorityQueue, state)

	visited := make(map[VisitedKey]bool)

	for priorityQueue.Len() > 0 {
		var s = heap.Pop(priorityQueue).(RoomState)

		if s.rooms == gFinalRooms {
			return s.cost
		}

		key := VisitedKey{s.hall, s.rooms}
		if _, ok := visited[key]; ok {
			continue
		}
		visited[key] = true

		nextStepsCount := calcNextSteps(s)
		for i := 0; i < nextStepsCount; i++ {
			heap.Push(priorityQueue, gNextSteps[i])
		}
	}

	fmt.Println("Never found a valid solution...")
	return -1
}

func parseString(s string) (res int64) {
	for i, c := range s {
		res = setAt(res, i, gMapping[byte(c)])
	}
	return
}

func main() {

	//defer profile.Start(profile.ProfilePath(".")).Stop()
	if aoc, ok := InitAOC(); ok {

		fmt.Println(aoc.GetGroups())

		fmt.Println(aoc.GetChars())

		fmt.Println(Chars(aoc.GetGroups()[0]))

		var rooms [16]byte
		for i, c := range aoc.GetChars() {
			rooms[i%4] = c
		}

	}

	emptyHall := parseString("  x x x x  ")

	parts := []struct {
		finalRoom        int64
		roomHeight       int
		roomsArrayLength int
		hall             int64
		rooms            int64
	}{
		{parseString("aabbccdd"), 2, 8, emptyHall, parseString("bcadbdca")},
		{parseString("aaaabbbbccccdddd"), 4, 16, emptyHall, parseString("bddcacbdbbadcaca")},
	}

	var timings [2]int64

	for i, part := range parts {
		gFinalRooms = part.finalRoom
		gRoomHeight = part.roomHeight
		gRoomsArrayLength = part.roomsArrayLength

		start := time.Now()
		score := dijkstra(RoomState{0, part.hall, part.rooms})
		timings[i] = time.Since(start).Milliseconds()

		fmt.Printf("Part %v: %v in %vms\n", i+1, score, timings[i])

	}

	fmt.Printf("Total runtime: %vms\n", timings[0]+timings[1])

}
