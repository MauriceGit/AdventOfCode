// 23_reworked project main.go
package main

import (
	"container/heap"
	"fmt"
	"time"
	//"github.com/pkg/profile"
)

const (
	A             byte  = 0
	B             byte  = 1
	C             byte  = 2
	D             byte  = 3
	EMPTY         byte  = 4
	X             byte  = 5
	HALL_LENGTH         = 11
	LONGEMPTY     int64 = int64(EMPTY)<<6 | int64(EMPTY)<<3 | int64(EMPTY)
	IMPORTANTBITS int64 = 511
)

var gFinalRooms int64
var gRoomHeight int
var gRoomsArrayLength int

// 4*7 is the theoretical maximum of next possible steps.
// That is: All the 7 hall places are empty and each of the 4 rooms tries all different hall placements.
var gNextSteps [28]RoomState
var gStepCost = [...]int{1, 10, 100, 1000, 0, 0}
var gMapping = map[byte]byte{'a': A, 'b': B, 'c': C, 'd': D, ' ': EMPTY, 'x': X}

type RoomState struct {
	cost int
	// 3 bit per entry. 0..3 == a..d, 4==empty, 5 == x. Corresponding to the final column!
	// 11 places == 33bit --> 64bit int
	hall int64
	// 3 bit per entry. 0..3 == a..d, 4==empty.
	// Max 16 places == 48bit --> 64bit int
	rooms                int64
	roomsReadyToMoveInto int16
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

func emptyAt(i int64, pos int) int64 {
	return i & ^(7 << (pos * 3))
}
func setAt(i int64, pos int, c byte) int64 {
	return emptyAt(i, pos) | (int64(c) << (pos * 3))
}
func getAt(i int64, pos int) byte {
	return byte((i >> (pos * 3)) & 7)
}

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

// Only check the very next position, as there cann ever be empty spaces within a room!
func canMoveUp(col, yPos int, rooms int64) bool {
	return yPos == 0 || getAt(rooms, col*gRoomHeight+yPos-1) == EMPTY
}

func moveRoomToHall(rPos, hPos, hallSteps int, c byte, s RoomState) RoomState {
	cost := hallSteps * gStepCost[c]
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

	p0, p1, p2 := getAt(s.hall, 3), getAt(s.hall, 5), getAt(s.hall, 7)

	// Deadlock detection.
	// If two characters need to go to the other side of each other, this situation can not be resolved!
	// Relevant positions within the hall are: 3, 5, 7
	// So we only check those positions explicitely!
	if p0 == D && (p1 == A || p2 == A) {
		return 0
	}
	if p0 == C && p1 == A {
		return 0
	}
	if p1 == A && (p0 == C || p0 == D) {
		return 0
	}
	if p1 == D && (p2 == A || p2 == B) {
		return 0
	}
	if p2 == A && (p0 == D || p1 == D) {
		return 0
	}
	if p2 == B && p1 == D {
		return 0
	}

	minHallX, maxHallX := 0, HALL_LENGTH
	// Divide-Conquer approach.
	// If a character is in the middle hall from their corresponding room, only the target side of the rooms+hall
	// matter right now. We can approach one side of the game state as a sub-problem and solve it independently first!
	if p0 == A {
		maxHallX = 3 + 1
	} else if p2 == D {
		minHallX = 7
	} else if p1 == A || p1 == B {
		maxHallX = 5 + 1
	} else if p1 == C || p1 == D {
		minHallX = 5
	}

	// Move from hall to destination room!
	for i := minHallX; i < maxHallX; i++ {
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
		for p := hallCol - 1; p >= minHallX; p-- {

			h := getAt(s.hall, p)
			if h == X {
				continue
			}
			if h != EMPTY {
				break
			}
			gNextSteps[nextStepsCount] = moveRoomToHall(i, p, hallCol-p, c, s)
			nextStepsCount++
		}
		// Check open positions to the right and break if one is not empty
		for p := hallCol + 1; p < maxHallX; p++ {
			h := getAt(s.hall, p)
			if h == X {
				continue
			}
			if h != EMPTY {
				break
			}
			gNextSteps[nextStepsCount] = moveRoomToHall(i, p, p-hallCol, c, s)
			nextStepsCount++
		}
	}

	return nextStepsCount
}

// Called only once in the very beginning. Each non-final pod needs to move out.
// So the cost for that can be precomputed once.
func precomputeMovingOutOfRoom(state RoomState) int {
	cost := 0
	for i := 0; i < gRoomsArrayLength; i++ {
		c := getAt(state.rooms, i)
		roomCol := int(i / gRoomHeight)
		yPos := i % gRoomHeight

		if !isInFinalPosition(c, roomCol, yPos, state.rooms) {
			cost += (yPos + 1) * gStepCost[c]
		}

	}
	return cost
}

// All places are either empty or filled with the correct pod
func roomIsClean(rooms int64, col int) bool {
	for y := gRoomHeight; y >= 0; y-- {
		c := getAt(rooms, y)
		if c == EMPTY {
			return true
		}
		if int(c) != col {
			return false
		}
	}
	return true
}

func initReadyToMoveIntoRooms(rooms int64) int8 {
	var ready int8
	for col := 0; col < 4; col++ {
		if roomIsClean(rooms, col) {
			ready = ready | (1 << col * gRoomHeight)
		}
	}
	return ready
}

func dijkstra(state RoomState) int {

	// Precompute the cost of moving from the room into the hall.
	state.cost = precomputeMovingOutOfRoom(state)

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

	// This is not yet working. So ignore that. Need to revisit at some time for proper input parsing
	if false {
		if aoc, ok := InitAOC(); ok {
			fmt.Println(aoc.GetGroups())
			fmt.Println(aoc.GetChars())
			fmt.Println(Chars(aoc.GetGroups()[0]))
			var rooms [16]byte
			for i, c := range aoc.GetChars() {
				rooms[i%4] = c
			}
		}
	}

	emptyHall := parseString("  x x x x  ")

	// Try out all possible solutions and print out timings for each one. Good for statistical analysis later.
	if false {
		// all valid variations that have solutions
		variations := []string{"cacbddab", "cddaccbbdbadaacb", "bdacacdb", "bdddacbcabacdacb", "dacdacbb", "dddaccbdabacbacb", "cadabdbc", "cddadcbabbadbacc", "bacddabc", "bddaccbddbaabacc", "cbaadcdb", "cddbacbadbacdacb", "daccbdba", "dddaccbcbbadbaca", "cdbdbcaa", "cdddbcbdbbacaaca", "abacdcbd", "addbacbcdbacbacd", "dcabdbac", "dddcacbbdbabaacc", "dcbaabcd", "dddcbcbaababcacd", "daacbcdb", "dddaacbcbbacdacb", "bdaccadb", "bdddacbccbaadacb", "dadccbba", "dddadcbccbabbaca", "bcadacbd", "bddcacbdabacbacd", "bcbdacda", "bddcbcbdabacdaca", "dbcacbda", "dddbccbacbabdaca", "cabdcadb", "cddabcbdcbaadacb", "acdcbbad", "addcdcbcbbabaacd", "bcdabcda", "bddcdcbabbacdaca", "bdccbdaa", "bdddccbcbbadaaca", "abdccadb", "addbdcbccbaadacb", "acbdbadc", "addcbcbdbbaadacc", "dbdbcaca", "dddbdcbbcbaacaca", "cadabcbd", "cddadcbabbacbacd", "dadcbcba", "dddadcbcbbacbaca", "dbcabcad", "dddbccbabbacaacd", "badabccd", "bddadcbabbaccacd", "cbdcabad", "cddbdcbcababaacd", "ccabaddb", "cddcacbbabaddacb", "dbcdaacb", "dddbccbdabaacacb", "bcbadcda", "bddcbcbadbacdaca", "bddbacac", "bddddcbbabacaacc", "addcbcba", "addddcbcbbacbaca", "badccdab", "bddadcbccbadaacb", "bdcbacad", "bdddccbbabacaacd", "bcaacbdd", "bddcacbacbabdacd", "cadbcbda", "cddadcbbcbabdaca", "ddbabcca", "ddddbcbabbaccaca", "abbcacdd", "addbbcbcabacdacd", "abccaddb", "addbccbcabaddacb", "cacbdbda", "cddaccbbdbabdaca", "abbcddac", "addbbcbcdbadaacc", "baccadbd", "bddaccbcabadbacd", "abcdacdb", "addbccbdabacdacb", "cdbdbaca", "cdddbcbdbbaacaca", "dcbbdaca", "dddcbcbbdbaacaca", "dbacadcb", "dddbacbcabadcacb", "abccbdda", "addbccbcbbaddaca", "bbdcacda", "bddbdcbcabacdaca", "dccabbad", "dddcccbabbabaacd", "cbacbadd", "cddbacbcbbaadacd", "bcadbdca", "bddcacbdbbadcaca", "adacbcdb", "adddacbcbbacdacb", "bcadacdb", "bddcacbdabacdacb", "aabcbddc", "addabcbcbbaddacc", "dbbadcac", "dddbbcbadbacaacc", "cadcbabd", "cddadcbcbbaabacd", "abadccdb", "addbacbdcbacdacb", "caadbcdb", "cddaacbdbbacdacb", "dadbcabc", "dddadcbbcbaabacc", "dbabccda", "dddbacbbcbacdaca", "bcbdcada", "bddcbcbdcbaadaca", "abddbcca", "addbdcbdbbaccaca", "accadbbd", "addcccbadbabbacd", "dccdaabb", "dddcccbdabaabacb", "dabdacbc", "dddabcbdabacbacc", "adadcbbc", "adddacbdcbabbacc", "addbccab", "addddcbbcbacaacb", "ddaccbba", "ddddacbccbabbaca", "dbdccaab", "dddbdcbccbaaaacb", "adcbcbad", "adddccbbcbabaacd", "cddbabac", "cddddcbbababaacc", "ddabcacb", "ddddacbbcbaacacb", "aabcbcdd", "addabcbcbbacdacd", "baaddccb", "bddaacbddbaccacb", "bdacbdca", "bdddacbcbbadcaca", "dabacbcd", "dddabcbacbabcacd", "dabadcbc", "dddabcbadbacbacc", "dccbadba", "dddcccbbabadbaca", "daccbadb", "dddaccbcbbaadacb", "aadbdcbc", "addadcbbdbacbacc", "dcbbdcaa", "dddcbcbbdbacaaca", "badabdcc", "bddadcbabbadcacc", "abadbcdc", "addbacbdbbacdacc", "bacabdcd", "bddaccbabbadcacd", "ccadbbad", "cddcacbdbbabaacd", "dcbcbaad", "dddcbcbcbbaaaacd", "baaccdbd", "bddaacbccbadbacd", "acbbacdd", "addcbcbbabacdacd", "bddcaabc", "bddddcbcabaabacc", "cacadbbd", "cddaccbadbabbacd", "cabadbdc", "cddabcbadbabdacc", "dbbacdac", "dddbbcbacbadaacc", "bacdcdab", "bddaccbdcbadaacb", "dacabcdb", "dddaccbabbacdacb", "cabdadbc", "cddabcbdabadbacc", "dcdbbaca", "dddcdcbbbbaacaca", "acdcabbd", "addcdcbcababbacd", "daccadbb", "dddaccbcabadbacb", "caabdbdc", "cddaacbbdbabdacc", "abcabddc", "addbccbabbaddacc", "abacbddc", "addbacbcbbaddacc", "daacbdcb", "dddaacbcbbadcacb", "cacbbdad", "cddaccbbbbadaacd", "cdbbdcaa", "cdddbcbbdbacaaca", "dabdbcca", "dddabcbdbbaccaca", "cbaacddb", "cddbacbacbaddacb", "cdabadbc", "cdddacbbabadbacc", "dcbaadbc", "dddcbcbaabadbacc", "abaccbdd", "addbacbccbabdacd", "adabbcdc", "adddacbbbbacdacc", "bcadbadc", "bddcacbdbbaadacc", "abcbcdad", "addbccbbcbadaacd", "bdabccda", "bdddacbbcbacdaca", "aadcdbcb", "addadcbcdbabcacb", "aabddbcc", "addabcbddbabcacc", "cabdcbda", "cddabcbdcbabdaca", "dbabdcca", "dddbacbbdbaccaca", "abccdbad", "addbccbcdbabaacd", "dcacabbd", "dddcacbcababbacd", "dabaccbd", "dddabcbacbacbacd", "dbacbacd", "dddbacbcbbaacacd", "aacbdcbd", "addaccbbdbacbacd", "badcdbca", "bddadcbcdbabcaca", "bacdcbda", "bddaccbdcbabdaca", "cbadcbda", "cddbacbdcbabdaca", "bbacddac", "bddbacbcdbadaacc", "cbcdaabd", "cddbccbdabaabacd", "badcabcd", "bddadcbcababcacd", "bacdadcb", "bddaccbdabadcacb", "aabbdcdc", "addabcbbdbacdacc", "cdbcbdaa", "cdddbcbcbbadaaca", "baacdbcd", "bddaacbcdbabcacd", "abdbacdc", "addbdcbbabacdacc", "ababcddc", "addbacbbcbaddacc", "acbdcdab", "addcbcbdcbadaacb", "cdabbacd", "cdddacbbbbaacacd", "acdcabdb", "addcdcbcababdacb", "dcbabacd", "dddcbcbabbaacacd", "bcbaacdd", "bddcbcbaabacdacd", "bcdcaabd", "bddcdcbcabaabacd", "daadbccb", "dddaacbdbbaccacb", "cdacbdba", "cdddacbcbbadbaca", "adbdccba", "adddbcbdcbacbaca", "dcdcbaba", "dddcdcbcbbaabaca", "cbacdbda", "cddbacbcdbabdaca", "badcbdca", "bddadcbcbbadcaca", "cabdabdc", "cddabcbdababdacc", "bcddbcaa", "bddcdcbdbbacaaca", "ddbacbca", "ddddbcbacbabcaca", "accdbadb", "addcccbdbbaadacb", "abadcdcb", "addbacbdcbadcacb", "ccaabdbd", "cddcacbabbadbacd", "adbaccdb", "adddbcbacbacdacb", "ccaabbdd", "cddcacbabbabdacd", "dbabcdca", "dddbacbbcbadcaca", "abacdbcd", "addbacbcdbabcacd", "abdabccd", "addbdcbabbaccacd", "adcabdbc", "adddccbabbadbacc", "dababccd", "dddabcbabbaccacd", "dbdcabca", "dddbdcbcababcaca", "acbcabdd", "addcbcbcababdacd", "aacbdcdb", "addaccbbdbacdacb", "caaddcbb", "cddaacbddbacbacb", "baadbcdc", "bddaacbdbbacdacc", "aaddbbcc", "addadcbdbbabcacc", "baccbdad", "bddaccbcbbadaacd", "cbbcadda", "cddbbcbcabaddaca", "ddbacbac", "ddddbcbacbabaacc", "caddcbba", "cddadcbdcbabbaca", "dcabacdb", "dddcacbbabacdacb", "adcacbbd", "adddccbacbabbacd", "bdcabcda", "bdddccbabbacdaca", "adcdbcab", "adddccbdbbacaacb", "acbdcbda", "addcbcbdcbabdaca", "cadabbcd", "cddadcbabbabcacd", "ddaacbbc", "ddddacbacbabbacc", "babccdda", "bddabcbccbaddaca", "dcabbdac", "dddcacbbbbadaacc", "bccbaadd", "bddcccbbabaadacd", "adbcdcab", "adddbcbcdbacaacb", "addbacbc", "addddcbbabacbacc", "bbdaccda", "bddbdcbacbacdaca", "dcabcadb", "dddcacbbcbaadacb", "badaccdb", "bddadcbacbacdacb", "acabddbc", "addcacbbdbadbacc", "dcbabcad", "dddcbcbabbacaacd", "accbbdda", "addcccbbbbaddaca", "bcabacdd", "bddcacbbabacdacd", "dcdabbca", "dddcdcbabbabcaca", "dabacdbc", "dddabcbacbadbacc", "cdcababd", "cdddccbabbaabacd", "bcabddac", "bddcacbbdbadaacc", "cdcbabad", "cdddccbbababaacd", "bbdcaadc", "bddbdcbcabaadacc", "cbadadbc", "cddbacbdabadbacc", "badadbcc", "bddadcbadbabcacc", "cabdbacd", "cddabcbdbbaacacd", "dbdacacb", "dddbdcbacbaacacb", "bacddbca", "bddaccbddbabcaca", "ccabdbad", "cddcacbbdbabaacd", "daaccbbd", "dddaacbccbabbacd", "acdbadcb", "addcdcbbabadcacb", "bcddabac", "bddcdcbdababaacc", "abbdccad", "addbbcbdcbacaacd", "dbacbcad", "dddbacbcbbacaacd", "bcaddbac", "bddcacbddbabaacc", "adcbdbac", "adddccbbdbabaacc", "adbccdba", "adddbcbccbadbaca", "dcdbabca", "dddcdcbbababcaca", "ccdbbaad", "cddcdcbbbbaaaacd", "ddabbacc", "ddddacbbbbaacacc", "bacbacdd", "bddaccbbabacdacd", "cdadabcb", "cdddacbdababcacb", "bccdaabd", "bddcccbdabaabacd", "dcbbaacd", "dddcbcbbabaacacd", "bdcdbcaa", "bdddccbdbbacaaca", "bacddbac", "bddaccbddbabaacc", "dbaabdcc", "dddbacbabbadcacc", "aaddcbbc", "addadcbdcbabbacc", "cbadacbd", "cddbacbdabacbacd", "dabadbcc", "dddabcbadbabcacc", "bacbcdda", "bddaccbbcbaddaca", "ddaabbcc", "ddddacbabbabcacc", "dadabccb", "dddadcbabbaccacb", "abcacdbd", "addbccbacbadbacd", "ddacbcab", "ddddacbcbbacaacb", "acdbbcda", "addcdcbbbbacdaca", "bdbdcaca", "bdddbcbdcbaacaca", "cdacbadb", "cdddacbcbbaadacb", "abdabdcc", "addbdcbabbadcacc", "dbaabccd", "dddbacbabbaccacd", "abcabdcd", "addbccbabbadcacd", "baddacbc", "bddadcbdabacbacc", "bacbdcad", "bddaccbbdbacaacd", "acabbcdd", "addcacbbbbacdacd", "cdbdcaab", "cdddbcbdcbaaaacb", "abacbdcd", "addbacbcbbadcacd", "babdcadc", "bddabcbdcbaadacc", "daccbdab", "dddaccbcbbadaacb", "adbdbcac", "adddbcbdbbacaacc", "bbcacdad", "bddbccbacbadaacd", "dbabcadc", "dddbacbbcbaadacc", "acbbdadc", "addcbcbbdbaadacc", "ccbaadbd", "cddcbcbaabadbacd", "adabbccd", "adddacbbbbaccacd", "abdbadcc", "addbdcbbabadcacc", "cabdbcad", "cddabcbdbbacaacd", "dcabbadc", "dddcacbbbbaadacc", "dbdaacbc", "dddbdcbaabacbacc", "dadcbcab", "dddadcbcbbacaacb", "ddacabcb", "ddddacbcababcacb", "bbdaaccd", "bddbdcbaabaccacd", "aadcdcbb", "addadcbcdbacbacb", "aabddcbc", "addabcbddbacbacc", "abddccab", "addbdcbdcbacaacb", "adbbdcac", "adddbcbbdbacaacc", "cdbabcad", "cdddbcbabbacaacd", "aabbcddc", "addabcbbcbaddacc", "ddbabcac", "ddddbcbabbacaacc", "ccababdd", "cddcacbbababdacd", "aabbdccd", "addabcbbdbaccacd", "badccbad", "bddadcbccbabaacd", "abdbaccd", "addbdcbbabaccacd", "cddcaabb", "cddddcbcabaabacb", "ababcdcd", "addbacbbcbadcacd", "cbadbcad", "cddbacbdbbacaacd", "adbdabcc", "adddbcbdababcacc", "cababddc", "cddabcbabbaddacc", "cadabbdc", "cddadcbabbabdacc", "cdbacabd", "cdddbcbacbaabacd", "daccbbda", "dddaccbcbbabdaca", "cabadcbd", "cddabcbadbacbacd", "cabddacb", "cddabcbddbaacacb", "caacbbdd", "cddaacbcbbabdacd", "dccbaabd", "dddcccbbabaabacd", "dabcabcd", "dddabcbcababcacd", "baabdcdc", "bddaacbbdbacdacc", "baddcabc", "bddadcbdcbaabacc", "cdabcbda", "cdddacbbcbabdaca", "dcacbadb", "dddcacbcbbaadacb", "cacbadbd", "cddaccbbabadbacd", "abcbdadc", "addbccbbdbaadacc", "bdbcaadc", "bdddbcbcabaadacc", "cbdbaadc", "cddbdcbbabaadacc", "cdbaabcd", "cdddbcbaababcacd", "ddbaccba", "ddddbcbacbacbaca", "cabbddca", "cddabcbbdbadcaca", "baadbccd", "bddaacbdbbaccacd", "bacbddac", "bddaccbbdbadaacc", "abcadcbd", "addbccbadbacbacd", "ddaccbab", "ddddacbccbabaacb", "dbdcacba", "dddbdcbcabacbaca", "abdcbdca", "addbdcbcbbadcaca", "cbadbacd", "cddbacbdbbaacacd", "bdbdccaa", "bdddbcbdcbacaaca", "cadadbbc", "cddadcbadbabbacc", "bbadccad", "bddbacbdcbacaacd", "bdccaabd", "bdddccbcabaabacd", "adcbcadb", "adddccbbcbaadacb", "bcbaadcd", "bddcbcbaabadcacd", "dbcadbac", "dddbccbadbabaacc", "cadbdbac", "cddadcbbdbabaacc", "dbabdacc", "dddbacbbdbaacacc", "dbdabcac", "dddbdcbabbacaacc", "acdbbdca", "addcdcbbbbadcaca", "ddbbacca", "ddddbcbbabaccaca", "bdadccba", "bdddacbdcbacbaca", "abdcbdac", "addbdcbcbbadaacc", "dbaccdab", "dddbacbccbadaacb", "baacbdcd", "bddaacbcbbadcacd", "cabcbdda", "cddabcbcbbaddaca", "dbccdbaa", "dddbccbcdbabaaca", "acdbbdac", "addcdcbbbbadaacc", "daabcdcb", "dddaacbbcbadcacb", "dccadbba", "dddcccbadbabbaca", "ddbbacac", "ddddbcbbabacaacc", "abdacbcd", "addbdcbacbabcacd", "bbadaccd", "bddbacbdabaccacd", "dbccabad", "dddbccbcababaacd", "bdadbacc", "bdddacbdbbaacacc", "bbcddaac", "bddbccbddbaaaacc", "bdaabdcc", "bdddacbabbadcacc", "dccaabbd", "dddcccbaababbacd", "cbcabdda", "cddbccbabbaddaca", "cbadbdac", "cddbacbdbbadaacc", "dcdbbaac", "dddcdcbbbbaaaacc", "bbadcacd", "bddbacbdcbaacacd", "caabbdcd", "cddaacbbbbadcacd", "adbcabcd", "adddbcbcababcacd", "adacbdbc", "adddacbcbbadbacc", "dcbbcada", "dddcbcbbcbaadaca", "cbcbadda", "cddbccbbabaddaca", "acabcddb", "addcacbbcbaddacb", "cbcdabad", "cddbccbdababaacd", "dabdcacb", "dddabcbdcbaacacb", "adaccbbd", "adddacbccbabbacd", "dbabdcac", "dddbacbbdbacaacc", "adabcdcb", "adddacbbcbadcacb", "dacbdacb", "dddaccbbdbaacacb", "babdcacd", "bddabcbdcbaacacd", "abcaddbc", "addbccbadbadbacc", "acacbdbd", "addcacbcbbadbacd", "bbdccaad", "bddbdcbccbaaaacd", "babacddc", "bddabcbacbaddacc", "bccbdada", "bddcccbbdbaadaca", "bdcdbaac", "bdddccbdbbaaaacc", "cabbdadc", "cddabcbbdbaadacc", "acdabbcd", "addcdcbabbabcacd", "dcabbacd", "dddcacbbbbaacacd", "bdcbcaad", "bdddccbbcbaaaacd", "acadcdbb", "addcacbdcbadbacb", "abcdbcda", "addbccbdbbacdaca", "adccbadb", "adddccbcbbaadacb", "bdadbcac", "bdddacbdbbacaacc", "adcbacdb", "adddccbbabacdacb", "abdcbadc", "addbdcbcbbaadacc", "dcbadcba", "dddcbcbadbacbaca", "abddacbc", "addbdcbdabacbacc", "dccbabda", "dddcccbbababdaca", "dbbaacdc", "dddbbcbaabacdacc", "cacdbdba", "cddaccbdbbadbaca", "acdbbadc", "addcdcbbbbaadacc", "dcacadbb", "dddcacbcabadbacb", "aacbdbdc", "addaccbbdbabdacc", "cadbabcd", "cddadcbbababcacd", "dbadccba", "dddbacbdcbacbaca", "bddccaba", "bddddcbccbaabaca", "bbcdaadc", "bddbccbdabaadacc", "aabdcbcd", "addabcbdcbabcacd", "bdcbaacd", "bdddccbbabaacacd", "dcbdbaca", "dddcbcbdbbaacaca", "ddacbabc", "ddddacbcbbaabacc", "acbbddac", "addcbcbbdbadaacc", "dbdcabac", "dddbdcbcababaacc", "dbaaccdb", "dddbacbacbacdacb", "cababdcd", "cddabcbabbadcacd", "bbccdaad", "bddbccbcdbaaaacd", "bcdbacda", "bddcdcbbabacdaca", "dbdbacac", "dddbdcbbabacaacc", "bbcadadc", "bddbccbadbaadacc", "baadcdbc", "bddaacbdcbadbacc", "addcbbca", "addddcbcbbabcaca", "dcbdbaac", "dddcbcbdbbaaaacc", "abdccbad", "addbdcbccbabaacd", "caddcbab", "cddadcbdcbabaacb", "cadbcadb", "cddadcbbcbaadacb", "aacddbbc", "addaccbddbabbacc", "acbadbcd", "addcbcbadbabcacd", "cdbbcada", "cdddbcbbcbaadaca", "accdabbd", "addcccbdababbacd", "acdbcbad", "addcdcbbcbabaacd", "abcdabdc", "addbccbdababdacc", "caadcdbb", "cddaacbdcbadbacb", "acddabcb", "addcdcbdababcacb", "bccdabad", "bddcccbdababaacd", "cdbaacbd", "cdddbcbaabacbacd", "dbbccaad", "dddbbcbccbaaaacd", "bddcbaca", "bddddcbcbbaacaca", "baccdabd", "bddaccbcdbaabacd", "dccbbdaa", "dddcccbbbbadaaca", "abcddbca", "addbccbddbabcaca", "addbcbca", "addddcbbcbabcaca", "dacbdcab", "dddaccbbdbacaacb", "ccbddbaa", "cddcbcbddbabaaca", "abadcbdc", "addbacbdcbabdacc", "cdcdabba", "cdddccbdababbaca", "bddcbaac", "bddddcbcbbaaaacc", "bdccbaad", "bdddccbcbbaaaacd", "adcabbdc", "adddccbabbabdacc", "cbdacbad", "cddbdcbacbabaacd", "cdbcdbaa", "cdddbcbcdbabaaca", "ddaabccb", "ddddacbabbaccacb", "cbdbadac", "cddbdcbbabadaacc", "dcadcbba", "dddcacbdcbabbaca", "adbbaccd", "adddbcbbabaccacd", "aacbcbdd", "addaccbbcbabdacd", "ddcabacb", "ddddccbabbaacacb", "bddbcaac", "bddddcbbcbaaaacc", "adacdbcb", "adddacbcdbabcacb", "adbcadbc", "adddbcbcabadbacc", "cbdcbada", "cddbdcbcbbaadaca", "bdacabdc", "bdddacbcababdacc", "dabcacdb", "dddabcbcabacdacb", "cabbdcad", "cddabcbbdbacaacd", "daaccdbb", "dddaacbccbadbacb", "dbacdcba", "dddbacbcdbacbaca", "bbccaadd", "bddbccbcabaadacd", "bbaaccdd", "bddbacbacbacdacd", "abcdbdac", "addbccbdbbadaacc", "accdbbad", "addcccbdbbabaacd", "cdbbaadc", "cdddbcbbabaadacc", "dcdcabab", "dddcdcbcababaacb", "bacdcabd", "bddaccbdcbaabacd", "ccddaabb", "cddcdcbdabaabacb", "adbcacbd", "adddbcbcabacbacd", "dbbacacd", "dddbbcbacbaacacd", "adbccbda", "adddbcbccbabdaca", "baddcbca", "bddadcbdcbabcaca", "cadcbbad", "cddadcbcbbabaacd", "cadacdbb", "cddadcbacbadbacb", "dbadcbac", "dddbacbdcbabaacc", "abdcadcb", "addbdcbcabadcacb", "cdcbbdaa", "cdddccbbbbadaaca", "cdcaabbd", "cdddccbaababbacd", "babacdcd", "bddabcbacbadcacd", "cbbadacd", "cddbbcbadbaacacd", "adbbcacd", "adddbcbbcbaacacd", "dacdbabc", "dddaccbdbbaabacc", "badcacbd", "bddadcbcabacbacd", "cbacdabd", "cddbacbcdbaabacd", "bdbaadcc", "bdddbcbaabadcacc", "cbabcdad", "cddbacbbcbadaacd", "ddbaabcc", "ddddbcbaababcacc", "abcacbdd", "addbccbacbabdacd", "bdcdacba", "bdddccbdabacbaca", "abbadcdc", "addbbcbadbacdacc", "ccddbbaa", "cddcdcbdbbabaaca", "dcdbaabc", "dddcdcbbabaabacc", "ddccaabb", "ddddccbcabaabacb", "caabdcbd", "cddaacbbdbacbacd", "cdbcaadb", "cdddbcbcabaadacb", "addbbcac", "addddcbbbbacaacc", "ddbccaab", "ddddbcbccbaaaacb", "acdbbacd", "addcdcbbbbaacacd", "bcacdbda", "bddcacbcdbabdaca", "aacbdbcd", "addaccbbdbabcacd", "ccbabadd", "cddcbcbabbaadacd", "abcbadcd", "addbccbbabadcacd", "bbcdaacd", "bddbccbdabaacacd", "abddabcc", "addbdcbdababcacc", "daacbdbc", "dddaacbcbbadbacc", "cabbacdd", "cddabcbbabacdacd", "adbbcdac", "adddbcbbcbadaacc", "cabbddac", "cddabcbbdbadaacc", "dacdbcba", "dddaccbdbbacbaca", "babcdadc", "bddabcbcdbaadacc", "cabbcdda", "cddabcbbcbaddaca", "cbbdadac", "cddbbcbdabadaacc", "ddacacbb", "ddddacbcabacbacb", "baccabdd", "bddaccbcababdacd", "bccdbaad", "bddcccbdbbaaaacd", "dbdcacab", "dddbdcbcabacaacb", "dabccbda", "dddabcbccbabdaca", "abcbdcda", "addbccbbdbacdaca", "aadbcdbc", "addadcbbcbadbacc", "cabddcab", "cddabcbddbacaacb", "cdcabbad", "cdddccbabbabaacd", "adbbccad", "adddbcbbcbacaacd", "cdaabdbc", "cdddacbabbadbacc", "dabcadcb", "dddabcbcabadcacb", "adbacdbc", "adddbcbacbadbacc", "cbacabdd", "cddbacbcababdacd", "dccbdbaa", "dddcccbbdbabaaca", "accabdbd", "addcccbabbadbacd", "bbcdadac", "bddbccbdabadaacc", "acbcdbad", "addcbcbcdbabaacd", "cabcddba", "cddabcbcdbadbaca", "cabdcabd", "cddabcbdcbaabacd", "dabcbcda", "dddabcbcbbacdaca", "baadccdb", "bddaacbdcbacdacb", "dacbcdab", "dddaccbbcbadaacb", "bcbcadda", "bddcbcbcabaddaca", "bdadccab", "bdddacbdcbacaacb", "caaddbcb", "cddaacbddbabcacb", "cbbdacad", "cddbbcbdabacaacd", "cdcbbada", "cdddccbbbbaadaca", "ccbbdaad", "cddcbcbbdbaaaacd", "daabbdcc", "dddaacbbbbadcacc", "ccdabbad", "cddcdcbabbabaacd", "dbacadbc", "dddbacbcabadbacc", "dcabadbc", "dddcacbbabadbacc", "cadcdbab", "cddadcbcdbabaacb", "bdcdcbaa", "bdddccbdcbabaaca", "acbdbacd", "addcbcbdbbaacacd", "bdaaccbd", "bdddacbacbacbacd", "adbdcabc", "adddbcbdcbaabacc", "cdaabcbd", "cdddacbabbacbacd", "cdbdaacb", "cdddbcbdabaacacb", "abacdcdb", "addbacbcdbacdacb", "bcbacdda", "bddcbcbacbaddaca", "bdcacdab", "bdddccbacbadaacb", "addccabb", "addddcbccbaabacb", "aadcbcbd", "addadcbcbbacbacd", "abcabcdd", "addbccbabbacdacd", "abcddcba", "addbccbddbacbaca", "cbbadcad", "cddbbcbadbacaacd", "adcabbcd", "adddccbabbabcacd", "abbdacdc", "addbbcbdabacdacc", "adacbdcb", "adddacbcbbadcacb", "babdccda", "bddabcbdcbacdaca", "badbcdac", "bddadcbbcbadaacc", "ddcbacba", "ddddccbbabacbaca", "cdabacbd", "cdddacbbabacbacd", "dbaccbda", "dddbacbccbabdaca", "cbdabadc", "cddbdcbabbaadacc", "dcbaacbd", "dddcbcbaabacbacd", "dcbdaacb", "dddcbcbdabaacacb", "bacddacb", "bddaccbddbaacacb", "dcdcbbaa", "dddcdcbcbbabaaca", "accbdbad", "addcccbbdbabaacd", "babddacc", "bddabcbddbaacacc", "aabcbdcd", "addabcbcbbadcacd", "dcaabbcd", "dddcacbabbabcacd", "dbcdcbaa", "dddbccbdcbabaaca", "accbaddb", "addcccbbabaddacb", "dbcbcada", "dddbccbbcbaadaca", "dadbabcc", "dddadcbbababcacc", "ddacbbca", "ddddacbcbbabcaca", "cdbbaacd", "cdddbcbbabaacacd", "bdaaccdb", "bdddacbacbacdacb", "dbbdacca", "dddbbcbdabaccaca", "cbaabddc", "cddbacbabbaddacc", "ccbadbad", "cddcbcbadbabaacd", "aadcbbdc", "addadcbcbbabdacc", "bbaadcdc", "bddbacbadbacdacc", "daacbbdc", "dddaacbcbbabdacc", "acbdbcad", "addcbcbdbbacaacd", "bacaddcb", "bddaccbadbadcacb", "abbdcdca", "addbbcbdcbadcaca", "abcbaddc", "addbccbbabaddacc", "babccadd", "bddabcbccbaadacd", "bccabadd", "bddcccbabbaadacd", "ccbdaabd", "cddcbcbdabaabacd", "dccaadbb", "dddcccbaabadbacb", "dabcdbac", "dddabcbcdbabaacc", "adcdbabc", "adddccbdbbaabacc", "ddcbbcaa", "ddddccbbbbacaaca", "cdbbadac", "cdddbcbbabadaacc", "cdabcabd", "cdddacbbcbaabacd", "abadbccd", "addbacbdbbaccacd", "abddcbca", "addbdcbdcbabcaca", "bcbddaac", "bddcbcbddbaaaacc", "cbbaacdd", "cddbbcbaabacdacd", "ddbaacbc", "ddddbcbaabacbacc", "ddcacbba", "ddddccbacbabbaca", "acbabddc", "addcbcbabbaddacc", "cabadbcd", "cddabcbadbabcacd", "abcdadbc", "addbccbdabadbacc", "aabccbdd", "addabcbccbabdacd", "cbaddbac", "cddbacbddbabaacc", "badabcdc", "bddadcbabbacdacc", "bacabcdd", "bddaccbabbacdacd", "cdaacbbd", "cdddacbacbabbacd", "caddbbac", "cddadcbdbbabaacc", "dbccaabd", "dddbccbcabaabacd", "aadcdbbc", "addadcbcdbabbacc", "ddcbcaba", "ddddccbbcbaabaca", "acacbbdd", "addcacbcbbabdacd", "dadcabcb", "dddadcbcababcacb", "bbcdacda", "bddbccbdabacdaca", "bcbaddac", "bddcbcbadbadaacc", "cdbbacad", "cdddbcbbabacaacd", "badcdabc", "bddadcbcdbaabacc", "dbacdacb", "dddbacbcdbaacacb", "bcdaacbd", "bddcdcbaabacbacd", "aacdcdbb", "addaccbdcbadbacb", "bdbaccda", "bdddbcbacbacdaca", "caadbdbc", "cddaacbdbbadbacc", "dabcbdca", "dddabcbcbbadcaca", "abcdbacd", "addbccbdbbaacacd", "dcbdbcaa", "dddcbcbdbbacaaca", "ddcbbaca", "ddddccbbbbaacaca", "acbcbdad", "addcbcbcbbadaacd", "cacdbbda", "cddaccbdbbabdaca", "bcadbacd", "bddcacbdbbaacacd", "caadbdcb", "cddaacbdbbadcacb", "baccddba", "bddaccbcdbadbaca", "dbaadccb", "dddbacbadbaccacb", "cbabdadc", "cddbacbbdbaadacc", "daabdbcc", "dddaacbbdbabcacc", "dbcacdba", "dddbccbacbadbaca", "ddcbabac", "ddddccbbababaacc", "aacbcdbd", "addaccbbcbadbacd", "badacbcd", "bddadcbacbabcacd", "cadbadcb", "cddadcbbabadcacb", "cbadbdca", "cddbacbdbbadcaca", "cadbdacb", "cddadcbbdbaacacb", "cdcdabab", "cdddccbdababaacb", "aaccdbbd", "addaccbcdbabbacd", "cdaacbdb", "cdddacbacbabdacb", "dbccaadb", "dddbccbcabaadacb", "abbcdadc", "addbbcbcdbaadacc", "dacadbcb", "dddaccbadbabcacb", "ccdbabda", "cddcdcbbababdaca", "babdcdca", "bddabcbdcbadcaca", "abdcabdc", "addbdcbcababdacc", "cdbdbaac", "cdddbcbdbbaaaacc", "cbdaacbd", "cddbdcbaabacbacd", "cabddabc", "cddabcbddbaabacc", "bdcbcdaa", "bdddccbbcbadaaca", "ccbdabda", "cddcbcbdababdaca", "bcbdaadc", "bddcbcbdabaadacc", "bcddcbaa", "bddcdcbdcbabaaca", "acdbdcab", "addcdcbbdbacaacb", "acadcbbd", "addcacbdcbabbacd", "bbdacacd", "bddbdcbacbaacacd", "cdabbdac", "cdddacbbbbadaacc", "cacddabb", "cddaccbddbaabacb", "ddabbcac", "ddddacbbbbacaacc", "dbacdcab", "dddbacbcdbacaacb", "cdbcabda", "cdddbcbcababdaca", "dbbcacda", "dddbbcbcabacdaca", "dcabdcba", "dddcacbbdbacbaca", "abddbcac", "addbdcbdbbacaacc", "aacbcddb", "addaccbbcbaddacb", "dacdbbac", "dddaccbdbbabaacc", "dccababd", "dddcccbabbaabacd", "cbacdbad", "cddbacbcdbabaacd", "dacbadbc", "dddaccbbabadbacc", "bcadbcad", "bddcacbdbbacaacd", "adccbdba", "adddccbcbbadbaca", "bccabdda", "bddcccbabbaddaca", "baddbcca", "bddadcbdbbaccaca", "bbadcdca", "bddbacbdcbadcaca", "cbcbdaad", "cddbccbbdbaaaacd", "cdabbcad", "cdddacbbbbacaacd", "dabdbacc", "dddabcbdbbaacacc", "acdcbdab", "addcdcbcbbadaacb", "acadbcdb", "addcacbdbbacdacb", "bccaadbd", "bddcccbaabadbacd", "daabdcbc", "dddaacbbdbacbacc", "aabbccdd", "addabcbbcbacdacd", "dcaabcbd", "dddcacbabbacbacd", "dccabdba", "dddcccbabbadbaca", "badaccbd", "bddadcbacbacbacd", "cbaabdcd", "cddbacbabbadcacd", "dacbacbd", "dddaccbbabacbacd", "bdabcdca", "bdddacbbcbadcaca", "dbadacbc", "dddbacbdabacbacc", "ddababcc", "ddddacbbababcacc", "aadcbbcd", "addadcbcbbabcacd", "addcabbc", "addddcbcababbacc", "dacadcbb", "dddaccbadbacbacb", "ddbcbaca", "ddddbcbcbbaacaca", "dacbcbda", "dddaccbbcbabdaca", "bcdcbada", "bddcdcbcbbaadaca", "adcacbdb", "adddccbacbabdacb", "bdccabad", "bdddccbcababaacd", "bdcdacab", "bdddccbdabacaacb", "bcdacbda", "bddcdcbacbabdaca", "baabcddc", "bddaacbbcbaddacc", "dcbcaadb", "dddcbcbcabaadacb", "ddbcbaac", "ddddbcbcbbaaaacc", "bbacdacd", "bddbacbcdbaacacd", "bbcadcda", "bddbccbadbacdaca", "bddcacab", "bddddcbcabacaacb", "dcdabcba", "dddcdcbabbacbaca", "ccbdbaad", "cddcbcbdbbaaaacd", "daadbbcc", "dddaacbdbbabcacc", "cdbadcba", "cdddbcbadbacbaca", "badadcbc", "bddadcbadbacbacc", "acdbacdb", "addcdcbbabacdacb", "cdbcbaad", "cdddbcbcbbaaaacd", "dbcadacb", "dddbccbadbaacacb", "acbabdcd", "addcbcbabbadcacd", "addbaccb", "addddcbbabaccacb", "bdacbcad", "bdddacbcbbacaacd", "adabdccb", "adddacbbdbaccacb", "cdacbabd", "cdddacbcbbaabacd", "bdcbacda", "bdddccbbabacdaca", "acdbcadb", "addcdcbbcbaadacb", "adcdabbc", "adddccbdababbacc", "dbcdacba", "dddbccbdabacbaca", "ccadbdba", "cddcacbdbbadbaca", "cdadbbac", "cdddacbdbbabaacc", "dabacdcb", "dddabcbacbadcacb", "adbdcbac", "adddbcbdcbabaacc", "cbcbaadd", "cddbccbbabaadacd", "bacbcdad", "bddaccbbcbadaacd", "aacbddcb", "addaccbbdbadcacb", "bbcdcada", "bddbccbdcbaadaca", "dcadacbb", "dddcacbdabacbacb", "aabcdbdc", "addabcbcdbabdacc", "bcbcdada", "bddcbcbcdbaadaca", "acdcbadb", "addcdcbcbbaadacb", "badcdbac", "bddadcbcdbabaacc", "bbccadda", "bddbccbcabaddaca", "cbcaadbd", "cddbccbaabadbacd", "cbdbcada", "cddbdcbbcbaadaca", "acddacbb", "addcdcbdabacbacb", "dbdccbaa", "dddbdcbccbabaaca", "bdcabdca", "bdddccbabbadcaca", "babcdcda", "bddabcbcdbacdaca", "abdabcdc", "addbdcbabbacdacc", "dbabcacd", "dddbacbbcbaacacd", "bdcaacdb", "bdddccbaabacdacb", "acbbdacd", "addcbcbbdbaacacd", "cabcddab", "cddabcbcdbadaacb", "bcdabcad", "bddcdcbabbacaacd", "addcbacb", "addddcbcbbaacacb", "abacbcdd", "addbacbcbbacdacd", "badacdbc", "bddadcbacbadbacc", "dadacbbc", "dddadcbacbabbacc", "aacdbdbc", "addaccbdbbadbacc", "cdbbdaac", "cdddbcbbdbaaaacc", "bdcacbad", "bdddccbacbabaacd", "aabbcdcd", "addabcbbcbadcacd", "cadbcbad", "cddadcbbcbabaacd", "bacdbcda", "bddaccbdbbacdaca", "abcddcab", "addbccbddbacaacb", "daacdbcb", "dddaacbcdbabcacb", "abdcabcd", "addbdcbcababcacd", "ddcbacab", "ddddccbbabacaacb", "dbdacbca", "dddbdcbacbabcaca", "caddacbb", "cddadcbdabacbacb", "adccadbb", "adddccbcabadbacb", "bbdcacad", "bddbdcbcabacaacd", "dbadabcc", "dddbacbdababcacc", "adbcbadc", "adddbcbcbbaadacc", "baddaccb", "bddadcbdabaccacb", "bbacdcad", "bddbacbcdbacaacd", "cdcdbaab", "cdddccbdbbaaaacb", "cdbdacba", "cdddbcbdabacbaca", "acabdbcd", "addcacbbdbabcacd", "bcbdaacd", "bddcbcbdabaacacd", "cdaabbdc", "cdddacbabbabdacc", "bdbccdaa", "bdddbcbccbadaaca", "dabdccba", "dddabcbdcbacbaca", "dcabcdba", "dddcacbbcbadbaca", "caadcbbd", "cddaacbdcbabbacd", "dcabcbda", "dddcacbbcbabdaca", "ddccbaba", "ddddccbcbbaabaca", "acadbdcb", "addcacbdbbadcacb", "cbadabcd", "cddbacbdababcacd", "baabdccd", "bddaacbbdbaccacd", "dcadcabb", "dddcacbdcbaabacb", "acbcadbd", "addcbcbcabadbacd", "bcacbadd", "bddcacbcbbaadacd", "abdcdcba", "addbdcbcdbacbaca", "adaccdbb", "adddacbccbadbacb", "cbcadadb", "cddbccbadbaadacb", "dbacabdc", "dddbacbcababdacc", "ccbabdda", "cddcbcbabbaddaca", "dadbccba", "dddadcbbcbacbaca", "acddcbab", "addcdcbdcbabaacb", "bdcdcaba", "bdddccbdcbaabaca", "dbacdbca", "dddbacbcdbabcaca", "bacadbcd", "bddaccbadbabcacd", "adcabcbd", "adddccbabbacbacd", "adcdbacb", "adddccbdbbaacacb", "bcbdadac", "bddcbcbdabadaacc", "badcbcad", "bddadcbcbbacaacd", "daadccbb", "dddaacbdcbacbacb", "cbdaabcd", "cddbdcbaababcacd", "dcdaacbb", "dddcdcbaabacbacb", "aabccdbd", "addabcbccbadbacd", "abbccdda", "addbbcbccbaddaca", "ddcbcbaa", "ddddccbbcbabaaca", "dabccdab", "dddabcbccbadaacb", "acbbdcad", "addcbcbbdbacaacd", "dccbbaad", "dddcccbbbbaaaacd", "dbcbadca", "dddbccbbabadcaca", "dcadbacb", "dddcacbdbbaacacb", "baddcacb", "bddadcbdcbaacacb", "dbdaabcc", "dddbdcbaababcacc", "cabdcdba", "cddabcbdcbadbaca", "ddabacbc", "ddddacbbabacbacc", "baabcdcd", "bddaacbbcbadcacd", "cdacbbda", "cdddacbcbbabdaca", "bdaccdba", "bdddacbccbadbaca", "acabdcbd", "addcacbbdbacbacd", "ddcacbab", "ddddccbacbabaacb", "bcabdcad", "bddcacbbdbacaacd", "bbdcadac", "bddbdcbcabadaacc", "cddcbaba", "cddddcbcbbaabaca", "aacdbbdc", "addaccbdbbabdacc", "acdcadbb", "addcdcbcabadbacb", "aadbdbcc", "addadcbbdbabcacc", "aaddbcbc", "addadcbdbbacbacc", "aacdcbbd", "addaccbdcbabbacd", "cdcbadab", "cdddccbbabadaacb", "bdcaadcb", "bdddccbaabadcacb", "dccaabdb", "dddcccbaababdacb", "cdadcbba", "cdddacbdcbabbaca", "dccdbaba", "dddcccbdbbaabaca", "aacbbdcd", "addaccbbbbadcacd", "abdcadbc", "addbdcbcabadbacc", "adccabdb", "adddccbcababdacb", "bbcaaddc", "bddbccbaabaddacc", "bbdadcac", "bddbdcbadbacaacc", "ccadabbd", "cddcacbdababbacd", "aabcdbcd", "addabcbcdbabcacd", "cbcdbaad", "cddbccbdbbaaaacd", "bacbdacd", "bddaccbbdbaacacd", "bcdcdbaa", "bddcdcbcdbabaaca", "adbccabd", "adddbcbccbaabacd", "abbdcadc", "addbbcbdcbaadacc", "babdacdc", "bddabcbdabacdacc", "baddccab", "bddadcbdcbacaacb", "cabbdacd", "cddabcbbdbaacacd", "dadccabb", "dddadcbccbaabacb", "cabddbca", "cddabcbddbabcaca", "abcdcadb", "addbccbdcbaadacb", "cbabdcda", "cddbacbbdbacdaca", "badbaccd", "bddadcbbabaccacd", "abdcbacd", "addbdcbcbbaacacd", "cbdcdbaa", "cddbdcbcdbabaaca", "dbbadcca", "dddbbcbadbaccaca", "cabaddcb", "cddabcbadbadcacb", "dcbacbda", "dddcbcbacbabdaca", "cbbcdada", "cddbbcbcdbaadaca", "bcbaaddc", "bddcbcbaabaddacc", "dccbdaab", "dddcccbbdbaaaacb", "acbacddb", "addcbcbacbaddacb", "bcacadbd", "bddcacbcabadbacd", "bbaccdad", "bddbacbccbadaacd", "bdadabcc", "bdddacbdababcacc", "dcbcabda", "dddcbcbcababdaca", "dbcbaadc", "dddbccbbabaadacc", "aacdbcdb", "addaccbdbbacdacb", "cabcbadd", "cddabcbcbbaadacd", "bcadcdba", "bddcacbdcbadbaca", "baccdbda", "bddaccbcdbabdaca", "caacbdbd", "cddaacbcbbadbacd", "adcbcdba", "adddccbbcbadbaca", "cbacbdda", "cddbacbcbbaddaca", "dacbbcda", "dddaccbbbbacdaca", "dcabdcab", "dddcacbbdbacaacb", "bdcadbac", "bdddccbadbabaacc", "daabdccb", "dddaacbbdbaccacb", "dcabbcad", "dddcacbbbbacaacd", "cdbacdba", "cdddbcbacbadbaca", "badccdba", "bddadcbccbadbaca", "cababcdd", "cddabcbabbacdacd", "cddbaacb", "cddddcbbabaacacb", "bbdaccad", "bddbdcbacbacaacd", "dabcbadc", "dddabcbcbbaadacc", "bdabcdac", "bdddacbbcbadaacc", "acbdadbc", "addcbcbdabadbacc", "cdcbaadb", "cdddccbbabaadacb", "caaddbbc", "cddaacbddbabbacc", "bddcabac", "bddddcbcababaacc", "bbdcdaac", "bddbdcbcdbaaaacc", "ddcababc", "ddddccbabbaabacc", "bbaddcac", "bddbacbddbacaacc", "bdbdacac", "bdddbcbdabacaacc", "caddabcb", "cddadcbdababcacb", "badbccda", "bddadcbbcbacdaca", "bcbcaadd", "bddcbcbcabaadacd", "cbcddbaa", "cddbccbddbabaaca", "dbcabcda", "dddbccbabbacdaca", "ddcbaabc", "ddddccbbabaabacc", "cbdcabda", "cddbdcbcababdaca", "dacbabdc", "dddaccbbababdacc", "bdbdcaac", "bdddbcbdcbaaaacc", "dcbcbdaa", "dddcbcbcbbadaaca", "dcbcdaab", "dddcbcbcdbaaaacb", "cdcdaabb", "cdddccbdabaabacb", "dbbaadcc", "dddbbcbaabadcacc", "aadbbdcc", "addadcbbbbadcacc", "abcadbcd", "addbccbadbabcacd", "abdcbcad", "addbdcbcbbacaacd", "cdcdbaba", "cdddccbdbbaabaca", "aacddbcb", "addaccbddbabcacb", "ddbbaacc", "ddddbcbbabaacacc", "dbcbacda", "dddbccbbabacdaca", "bdadcabc", "bdddacbdcbaabacc", "dacbdbca", "dddaccbbdbabcaca", "cdabdbac", "cdddacbbdbabaacc", "dbaacdbc", "dddbacbacbadbacc", "dcbadbac", "dddcbcbadbabaacc", "ddabcabc", "ddddacbbcbaabacc", "acdbbcad", "addcdcbbbbacaacd", "adadccbb", "adddacbdcbacbacb", "dcacbbda", "dddcacbcbbabdaca", "bdacabcd", "bdddacbcababcacd", "cacdbabd", "cddaccbdbbaabacd", "cbddbcaa", "cddbdcbdbbacaaca", "dbcdacab", "dddbccbdabacaacb", "dacbbacd", "dddaccbbbbaacacd", "adacdcbb", "adddacbcdbacbacb", "aadbbccd", "addadcbbbbaccacd", "bdaabccd", "bdddacbabbaccacd", "cacaddbb", "cddaccbadbadbacb", "dadbcbac", "dddadcbbcbabaacc", "bdcabdac", "bdddccbabbadaacc", "dadaccbb", "dddadcbacbacbacb", "dbccbada", "dddbccbcbbaadaca", "bcdcabad", "bddcdcbcababaacd", "bacaddbc", "bddaccbadbadbacc", "cbaaddbc", "cddbacbadbadbacc", "abbddcca", "addbbcbddbaccaca", "ccdbaabd", "cddcdcbbabaabacd", "bcdbadac", "bddcdcbbabadaacc", "abcdcdba", "addbccbdcbadbaca", "bbcaadcd", "bddbccbaabadcacd", "bcadcbda", "bddcacbdcbabdaca", "adcbcbda", "adddccbbcbabdaca", "bcdbdaac", "bddcdcbbdbaaaacc", "adbabcdc", "adddbcbabbacdacc", "bddabcac", "bddddcbabbacaacc", "caacdbbd", "cddaacbcdbabbacd", "adadbcbc", "adddacbdbbacbacc", "dacbbdac", "dddaccbbbbadaacc", "dbdcbaac", "dddbdcbcbbaaaacc", "abbdcacd", "addbbcbdcbaacacd", "cdabbdca", "cdddacbbbbadcaca", "dbbcdaca", "dddbbcbcdbaacaca", "adbcadcb", "adddbcbcabadcacb", "dcbabdca", "dddcbcbabbadcaca", "adadbccb", "adddacbdbbaccacb", "dcacdbab", "dddcacbcdbabaacb", "babaccdd", "bddabcbacbacdacd", "caabcdbd", "cddaacbbcbadbacd", "daccdbba", "dddaccbcdbabbaca", "cdbdacab", "cdddbcbdabacaacb", "dbcdcaab", "dddbccbdcbaaaacb", "bccbadad", "bddcccbbabadaacd", "bdacacbd", "bdddacbcabacbacd", "cbdbdaac", "cddbdcbbdbaaaacc", "cdabcbad", "cdddacbbcbabaacd", "dabdccab", "dddabcbdcbacaacb", "badcacdb", "bddadcbcabacdacb", "dcabcdab", "dddcacbbcbadaacb", "dcbacbad", "dddcbcbacbabaacd", "dbcbaacd", "dddbccbbabaacacd", "dabcadbc", "dddabcbcabadbacc", "cadcdbba", "cddadcbcdbabbaca", "babddcca", "bddabcbddbaccaca", "bcadadbc", "bddcacbdabadbacc", "ddbacacb", "ddddbcbacbaacacb", "abaddcbc", "addbacbddbacbacc", "abdcdcab", "addbdcbcdbacaacb", "bdbcacda", "bdddbcbcabacdaca", "cacbaddb", "cddaccbbabaddacb", "addbabcc", "addddcbbababcacc", "bbacacdd", "bddbacbcabacdacd", "cacadbdb", "cddaccbadbabdacb", "bdaccabd", "bdddacbccbaabacd", "dacdcabb", "dddaccbdcbaabacb", "cdbaadcb", "cdddbcbaabadcacb", "dabcdacb", "dddabcbcdbaacacb", "dcbdacab", "dddcbcbdabacaacb", "abcbacdd", "addbccbbabacdacd", "dcaacbbd", "dddcacbacbabbacd", "cbabaddc", "cddbacbbabaddacc", "ddbcbcaa", "ddddbcbcbbacaaca", "babddcac", "bddabcbddbacaacc", "abcbcdda", "addbccbbcbaddaca", "abacddbc", "addbacbcdbadbacc", "dbdbccaa", "dddbdcbbcbacaaca", "dbcaacdb", "dddbccbaabacdacb", "badbcdca", "bddadcbbcbadcaca", "bcdbaadc", "bddcdcbbabaadacc", "baadccbd", "bddaacbdcbacbacd", "dcbcadab", "dddcbcbcabadaacb", "caddbacb", "cddadcbdbbaacacb", "dbcbadac", "dddbccbbabadaacc", "bcaabddc", "bddcacbabbaddacc", "cabcbdad", "cddabcbcbbadaacd", "dabccbad", "dddabcbccbabaacd", "dbcacabd", "dddbccbacbaabacd", "abcdacbd", "addbccbdabacbacd", "abadcdbc", "addbacbdcbadbacc", "cdbbcdaa", "cdddbcbbcbadaaca", "cadbbcad", "cddadcbbbbacaacd", "adcdbcba", "adddccbdbbacbaca", "dbaacbcd", "dddbacbacbabcacd", "dcbdcaba", "dddcbcbdcbaabaca", "cdcabdab", "cdddccbabbadaacb", "cadabdcb", "cddadcbabbadcacb", "dcacabdb", "dddcacbcababdacb", "cbcabdad", "cddbccbabbadaacd", "abdccdab", "addbdcbccbadaacb", "cbdadbac", "cddbdcbadbabaacc", "daabbcdc", "dddaacbbbbacdacc", "bdabaccd", "bdddacbbabaccacd", "acddbcab", "addcdcbdbbacaacb", "abcdcbda", "addbccbdcbabdaca", "aaddbccb", "addadcbdbbaccacb", "baacdbdc", "bddaacbcdbabdacc", "bcaabcdd", "bddcacbabbacdacd", "dbbcaadc", "dddbbcbcabaadacc", "ddcaabbc", "ddddccbaababbacc", "cdabbadc", "cdddacbbbbaadacc", "acdbcdab", "addcdcbbcbadaacb", "cbcdaadb", "cddbccbdabaadacb", "cddcbaab", "cddddcbcbbaaaacb", "cbbddaac", "cddbbcbddbaaaacc", "caadbcbd", "cddaacbdbbacbacd", "cacbdabd", "cddaccbbdbaabacd", "ddccabba", "ddddccbcababbaca", "bdacadbc", "bdddacbcabadbacc", "cbcbadad", "cddbccbbabadaacd", "daccabdb", "dddaccbcababdacb", "cbdbacad", "cddbdcbbabacaacd", "aaccbddb", "addaccbcbbaddacb", "dcadbcab", "dddcacbdbbacaacb", "baccbdda", "bddaccbcbbaddaca", "bdcaabcd", "bdddccbaababcacd", "bdbaacdc", "bdddbcbaabacdacc", "abadbdcc", "addbacbdbbadcacc", "cbbdcada", "cddbbcbdcbaadaca", "acdbdabc", "addcdcbbdbaabacc", "dababcdc", "dddabcbabbacdacc", "dacabdbc", "dddaccbabbadbacc", "badcadcb", "bddadcbcabadcacb", "bdaccbda", "bdddacbccbabdaca", "bcddacab", "bddcdcbdabacaacb", "bccbdaad", "bddcccbbdbaaaacd", "adcbdcab", "adddccbbdbacaacb", "cdadabbc", "cdddacbdababbacc", "aabdbccd", "addabcbdbbaccacd", "ddacbcba", "ddddacbcbbacbaca", "bdbcadca", "bdddbcbcabadcaca", "adbcbcda", "adddbcbcbbacdaca", "abcdbcad", "addbccbdbbacaacd", "daacbbcd", "dddaacbcbbabcacd", "caabddcb", "cddaacbbdbadcacb", "bacddcab", "bddaccbddbacaacb", "bacacbdd", "bddaccbacbabdacd", "cbaacbdd", "cddbacbacbabdacd", "dccbabad", "dddcccbbababaacd", "cdcbabda", "cdddccbbababdaca", "bdabcacd", "bdddacbbcbaacacd", "dadabcbc", "dddadcbabbacbacc", "dbdbaacc", "dddbdcbbabaacacc", "dacbcabd", "dddaccbbcbaabacd", "bdbadcac", "bdddbcbadbacaacc", "cdbdcaba", "cdddbcbdcbaabaca", "dacabcbd", "dddaccbabbacbacd", "dcadabcb", "dddcacbdababcacb", "ccabdbda", "cddcacbbdbabdaca", "bacadcdb", "bddaccbadbacdacb", "badbcadc", "bddadcbbcbaadacc", "dcdbacab", "dddcdcbbabacaacb", "dbacbcda", "dddbacbcbbacdaca", "caddbcab", "cddadcbdbbacaacb", "dabdaccb", "dddabcbdabaccacb", "ddcabbca", "ddddccbabbabcaca", "aadbcbcd", "addadcbbcbabcacd", "aabdcdbc", "addabcbdcbadbacc", "abbdadcc", "addbbcbdabadcacc", "dbcdaabc", "dddbccbdabaabacc", "adcbcdab", "adddccbbcbadaacb", "cbbdaadc", "cddbbcbdabaadacc", "bdbacdca", "bdddbcbacbadcaca", "daaccbdb", "dddaacbccbabdacb", "dcaabcdb", "dddcacbabbacdacb", "abddccba", "addbdcbdcbacbaca", "ddcbabca", "ddddccbbababcaca", "dabadccb", "dddabcbadbaccacb", "bdcdaabc", "bdddccbdabaabacc", "cdbacdab", "cdddbcbacbadaacb", "cdababcd", "cdddacbbababcacd", "abcddbac", "addbccbddbabaacc", "dccdabba", "dddcccbdababbaca", "bccdaadb", "bddcccbdabaadacb", "ddacabbc", "ddddacbcababbacc", "dbadbacc", "dddbacbdbbaacacc", "bdadcbca", "bdddacbdcbabcaca", "cdacadbb", "cdddacbcabadbacb", "cbabadcd", "cddbacbbabadcacd", "baabccdd", "bddaacbbcbacdacd", "ddabcbca", "ddddacbbcbabcaca", "addccbba", "addddcbccbabbaca", "cabdadcb", "cddabcbdabadcacb", "cabdbcda", "cddabcbdbbacdaca", "bdadcbac", "bdddacbdcbabaacc", "adcdacbb", "adddccbdabacbacb", "cbabdacd", "cddbacbbdbaacacd", "aadcbdcb", "addadcbcbbadcacb", "aabdbdcc", "addabcbdbbadcacc", "adbdaccb", "adddbcbdabaccacb", "bbddccaa", "bddbdcbdcbacaaca", "ddbaaccb", "ddddbcbaabaccacb", "bacdacdb", "bddaccbdabacdacb", "dcbdabca", "dddcbcbdababcaca", "acbbcdda", "addcbcbbcbaddaca", "ddcabcba", "ddddccbabbacbaca", "bcaabdcd", "bddcacbabbadcacd", "cbadcabd", "cddbacbdcbaabacd", "cdbabcda", "cdddbcbabbacdaca", "aadbccbd", "addadcbbcbacbacd", "acdcbdba", "addcdcbcbbadbaca", "cdabadcb", "cdddacbbabadcacb", "adbaccbd", "adddbcbacbacbacd", "cdadbacb", "cdddacbdbbaacacb", "badccbda", "bddadcbccbabdaca", "dcbaadcb", "dddcbcbaabadcacb", "baccaddb", "bddaccbcabaddacb", "daabbccd", "dddaacbbbbaccacd", "daadcbcb", "dddaacbdcbabcacb", "cbdcbaad", "cddbdcbcbbaaaacd", "dacacbbd", "dddaccbacbabbacd", "dcabacbd", "dddcacbbabacbacd", "dbaccdba", "dddbacbccbadbaca", "bdcdbaca", "bdddccbdbbaacaca", "aaccdbdb", "addaccbcdbabdacb", "caabcbdd", "cddaacbbcbabdacd", "dadabbcc", "dddadcbabbabcacc", "bcdadbac", "bddcdcbadbabaacc", "badbdcca", "bddadcbbdbaccaca", "ddacbbac", "ddddacbcbbabaacc", "bccddbaa", "bddcccbddbabaaca", "dcbbacda", "dddcbcbbabacdaca", "dcabcabd", "dddcacbbcbaabacd", "cadbdcab", "cddadcbbdbacaacb", "acbacbdd", "addcbcbacbabdacd", "accdbdab", "addcccbdbbadaacb", "baacdcdb", "bddaacbcdbacdacb", "cadcbadb", "cddadcbcbbaadacb", "dabcabdc", "dddabcbcababdacc", "daabcdbc", "dddaacbbcbadbacc", "daabcbdc", "dddaacbbcbabdacc", "acbdabdc", "addcbcbdababdacc", "abcdcdab", "addbccbdcbadaacb", "dacdcbba", "dddaccbdcbabbaca", "addbbacc", "addddcbbbbaacacc", "acbdcabd", "addcbcbdcbaabacd", "bbdcaacd", "bddbdcbcabaacacd", "bbddacac", "bddbdcbdabacaacc", "dcdbcaba", "dddcdcbbcbaabaca", "dcabbdca", "dddcacbbbbadcaca", "dacacdbb", "dddaccbacbadbacb", "dbbaccad", "dddbbcbacbacaacd", "ccabbdda", "cddcacbbbbaddaca", "dacacbdb", "dddaccbacbabdacb", "dbcdbaca", "dddbccbdbbaacaca", "dcadbabc", "dddcacbdbbaabacc", "bacacddb", "bddaccbacbaddacb", "dbcbcdaa", "dddbccbbcbadaaca", "bddbaacc", "bddddcbbabaacacc", "dcbcaabd", "dddcbcbcabaabacd", "bbcaddac", "bddbccbadbadaacc", "cabdacbd", "cddabcbdabacbacd", "bcacbdad", "bddcacbcbbadaacd", "cadbcdab", "cddadcbbcbadaacb", "daacbcbd", "dddaacbcbbacbacd", "abccabdd", "addbccbcababdacd", "daccdbab", "dddaccbcdbabaacb", "dcaabdcb", "dddcacbabbadcacb", "dabdbcac", "dddabcbdbbacaacc", "dacbadcb", "dddaccbbabadcacb", "badacbdc", "bddadcbacbabdacc", "adabcdbc", "adddacbbcbadbacc", "bacadbdc", "bddaccbadbabdacc", "bcabcdad", "bddcacbbcbadaacd", "abdacbdc", "addbdcbacbabdacc", "daadbcbc", "dddaacbdbbacbacc", "acbdcadb", "addcbcbdcbaadacb", "cbbdaacd", "cddbbcbdabaacacd", "cacbabdd", "cddaccbbababdacd", "acdbcabd", "addcdcbbcbaabacd", "ababddcc", "addbacbbdbadcacc", "abdbcadc", "addbdcbbcbaadacc", "bcbdacad", "bddcbcbdabacaacd", "ddcbbaac", "ddddccbbbbaaaacc", "cbcdabda", "cddbccbdababdaca", "cadbacdb", "cddadcbbabacdacb", "baddbacc", "bddadcbdbbaacacc", "dcbdcbaa", "dddcbcbdcbabaaca", "cabdbdca", "cddabcbdbbadcaca", "aabdccdb", "addabcbdcbacdacb", "acabbddc", "addcacbbbbaddacc", "dabbadcc", "dddabcbbabadcacc", "dacdabbc", "dddaccbdababbacc", "dabbccda", "dddabcbbcbacdaca", "adcbbcda", "adddccbbbbacdaca", "bccadbda", "bddcccbadbabdaca", "dabcdcba", "dddabcbcdbacbaca", "bcbadcad", "bddcbcbadbacaacd", "bcbcadad", "bddcbcbcabadaacd", "adbdbcca", "adddbcbdbbaccaca", "cabdbdac", "cddabcbdbbadaacc", "accabddb", "addcccbabbaddacb", "dcbbadca", "dddcbcbbabadcaca", "bbdccada", "bddbdcbccbaadaca", "cacbdbad", "cddaccbbdbabaacd", "dcaacdbb", "dddcacbacbadbacb", "cabaddbc", "cddabcbadbadbacc", "adcdcabb", "adddccbdcbaabacb", "baacddcb", "bddaacbcdbadcacb", "badbccad", "bddadcbbcbacaacd", "ddabccba", "ddddacbbcbacbaca", "abccbdad", "addbccbcbbadaacd", "dbabcdac", "dddbacbbcbadaacc", "dcbdcaab", "dddcbcbdcbaaaacb", "ddbcaacb", "ddddbcbcabaacacb", "dcbbadac", "dddcbcbbabadaacc", "accdadbb", "addcccbdabadbacb", "caddbcba", "cddadcbdbbacbaca", "ababccdd", "addbacbbcbacdacd", "baadcbdc", "bddaacbdcbabdacc", "dbcdbcaa", "dddbccbdbbacaaca", "bddccbaa", "bddddcbccbabaaca", "dcacbabd", "dddcacbcbbaabacd", "dcbacabd", "dddcbcbacbaabacd", "dbcbdcaa", "dddbccbbdbacaaca", "dbbdacac", "dddbbcbdabacaacc", "cadcadbb", "cddadcbcabadbacb", "aacddcbb", "addaccbddbacbacb", "dadbcbca", "dddadcbbcbabcaca", "cbdabcda", "cddbdcbabbacdaca", "acdbadbc", "addcdcbbabadbacc", "dbabccad", "dddbacbbcbacaacd", "bcbdcaad", "bddcbcbdcbaaaacd", "ddccabab", "ddddccbcababaacb", "dadcacbb", "dddadcbcabacbacb", "dacbdcba", "dddaccbbdbacbaca", "adccdbab", "adddccbcdbabaacb", "cdbcadba", "cdddbcbcabadbaca", "addcbcab", "addddcbcbbacaacb", "dadcbabc", "dddadcbcbbaabacc", "bacbcadd", "bddaccbbcbaadacd", "cbaabcdd", "cddbacbabbacdacd", "daccbabd", "dddaccbcbbaabacd", "adacbbdc", "adddacbcbbabdacc", "dbccbdaa", "dddbccbcbbadaaca", "bcadabdc", "bddcacbdababdacc", "dcdabbac", "dddcdcbabbabaacc", "bcadcabd", "bddcacbdcbaabacd", "adcbcabd", "adddccbbcbaabacd", "abdccbda", "addbdcbccbabdaca", "aaddccbb", "addadcbdcbacbacb", "badacdcb", "bddadcbacbadcacb", "bdcbdcaa", "bdddccbbdbacaaca", "cabcdadb", "cddabcbcdbaadacb", "dbdcaacb", "dddbdcbcabaacacb", "dbacabcd", "dddbacbcababcacd", "caadbbdc", "cddaacbdbbabdacc", "adabcbdc", "adddacbbcbabdacc", "dbcdabca", "dddbccbdababcaca", "dcabcbad", "dddcacbbcbabaacd", "abcbddac", "addbccbbdbadaacc", "acdbcbda", "addcdcbbcbabdaca", "dbadcacb", "dddbacbdcbaacacb", "dcdbabac", "dddcdcbbababaacc", "bccdabda", "bddcccbdababdaca", "bdcdabca", "bdddccbdababcaca", "adadcbcb", "adddacbdcbabcacb", "dbcbdaca", "dddbccbbdbaacaca", "dbdaccba", "dddbdcbacbacbaca", "ccbabdad", "cddcbcbabbadaacd", "abdbdcca", "addbdcbbdbaccaca", "dbcdabac", "dddbccbdababaacc", "babcddca", "bddabcbcdbadcaca", "caabdbcd", "cddaacbbdbabcacd", "baaddbcc", "bddaacbddbabcacc", "adacdbbc", "adddacbcdbabbacc", "adbbcdca", "adddbcbbcbadcaca", "aabdcdcb", "addabcbdcbadcacb", "dcdcabba", "dddcdcbcababbaca", "dabbcdca", "dddabcbbcbadcaca", "daabccdb", "dddaacbbcbacdacb", "bdccbada", "bdddccbcbbaadaca", "adcbbdca", "adddccbbbbadcaca", "cdbaacdb", "cdddbcbaabacdacb", "adcabcdb", "adddccbabbacdacb", "bdbccada", "bdddbcbccbaadaca", "cbdcaabd", "cddbdcbcabaabacd", "acabcdbd", "addcacbbcbadbacd", "cdbabdca", "cdddbcbabbadcaca", "acabcbdd", "addcacbbcbabdacd", "bacdbdca", "bddaccbdbbadcaca", "ccabbdad", "cddcacbbbbadaacd", "cdcaadbb", "cdddccbaabadbacb", "bddcaacb", "bddddcbcabaacacb", "cbadacdb", "cddbacbdabacdacb", "cacddbba", "cddaccbddbabbaca", "dabbcdac", "dddabcbbcbadaacc", "acacdbbd", "addcacbcdbabbacd", "bbcdadca", "bddbccbdabadcaca", "dacabbdc", "dddaccbabbabdacc", "adcbbdac", "adddccbbbbadaacc", "dccbadab", "dddcccbbabadaacb", "adbbacdc", "adddbcbbabacdacc", "adcbadbc", "adddccbbabadbacc", "bdabccad", "bdddacbbcbacaacd", "abcacddb", "addbccbacbaddacb", "cabdcbad", "cddabcbdcbabaacd", "ddaaccbb", "ddddacbacbacbacb", "aacdbbcd", "addaccbdbbabcacd", "ccbbadda", "cddcbcbbabaddaca", "badbadcc", "bddadcbbabadcacc", "acbddbac", "addcbcbddbabaacc", "dccdabab", "dddcccbdababaacb", "badbdacc", "bddadcbbdbaacacc", "bdbaccad", "bdddbcbacbacaacd", "adccbbda", "adddccbcbbabdaca", "bacdcbad", "bddaccbdcbabaacd", "cbadcbad", "cddbacbdcbabaacd", "ddabcbac", "ddddacbbcbabaacc", "ddbccaba", "ddddbcbccbaabaca", "bccaabdd", "bddcccbaababdacd", "adabccdb", "adddacbbcbacdacb", "aadccbbd", "addadcbccbabbacd", "abdcdbca", "addbdcbcdbabcaca", "adcbacbd", "adddccbbabacbacd", "addccbab", "addddcbccbabaacb", "dcbbcdaa", "dddcbcbbcbadaaca", "cabdabcd", "cddabcbdababcacd", "bdabadcc", "bdddacbbabadcacc", "dabccadb", "dddabcbccbaadacb", "cdbacbda", "cdddbcbacbabdaca", "abdcdbac", "addbdcbcdbabaacc", "cbbddcaa", "cddbbcbddbacaaca", "abcdcabd", "addbccbdcbaabacd", "aacdcbdb", "addaccbdcbabdacb", "ccdbabad", "cddcdcbbababaacd", "aabcdcbd", "addabcbcdbacbacd", "ddcabcab", "ddddccbabbacaacb", "cbabcdda", "cddbacbbcbaddaca", "dbbcadac", "dddbbcbcabadaacc", "bccadbad", "bddcccbadbabaacd", "dbaaccbd", "dddbacbacbacbacd", "cabddcba", "cddabcbddbacbaca", "ddbbcaca", "ddddbcbbcbaacaca", "acbacdbd", "addcbcbacbadbacd", "cabcadbd", "cddabcbcabadbacd", "cbcadbda", "cddbccbadbabdaca", "dbcaabdc", "dddbccbaababdacc", "cabacbdd", "cddabcbacbabdacd", "adbbcadc", "adddbcbbcbaadacc", "bcdbcada", "bddcdcbbcbaadaca", "cbbcadad", "cddbbcbcabadaacd", "cadbcabd", "cddadcbbcbaabacd", "abbccadd", "addbbcbccbaadacd", "dacbcdba", "dddaccbbcbadbaca", "bdcabcad", "bdddccbabbacaacd", "aacdbcbd", "addaccbdbbacbacd", "cabadcdb", "cddabcbadbacdacb", "bdacbadc", "bdddacbcbbaadacc", "cdacabdb", "cdddacbcababdacb", "dcadbbca", "dddcacbdbbabcaca", "cdadbcba", "cdddacbdbbacbaca", "acbdcbad", "addcbcbdcbabaacd", "dabbcadc", "dddabcbbcbaadacc", "dbbdcaca", "dddbbcbdcbaacaca", "adcbbadc", "adddccbbbbaadacc", "acddbbca", "addcdcbdbbabcaca", "adbacbdc", "adddbcbacbabdacc", "babccdad", "bddabcbccbadaacd", "adcdbbca", "adddccbdbbabcaca", "cbbacdad", "cddbbcbacbadaacd", "abddaccb", "addbdcbdabaccacb", "bccabdad", "bddcccbabbadaacd", "bdcacdba", "bdddccbacbadbaca", "adbdccab", "adddbcbdcbacaacb", "dcdcbaab", "dddcdcbcbbaaaacb", "dbbdcaac", "dddbbcbdcbaaaacc", "adcabdcb", "adddccbabbadcacb", "acddbbac", "addcdcbdbbabaacc", "dbdbacca", "dddbdcbbabaccaca", "dcababdc", "dddcacbbababdacc", "cdbbadca", "cdddbcbbabadcaca", "adcdbbac", "adddccbdbbabaacc", "acdcbbda", "addcdcbcbbabdaca", "cdbdaabc", "cdddbcbdabaabacc", "cdcbaabd", "cdddccbbabaabacd", "dacdcbab", "dddaccbdcbabaacb", "ccabadbd", "cddcacbbabadbacd", "caacbddb", "cddaacbcbbaddacb", "dabcbacd", "dddabcbcbbaacacd", "dcdbcaab", "dddcdcbbcbaaaacb", "ccabdabd", "cddcacbbdbaabacd", "dabdcabc", "dddabcbdcbaabacc", "dbcdbaac", "dddbccbdbbaaaacc", "bdccaadb", "bdddccbcabaadacb", "dbcabdca", "dddbccbabbadcaca", "cadbbdca", "cddadcbbbbadcaca", "dacbcbad", "dddaccbbcbabaacd", "abcbcadd", "addbccbbcbaadacd", "bdadacbc", "bdddacbdabacbacc", "acbcdbda", "addcbcbcdbabdaca", "aacbbddc", "addaccbbbbaddacc", "cbbdacda", "cddbbcbdabacdaca", "ddbabacc", "ddddbcbabbaacacc", "ccbbdada", "cddcbcbbdbaadaca", "acabddcb", "addcacbbdbadcacb", "ccdabbda", "cddcdcbabbabdaca", "dbabacdc", "dddbacbbabacdacc", "aabcddbc", "addabcbcdbadbacc", "dbcabdac", "dddbccbabbadaacc", "babdadcc", "bddabcbdabadcacc", "bdcbadac", "bdddccbbabadaacc", "adacbcbd", "adddacbcbbacbacd", "bdaacbcd", "bdddacbacbabcacd", "dbcacbad", "dddbccbacbabaacd", "dccabbda", "dddcccbabbabdaca", "bddbacca", "bddddcbbabaccaca", "cbbadcda", "cddbbcbadbacdaca", "dacbabcd", "dddaccbbababcacd", "dbbcdcaa", "dddbbcbcdbacaaca", "aacbbcdd", "addaccbbbbacdacd", "cddbacab", "cddddcbbabacaacb", "cbbcaadd", "cddbbcbcabaadacd", "caabbddc", "cddaacbbbbaddacc", "babaddcc", "bddabcbadbadcacc", "cbdbdcaa", "cddbdcbbdbacaaca", "badbacdc", "bddadcbbabacdacc", "cdcbdbaa", "cdddccbbdbabaaca", "dadbaccb", "dddadcbbabaccacb", "cddbbcaa", "cddddcbbbbacaaca", "dbccadba", "dddbccbcabadbaca", "aaddcbcb", "addadcbdcbabcacb", "bddbcaca", "bddddcbbcbaacaca", "adbccdab", "adddbcbccbadaacb", "cadadcbb", "cddadcbadbacbacb", "dabbdacc", "dddabcbbdbaacacc", "aadcbcdb", "addadcbcbbacdacb", "accbdbda", "addcccbbdbabdaca", "bbcdcaad", "bddbccbdcbaaaacd", "adaccbdb", "adddacbccbabdacb", "dbcbacad", "dddbccbbabacaacd", "accbbadd", "addcccbbbbaadacd", "adbabdcc", "adddbcbabbadcacc", "bbccadad", "bddbccbcabadaacd", "cbdbcaad", "cddbdcbbcbaaaacd", "cddbcaba", "cddddcbbcbaabaca", "badcbadc", "bddadcbcbbaadacc", "abcdbdca", "addbccbdbbadcaca", "dabcdcab", "dddabcbcdbacaacb", "ccbadbda", "cddcbcbadbabdaca", "cabddbac", "cddabcbddbabaacc", "dadcbbca", "dddadcbcbbabcaca", "ddcbaacb", "ddddccbbabaacacb", "dcaabbdc", "dddcacbabbabdacc", "accabbdd", "addcccbabbabdacd", "dbdacbac", "dddbdcbacbabaacc", "cacdbadb", "cddaccbdbbaadacb", "cabcdbda", "cddabcbcdbabdaca", "ccadbbda", "cddcacbdbbabdaca", "adbabccd", "adddbcbabbaccacd", "ddabccab", "ddddacbbcbacaacb", "dcbcbada", "dddcbcbcbbaadaca", "dadcbbac", "dddadcbcbbabaacc", "abcbdacd", "addbccbbdbaacacd", "bbaccadd", "bddbacbccbaadacd", "bdbcaacd", "bdddbcbcabaacacd", "cbdbaacd", "cddbdcbbabaacacd", "daccbbad", "dddaccbcbbabaacd", "dcbdacba", "dddcbcbdabacbaca", "caddcabb", "cddadcbdcbaabacb", "dabbdcca", "dddabcbbdbaccaca", "dadcabbc", "dddadcbcababbacc", "dbdaaccb", "dddbdcbaabaccacb", "bcadcbad", "bddcacbdcbabaacd", "aabddccb", "addabcbddbaccacb", "dbcabadc", "dddbccbabbaadacc", "cadbbadc", "cddadcbbbbaadacc", "cabacddb", "cddabcbacbaddacb", "cadcabbd", "cddadcbcababbacd", "dcbcadba", "dddcbcbcabadbaca", "ddaabcbc", "ddddacbabbacbacc", "addbbcca", "addddcbbbbaccaca", "cacbbdda", "cddaccbbbbaddaca", "cdbcadab", "cdddbcbcabadaacb", "dbaadcbc", "dddbacbadbacbacc", "dacdbacb", "dddaccbdbbaacacb", "ddbcacab", "ddddbcbcabacaacb", "cdbbacda", "cdddbcbbabacdaca", "bdbacacd", "bdddbcbacbaacacd", "dadbbacc", "dddadcbbbbaacacc", "abccdbda", "addbccbcdbabdaca", "cadbdabc", "cddadcbbdbaabacc", "acddbcba", "addcdcbdbbacbaca", "bdcdabac", "bdddccbdababaacc", "accdabdb", "addcccbdababdacb", "dbcbdaac", "dddbccbbdbaaaacc", "dcababcd", "dddcacbbababcacd", "babcacdd", "bddabcbcabacdacd", "acdbcdba", "addcdcbbcbadbaca", "acbcbdda", "addcbcbcbbaddaca", "babcddac", "bddabcbcdbadaacc", "dacbbadc", "dddaccbbbbaadacc", "dbdaccab", "dddbdcbacbacaacb", "dbccdaba", "dddbccbcdbaabaca", "aadbbcdc", "addadcbbbbacdacc", "bbcacadd", "bddbccbacbaadacd", "abbccdad", "addbbcbccbadaacd", "baccdadb", "bddaccbcdbaadacb", "bcdbaacd", "bddcdcbbabaacacd", "cadcabdb", "cddadcbcababdacb", "acdbabdc", "addcdcbbababdacc", "abcdbadc", "addbccbdbbaadacc", "dabdcbac", "dddabcbdcbabaacc", "cddcabab", "cddddcbcababaacb", "acbdacbd", "addcbcbdabacbacd", "bdaacdbc", "bdddacbacbadbacc", "abdbccda", "addbdcbbcbacdaca", "cdacbbad", "cdddacbcbbabaacd", "bacdbdac", "bddaccbdbbadaacc", "dcbbcaad", "dddcbcbbcbaaaacd", "cdaacdbb", "cdddacbacbadbacb", "bdcadcba", "bdddccbadbacbaca", "bdaacdcb", "bdddacbacbadcacb", "bdacdbac", "bdddacbcdbabaacc", "ddbccbaa", "ddddbcbccbabaaca", "bcacabdd", "bddcacbcababdacd", "badccabd", "bddadcbccbaabacd", "cacddbab", "cddaccbddbabaacb", "dbbcaacd", "dddbbcbcabaacacd", "aaccbdbd", "addaccbcbbadbacd", "dcacbdba", "dddcacbcbbadbaca", "abcdcbad", "addbccbdcbabaacd", "dbaccabd", "dddbacbccbaabacd", "bddcacba", "bddddcbcabacbaca", "adbdcacb", "adddbcbdcbaacacb", "abbddcac", "addbbcbddbacaacc", "dbbaaccd", "dddbbcbaabaccacd", "dbadbcca", "dddbacbdbbaccaca", "dadbbcca", "dddadcbbbbaccaca", "abbcdcda", "addbbcbcdbacdaca", "adbcbdca", "adddbcbcbbadcaca", "cbcbdada", "cddbccbbdbaadaca", "cdabbcda", "cdddacbbbbacdaca", "adbcacdb", "adddbcbcabacdacb", "dcbabcda", "dddcbcbabbacdaca", "bdbaaccd", "bdddbcbaabaccacd", "cabbcadd", "cddabcbbcbaadacd", "babcaddc", "bddabcbcabaddacc", "dadbbcac", "dddadcbbbbacaacc", "dbcaadbc", "dddbccbaabadbacc", "cbbaaddc", "cddbbcbaabaddacc", "ddaccabb", "ddddacbccbaabacb", "badccadb", "bddadcbccbaadacb", "abbdccda", "addbbcbdcbacdaca", "acbdbdac", "addcbcbdbbadaacc", "cdcaabdb", "cdddccbaababdacb", "dbcaadcb", "dddbccbaabadcacb", "dbcadabc", "dddbccbadbaabacc", "ccdbbada", "cddcdcbbbbaadaca", "cbcabadd", "cddbccbabbaadacd", "ddcaabcb", "ddddccbaababcacb", "bbcadacd", "bddbccbadbaacacd", "adcbabdc", "adddccbbababdacc", "ddccbbaa", "ddddccbcbbabaaca", "aadccdbb", "addadcbccbadbacb", "ddbbcaac", "ddddbcbbcbaaaacc", "cbbcdaad", "cddbbcbcdbaaaacd", "cdbdabca", "cdddbcbdababcaca", "ccabbadd", "cddcacbbbbaadacd", "bdacadcb", "bdddacbcabadcacb", "adabdcbc", "adddacbbdbacbacc", "bcdbacad", "bddcdcbbabacaacd", "dbaccadb", "dddbacbccbaadacb", "badbcacd", "bddadcbbcbaacacd", "ccbdbada", "cddcbcbdbbaadaca", "abcdabcd", "addbccbdababcacd", "caabdcdb", "cddaacbbdbacdacb", "cacdadbb", "cddaccbdabadbacb", "dabcdbca", "dddabcbcdbabcaca", "accbbdad", "addcccbbbbadaacd", "cddbacba", "cddddcbbabacbaca", "bacdbadc", "bddaccbdbbaadacc", "abdccabd", "addbdcbccbaabacd", "cdadbcab", "cdddacbdbbacaacb", "cbacbdad", "cddbacbcbbadaacd", "dacbbcad", "dddaccbbbbacaacd", "dcbadcab", "dddcbcbadbacaacb", "cdbbcaad", "cdddbcbbcbaaaacd", "cdbcbada", "cdddbcbcbbaadaca", "dbaacbdc", "dddbacbacbabdacc", "dcbaabdc", "dddcbcbaababdacc", "bacbdcda", "bddaccbbdbacdaca", "dacabdcb", "dddaccbabbadcacb", "cacdbdab", "cddaccbdbbadaacb", "bbcacdda", "bddbccbacbaddaca", "abadcbcd", "addbacbdcbabcacd", "addcbabc", "addddcbcbbaabacc", "dbadccab", "dddbacbdcbacaacb", "caddbbca", "cddadcbdbbabcaca", "bdacbcda", "bdddacbcbbacdaca", "bddccaab", "bddddcbccbaaaacb", "abccadbd", "addbccbcabadbacd", "adbdacbc", "adddbcbdabacbacc", "ddbbccaa", "ddddbcbbcbacaaca", "baadcdcb", "bddaacbdcbadcacb", "dbacacbd", "dddbacbcabacbacd", "dcbdaabc", "dddcbcbdabaabacc", "abdcbcda", "addbdcbcbbacdaca", "daacdbbc", "dddaacbcdbabbacc", "cadabcdb", "cddadcbabbacdacb", "abcdadcb", "addbccbdabadcacb", "dbbdccaa", "dddbbcbdcbacaaca", "adabbdcc", "adddacbbbbadcacc", "cdabcdba", "cdddacbbcbadbaca", "dcbacdba", "dddcbcbacbadbaca", "dababdcc", "dddabcbabbadcacc", "baccbadd", "bddaccbcbbaadacd", "bacdacbd", "bddaccbdabacbacd", "baaddcbc", "bddaacbddbacbacc", "cddcbbaa", "cddddcbcbbabaaca", "cbadbcda", "cddbacbdbbacdaca", "badcdacb", "bddadcbcdbaacacb", "cbabddac", "cddbacbbdbadaacc", "ddcacabb", "ddddccbacbaabacb", "acadbdbc", "addcacbdbbadbacc", "cdaabcdb", "cdddacbabbacdacb", "acddcbba", "addcdcbdcbabbaca", "dadccbab", "dddadcbccbabaacb", "ccbaabdd", "cddcbcbaababdacd", "bdcacbda", "bdddccbacbabdaca", "aabdbcdc", "addabcbdbbacdacc", "bdcdaacb", "bdddccbdabaacacb", "dbdbcaac", "dddbdcbbcbaaaacc", "cddbcbaa", "cddddcbbcbabaaca", "dccdbbaa", "dddcccbdbbabaaca", "dbacbdca", "dddbacbcbbadcaca", "dbacacdb", "dddbacbcabacdacb", "acbbcdad", "addcbcbbcbadaacd", "dbccadab", "dddbccbcabadaacb", "cdabacdb", "cdddacbbabacdacb", "bbacdcda", "bddbacbcdbacdaca", "dcbaacdb", "dddcbcbaabacdacb", "dcacbbad", "dddcacbcbbabaacd", "acadbcbd", "addcacbdbbacbacd", "ccdbdbaa", "cddcdcbbdbabaaca", "dcdcaabb", "dddcdcbcabaabacb", "accbddab", "addcccbbdbadaacb", "adbccbad", "adddbcbccbabaacd", "dabccdba", "dddabcbccbadbaca", "dcadcbab", "dddcacbdcbabaacb", "dbacbdac", "dddbacbcbbadaacc", "abbdcdac", "addbbcbdcbadaacc", "dcbbdaac", "dddcbcbbdbaaaacc", "dbdcaabc", "dddbdcbcabaabacc", "ddabbcca", "ddddacbbbbaccaca", "cadbcdba", "cddadcbbcbadbaca", "baacdcbd", "bddaacbcdbacbacd", "bacbaddc", "bddaccbbabaddacc", "cdbcaabd", "cdddbcbcabaabacd", "acabdbdc", "addcacbbdbabdacc", "bbadccda", "bddbacbdcbacdaca", "bcadbdac", "bddcacbdbbadaacc", "cddbcaab", "cddddcbbcbaaaacb", "dbccbaad", "dddbccbcbbaaaacd", "baadbdcc", "bddaacbdbbadcacc", "dabacbdc", "dddabcbacbabdacc", "dacdbbca", "dddaccbdbbabcaca", "cbadabdc", "cddbacbdababdacc", "abddcbac", "addbdcbdcbabaacc", "bacbddca", "bddaccbbdbadcaca", "daabcbcd", "dddaacbbcbabcacd", "acbdabcd", "addcbcbdababcacd", "dbacdabc", "dddbacbcdbaabacc", "acbcaddb", "addcbcbcabaddacb", "bdbdaacc", "bdddbcbdabaacacc", "dabbdcac", "dddabcbbdbacaacc", "badcbcda", "bddadcbcbbacdaca", "babcadcd", "bddabcbcabadcacd", "cbdadcba", "cddbdcbadbacbaca", "dbcadbca", "dddbccbadbabcaca", "cbbaadcd", "cddbbcbaabadcacd", "cadbdbca", "cddadcbbdbabcaca", "bcacdbad", "bddcacbcdbabaacd", "dbccabda", "dddbccbcababdaca", "bacacdbd", "bddaccbacbadbacd", "cbaacdbd", "cddbacbacbadbacd", "cdcbadba", "cdddccbbabadbaca", "ddcabbac", "ddddccbabbabaacc", "bacdadbc", "bddaccbdabadbacc", "acdbacbd", "addcdcbbabacbacd", "babcdacd", "bddabcbcdbaacacd", "acbbdcda", "addcbcbbdbacdaca", "cbaadbdc", "cddbacbadbabdacc", "dccbbada", "dddcccbbbbaadaca", "adcbabcd", "adddccbbababcacd", "bdacbdac", "bdddacbcbbadaacc", "acbcbadd", "addcbcbcbbaadacd", "aadbdccb", "addadcbbdbaccacb", "cbdaabdc", "cddbdcbaababdacc", "cdabcadb", "cdddacbbcbaadacb", "bdcaadbc", "bdddccbaabadbacc", "ddcaacbb", "ddddccbaabacbacb", "cadbadbc", "cddadcbbabadbacc", "abbcaddc", "addbbcbcabaddacc", "dabcbdac", "dddabcbcbbadaacc", "dcdbaacb", "dddcdcbbabaacacb", "cabbcdad", "cddabcbbcbadaacd", "aabccddb", "addabcbccbaddacb", "dacadbbc", "dddaccbadbabbacc", "bcabdcda", "bddcacbbdbacdaca", "adadbbcc", "adddacbdbbabcacc", "baddccba", "bddadcbdcbacbaca", "addcabcb", "addddcbcababcacb", "cbabacdd", "cddbacbbabacdacd", "bbdaadcc", "bddbdcbaabadcacc", "acbbcadd", "addcbcbbcbaadacd", "bacdbacd", "bddaccbdbbaacacd", "acbabcdd", "addcbcbabbacdacd", "abcbdcad", "addbccbbdbacaacd", "bdbcacad", "bdddbcbcabacaacd", "acdcbabd", "addcdcbcbbaabacd", "cabdacdb", "cddabcbdabacdacb", "aabbddcc", "addabcbbdbadcacc", "dbacbadc", "dddbacbcbbaadacc", "cadbacbd", "cddadcbbabacbacd", "dccbdaba", "dddcccbbdbaabaca", "abdbcacd", "addbdcbbcbaacacd", "cbddcbaa", "cddbdcbdcbabaaca", "cdcbbaad", "cdddccbbbbaaaacd", "dabaccdb", "dddabcbacbacdacb", "babdcdac", "bddabcbdcbadaacc", "aabdccbd", "addabcbdcbacbacd", "baacddbc", "bddaacbcdbadbacc", "badcabdc", "bddadcbcababdacc", "adccbabd", "adddccbcbbaabacd", "abbdaccd", "addbbcbdabaccacd", "ddbcaabc", "ddddbcbcabaabacc", "accdbabd", "addcccbdbbaabacd", "bdcbcada", "bdddccbbcbaadaca", "ababdcdc", "addbacbbdbacdacc", "abadccbd", "addbacbdcbacbacd", "acabbdcd", "addcacbbbbadcacd", "abbacddc", "addbbcbacbaddacc", "cdadbbca", "cdddacbdbbabcaca", "adbdcbca", "adddbcbdcbabcaca", "dbccdaab", "dddbccbcdbaaaacb", "bcbacdad", "bddcbcbacbadaacd", "dcbdabac", "dddcbcbdababaacc", "cbcdbada", "cddbccbdbbaadaca", "aadbcdcb", "addadcbbcbadcacb", "cbdbacda", "cddbdcbbabacdaca", "cbdabacd", "cddbdcbabbaacacd", "dacdbcab", "dddaccbdbbacaacb", "cdaabdcb", "cdddacbabbadcacb", "adbacdcb", "adddbcbacbadcacb", "cbbacdda", "cddbbcbacbaddaca", "dabbacdc", "dddabcbbabacdacc", "babdccad", "bddabcbdcbacaacd", "dbaccbad", "dddbacbccbabaacd", "bacbdadc", "bddaccbbdbaadacc", "abbaccdd", "addbbcbacbacdacd", "dcabadcb", "dddcacbbabadcacb", "abacdbdc", "addbacbcdbabdacc", "cbdaacdb", "cddbdcbaabacdacb", "bdcadcab", "bdddccbadbacaacb", "baddbcac", "bddadcbdbbacaacc", "bbadcdac", "bddbacbdcbadaacc", "cadcbdba", "cddadcbcbbadbaca", "cbabcadd", "cddbacbbcbaadacd", "baadcbcd", "bddaacbdcbabcacd", "acbbaddc", "addcbcbbabaddacc", "aadccbdb", "addadcbccbabdacb", "bbaccdda", "bddbacbccbaddaca", "acadcbdb", "addcacbdcbabdacb", "cddbaabc", "cddddcbbabaabacc", "dbcbcaad", "dddbccbbcbaaaacd", "dadacbcb", "dddadcbacbabcacb", "dacdabcb", "dddaccbdababcacb", "aaccddbb", "addaccbcdbadbacb", "dbadcabc", "dddbacbdcbaabacc", "dcacbdab", "dddcacbcbbadaacb", "dbadbcac", "dddbacbdbbacaacc", "cdacbdab", "cdddacbcbbadaacb", "badcbdac", "bddadcbcbbadaacc", "bdbcadac", "bdddbcbcabadaacc", "adbcbdac", "adddbcbcbbadaacc", "dadbcacb", "dddadcbbcbaacacb", "baabddcc", "bddaacbbdbadcacc", "dcabbcda", "dddcacbbbbacdaca", "adacbbcd", "adddacbcbbabcacd", "bbcddcaa", "bddbccbddbacaaca", "bcadabcd", "bddcacbdababcacd", "dcbcdaba", "dddcbcbcdbaabaca", "cabcdabd", "cddabcbcdbaabacd", "cbbdcaad", "cddbbcbdcbaaaacd", "cbadbadc", "cddbacbdbbaadacc", "bdbcdaac", "bdddbcbcdbaaaacc", "dbbccada", "dddbbcbccbaadaca", "ccadbabd", "cddcacbdbbaabacd", "cabdbadc", "cddabcbdbbaadacc", "bacbadcd", "bddaccbbabadcacd", "bdaccbad", "bdddacbccbabaacd", "baddabcc", "bddadcbdababcacc", "caadbbcd", "cddaacbdbbabcacd", "dbdabcca", "dddbdcbabbaccaca", "adabcbcd", "adddacbbcbabcacd", "adbcbcad", "adddbcbcbbacaacd", "abccbadd", "addbccbcbbaadacd", "abdadcbc", "addbdcbadbacbacc", "dacbacdb", "dddaccbbabacdacb", "bcbacadd", "bddcbcbacbaadacd", "cbdacbda", "cddbdcbacbabdaca", "dcbbaadc", "dddcbcbbabaadacc", "cdbdabac", "cdddbcbdababaacc", "aacbddbc", "addaccbbdbadbacc", "bbacaddc", "bddbacbcabaddacc", "bdbacdac", "bdddbcbacbadaacc", "acbcdabd", "addcbcbcdbaabacd", "daabccbd", "dddaacbbcbacbacd", "dacbcadb", "dddaccbbcbaadacb", "bcabcadd", "bddcacbbcbaadacd", "bbcdacad", "bddbccbdabacaacd", "dadcbacb", "dddadcbcbbaacacb", "cacdabbd", "cddaccbdababbacd", "cbaadbcd", "cddbacbadbabcacd", "dbcadcba", "dddbccbadbacbaca", "cabbdcda", "cddabcbbdbacdaca", "dbaabcdc", "dddbacbabbacdacc", "bdccadba", "bdddccbcabadbaca", "bbadcadc", "bddbacbdcbaadacc", "cdcdbbaa", "cdddccbdbbabaaca", "dbdcbcaa", "dddbdcbcbbacaaca", "abccdabd", "addbccbcdbaabacd", "daccdabb", "dddaccbcdbaabacb", "abbcadcd", "addbbcbcabadcacd", "accdbbda", "addcccbdbbabdaca", "caacddbb", "cddaacbcdbadbacb", "dacabbcd", "dddaccbabbabcacd", "adccabbd", "adddccbcababbacd", "cacdbbad", "cddaccbdbbabaacd", "dabdabcc", "dddabcbdababcacc", "bbaacddc", "bddbacbacbaddacc", "abbcdacd", "addbbcbcdbaacacd", "abcadbdc", "addbccbadbabdacc", "dcacdbba", "dddcacbcdbabbaca", "cbcdadba", "cddbccbdabadbaca", "cadcdabb", "cddadcbcdbaabacb", "bbdcdcaa", "bddbdcbcdbacaaca", "ddabaccb", "ddddacbbabaccacb", "adcdcbba", "adddccbdcbabbaca", "addcacbb", "addddcbcabacbacb", "cadcbbda", "cddadcbcbbabdaca", "accbdabd", "addcccbbdbaabacd", "dbbcadca", "dddbbcbcabadcaca", "adabccbd", "adddacbbcbacbacd", "bbdaacdc", "bddbdcbaabacdacc", "ddbcabca", "ddddbcbcababcaca", "acacdbdb", "addcacbcdbabdacb", "bcdcabda", "bddcdcbcababdaca", "dbcdcaba", "dddbccbdcbaabaca", "ddcbcaab", "ddddccbbcbaaaacb", "cdabcdab", "cdddacbbcbadaacb", "cacdabdb", "cddaccbdababdacb", "dabccabd", "dddabcbccbaabacd", "dcbacdab", "dddcbcbacbadaacb", "bdaabcdc", "bdddacbabbacdacc", "dbaadbcc", "dddbacbadbabcacc", "ababdccd", "addbacbbdbaccacd", "abbacdcd", "addbbcbacbadcacd", "bbdadcca", "bddbdcbadbaccaca", "ddbcabac", "ddddbcbcababaacc", "bdadbcca", "bdddacbdbbaccaca", "ccbdabad", "cddcbcbdababaacd", "bcabaddc", "bddcacbbabaddacc", "abccdadb", "addbccbcdbaadacb", "dcdbbcaa", "dddcdcbbbbacaaca", "caabbcdd", "cddaacbbbbacdacd", "dabbaccd", "dddabcbbabaccacd", "badbdcac", "bddadcbbdbacaacc", "adcbadcb", "adddccbbabadcacb", "baccddab", "bddaccbcdbadaacb", "cdbcabad", "cdddbcbcababaacd", "dbcacdab", "dddbccbacbadaacb", "dccbaadb", "dddcccbbabaadacb", "cdbaadbc", "cdddbcbaabadbacc", "dabcdabc", "dddabcbcdbaabacc", "cdbaabdc", "cdddbcbaababdacc", "badcdcba", "bddadcbcdbacbaca", "adbdbacc", "adddbcbdbbaacacc", "bacdabdc", "bddaccbdababdacc", "dbcaabcd", "dddbccbaababcacd", "acdbdbac", "addcdcbbdbabaacc", "cdacabbd", "cdddacbcababbacd", "acbbadcd", "addcbcbbabadcacd", "dbbaccda", "dddbbcbacbacdaca", "cacbddba", "cddaccbbdbadbaca", "bccbadda", "bddcccbbabaddaca", "aabcdcdb", "addabcbcdbacdacb", "cdadcabb", "cdddacbdcbaabacb", "dbacdbac", "dddbacbcdbabaacc", "bddcbcaa", "bddddcbcbbacaaca", "bdacbacd", "bdddacbcbbaacacd", "bdabdcac", "bdddacbbdbacaacc", "dcbbacad", "dddcbcbbabacaacd", "caadcbdb", "cddaacbdcbabdacb", "dabbcacd", "dddabcbbcbaacacd", "bccdbada", "bddcccbdbbaadaca", "abcadcdb", "addbccbadbacdacb", "adcbbacd", "adddccbbbbaacacd", "adbacbcd", "adddbcbacbabcacd", "bcdbcaad", "bddcdcbbcbaaaacd", "cacbbadd", "cddaccbbbbaadacd", "caddbabc", "cddadcbdbbaabacc", "adbbadcc", "adddbcbbabadcacc", "cdcabdba", "cdddccbabbadbaca", "bcdbdcaa", "bddcdcbbdbacaaca", "cdcabbda", "cdddccbabbabdaca", "cdbabacd", "cdddbcbabbaacacd", "adbbccda", "adddbcbbcbacdaca", "abdccdba", "addbdcbccbadbaca", "cabcaddb", "cddabcbcabaddacb", "dcabdbca", "dddcacbbdbabcaca", "ddaacbcb", "ddddacbacbabcacb", "bddbccaa", "bddddcbbcbacaaca", "bcdcbaad", "bddcdcbcbbaaaacd", "acadbbdc", "addcacbdbbabdacc", "bdcbadca", "bdddccbbabadcaca", "cacabdbd", "cddaccbabbadbacd", "baacbddc", "bddaacbcbbaddacc", "bcabcdda", "bddcacbbcbaddaca", "bcdacbad", "bddcdcbacbabaacd", "cacabbdd", "cddaccbabbabdacd", "bbcadcad", "bddbccbadbacaacd", "dacbdabc", "dddaccbbdbaabacc", "bccdadba", "bddcccbdabadbaca", "ccbbaadd", "cddcbcbbabaadacd", "bbadacdc", "bddbacbdabacdacc", "ddbaccab", "ddddbcbacbacaacb", "cbdadcab", "cddbdcbadbacaacb", "adccbdab", "adddccbcbbadaacb", "cadacbbd", "cddadcbacbabbacd", "bddcabca", "bddddcbcababcaca", "dcaacbdb", "dddcacbacbabdacb", "dcadbcba", "dddcacbdbbacbaca", "addbcabc", "addddcbbcbaabacc", "dbadaccb", "dddbacbdabaccacb", "baacbcdd", "bddaacbcbbacdacd", "dadbacbc", "dddadcbbabacbacc", "addbcacb", "addddcbbcbaacacb", "cdbabdac", "cdddbcbabbadaacc", "bbacadcd", "bddbacbcabadcacd", "adbcabdc", "adddbcbcababdacc", "bdbdacca", "bdddbcbdabaccaca", "dbabaccd", "dddbacbbabaccacd", "cadbbcda", "cddadcbbbbacdaca", "adabdbcc", "adddacbbdbabcacc", "dccabdab", "dddcccbabbadaacb", "bdcaacbd", "bdddccbaabacbacd", "acbdadcb", "addcbcbdabadcacb", "acabdcdb", "addcacbbdbacdacb", "acbadcbd", "addcbcbadbacbacd", "dabcbcad", "dddabcbcbbacaacd", "dbbccdaa", "dddbbcbccbadaaca", "cbbacadd", "cddbbcbacbaadacd", "accbadbd", "addcccbbabadbacd", "cacabddb", "cddaccbabbaddacb", "badadccb", "bddadcbadbaccacb", "accbabdd", "addcccbbababdacd", "bacddcba", "bddaccbddbacbaca", "badcadbc", "bddadcbcabadbacc", "dbdabacc", "dddbdcbabbaacacc", "bcbcdaad", "bddcbcbcdbaaaacd", "dccadbab", "dddcccbadbabaacb", "dcdabcab", "dddcdcbabbacaacb", "bdabacdc", "bdddacbbabacdacc", "babcdcad", "bddabcbcdbacaacd", "dcdbacba", "dddcdcbbabacbaca", "addbccba", "addddcbbcbacbaca", "cadacbdb", "cddadcbacbabdacb", "cdadacbb", "cdddacbdabacbacb", "cbacadbd", "cddbacbcabadbacd", "cdbadcab", "cdddbcbadbacaacb", "dbdccaba", "dddbdcbccbaabaca", "dcbadbca", "dddcbcbadbabcaca", "babadcdc", "bddabcbadbacdacc", "caabddbc", "cddaacbbdbadbacc", "bbaacdcd", "bddbacbacbadcacd", "acacbddb", "addcacbcbbaddacb", "bdadaccb", "bdddacbdabaccacb", "adcdabcb", "adddccbdababcacb", "acbdbcda", "addcbcbdbbacdaca", "dabbccad", "dddabcbbcbacaacd", "cddbabca", "cddddcbbababcaca", "bcaacdbd", "bddcacbacbadbacd", "dcadabbc", "dddcacbdababbacc", "adcbbcad", "adddccbbbbacaacd", "cacbdadb", "cddaccbbdbaadacb", "dbadcbca", "dddbacbdcbabcaca", "aabcddcb", "addabcbcdbadcacb", "badcbacd", "bddadcbcbbaacacd", "acddabbc", "addcdcbdababbacc", "adbcbacd", "adddbcbcbbaacacd", "abdcacbd", "addbdcbcabacbacd", "bdadcacb", "bdddacbdcbaacacb", "bbcaacdd", "bddbccbaabacdacd", "abaccdbd", "addbacbccbadbacd", "bacdbcad", "bddaccbdbbacaacd", "bdcaabdc", "bdddccbaababdacc", "cabbaddc", "cddabcbbabaddacc", "cadbabdc", "cddadcbbababdacc", "adbccadb", "adddbcbccbaadacb", "dbaacdcb", "dddbacbacbadcacb", "cdaabbcd", "cdddacbabbabcacd", "dbbdaacc", "dddbbcbdabaacacc", "bbccdada", "bddbccbcdbaadaca", "bdcacabd", "bdddccbacbaabacd", "ddbcacba", "ddddbcbcabacbaca", "aabdcbdc", "addabcbdcbabdacc", "bdcbaadc", "bdddccbbabaadacc", "cbcadabd", "cddbccbadbaabacd", "bacdcdba", "bddaccbdcbadbaca", "bcabadcd", "bddcacbbabadcacd", "cbadcdba", "cddbacbdcbadbaca", "aacdbdcb", "addaccbdbbadcacb", "dcbcdbaa", "dddcbcbcdbabaaca", "dbbacdca", "dddbbcbacbadcaca", "dacbbdca", "dddaccbbbbadcaca", "cabcdbad", "cddabcbcdbabaacd", "cadcbdab", "cddadcbcbbadaacb", "dbabadcc", "dddbacbbabadcacc", "dbdcbaca", "dddbdcbcbbaacaca", "dbcabacd", "dddbccbabbaacacd", "cadbbacd", "cddadcbbbbaacacd", "bbadadcc", "bddbacbdabadcacc", "abbaddcc", "addbbcbadbadcacc", "cabacdbd", "cddabcbacbadbacd", "bdabcadc", "bdddacbbcbaadacc", "cbdabcad", "cddbdcbabbacaacd", "caddabbc", "cddadcbdababbacc", "baaccbdd", "bddaacbccbabdacd", "bacdabcd", "bddaccbdababcacd", "bdcbdaac", "bdddccbbdbaaaacc", "ddacbacb", "ddddacbcbbaacacb", "abdcacdb", "addbdcbcabacdacb", "dcdbcbaa", "dddcdcbbcbabaaca", "abaccddb", "addbacbccbaddacb", "aadbcbdc", "addadcbbcbabdacc", "bdaacbdc", "bdddacbacbabdacc", "cddcabba", "cddddcbcababbaca", "abbadccd", "addbbcbadbaccacd", "bdcabacd", "bdddccbabbaacacd", "abdbdcac", "addbdcbbdbacaacc", "dbcaacbd", "dddbccbaabacbacd", "dabdcbca", "dddabcbdcbabcaca", "aadcbdbc", "addadcbcbbadbacc", "cbbaddac", "cddbbcbadbadaacc", "cadadbcb", "cddadcbadbabcacb", "cadbbdac", "cddadcbbbbadaacc", "addcbbac", "addddcbcbbabaacc", "dabcacbd", "dddabcbcabacbacd", "ddccbaab", "ddddccbcbbaaaacb", "cdababdc", "cdddacbbababdacc", "cdadbabc", "cdddacbdbbaabacc", "acadbbcd", "addcacbdbbabcacd", "acbdcdba", "addcbcbdcbadbaca", "aaccbbdd", "addaccbcbbabdacd", "bdbcdcaa", "bdddbcbcdbacaaca", "abdbcdca", "addbdcbbcbadcaca", "baaccddb", "bddaacbccbaddacb", "daadcbbc", "dddaacbdcbabbacc", "dadbccab", "dddadcbbcbacaacb", "dacbdbac", "dddaccbbdbabaacc", "cadbdcba", "cddadcbbdbacbaca", "accdbdba", "addcccbdbbadbaca", "acdbabcd", "addcdcbbababcacd", "abdbcdac", "addbdcbbcbadaacc", "bdcdcaab", "bdddccbdcbaaaacb", "addbcbac", "addddcbbcbabaacc", "daacdcbb", "dddaacbcdbacbacb", "dbcadcab", "dddbccbadbacaacb", "bdbccaad", "bdddbcbccbaaaacd", "daccabbd", "dddaccbcababbacd", "cabcabdd", "cddabcbcababdacd", "bdccadab", "bdddccbcabadaacb", "cbdadbca", "cddbdcbadbabcaca", "bcadbcda", "bddcacbdbbacdaca", "adcacdbb", "adddccbacbadbacb", "abdbccad", "addbdcbbcbacaacd", "babdaccd", "bddabcbdabaccacd", "bacdcadb", "bddaccbdcbaadacb", "ccbbadad", "cddcbcbbabadaacd", "aadbccdb", "addadcbbcbacdacb", "acbdbdca", "addcbcbdbbadcaca", "cabdcdab", "cddabcbdcbadaacb", "abdaccbd", "addbdcbacbacbacd", "acbdacdb", "addcbcbdabacdacb", "adccbbad", "adddccbcbbabaacd", "bdaccdab", "bdddacbccbadaacb", "bcbddcaa", "bddcbcbddbacaaca", "adcdcbab", "adddccbdcbabaacb", "cddbbaca", "cddddcbbbbaacaca", "dbbcdaac", "dddbbcbcdbaaaacc", "cbbadadc", "cddbbcbadbaadacc", "dcbabdac", "dddcbcbabbadaacc", "babadccd", "bddabcbadbaccacd", "cbcaabdd", "cddbccbaababdacd", "cbabdcad", "cddbacbbdbacaacd", "ddbacabc", "ddddbcbacbaabacc", "bacabddc", "bddaccbabbaddacc", "cddbbaac", "cddddcbbbbaaaacc", "ccdbaadb", "cddcdcbbabaadacb", "dbbcacad", "dddbbcbcabacaacd", "bacadcbd", "bddaccbadbacbacd", "cbaadcbd", "cddbacbadbacbacd", "cdbacbad", "cdddbcbacbabaacd", "bdccabda", "bdddccbcababdaca", "dcaabdbc", "dddcacbabbadbacc", "abbcdcad", "addbbcbcdbacaacd", "cabbadcd", "cddabcbbabadcacd", "cdadcbab", "cdddacbdcbabaacb", "dccdbaab", "dddcccbdbbaaaacb", "dcadbbac", "dddcacbdbbabaacc", "baddcbac", "bddadcbdcbabaacc", "caacdbdb", "cddaacbcdbabdacb", "dcbcabad", "dddcbcbcababaacd", "baccdbad", "bddaccbcdbabaacd", "abdaccdb", "addbdcbacbacdacb", "cbcadbad", "cddbccbadbabaacd", "bcacbdda", "bddcacbcbbaddaca", "badcdcab", "bddadcbcdbacaacb", "caabcddb", "cddaacbbcbaddacb", "acdabcbd", "addcdcbabbacbacd", "bbaadccd", "bddbacbadbaccacd"}

		for _, v := range variations {
			gRoomHeight = int(len(v) / 4)
			gRoomsArrayLength = len(v)
			gFinalRooms = parseString("aaaabbbbccccdddd")
			if gRoomHeight == 2 {
				gFinalRooms = parseString("aabbccdd")
			}

			start := time.Now()
			score := dijkstra(RoomState{0, emptyHall, parseString(v)})
			t := time.Since(start).Milliseconds()
			fmt.Printf("%v: %v in %vms\n", v, score, t)
		}
		return
	}

	// My input
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
		score := 0
		for t := 0; t < 100; t++ {
			score = dijkstra(RoomState{0, part.hall, part.rooms, 0})
		}
		timings[i] = time.Since(start).Milliseconds() / 100

		fmt.Printf("Part %v: %v in %vms\n", i+1, score, timings[i])
	}

	fmt.Printf("Total runtime: %vms\n", timings[0]+timings[1])
}
