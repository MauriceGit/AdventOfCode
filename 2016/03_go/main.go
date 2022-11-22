// 03 project main.go
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func valid(a, b, c int) int {
	if a+b > c && a+c > b && b+c > a {
		return 1
	}
	return 0
}

type triangle struct {
	a, b, c int
}

func toInts(lines []string) []triangle {
	ints := make([]triangle, 0, len(lines))
	for _, l := range lines {
		i := strings.Fields(l)
		a, _ := strconv.Atoi(i[0])
		b, _ := strconv.Atoi(i[1])
		c, _ := strconv.Atoi(i[2])
		ints = append(ints, triangle{a, b, c})
	}
	return ints
}

func main() {

	if aoc, ok := InitAOC(); ok {
		lines := aoc.GetLines()

		sum := 0
		for c := 0; c < 10000; c++ {
			ints := toInts(lines)
			count := 0
			for _, l := range ints {
				count += valid(l.a, l.b, l.c)
			}
			//fmt.Println(count)
			sum += count

			count = 0
			for i := 0; i < len(ints); i += 3 {
				count += valid(ints[i].a, ints[i+1].a, ints[i+2].a)
				count += valid(ints[i].b, ints[i+1].b, ints[i+2].b)
				count += valid(ints[i].c, ints[i+1].c, ints[i+2].c)
			}
			//fmt.Println(count)
			sum += count
		}
		fmt.Println(sum)
	}
}
