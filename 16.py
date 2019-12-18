from itertools import repeat, chain, islice
import math
import numpy as np

def create_pattern(signal, pattern, i):
    r = math.ceil(len(signal)/(len(pattern)-1))
    ll = [[p]*(i+1) for p in pattern]
    l = list(chain(*ll))
    return list(chain.from_iterable(repeat(l, r)))[1:]

def phase(signal, pattern):

    out = []
    for i,e in enumerate(signal):
        p = create_pattern(signal, pattern, i)
        v = 0
        for i2,e2 in enumerate(signal):
            v += int(e2) * p[i2%len(p)]
        out.append(str(v)[-1])
    return "".join(out)


def phase2(signal):

    signal_int = list(map(int, signal))
    out = []
    for i,_ in enumerate(signal):
        # until one of the [0, 1, 0, -1] are used.
        # The first one -1.

        #print("i: {}".format(i))

        v = 0
        # count
        offset = 0
        while offset < len(signal_int):
            c = i+1
            v += sum(signal_int[c-1+offset:2*c-1+offset]) - sum(signal_int[3*c-1+offset:4*c-1+offset])
            offset += 4*c

        out.append(str(v)[-1])

    return "".join(out)

def create_pattern2(length, pattern, i):
    r = math.ceil(length/(len(pattern)-1))
    ll = [[p]*(i+1) for p in pattern]
    l = list(chain(*ll))

    c = chain.from_iterable(repeat(l, r))
    next(c)

    return list(islice(c, length))

def phase3(signal, matrix):

    signal_int = list(map(int, signal))
    v_out = np.matmul(matrix, signal_int)
    return "".join((map(lambda x: str(x)[-1], v_out)))


if __name__ == "__main__":

    signal = "59777373021222668798567802133413782890274127408951008331683345339720122013163879481781852674593848286028433137581106040070180511336025315315369547131580038526194150218831127263644386363628622199185841104247623145887820143701071873153011065972442452025467973447978624444986367369085768018787980626750934504101482547056919570684842729787289242525006400060674651940042434098846610282467529145541099887483212980780487291529289272553959088376601234595002785156490486989001949079476624795253075315137318482050376680864528864825100553140541159684922903401852101186028076448661695003394491692419964366860565639600430440581147085634507417621986668549233797848"
    signal = "12345678"
    #signal = "80871224585914546619083218645595"
    #signal = "19617804207202209144916044189917"
    pattern = [0, 1, 0, -1]

    signal = signal * 2

    #matrix = []
    #for i in range(len(signal)):
    #    matrix.append(create_pattern2(len(signal), [0,1,0,-1], i)[:len(signal)])

    for i in range(4):
        #signal = phase3(signal, matrix)
        signal = phase2(signal)
    print(signal)
