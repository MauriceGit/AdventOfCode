// 20_reworked project main.go
package main

import (
	"fmt"
	"strconv"
	//"github.com/pkg/profile"
)

type Node struct {
	v    int
	next int
}

type LinkedList struct {
	backing []Node
	first   int
	last    int
	size    int
}

type Buckets []LinkedList

func (b Buckets) at(bucketID, nodeIndex int) *Node {
	return &b[bucketID].backing[nodeIndex]
}

func (b Buckets) first(bucketID int) Node {
	return b[bucketID].backing[b[bucketID].first]
}

func (n Node) toString(mapping map[int]int) string {
	return fmt.Sprintf("(e: %v nextI: %v)", mapping[n.v], n.next)
}

func newLinkedList(size int) LinkedList {
	var ll LinkedList
	ll.backing = make([]Node, 0, size)
	ll.first = -1
	ll.last = -1
	return ll
}

func (ll *LinkedList) Append(v int) {
	ll.backing = append(ll.backing, Node{v, -1})
	if ll.last != -1 {
		ll.backing[ll.last].next = len(ll.backing) - 1
	} else {
		ll.first = len(ll.backing) - 1
	}
	ll.last = len(ll.backing) - 1
	ll.size++
}

func (ll LinkedList) toString(mapping map[int]int) string {
	s := ""

	if ll.size == 0 {
		return s
	}

	for n := ll.first; n != -1; n = ll.backing[n].next {
		pre := " -> "
		if n == ll.first {
			pre = ""
		}
		v := ll.backing[n].v
		if tmp, ok := mapping[v]; ok {
			v = tmp
		}
		s += fmt.Sprintf("%v%v", pre, v)
	}

	return s
}

func (ll LinkedList) String() string {
	return ll.toString(nil)
}

func repositionNode(buckets Buckets, bi, offset, element int, nToBucket *map[int]int, mapping map[int]int) (int, int, int, int) {
	count := 0
	nodeBi := bi
	node := buckets[bi].first

	bb := buckets[bi].backing

	// only the first element is referenced directly!
	if bb[buckets[bi].first].v != element {
		count++
		for bb[bb[node].next].v != element {
			node = bb[node].next
			count++
		}
	}

	// Remove old node
	if node == buckets[nodeBi].first && buckets.first(nodeBi).v == element {
		buckets[nodeBi].first = buckets.at(nodeBi, node).next
	} else {
		nodeNext := buckets[nodeBi].backing[node].next
		nodeNextNext := buckets[nodeBi].backing[nodeNext].next
		buckets[nodeBi].backing[node].next = nodeNextNext
	}
	buckets[nodeBi].size--

	// node is the node that contains element!
	newNode := node

	if offset > buckets[bi].size-count {
		offset -= buckets[bi].size - count
		bi = (bi + 1) % len(buckets)
		// when jumping a bucket, we implicitely jump one element because we always insert _after_ a node.
		offset--

		// offset whole buckets
		for offset >= buckets[bi].size {
			offset -= buckets[bi].size
			bi = (bi + 1) % len(buckets)
		}
		newNode = buckets[bi].first
	}

	// find node where we want to insert _after_
	for i := 0; i < offset; i++ {
		newNode = buckets[bi].backing[newNode].next
	}

	// Insert new node
	buckets[bi].backing = append(buckets[bi].backing, Node{element, buckets[bi].backing[newNode].next})
	buckets[bi].backing[newNode].next = len(buckets[bi].backing) - 1
	buckets[bi].size++
	(*nToBucket)[element] = bi

	return node, nodeBi, newNode, bi
}

func mix(buckets Buckets, origNumbers []int, numberMapping map[int]int, nToBucket *map[int]int) Buckets {

	for _, nn := range origNumbers {
		bi := (*nToBucket)[nn]
		offset := numberMapping[nn]
		if offset < 0 {
			tmp := (-offset) % (len(origNumbers) - 1)
			offset = len(origNumbers) - tmp - 1
		}
		offset = offset % (len(origNumbers) - 1)

		if offset != 0 {
			repositionNode(buckets, bi, offset, nn, nToBucket, numberMapping)
		}
	}

	return buckets
}

func findNodeAtOffset(buckets Buckets, bi, offset, element int, mapping map[int]int) int {

	node := buckets[bi].first
	count := 1
	for mapping[buckets[bi].backing[node].v] != element {
		node = buckets[bi].backing[node].next
		count++
	}
	if offset > buckets[bi].size-count {
		offset -= buckets[bi].size - count
		bi = (bi + 1) % len(buckets)
		node = buckets[bi].first
		offset--

		for offset >= buckets[bi].size {
			offset -= buckets[bi].size
			bi = (bi + 1) % len(buckets)
		}
		node = buckets[bi].first
	}

	for offset > 0 {
		node = buckets[bi].backing[node].next
		offset--
	}

	return mapping[buckets[bi].backing[node].v]
}

func getSolution(buckets Buckets, num0 int, numberMapping map[int]int, nToBucket map[int]int, numberCount int) int {
	v0 := findNodeAtOffset(buckets, nToBucket[num0], 1000%numberCount, 0, numberMapping)
	v1 := findNodeAtOffset(buckets, nToBucket[num0], 2000%numberCount, 0, numberMapping)
	v2 := findNodeAtOffset(buckets, nToBucket[num0], 3000%numberCount, 0, numberMapping)

	return v0 + v1 + v2
}

func main() {

	//defer profile.Start(profile.ProfilePath(".")).Stop()

	bucketSize := 500
	var buckets Buckets
	buckets = append(buckets, newLinkedList(bucketSize))

	var buckets2 Buckets
	buckets2 = append(buckets2, newLinkedList(bucketSize))

	numberMapping := make(map[int]int)
	numberMapping2 := make(map[int]int)
	var origNumbers []int
	var num0 int

	nToBucket := make(map[int]int)
	nToBucket2 := make(map[int]int)

	if aoc, ok := InitAOC(); ok {
		for i, v := range aoc.GetLines() {
			var conv int
			conv, _ = strconv.Atoi(v)
			numberMapping[i] = conv
			numberMapping2[i] = conv * 811589153

			if i != 0 && i%bucketSize == 0 {
				buckets = append(buckets, newLinkedList(bucketSize))
			}

			buckets[len(buckets)-1].Append(i)
			nToBucket[i] = len(buckets) - 1
			buckets2[len(buckets2)-1].Append(i)
			nToBucket2[i] = len(buckets2) - 1

			origNumbers = append(origNumbers, i)
			if conv == 0 {
				num0 = i
			}
		}
	}
	buckets = mix(buckets, origNumbers, numberMapping, &nToBucket)
	fmt.Println(getSolution(buckets, num0, numberMapping, nToBucket, len(origNumbers)))

	for i := 0; i < 10; i++ {
		buckets2 = mix(buckets2, origNumbers, numberMapping2, &nToBucket2)
	}
	fmt.Println(getSolution(buckets2, num0, numberMapping2, nToBucket2, len(origNumbers)))
}
