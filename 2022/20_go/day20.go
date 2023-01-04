// 20_reworked project main.go
package main

import (
	"fmt"
	"strconv"
	//"math"
	//"github.com/pkg/profile"
)

type Node struct {
	prev int
	v    int
	next int
}

type LinkedList struct {
	nextFree int
	backing  []Node
	start    int
	size     int
}

func newLinkedList() LinkedList {
	var ll LinkedList
	ll.nextFree = -1
	return ll
}

func newLinkedList(size int) LinkedList {
	var ll LinkedList
	ll.nextFree = -1
	ll.backing = make([]Node, size)
	return ll
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

		node := Node{ll.backing[ll.start].prev, v, ll.start}
		n := ll.nextFree
		if ll.nextFree != -1 {
			ll.backing[ll.nextFree] = node
			ll.nextFree = -1
		} else {
			ll.backing = append(ll.backing, node)
			n = len(ll.backing) - 1
		}

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

	ll.nextFree = ll.start

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

func findBucket(buckets []LinkedList, bi, offset, element int) (int, int) {
	// count indices to get out of this bucket (and return early, if the element stays in this bucket!)

	// we know, that element is in buckets[bi]!
	count := 0
	node := buckets[bi].start
	for buckets[bi].backing[node].v != element {
		node = buckets[bi].backing[node].next
		count++
	}

	// element will be inserted into the same bucket again
	if offset < (buckets[bi].size-1)-count {

	}

	// offset whole buckets

	// iterate target bucket to find exact insertion position

	// insert number at target bucket

	// remove number from source bucket

	// update nToBucket reference

}

func mix(buckets []LinkedList, origNumbers []int, numberMapping map[int]int, nToBucket *map[int]int) []LinkedList {

	// for _, nn := range origNumbers {
	// 	i := numbers.Index(nn)
	// 	numbers.RotateLeft(i)
	// 	n := numbers.PopLeft()
	// 	numbers.RotateLeft(numberMapping[nn])
	// 	numbers.AppendLeft(n)
	// }

	for _, nn := range origNumbers {
		bi := nToBucket[nn]
		i := buckets[bi].Index(nn)
		nextBi := findBucket(buckets, i)
	}

	return numbers
}

func getSolution(numbers LinkedList, num0 int, numberMapping map[int]int) int {
	// i := numbers.Index(num0)
	// numbers.RotateLeft(i)
	// numbers.RotateLeft(1000)
	// nn := numberMapping[numbers.backing[numbers.start].v]
	// numbers.RotateLeft(1000)
	// nn += numberMapping[numbers.backing[numbers.start].v]
	// numbers.RotateLeft(1000)
	// nn += numberMapping[numbers.backing[numbers.start].v]

	return 0
}

func main() {

	//defer profile.Start(profile.ProfilePath(".")).Stop()

	//numbers := newLinkedList()
	//numbers2 := newLinkedList()

	bucketSize := 10
	var buckets []LinkedList

	buckets = append(buckets, newLinkedList(bucketSize))

	numberMapping := make(map[int]int)
	numberMapping2 := make(map[int]int)
	var origNumbers []int
	var num0 int

	nToBucket := make(map[int]int)

	if aoc, ok := InitAOC(); ok {
		for i, v := range aoc.GetLines() {
			var conv int
			conv, _ = strconv.Atoi(v)
			numberMapping[i] = conv
			numberMapping2[i] = conv * 811589153
			//numbers.Append(i)
			//numbers2.Append(i)

			buckets[len(buckets)-1].Append(i)
			nToBucket[i] = len(buckets) - 1

			origNumbers = append(origNumbers, i)
			if conv == 0 {
				num0 = i
			}
		}
	}

	numbers = mix(numbers, origNumbers, numberMapping, &nToBucket)
	fmt.Println(getSolution(numbers, num0, numberMapping))

	return
	for i := 0; i < 10; i++ {
		numbers2 = mix(numbers2, origNumbers, numberMapping2)
	}
	fmt.Println(getSolution(numbers2, num0, numberMapping2))
}
