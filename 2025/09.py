#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *



def edge_length(red_tiles, i, j):
    return max(abs(red_tiles[i][0] - red_tiles[j][0]), abs(red_tiles[i][1] - red_tiles[j][1]))


def plot_numbers(rectangle):

    # Separate x and y coordinates
    x_coords = [p[0][0] for p in original_red_tiles]
    y_coords = [p[0][1] for p in original_red_tiles]

    # Close the polygon by adding the first point at the end
    # x_coords.append(original_red_tiles[0][0])
    # y_coords.append(original_red_tiles[0][1])

    # Plot the polygon
    plt.figure(figsize=(6, 6))
    plt.plot(x_coords, y_coords, marker="o", linestyle="-", color="blue")

    rectangle.sort()
    p1, p2 = rectangle

    rectangle = [p1, (p2[0], p1[1]), p2, (p1[0], p2[1]), p1]

    plt.plot([p[0] for p in rectangle], [p[1] for p in rectangle], marker="o", linestyle="-", color="red")

    # Annotate points with their index
    # for i, (x, y) in enumerate(red_tiles):
    #    plt.text(x, y, f"{i}", fontsize=9, ha="right")

    plt.title("Polygon from Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")  # Keep aspect ratio equal for proper polygon shape

    plt.show()


# plot_code()
# exit(0)


class Corner(Enum):
    INNER_LU = 0
    INNER_RU = 1
    INNER_RD = 2
    INNER_LD = 3
    OUTER_LU = 4
    OUTER_RU = 5
    OUTER_RD = 6
    OUTER_LD = 7


def calc_corner_type(red_tiles, i, p1):
    p0, p2 = red_tiles[(i - 1) % len(red_tiles)], red_tiles[(i + 1) % len(red_tiles)]
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2

    # Direction vectors
    v1x, v1y = x1 - x0, y1 - y0
    v2x, v2y = x2 - x1, y2 - y1

    # Determine turn direction via cross product
    clockwise = v1x * v2y - v1y * v2x > 0
    if clockwise:
        if v1y < 0 and v2x > 0:
            return Corner.OUTER_LU
        if v1x > 0 and v2y > 0:
            return Corner.OUTER_RU
        if v1y > 0 and v2x < 0:
            return Corner.OUTER_RD
        if v1x < 0 and v2y < 0:
            return Corner.OUTER_LD
    else:
        if v2y > 0 and v1x < 0:
            return Corner.INNER_LU
        if v2x > 0 and v1y > 0:
            return Corner.INNER_LD
        if v2y < 0 and v1x > 0:
            return Corner.INNER_RD
        if v2x < 0 and v1y < 0:
            return Corner.INNER_RU


# any neighbor is on the right side of the current point. This might be not sufficient
# because inner corners (that would be valid corner points!) will be ignored.
# But on the first glance, those inner corners might only create smaller/worse rectangles compared to the
# neighbor points on the same column further up/down. If the result is not correct, we might need to look at this.
def valid_start_point(t):
    # return p2[0] > p1[0] or p0[0] > p1[0]
    return t[1] in {Corner.OUTER_LU, Corner.OUTER_LD, Corner.INNER_RU, Corner.INNER_RD}


# could be binary/interpolation search
def get_start_index(red_tiles, p):
    for i, t in enumerate(red_tiles):
        if t[0][0] > p[0]:
            return i


# INNER_LU = 0
# INNER_RU = 1
# INNER_RD = 2
# INNER_LD = 3
# OUTER_LU = 4
# OUTER_RU = 5
# OUTER_RD = 6
# OUTER_LD = 7


def valid_end_corner(corner):
    match corner:
        case Corner.OUTER_LU:
            return {Corner.OUTER_RD, Corner.INNER_RU, Corner.INNER_LU, Corner.INNER_LD}
        case Corner.OUTER_LD:
            return {Corner.OUTER_RU, Corner.INNER_LU, Corner.INNER_LD, Corner.INNER_RD}
        case Corner.INNER_RU | Corner.INNER_RD:
            return {
                Corner.OUTER_RU,
                Corner.OUTER_RD,
                Corner.INNER_LU,
                Corner.INNER_LD,
                Corner.INNER_RU,
                Corner.INNER_RD,
            }


# No horizontal line crosses the rectangle made by p0 and p1
def no_column_crosses_horizontal_line(horizontal_edges, p0, p1):
    min_y, max_y = min(p0[1], p1[1]), max(p0[1], p1[1])
    # Horizontal line is in-between p0 and p1 (Y)
    lines = filter(lambda e: min_y < e[0][1] < max_y, horizontal_edges)
    min_x, max_x = min(p0[0], p1[0]), max(p0[0], p1[0])
    # An endpoint of a horizontal line lies in-between or crosses the rectangle by p0, p1
    lines = filter(lambda e: min(e[0][0], e[1][0]) < min_x < max(e[0][0], e[1][0]), lines)
    return len(list(lines)) == 0


