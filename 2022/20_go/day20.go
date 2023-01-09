// 20_reworked project main.go
package main

import (
	"fmt"
	"strconv"
	//"math"
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
		//n = ll.backing[n].next
		// if n == -1 {
		// 	break
		// }
	}

	return s
}

func (ll LinkedList) String() string {
	return ll.toString(nil)
}

// getOffsetNode Returns the node and bucketIndex that contains element and the Node and bucketIndex the given offset
func getOffsetNode(buckets Buckets, bi, offset, element int, nToBucket *map[int]int, mapping map[int]int, edit bool) (int, int, int, int) {
	count := 0
	nodeBi := bi
	node := buckets[bi].first

	bb := buckets[bi].backing

	// only the first element is referenced directly!
	if bb[buckets[bi].first].v != element {
		//offset++
		for bb[bb[node].next].v != element {
			node = bb[node].next
			count++
		}
	}

	if edit {
		// Remove old node
		if node == buckets[nodeBi].first && buckets.first(nodeBi).v == element {
			buckets[nodeBi].first = buckets.at(nodeBi, node).next
		} else {
			nodeNext := buckets[nodeBi].backing[node].next
			nodeNextNext := buckets[nodeBi].backing[nodeNext].next
			buckets[nodeBi].backing[node].next = nodeNextNext
		}
		buckets[nodeBi].size--
	}

	// node is the node that contains element!
	newNode := node

	//fmt.Printf("  %v, offset: %v\n", mapping[buckets[bi].backing[newNode].v], offset)

	if offset > (buckets[bi].size-1)-count {
		offset -= (buckets[bi].size - 1) - count
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
		//fmt.Println(offset - i)
		newNode = buckets[bi].backing[newNode].next
	}

	if edit {
		// Insert new node
		buckets[bi].backing = append(buckets[bi].backing, Node{element, buckets[bi].backing[newNode].next})
		buckets[bi].backing[newNode].next = len(buckets[bi].backing) - 1
		buckets[bi].size++
		(*nToBucket)[element] = bi
	}

	return node, nodeBi, newNode, bi
}

func repositionNode(buckets Buckets, bi, offset, element int, nToBucket *map[int]int, mapping map[int]int) {
	// count indices to get out of this bucket (and return early, if the element stays in this bucket!)

	if offset == 0 {
		return
	}

	// node is the node just BEFORE the one that contains element, so that we can remove the previous next reference
	// Same thing for newNode!
	//node, nodeBi, newNode, bi := getOffsetNode(buckets, bi, offset, element, nToBucket)
	getOffsetNode(buckets, bi, offset, element, nToBucket, mapping, true)

	//fmt.Printf("    %v --> newNode: %v at bucket %v | %v\n", buckets[nodeBi].backing[node].toString(mapping), newNode, bi, buckets[bi].backing[newNode].toString(mapping))

	// The node is the very first node and would be inserted exactly at the end of the linkedList (offset == len(bucket))
	// So we just move the start-pointer and are done.
	// if node == newNode && nodeBi == bi {
	// 	buckets[nodeBi].start = buckets[nodeBi].backing[node].next
	// 	return
	// }

	// nodeBi is the source bucket index
	// node is the source node
	// bi is the target bucket index
	// newNode is the target node (insert node _after_?)

	// Remove old node

	// fmt.Printf("Before everything: ")
	// fmt.Printf("    First Index: %v --> ", buckets[bi].first)
	// for i, n := range buckets[bi].backing {
	// 	fmt.Printf("  [%v]%v ", i, n.toString(mapping))
	// }
	// fmt.Printf("\n")

	// fmt.Printf("Node: %v\n", buckets[nodeBi].backing[node].toString(mapping))

	// if node == buckets[nodeBi].first && buckets.first(nodeBi).v == element {
	// 	buckets[nodeBi].first = buckets.at(nodeBi, node).next
	// } else {
	// 	nodeNext := buckets[nodeBi].backing[node].next
	// 	nodeNextNext := buckets[nodeBi].backing[nodeNext].next
	// 	buckets[nodeBi].backing[node].next = nodeNextNext
	// }
	// buckets[nodeBi].size--

	// fmt.Printf("After deletion:    ")
	// fmt.Printf("    First Index: %v --> ", buckets[bi].first)
	// for i, n := range buckets[bi].backing {
	// 	fmt.Printf("  [%v]%v ", i, n.toString(mapping))
	// }
	// fmt.Printf("\n")

	// for _, n := range buckets[bi].backing {
	// 	fmt.Printf("  %v ", n)
	// }
	// fmt.Printf("\n")
	// fmt.Println(buckets[bi].toString(nil))

	// Insert new node
	// buckets[bi].backing = append(buckets[bi].backing, Node{element, buckets[bi].backing[newNode].next})
	// buckets[bi].backing[newNode].next = len(buckets[bi].backing) - 1
	// buckets[bi].size++
	// (*nToBucket)[element] = bi

	// fmt.Printf("After insertion:   ")
	// fmt.Printf("    First Index: %v --> ", buckets[bi].first)
	// for i, n := range buckets[bi].backing {
	// 	fmt.Printf("  [%v]%v ", i, n.toString(mapping))
	// }
	// fmt.Printf("\n")

}

