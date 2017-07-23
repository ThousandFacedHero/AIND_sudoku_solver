assignments = []
import time


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    twin_list = []
    return_dict = values
    for key, value in values.items():
        if len(value) == 2:
            # now check all peers for twins
            for pvalue in peers[key]:
                # see if values[pvalue] contains the exact same digits as value
                if len(return_dict[pvalue]) == 2:
                    # make sure we haven't already processed the twins
                    if [pvalue, key] not in twin_list:
                        if (value[0] in return_dict[pvalue]) & (value[1] in return_dict[pvalue]):
                            # add the new twin pair to the list so we don't iterate over the common peers again
                            twin_list.append([pvalue, key])
                            twin_list.append([key, pvalue])
                            # now eliminate the digits from all other in-common peers
                            common_peers = {x for x in peers[key] if x in peers[pvalue]}
                            for val in common_peers:
                                if val != pvalue:
                                    if len(return_dict[val]) >= 2:
                                        if value[0] in return_dict[val]:
                                            return_dict[val] = return_dict[val].replace(value[0], '')
                                        if value[1] in return_dict[val]:
                                            return_dict[val] = return_dict[val].replace(value[1], '')
    return return_dict


def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in a for t in b]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return_dict = {boxes[i]: (x if x != '.' else cols) for i, x in enumerate(grid)}
    return return_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):

    return_dict = values
    for key, value in values.items():
        if len(value) == 1:
            # now remove number from all peers
            for pvalue in peers[key]:
                return_dict[pvalue] = return_dict[pvalue].replace(value, '')

    return return_dict


def only_choice(values):

    for unit in unitlist:
        for digit in cols:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit

    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):

    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    """ This section will handle solving puzzles that are not diagonals
    if solution != False:
        return solution
    else:
        # failed on diagonal, try to solve without them.
        global unitlist
        global units
        global peers
        unitlist = row_units + column_units + square_units
        units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
        peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)
        values = grid_values(grid)
        solution = search(values)
        if solution != False:
            return solution
        else:
            # print('Failed to find a solution.')
            return False
            """
    return solution

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# Add diagonal units
diag_unit1 = [rows[i] + cols[i] for i in range(len(rows))]
diag_unit2 = [rows[-i - 1] + cols[i] for i in range(len(rows))]
unitlist = row_units + column_units + square_units + [diag_unit1, diag_unit2]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)


if __name__ == '__main__':

    start_time = time.time()
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    # diag_sudoku_grid = '...85...41927.....4......6...3..........8..........1...4......7.....15282...98...'
    # diag_sudoku_grid ='...6..5...6....19.9.8.......123......8.4.9.7......241.......7.9.43....2...5..6...'
    # diag_sudoku_grid = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
    # diag_sudoku_grid = '1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3..'
    # diag_sudoku_grid = '...7.9....85...31.2......7...........1..7.6......8...7.7.........3......85.......'

    # Get the solution
    display(solve(diag_sudoku_grid))
    """ Runtime and better error reporting
    result = solve(diag_sudoku_grid)
    if result != False:
        print('Runtime: ', time.time() - start_time, '\n')
        display(result)
    else:
        print('Failed to find a solution.')
        """

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
