// 03 project main.go
package main

import (
	"fmt"
)

func valid(a, b, c int) int {
	if a+b > c && a+c > b && b+c > a {
		return 1
	}
	return 0
}

func main() {

	if aoc, ok := InitAOC(); ok {
		lines := aoc.GetLines()

		count := 0
		for _, l := range lines {
			i := Ints(l)
			count += valid(i[0], i[1], i[2])
		}
		fmt.Println(count)

		count = 0
		for i := 0; i < len(lines); i += 3 {
			i0 := Ints(lines[i])
			i1 := Ints(lines[i+1])
			i2 := Ints(lines[i+2])

			count += valid(i0[0], i1[0], i2[0])
			count += valid(i0[1], i1[1], i2[1])
			count += valid(i0[2], i1[2], i2[2])
		}
		fmt.Println(count)
	}
}
