// 20_reworked project main.go
package main

import (
	"fmt"
	"strconv"

	//"math"
	"github.com/pkg/profile"
)

type Node struct {
	prev int
	v    int
	next int
}

type LinkedList struct {
	backing []Node
	start   int
	size    int
}

func (ll *LinkedList) RotateLeft(n int) {
	if n < 0 {
		n = ll.size - ((-n) % ll.size)
	}
	for i := 0; i < n%ll.size; i++ {
		ll.start = ll.backing[ll.start].next
	}
}

func (ll *LinkedList) Append(v int) {
	if ll.size == 0 {
		ll.backing = append(ll.backing, Node{0, v, 0})
		ll.start = 0
	} else {
		ll.backing = append(ll.backing, Node{ll.backing[ll.start].prev, v, ll.start})
		n := len(ll.backing) - 1
		ll.backing[ll.backing[ll.start].prev].next = n
		ll.backing[ll.start].prev = n
	}
	ll.size++
}

func (ll *LinkedList) AppendLeft(v int) {
	ll.Append(v)
	ll.start = ll.backing[ll.start].prev
}

func (ll LinkedList) Index(v int) int {
	count := 0
	n := ll.start

	for ll.backing[n].v != v {
		n = ll.backing[n].next
		count++
	}

	return count
}

func (ll *LinkedList) PopLeft() int {
	v := ll.backing[ll.start].v

	prev := ll.backing[ll.start].prev
	next := ll.backing[ll.start].next

	ll.backing[prev].next = next
	ll.backing[next].prev = prev

	ll.start = next
	ll.size--
	return v
}

func (ll LinkedList) String() string {
	s := ""
	n := ll.start
	first := true

	for first || n != ll.start {

		pre := " -> "
		if first {
			pre = ""
		}
		s += fmt.Sprintf("%v%v", pre, ll.backing[n].v)

		n = ll.backing[n].next
		first = false
	}
	return s
}

func mix(numbers LinkedList, origNumbers []int, numberMapping map[int]int) LinkedList {

	for _, nn := range origNumbers {
		i := numbers.Index(nn)
		numbers.RotateLeft(i)
		n := numbers.PopLeft()
		numbers.RotateLeft(numberMapping[nn])
		numbers.AppendLeft(n)
	}

	return numbers
}

func getSolution(numbers LinkedList, num0 int, numberMapping map[int]int) int {
	i := numbers.Index(num0)
	numbers.RotateLeft(i)
	numbers.RotateLeft(1000)
	nn := numberMapping[numbers.backing[numbers.start].v]
	numbers.RotateLeft(1000)
	nn += numberMapping[numbers.backing[numbers.start].v]
	numbers.RotateLeft(1000)
	nn += numberMapping[numbers.backing[numbers.start].v]
	return nn
}

func main() {

	defer profile.Start(profile.ProfilePath(".")).Stop()

	var numbers LinkedList
	var numbers2 LinkedList
	numberMapping := make(map[int]int)
	numberMapping2 := make(map[int]int)
	var origNumbers []int
	var num0 int

	if aoc, ok := InitAOC(); ok {
		for i, v := range aoc.GetLines() {
			var conv int
			conv, _ = strconv.Atoi(v)
			numberMapping[i] = conv
			numberMapping2[i] = conv * 811589153
			numbers.Append(i)
			numbers2.Append(i)
			origNumbers = append(origNumbers, i)
			if conv == 0 {
				num0 = i
			}
		}
	}

	fmt.Println(len(numbers2.backing))

	numbers = mix(numbers, origNumbers, numberMapping)
	fmt.Println(getSolution(numbers, num0, numberMapping))

	for i := 0; i < 10; i++ {
		numbers2 = mix(numbers2, origNumbers, numberMapping2)
	}

	fmt.Println(len(numbers2.backing))

	//fmt.Println(getSolution(numbers2, num0, numberMapping2))

}
