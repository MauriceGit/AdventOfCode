from itertools import repeat, chain, islice, accumulate
import math

def phase2(signal_int):

    out = []
    for i,_ in enumerate(signal_int):
        v = 0
        # count
        offset = 0
        while offset < len(signal_int):
            c = i+1
            v += sum(signal_int[c-1+offset:2*c-1+offset]) - sum(signal_int[3*c-1+offset:4*c-1+offset])
            offset += 4*c

        out.append(abs(v)%10)

    return out

# Used to visualize the pattern and find shortcuts
def create_pattern2(length, pattern, i):
    r = math.ceil(length/(len(pattern)-1))
    ll = [[p]*(i+1) for p in pattern]
    l = list(chain(*ll))

    c = chain.from_iterable(repeat(l, r))
    next(c)

    return list(islice(c, length))

# pretty-print the output of create_pattern2
def pp_list(l):
    return list(map(lambda x: "{0: <2}".format(x), l))

def phase3(signal, n):

    # Found this trick of reversing the list on Reddit.
    # After reversing, we can just calculate the accumulate (didn't know about this function too...) with the lambda
    # and use it next time again. Turns out, this turns hours into seconds.
    s1 = reversed(signal[:])
    for _ in range(n):
        s1 = list(accumulate(s1, lambda x,y: (x+y)%10))

    # This was my solution before (At least after some initial peeking at hints...)
    # Turns out, it is WAY too slow. Damn, because it would actually give the correct solution as well...
    #s1 = signal[:]
    #s2 = signal[:]
    #l = len(signal)
    #r = range(l)
    #for _ in range(n):
    #    for i in r:
    #        s2[i] = sum(s1[i:])%10
    #    s1, s2 = s2, s1

    return list(reversed(s1))

if __name__ == "__main__":

    signal = "59777373021222668798567802133413782890274127408951008331683345339720122013163879481781852674593848286028433137581106040070180511336025315315369547131580038526194150218831127263644386363628622199185841104247623145887820143701071873153011065972442452025467973447978624444986367369085768018787980626750934504101482547056919570684842729787289242525006400060674651940042434098846610282467529145541099887483212980780487291529289272553959088376601234595002785156490486989001949079476624795253075315137318482050376680864528864825100553140541159684922903401852101186028076448661695003394491692419964366860565639600430440581147085634507417621986668549233797848"
    #signal = "12345678"
    #signal = "80871224585914546619083218645595"
    #signal = "19617804207202209144916044189917"

    # solution for puzzle 1:
    s = list(map(int, signal[:]))
    for i in range(100):
        s = phase2(s)
    print("".join(list(map(lambda x: str(x), s[:8]))))

    # solution for puzzle 2:
    signal = signal * 10000
    signal = signal[5977737:]
    out = phase3(list(map(int, signal)), 100)[:8]
    print("".join(list(map(lambda x: str(x), out))))

# solution for 16.01: 53296082
# solution for 16.02: 43310035

