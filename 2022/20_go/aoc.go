package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

type AOC struct {
	text   string
	lines  []string
	groups [][]string
}

func (aoc *AOC) loadFile() bool {

	file, err := os.Open("input.txt")
	if err != nil {
		fmt.Println(err)
		return false
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		aoc.lines = append(aoc.lines, scanner.Text())
		aoc.text += scanner.Text()
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
		return false
	}

	return true
}

func (aoc *AOC) GetLines() []string {
	return aoc.lines
}

// Groups are defined by empty lines in between them. Empty lines are discarted in the process!
func (aoc *AOC) parseGroups() {
	groupStart := 0
	for i, l := range aoc.lines {
		if l == "" {
			aoc.groups = append(aoc.groups, aoc.lines[groupStart:i])
			groupStart = i + 1
		} else if i == len(aoc.lines)-1 {
			aoc.groups = append(aoc.groups, aoc.lines[groupStart:])
			groupStart = i + 1
		}
	}
}

func (aoc *AOC) GetGroups() [][]string {
	aoc.parseGroups()
	return aoc.groups
}

func (aoc *AOC) Ints() []int {
	re, err := regexp.Compile(`[-]?\d[\d]*`)
	if err != nil {
		fmt.Println(err)
		return nil
	}
	s := re.FindAllString(aoc.text, -1)
	ints := make([]int, 0, len(s))
	for _, tmp := range s {
		var conv int
		conv, err = strconv.Atoi(tmp)
		if err != nil {
			fmt.Println(err)
			return nil
		}
		ints = append(ints, conv)
	}
	return ints
}

func Chars(group []string) []byte {
	var chars []byte
	for _, s := range group {
		re, err := regexp.Compile(`[[:alpha:]]`)
		if err != nil {
			fmt.Println(err)
			return nil
		}

		//chars = append(chars, re.FindAllString(s, -1)...)
		for _, c := range re.FindAllString(s, -1) {
			chars = append(chars, byte(c[0]))
		}
	}
	return chars
}

// Parses single chars from the input. Only characters A..Z are recognized!
func (aoc *AOC) GetChars() []byte {
	return Chars([]string{aoc.text})
}

func InitAOC() (AOC, bool) {
	var aoc AOC

	if !aoc.loadFile() {
		return aoc, false
	}

	return aoc, true
}