func mix(buckets Buckets, origNumbers []int, numberMapping map[int]int, nToBucket *map[int]int) Buckets {

	for _, nn := range origNumbers {
		bi := (*nToBucket)[nn]
		//i := buckets[bi].Index(nn)
		//nextBi := findBucket(buckets, i)
		offset := numberMapping[nn]
		if offset < 0 {
			tmp := (-offset) % (len(origNumbers) - 1)
			offset = len(origNumbers) - tmp - 1
		}
		offset = offset % (len(origNumbers) - 1)

		//fmt.Printf("    %v (%v): bucket: %v, offset: %v\n", nn, numberMapping[nn], bi, offset)

		//fmt.Printf("%v, offset: %v:\n", numberMapping[nn], offset)

		repositionNode(buckets, bi, offset, nn, nToBucket, numberMapping)

		// for _, b := range buckets {
		// 	fmt.Printf("[%v] -> ", b.toString(numberMapping))
		// }
		// fmt.Printf("\n")
		// fmt.Printf("\n")

		//break
	}

	return buckets
}

func getSolution(buckets Buckets, num0 int, numberMapping map[int]int, nToBucket map[int]int, numberCount int) int {
	// i := numbers.Index(num0)
	// numbers.RotateLeft(i)
	// numbers.RotateLeft(1000)
	// nn := numberMapping[numbers.backing[numbers.start].v]
	// numbers.RotateLeft(1000)
	// nn += numberMapping[numbers.backing[numbers.start].v]
	// numbers.RotateLeft(1000)
	// nn += numberMapping[numbers.backing[numbers.start].v]

	_, _, n0, b0 := getOffsetNode(buckets, nToBucket[num0], 1000%numberCount, num0, nil, numberMapping, false)
	_, _, n1, b1 := getOffsetNode(buckets, nToBucket[num0], 2000%numberCount, num0, nil, numberMapping, false)
	_, _, n2, b2 := getOffsetNode(buckets, nToBucket[num0], 3000%numberCount, num0, nil, numberMapping, false)

	v0 := numberMapping[buckets[b0].backing[buckets[b0].backing[n0].next].v]
	v1 := numberMapping[buckets[b1].backing[buckets[b1].backing[n1].next].v]
	v2 := numberMapping[buckets[b2].backing[buckets[b2].backing[n2].next].v]

	fmt.Println(v0, v1, v2)
	return v0 + v1 + v2

	//return numberMapping[buckets[b0].backing[n0].v] + numberMapping[buckets[b1].backing[n1].v] + numberMapping[buckets[b2].backing[n2].v]
}

func main() {

	//defer profile.Start(profile.ProfilePath(".")).Stop()

	//numbers := newLinkedList()
	//numbers2 := newLinkedList()

	bucketSize := 500000
	var buckets Buckets

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

			if i != 0 && i%bucketSize == 0 {
				buckets = append(buckets, newLinkedList(bucketSize))
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
	mapping := numberMapping

	// for _, b := range buckets {
	// 	fmt.Printf("[%v] -> ", b.toString(mapping))
	// }
	// fmt.Printf("\n")
	buckets = mix(buckets, origNumbers, mapping, &nToBucket)

	// for _, b := range buckets {
	// 	fmt.Printf("[%v] -> ", b.toString(mapping))
	// }
	// fmt.Printf("\n")

	fmt.Println(getSolution(buckets, num0, mapping, nToBucket, len(origNumbers)))

	return
	// for i := 0; i < 10; i++ {
	//  numbers2 = mix(numbers2, origNumbers, numberMapping2)
	// }
	// fmt.Println(getSolution(numbers2, num0, numberMapping2))
}
