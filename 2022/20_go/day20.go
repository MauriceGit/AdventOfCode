// 20_reworked project main.go
package main

import (
	"fmt"
	"strconv"
	//"math"
	//"github.com/pkg/profile"
)

type Node struct {
	prev *Node
	v    int
	next *Node
}

type LinkedList struct {
	start *Node
	size  int
}

func (ll *LinkedList) RotateLeft(n int) {
	if n < 0 {
		n = ll.size - ((-n) % ll.size)
	}
	for i := 0; i < n%ll.size; i++ {
		ll.start = ll.start.next
	}
}

func (ll *LinkedList) Append(v int) {
	if ll.start == nil {
		ll.start = &Node{nil, v, nil}
		ll.start.prev = ll.start
		ll.start.next = ll.start
	} else {
		n := &Node{ll.start.prev, v, ll.start}
		ll.start.prev.next = n
		ll.start.prev = n
	}
	ll.size++
}

func (ll *LinkedList) AppendLeft(v int) {
	ll.Append(v)
	ll.start = ll.start.prev
}

func (ll LinkedList) Index(v int) int {
	count := 0
	n := ll.start
	start := true

	for n.v != v && (start || n != ll.start) {
		n = n.next
		count++
	}

	return count
}

func (ll *LinkedList) PopLeft() int {
	n := ll.start

	ll.start.prev.next = ll.start.next
	ll.start.next.prev = ll.start.prev

	ll.start = ll.start.next
	n.next = nil
	n.prev = nil
	ll.size--
	return n.v
}

func toString(node *Node, firstNode *Node, first bool, s string) string {
	if !first && node == firstNode {
		return s
	}
	pre := " -> "
	if first {
		pre = ""
	}
	return toString(node.next, firstNode, false, s+fmt.Sprintf("%v%v", pre, node.v))

}

func (ll LinkedList) String() string {
	return toString(ll.start, ll.start, true, "")
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
	nn := numberMapping[numbers.start.v]
	numbers.RotateLeft(1000)
	nn += numberMapping[numbers.start.v]
	numbers.RotateLeft(1000)
	nn += numberMapping[numbers.start.v]
	return nn
}

func main() {

	//defer profile.Start(profile.ProfilePath(".")).Stop()

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

	numbers = mix(numbers, origNumbers, numberMapping)
	fmt.Println(getSolution(numbers, num0, numberMapping))

	for i := 0; i < 10; i++ {
		numbers2 = mix(numbers2, origNumbers, numberMapping2)
	}
	fmt.Println(getSolution(numbers2, num0, numberMapping2))

}
