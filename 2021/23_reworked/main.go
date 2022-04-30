// 23_reworked project main.go
package main

import (
	"container/heap"
	"fmt"
	"time"

	"github.com/pkg/profile"
)

const (
	HALL_LENGTH = 11
)

var gFinalRooms [16]byte
var gRoomHeight int
var gRoomsArrayLength int
var gRoomX = []int{2, 4, 6, 8}
var gNextSteps [28]RoomState

var gStepCost = map[byte]int{'a': 1, 'b': 10, 'c': 100, 'd': 1000}

type RoomState struct {
	cost  int
	hall  [HALL_LENGTH]byte
	rooms [16]byte
}

type VisitedKey struct {
	hall  [HALL_LENGTH]byte
	rooms [16]byte
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

func isInFinalPosition(c byte, col, yPos int, rooms [16]byte) bool {
	// The final column is: a->0, b->1, c->2, d->3. So ascii-97.
	if int(c)-97 != col {
		return false
	}

	// If there is anything underneath the column that is not the same (correct) character, than the final position is not reached yet!
	for p := yPos + 1; p < gRoomHeight; p++ {
		if byte(rooms[col*gRoomHeight+p]) != c {
			return false
		}
	}
	return true
}

func canMoveUp(col, yPos int, rooms [16]byte) bool {
	for p := 0; p < yPos; p++ {
		if rooms[col*gRoomHeight+p] != ' ' {
			return false
		}
	}
	return true
}

func moveRoomToHall(rPos, hPos, roomSteps, hallSteps int, c byte, s RoomState) RoomState {
	cost := (hallSteps + roomSteps + 1) * gStepCost[c]

	tmpS := s
	tmpS.rooms[rPos] = ' '
	tmpS.hall[hPos] = c
	tmpS.cost += cost

	return tmpS
}

func moveHallToRoom(hPos, rPos, roomSteps, hallSteps int, c byte, s RoomState) RoomState {
	cost := (hallSteps + roomSteps + 1) * gStepCost[c]

	tmpS := s
	tmpS.hall[hPos] = ' '
	tmpS.rooms[rPos] = c
	tmpS.cost += cost

	return tmpS
}

// Does not check the start position and does not check the end position!
// Both are OK, as you can't stand above a room and it should not check the start position anyway!
func checkHallUntil(start, end, incr int, hall [HALL_LENGTH]byte) bool {
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

func roomPlacementPossible(col int, c byte, rooms [16]byte) (int, bool) {

	lastIndex := 0
	for i := 0; i < gRoomHeight; i++ {
		p := byte(rooms[col*gRoomHeight+i])

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

func calcNextSteps(s RoomState) int {

	nextStepsCount := 0
	// 4*7 is the theoretical maximum of next possible steps.
	// That is: All the 7 hall places are empty and each of the 4 rooms tries all different hall placements.
	//var nextSteps [28]RoomState

	// Move from room to hall
	for i, c := range s.rooms {
		if c == ' ' {
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
			h := s.hall[p]
			if h == 'x' {
				continue
			}
			if h != ' ' {
				break
			}
			gNextSteps[nextStepsCount] = moveRoomToHall(i, p, yPos, hallCol-p, c, s)
			nextStepsCount++
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
			gNextSteps[nextStepsCount] = moveRoomToHall(i, p, yPos, p-hallCol, c, s)
			nextStepsCount++
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
				gNextSteps[nextStepsCount] = moveHallToRoom(i, dstCol*gRoomHeight+index, index, (dstHallPos-i)*hallDir, c, s)
				nextStepsCount++
			}
		}

	}

	return nextStepsCount
}

func aStar(state RoomState) int {
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

	return 0
}

func elapsed() func() {
	start := time.Now()
	return func() {
		fmt.Printf("Runtime: %v\n", time.Since(start))
	}
}

func parseRoomsString(s string) (res [16]byte) {
	for i, c := range s {
		res[i] = byte(c)
	}
	return
}
func parseHallString(s string) (res [HALL_LENGTH]byte) {
	for i, c := range s {
		res[i] = byte(c)
	}
	return
}

func main() {

	defer profile.Start(profile.ProfilePath(".")).Stop()

	emptyHall := parseHallString("  x x x x  ")
	parts := []struct {
		finalRoom        [16]byte
		roomHeight       int
		roomsArrayLength int
		hall             [HALL_LENGTH]byte
		rooms            [16]byte
	}{
		{parseRoomsString("aabbccdd"), 2, 8, emptyHall, parseRoomsString("bcadbdca")},
		{parseRoomsString("aaaabbbbccccdddd"), 4, 16, emptyHall, parseRoomsString("bddcacbdbbadcaca")},
	}

	var timings [2]int64

	for i, part := range parts {
		gFinalRooms = part.finalRoom
		gRoomHeight = part.roomHeight
		gRoomsArrayLength = part.roomsArrayLength

		start := time.Now()
		score := aStar(RoomState{0, part.hall, part.rooms})
		timings[i] = time.Since(start).Milliseconds()

		fmt.Printf("Part %v: %v in %vms\n", i+1, score, timings[i])
	}

	fmt.Printf("Total runtime: %vms\n", timings[0]+timings[1])
}
