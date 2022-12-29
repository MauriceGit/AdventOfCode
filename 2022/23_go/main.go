// 23_reworked project main.go
package main

import (
	"fmt"
	"math"
	//"github.com/pkg/profile"
)

const (
	E = iota
	W
	S
	N
	SE
	NW
	SW
	NE
)

type Pos struct {
	x, y int
}

var (
	// Must be the same order as the const directions
	allDirs = [...]Pos{Pos{1, 0}, Pos{-1, 0}, Pos{0, 1}, Pos{0, -1}, Pos{1, 1}, Pos{-1, -1}, Pos{-1, 1}, Pos{1, -1}}
	check8  = [8]bool{false, false, false, false, false, false, false, false}
)

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func minMaxCoord(elves map[Pos]int) (int, int, int, int) {
	minX, maxX, minY, maxY := math.MaxInt, math.MinInt, math.MaxInt, math.MinInt
	for k, _ := range elves {
		minX = min(k.x, minX)
		maxX = max(k.x, maxX)
		minY = min(k.y, minY)
		maxY = max(k.y, maxY)
	}
	return minX, maxX, minY, maxY
}

func add(p1, p2 Pos) Pos {
	return Pos{p1.x + p2.x, p1.y + p2.y}
}

func proposeMove(elves map[Pos]int, elve Pos, rot int) (Pos, Pos, bool) {

	allFree := true
	for i, d := range allDirs {
		_, ok := elves[add(elve, d)]
		check8[i] = !ok
		allFree = allFree && !ok
	}
	if allFree {
		return elve, elve, false
	}

	for i := 0; i < 4; i++ {
		switch (i + rot) % 4 {
		case 0:
			if check8[N] && check8[NE] && check8[NW] {
				return add(elve, allDirs[N]), allDirs[N], true
			}
		case 1:
			if check8[S] && check8[SE] && check8[SW] {
				return add(elve, allDirs[S]), allDirs[S], true
			}
		case 2:
			if check8[W] && check8[NW] && check8[SW] {
				return add(elve, allDirs[W]), allDirs[W], true
			}
		case 3:
			if check8[E] && check8[NE] && check8[SE] {
				return add(elve, allDirs[E]), allDirs[E], true
			}
		}
	}

	return elve, elve, false
}

func nextRound(elves map[Pos]int, i int) (map[Pos]int, bool) {

	newElves := make(map[Pos]int, len(elves))
	someoneMoved := 0

	for e, _ := range elves {
		p, d, posOk := proposeMove(elves, e, i)

		if _, ok := newElves[p]; ok {
			newElves[add(p, d)] = 1
			delete(newElves, p)
			newElves[e] = 1
			someoneMoved--
		} else if posOk {
			newElves[p] = 1
			someoneMoved++
		} else {
			newElves[e] = 1
		}
	}

	return newElves, someoneMoved == 0
}

func main() {

	//defer profile.Start(profile.ProfilePath(".")).Stop()

	elves := make(map[Pos]int)
	if aoc, ok := InitAOC(); ok {
		for y, l := range aoc.GetLines() {
			for x, c := range l {
				if c == '#' {
					elves[Pos{x, y}] = 1
				}
			}
		}
	}

	done := false
	for i := 0; ; i++ {
		elves, done = nextRound(elves, i)

		if i == 9 {
			minX, maxX, minY, maxY := minMaxCoord(elves)
			fmt.Println((maxX-minX+1)*(maxY-minY+1) - len(elves))
		}
		if done {
			fmt.Println(i + 1)
			break
		}
	}

}
