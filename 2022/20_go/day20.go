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

func (n Node) toString(mapping map[int]int) string {
	return fmt.Sprintf("(%v %v %v)", n.prev, mapping[n.v], n.next)
}

func newLinkedList() LinkedList {
	var ll LinkedList
	ll.nextFree = -1
	return ll
}

func newLinkedListSize(size int) LinkedList {
	var ll LinkedList
	ll.nextFree = -1
	ll.backing = make([]Node, 0, size)
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

func (ll LinkedList) toString(mapping map[int]int) string {
	s := ""
	n := ll.start
	first := true

	for first || n != ll.start {

		pre := " -> "
		if first {
			pre = ""
		}
		v := ll.backing[n].v
		if tmp, ok := mapping[v]; ok {
			v = tmp
		}

		s += fmt.Sprintf("%v%v", pre, v)

		n = ll.backing[n].next
		first = false
	}
	return s
}

func (ll LinkedList) String() string {
	return ll.toString(nil)
}

func repositionNode(buckets []LinkedList, bi, offset, element int, nToBucket *map[int]int, mapping map[int]int) {
	// count indices to get out of this bucket (and return early, if the element stays in this bucket!)

	if offset == 0 {
		return
	}

	// we know, that element is in buckets[bi]!
	count := 0
	node := buckets[bi].start
	nodeBi := bi
	for buckets[bi].backing[node].v != element {
		node = buckets[bi].backing[node].next
		count++
	}

	fmt.Printf("    node: %v at bucket %v | %v\n", node, nodeBi, buckets[bi].backing[node].toString(mapping))

	// element will be inserted into the same bucket again
	// node is the node that contains element!
	newNode := node
	fmt.Printf("    offset: %v, size: %v, count: %v, all: %v\n", offset, buckets[bi].size, count, (buckets[bi].size-1)-count)
	if offset > (buckets[bi].size-1)-count {
		offset -= (buckets[bi].size - 1) - count
		fmt.Printf("    %v\n", offset)
		bi = (bi + 1) % len(buckets)
		// when jumping a bucket, we implicitely jump one element because we always insert _after_ a node.
		offset--

		// offset whole buckets
		for offset > buckets[bi].size {
			offset -= buckets[bi].size
			bi = (bi + 1) % len(buckets)
		}
		newNode = buckets[bi].start
	}

	for i := 0; i < offset; i++ {
		newNode = buckets[bi].backing[newNode].next
	}

	fmt.Printf("    newNode: %v at bucket %v | %v\n", newNode, bi, buckets[bi].backing[newNode].toString(mapping))

	// The node is the very first node and would be inserted exactly at the end of the linkedList (offset == len(bucket))
	// So we just move the start-pointer and are done.
	if node == newNode {
		buckets[nodeBi].start = buckets[nodeBi].backing[node].next
		return
	}

	// nodeBi is the source bucket index
	// node is the source node
	// bi is the target bucket index
	// newNode is the target node (insert node _after_?)

	// Remove old node
	prev := buckets[nodeBi].backing[node].prev
	next := buckets[nodeBi].backing[node].next
	buckets[nodeBi].backing[prev].next = next
	buckets[nodeBi].backing[next].prev = prev
	buckets[nodeBi].size--
	if buckets[nodeBi].start == node {
		buckets[nodeBi].start = next
	}
	//buckets[nodeBi].nextFree = node

	// for _, n := range buckets[bi].backing {
	// 	fmt.Printf("  %v ", n)
	// }
	// fmt.Printf("\n")

	// Insert new node
	buckets[bi].backing = append(buckets[bi].backing, Node{newNode, element, buckets[bi].backing[newNode].next})
	next = buckets[bi].backing[newNode].next
	buckets[bi].backing[newNode].next = len(buckets[bi].backing) - 1
	buckets[bi].backing[next].prev = len(buckets[bi].backing) - 1
	buckets[bi].size++
	(*nToBucket)[element] = bi

	// for _, n := range buckets[bi].backing {
	// 	fmt.Printf("  %v ", n)
	// }
	// fmt.Printf("\n")

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
		bi := (*nToBucket)[nn]
		//i := buckets[bi].Index(nn)
		//nextBi := findBucket(buckets, i)
		offset := numberMapping[nn]
		if offset < 0 {
			offset = len(origNumbers) + offset - 1
		}

		fmt.Printf("    %v (%v): bucket: %v, offset: %v\n", nn, numberMapping[nn], bi, offset)

		repositionNode(buckets, bi, offset, nn, nToBucket, numberMapping)

		for _, b := range buckets {
			fmt.Printf("[%v] -> ", b.toString(numberMapping))
		}
		fmt.Printf("\n")

		//break
	}

	return buckets
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

	bucketSize := 3
	var buckets []LinkedList

	buckets = append(buckets, newLinkedListSize(bucketSize))

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

			if i != 0 && i%bucketSize == 0 {
				buckets = append(buckets, newLinkedListSize(bucketSize))
			}

			buckets[len(buckets)-1].Append(i)
			nToBucket[i] = len(buckets) - 1

			origNumbers = append(origNumbers, i)
			if conv == 0 {
				num0 = i
			}
		}
	}
	num0 = num0

	for _, b := range buckets {
		fmt.Printf("[%v] -> ", b.toString(numberMapping))
	}
	fmt.Printf("\n")
	buckets = mix(buckets, origNumbers, numberMapping, &nToBucket)

	//fmt.Println(getSolution(numbers, num0, numberMapping))

	return
	// for i := 0; i < 10; i++ {
	// 	numbers2 = mix(numbers2, origNumbers, numberMapping2)
	// }
	// fmt.Println(getSolution(numbers2, num0, numberMapping2))
}
