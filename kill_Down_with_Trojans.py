import numpy as np
import scipy


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values, i, j, protection, multiplier):
    # TODO
    # Placeholder function - implement your logic here
    # Your code to check whether it is possible to reach the bottom-right
    # corner without running out of HP should go here.
    # You should use dynamic programming to solve the problem.
    # Return True if possible, False otherwise.

    # By default we return False
    # TODO you should change this
    if i >= n:   # check if past row limit
        return False
    if j >= n:   # check if past column limit
        return False
    if (H <= 0) and not (i == n-1 and j == n-1):    # check if Hp is 0 and not reach final tile
        return False
    if i == n-1 and j == n-1 and H >= 0:             # if reaches bottom-right tile with Hp left 
        return True
    if tile_types[i][j] == 0:   # check if damage tile
        if protection == True:  # Use protection if available
            opt_1 = DP(n, H, tile_types, tile_values, i+1, j, False, multiplier)  # go down, use protection
            opt_2 = DP(n, H, tile_types, tile_values, i, j+1, False, multiplier)  # go right, use protection
            opt_3 = DP(n, H - tile_values[i][j], tile_types, tile_values, i, j+1, protection, multiplier)  # go down, don't use protection
            opt_4 = DP(n, H - tile_values[i][j], tile_types, tile_values, i, j+1, protection, multiplier)  # go right, don't use protection
            res = opt_1 or opt_2 or opt_3 or opt_4
            return res
        else:  # Deal damage
            opt_1 = DP(n, H - tile_values[i][j], tile_types, tile_values, i+1, j, protection, multiplier)  # go down
            opt_2 = DP(n, H - tile_values[i][j], tile_types, tile_values, i, j+1, protection, multiplier)  # go right
    elif tile_types[i][j] == 1: # Check if healing tile
        if multiplier == True:  # Use multiplier if possible
            opt_1 = DP(n, H + 2*tile_values[i][j], tile_types, tile_values, i+1, j, protection, False)  # go down, use multiplier
            opt_2 = DP(n, H + 2*tile_values[i][j], tile_types, tile_values, i, j+1, protection, False)  # go right, use multiplier
            opt_3 = DP(n, H + tile_values[i][j], tile_types, tile_values, i+1, j, protection, multiplier)  # go down, don't use multiplier
            opt_4 = DP(n, H + tile_values[i][j], tile_types, tile_values, i, j+1, protection, multiplier)  # go right, don't use multiplier
            res = opt_1 or opt_2 or opt_3 or opt_4
            return res
        else:  # Heal Hp
            opt_1 = DP(n, H + tile_values[i][j], tile_types, tile_values, i+1, j, protection, multiplier)  # go down
            opt_2 = DP(n, H + tile_values[i][j], tile_types, tile_values, i, j+1, protection, multiplier)  # go right
    elif tile_types[i][j] == 2:
        opt_1 = DP(n, H, tile_types, tile_values, i+1, j, True, multiplier)  # go down
        opt_2 = DP(n, H, tile_types, tile_values, i, j+1, True, multiplier)  # go right
    elif tile_types[i][j] == 3:
        opt_1 = DP(n, H, tile_types, tile_values, i+1, j, protection, True)  # go down
        opt_2 = DP(n, H, tile_types, tile_values, i, j+1, protection, True)  # go right
    res = opt_1 or opt_2
    return res


def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values, 0, 0, False, False)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