def get_next_point_columns(red_tiles, horizontal_edges, p, corner, start_index):
    x_value = red_tiles[start_index][0][0]
    # All existing points in this column
    initial_column = [t for t in red_tiles[start_index:] if t[0][0] == x_value]
    # print(f"    --> {initial_column}")
    valid_column = [t for t in initial_column if t[1] in valid_end_corner(corner)]
    valid_column.sort(key=lambda t: abs(p[1] - t[0][1]))

    # filter out all points in the column, where the created rectangle would intersect with any horizontal edge!
    valid_column = list(filter(lambda x: no_column_crosses_horizontal_line(horizontal_edges, x[0], p), valid_column))

    if len(valid_column) == 0:
        return [], len(initial_column)
    # For outer points, each column can only have ONE point (the closest one!)
    # For inner points, we sort them by distance and need to adjust boundaries in both directions
    if corner in {Corner.OUTER_LU, Corner.OUTER_LD}:
        return valid_column[:1], len(initial_column)

    # For inner points as start point, we have to look at ALL valid points. But to make sure the boundary
    # logic/constraints still work, we reverse the sorting from furthest away, to closest.
    valid_column.reverse()

    return valid_column, len(initial_column)


def calc_area(t1, t2):
    return (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def part2(red_tiles):
    edges = [(i, (i + 1) % len(red_tiles)) for i in range(len(red_tiles))]
    edges = [(red_tiles[e[0]], red_tiles[e[1]]) for e in edges]

    # filters only horizontal edges
    horizontal_edges = filter(lambda e: e[0][1] == e[1][1], edges)
    # sort all edges by Y value and then by the miniumum X value (leftmost start or end point)
    horizontal_edges = sorted(horizontal_edges, key=lambda e: (e[0][1], min(e[0][0], e[1][0])))
    corners = []

    red_tiles = [(t, calc_corner_type(red_tiles, i, t)) for i, t in enumerate(red_tiles)]

    original_red_tiles = red_tiles.copy()

    start_points = list(filter(valid_start_point, red_tiles))
    start_points.sort()

    red_tiles.sort()

    min_y = min(red_tiles, key=lambda x: x[0][1])[0][1]
    max_y = max(red_tiles, key=lambda x: x[0][1])[0][1]

    max_area = 0
    best_points = []

    for point, corner in start_points:
        index = original_red_tiles.index((point, corner))
        upper_bound = min_y
        lower_bound = max_y

        match corner:
            case Corner.OUTER_LU:
                upper_bound = point[1]
            case Corner.OUTER_LD:
                lower_bound = point[1]
            case Corner.INNER_RD:
                pass
            case Corner.INNER_RU:
                pass
            case _:
                print("ERROR!!! Corner is invalid!")

        valid_point = lambda y: upper_bound <= y <= lower_bound

        start_index = get_start_index(red_tiles, point)

        while start_index < len(red_tiles):
            column, index_incr = get_next_point_columns(red_tiles, horizontal_edges, point, corner, start_index)
            should_stop = False

            for next_point, next_corner in column:
                if upper_bound <= next_point[1] <= lower_bound:
                    area = calc_area(point, next_point)
                    if area > max_area:
                        max_area = area
                        best_points = [point, next_point]

                    # adjust the new boundaries based on corner type
                    match corner:
                        case Corner.OUTER_LU:
                            # Corner.OUTER_RD, Corner.INNER_RU, Corner.INNER_LU, Corner.INNER_LD
                            lower_bound = next_point[1]
                            if next_corner in {Corner.OUTER_RD, Corner.INNER_LD}:
                                should_stop = True
                        case Corner.OUTER_LD:
                            # Corner.OUTER_RU, Corner.INNER_LU, Corner.INNER_LD, Corner.INNER_RD
                            upper_bound = next_point[1]
                            if next_corner in {Corner.OUTER_RU, Corner.INNER_LU}:
                                should_stop = True

                        case Corner.INNER_RD | Corner.INNER_RU:
                            # Corner.OUTER_RU, Corner.OUTER_RD, Corner.INNER_LU, Corner.INNER_LD, Corner.INNER_RU, Corner.INNER_RD
                            if next_point[1] > point[1]:
                                lower_bound = next_point[1]
                            else:
                                upper_bound = next_point[1]

                            tmp_i = original_red_tiles.index((next_point, next_corner))
                            tmp_next_point_y = original_red_tiles[(tmp_i + 1) % len(original_red_tiles)][0][1]
                            tmp_i = original_red_tiles.index((next_point, next_corner))
                            tmp_prev_point_y = original_red_tiles[(tmp_i - 1) % len(original_red_tiles)][0][1]

                            if next_corner == Corner.OUTER_RU:
                                upper_bound = tmp_next_point_y
                            if next_corner == Corner.OUTER_RD:
                                lower_bound = tmp_prev_point_y
                            # if any neighbor of next_point is lower AND another is higher than point.y, we cancel!
                            if (
                                tmp_next_point_y <= point[1] <= tmp_prev_point_y
                                or tmp_prev_point_y <= point[1] <= tmp_next_point_y
                            ):
                                should_stop = True

            if should_stop:
                break

            start_index += index_incr

    return max_area

def part1(rt):
    dists = {(i,j): manhatten_dist(t1, t2) for i,t1 in enumerate(rt) for j,t2 in enumerate(rt) if j>i}
    max_area = 0
    for (t1, t2), d in dists.items():
        max_area = max(max_area, (abs(rt[t1][0]-rt[t2][0])+1) * (abs(rt[t1][1]-rt[t2][1])+1))
    return max_area


def main():

    red_tiles = lmap(ints, open_data("09.data"))

    print(part1(red_tiles))
    print(part2(red_tiles))


if __name__ == "__main__":
    main()

# year 2025
# solution for 09.01: 4759930955
# solution for 09.02: 1525241870
