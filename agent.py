import copy
import time
import math

row = 16
col = 16
total_pawns = 19

utility_W = {"north": 1, "west": 1, "north_west": 2, "south": -1, "east": -1, "south_east": -2, "north_east": -1,
             "south_west": -1}
utility_B = {"south": 1, "east": 1, "south_east": 2, "north": -1, "west": -1, "north_west": -2, "north_east": -1,
             "south_west": -1}

possible_moves_W = {"north", "west", "north_west", "south", "east", "south_east", "north_east", "south_west"}
possible_moves_B = {"south", "east", "south_east", "north", "west", "north_west", "north_east", "south_west"}

jump_possible_actions = {"north", "west", "south", "east", "north_west", "north_east", "south_west", "south_east"}

top_left_camp = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2),
                 (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1))
bottom_right_camp = ((15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (14, 15), (14, 14), (14, 13), (14, 12), (14, 11),
                     (13, 15), (13, 14), (13, 13), (13, 12), (12, 15), (12, 14), (12, 13), (11, 15), (11, 14))


class Node:
    dummy = set()
    possible_jumps = {}
    paths = []
    actions = {"north": "jump_north", "east": "jump_east", "south": "jump_south", "west": "jump_west",
               "north_east": "jump_north_east", "north_west": "jump_north_west", "south_east": "jump_south_east",
               "south_west": "jump_south_west"}

    # constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self.x) + "," + str(self.y)

    def __eq__(self, other):
        if other is not None:
            return str(self.x) == str(other.x) and str(self.y) == str(other.y)
        return True

    def __ne__(self, other):
        if other is not None:
            return str(self.x) != str(other.x) or str(self.y) != str(other.y)
        return True

    def __cmp__(self, other):
        return str(self.x) == str(other.x) and str(self.y) == str(other.y)

    def __hash__(self):
        return (hash(self.x)) + (2 * hash(self.y))

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    # is_valid_location checks if a particular location is within the search space
    def is_valid_move(self, i, j, state):
        if 0 <= i < int(row) and 0 <= j < int(col) and state.game_board[i][j] == '.':
            return True
        return False

    def jump_east(self, state, flag):
        if self.is_valid_move(self.x, self.y + 2, state) and state.game_board[self.x][self.y + 1] != '.':
            return Node(self.x, self.y + 2), True
        elif self.is_valid_move(self.x, self.y + 1, state) and state.game_board[self.x][self.y + 1] == '.' and \
                not flag:
            return Node(self.x, self.y + 1), False
        return None, False

    def jump_west(self, state, flag):
        if self.is_valid_move(self.x, self.y - 2, state) and state.game_board[self.x][self.y - 1] != '.':
            return Node(self.x, self.y - 2), True
        elif self.is_valid_move(self.x, self.y - 1, state) and state.game_board[self.x][self.y - 1] == '.' and \
                not flag:
            return Node(self.x, self.y - 1), False
        return None, False

    def jump_north(self, state, flag):
        if self.is_valid_move(self.x - 2, self.y, state) and state.game_board[self.x - 1][self.y] != '.':
            return Node(self.x - 2, self.y), True
        elif self.is_valid_move(self.x - 1, self.y, state) and state.game_board[self.x - 1][self.y] == '.' and \
                not flag:
            return Node(self.x - 1, self.y), False
        return None, False

    def jump_south(self, state, flag):
        if self.is_valid_move(self.x + 2, self.y, state) and state.game_board[self.x + 1][self.y] != '.':
            return Node(self.x + 2, self.y), True
        elif self.is_valid_move(self.x + 1, self.y, state) and state.game_board[self.x + 1][self.y] == '.' and \
                not flag:
            return Node(self.x + 1, self.y), False
        return None, False

    def jump_north_east(self, state, flag):
        if self.is_valid_move(self.x - 2, self.y + 2, state) and state.game_board[self.x - 1][self.y + 1] != '.':
            return Node(self.x - 2, self.y + 2), True
        elif self.is_valid_move(self.x - 1, self.y + 1, state) and state.game_board[self.x - 1][self.y + 1] == '.' and \
                not flag:
            return Node(self.x - 1, self.y + 1), False
        return None, False

    def jump_south_east(self, state, flag):
        if self.is_valid_move(self.x + 2, self.y + 2, state) and state.game_board[self.x + 1][self.y + 1] != '.':
            return Node(self.x + 2, self.y + 2), True
        elif self.is_valid_move(self.x + 1, self.y + 1, state) and state.game_board[self.x + 1][self.y + 1] == '.' and \
                not flag:
            return Node(self.x + 1, self.y + 1), False
        return None, False

    def jump_north_west(self, state, flag):
        if self.is_valid_move(self.x - 2, self.y - 2, state) and state.game_board[self.x - 1][self.y - 1] != '.':
            return Node(self.x - 2, self.y - 2), True
        elif self.is_valid_move(self.x - 1, self.y - 1, state) and state.game_board[self.x - 1][self.y - 1] == '.' and \
                not flag:
            return Node(self.x - 1, self.y - 1), False
        return None, False

    def jump_south_west(self, state, flag):
        if self.is_valid_move(self.x + 2, self.y - 2, state) and state.game_board[self.x + 1][self.y - 1] != '.':
            return Node(self.x + 2, self.y - 2), True
        elif self.is_valid_move(self.x + 1, self.y - 1, state) and state.game_board[self.x + 1][self.y - 1] == '.' and \
                not flag:
            return Node(self.x + 1, self.y - 1), False
        return None, False

    # checks if the end location is farther away from the start location
    def further_away(self, start, player):
        if player == 'W':
            return (start.x - self.x > 0 and start.y - self.y > 0) or (
                    start.x - self.x > 0 and start.y - self.y == 0) or (
                           start.y - self.y > 0 and start.x - self.x == 0)
        else:
            return (self.x - start.x > 0 and self.y - start.y > 0) or (self.x - start.x > 0 and self.y - start.y == 0) \
                   or (self.y - start.y > 0 and self.x - start.x == 0)

    # recursive function which computes all possible jumps a pawn can make
    def jump(self, start, state, flag, visited, dummy, utility):
        if state.player == 'W':
            camp = bottom_right_camp
            opposing_camp = top_left_camp
            allowed_moves = possible_moves_W
            utility_values = utility_W
        else:
            camp = top_left_camp
            opposing_camp = bottom_right_camp
            allowed_moves = possible_moves_B
            utility_values = utility_B
        for action in jump_possible_actions:
            func = self.actions.get(action)
            target, flag2 = eval("self." + func + "(state, " + str(flag) + ")")
            if target is not None and target not in dummy:
                target_tuple = (target.x, target.y)
                self_tuple = (start.x, start.y)
                # possible jumps
                if flag2:
                    self.possible_jumps[target] = self
                    dummy.add(target)
                    if target_tuple in camp and self_tuple in camp:
                        if target.further_away(self, state.player):
                            visited[target] = utility + utility_values.get(action) + 2
                    elif target_tuple in opposing_camp and self_tuple in opposing_camp:
                        visited[target] = utility + 2 * utility_values.get(action) + 2
                    elif not ((target_tuple in camp and self_tuple not in camp) or (self_tuple in opposing_camp and
                                                                                    target_tuple not in opposing_camp)):
                        visited[target] = utility + utility_values.get(action) + 2
                        if (target_tuple not in camp and self_tuple in camp) or (
                                self_tuple not in opposing_camp and target_tuple in opposing_camp):
                            visited[target] = visited[target] + 3
                    if target in visited:
                        util = visited[target]
                    else:
                        util = utility + utility_values.get(action) + 2
                    target.jump(start, state, True, visited, dummy, util)
                # possible adjacent moves
                elif action in allowed_moves:
                    dummy.add(target)
                    if target_tuple in camp and self_tuple in camp:
                        if target.further_away(self, state.player):
                            visited[target] = utility + utility_values.get(action)
                    elif target_tuple in opposing_camp and self_tuple in opposing_camp:
                        visited[target] = utility + utility_values.get(action)
                    elif not ((target_tuple in camp and self_tuple not in camp) or (self_tuple in opposing_camp and
                                                                                    target_tuple not in opposing_camp)):
                        visited[target] = utility + utility_values.get(action)
                        if (target_tuple not in camp and self_tuple in camp) or (
                                self_tuple not in opposing_camp and target_tuple in opposing_camp):
                            visited[target] = visited[target] + 3
        return visited, self.possible_jumps

    def print_path(self, target, path):
        route = []
        p = ""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            p = "E " + str(self.y) + "," + str(self.x) + " " + str(target.y) + "," + str(target.x)
        else:
            while target != self:
                route.append(target)
                target = path[target]
            route.append(self)
            route = route[::-1]
            for i in range(1, len(route) - 1):
                fr = route[i - 1]
                to = route[i]
                p = p + "J " + str(fr.y) + "," + str(fr.x) + " " + str(to.y) + "," + str(to.x) + "\n"
            i = len(route) - 1
            fr = route[i - 1]
            to = route[i]
            p = p + "J " + str(fr.y) + "," + str(fr.x) + " " + str(to.y) + "," + str(to.x)
        output_file = open("output.txt", 'w')
        output_file.write(p)
        output_file.close()


class State:

    # constructor
    def __init__(self, game_board, player, time_now, total_time):
        self.game_board = game_board
        self.time_now = time_now
        self.total_time = total_time
        self.player = 'W' if player == 'WHITE' else 'B'
        self.opponent = 'B' if player == 'WHITE' else 'W'
        self.utility = -math.inf

    def __repr__(self):
        st = ""
        for i in range(row):
            for j in range(col):
                st = st + self.game_board[i][j]
            st = st + "\n"
        timepass = time.time()
        tt = time.gmtime(timepass).tm_hour * 3600 + time.gmtime(timepass).tm_min * 60 + time.gmtime(timepass).tm_sec
        st = st + "\n Player:" + self.player + "\n Opponent:" + self.opponent + "\n Total Time:" + self.total_time + \
             "\n Time remaining:" + str(float(self.total_time) + self.time_now - tt) + "Time.time:" + str(tt)
        return st


class AlphaBetaPruning:
    # constructor
    count = 0
    best_start_node = Node(0, 0)
    best_end_node = Node(0, 0)

    def __init__(self, state):
        self.state = state

    # returns the number of pawns in top left camp
    def check_top_left_camp(self, state, pawn_color):
        location = set()
        count = 0
        for i, j in top_left_camp:
            if state.game_board[i][j] == pawn_color:
                location.add(Node(i, j))
                count = count + 1
        return count, location

    # returns the number of pawns in bottom right camp
    def check_bottom_right_camp(self, state, pawn_color):
        location = set()
        count = 0
        for i, j in bottom_right_camp:
            if state.game_board[i][j] == pawn_color:
                location.add(Node(i, j))
                count = count + 1
        return count, location

    def check_game_board(self, state, camp, pawn_color):
        location = set()
        for i in range(row):
            for j in range(col):
                if (i, j) not in camp and state.game_board[i][j] == pawn_color:
                    location.add(Node(i, j))
        return location

    def utility(self, state):
        return state.utility

    def result(self, state, start, end, utility, player):
        st = copy.deepcopy(state)
        temp = st.game_board[start.x][start.y]
        st.game_board[start.x][start.y] = st.game_board[end.x][end.y]
        st.game_board[end.x][end.y] = temp
        st.utility = utility
        st.player = player
        st.opponent = 'W' if player == 'B' else 'B'
        return st

    # checks whether a game has ended
    def terminal_test(self, state, depth, max_depth):
        timepass = time.time()
        tt = time.gmtime(timepass).tm_hour * 3600 + time.gmtime(timepass).tm_min * 60 + time.gmtime(timepass).tm_sec
        st = float(state.total_time) + state.time_now - tt
        count_w, location_w = self.check_top_left_camp(state, 'W')
        count_b, location_b = self.check_bottom_right_camp(state, 'B')
        count_w_self, loc_w = self.check_bottom_right_camp(state, 'W')
        count_b_self, loc_b = self.check_top_left_camp(state, 'B')
        return depth >= max_depth or st <= 0 or count_w == total_pawns or count_b == total_pawns

    def actions(self, state, depth):
        # removing pawns present in the camp
        c = 0
        pawn_with_possible_actions = {}
        dummy2 = {}
        paths = {}
        flag = False
        if state.player == 'W':
            count, location = self.check_bottom_right_camp(state, state.player)
            camp = bottom_right_camp
        else:
            count, location = self.check_top_left_camp(state, state.player)
            camp = top_left_camp
        if location:
            for loc in location:
                pawn_with_possible_actions[loc], paths = loc.jump(loc, state, False, {}, set(), 0)
            for i in pawn_with_possible_actions.keys():
                moves = {}
                for j in pawn_with_possible_actions[i]:
                    x, y = str(j).split(',')
                    if not (int(x), int(y)) in camp:
                        moves[j] = pawn_with_possible_actions[i].get(j)
                dummy2[i] = moves
            if dummy2:
                for i in dummy2.keys():
                    for j in dummy2[i]:
                        if j:
                            pawn_with_possible_actions = dummy2
                            flag = True
            if pawn_with_possible_actions:
                for k in pawn_with_possible_actions.keys():
                    for v in pawn_with_possible_actions[k]:
                        if v:
                            flag = True
                            break
        if not flag:
            pawn_with_possible_actions = {}
            out_of_camp_locations = self.check_game_board(state, camp, state.player)
            for loc in out_of_camp_locations:
                pawn_with_possible_actions[loc], paths = loc.jump(loc, state, False, {}, set(), 0)
        for k in pawn_with_possible_actions.keys():
            if depth % 2 == 0:
                pawn_with_possible_actions2 = sorted(pawn_with_possible_actions[k].items(), key=lambda x: x[1],
                                                     reverse=True)
                pawn_with_possible_actions[k] = pawn_with_possible_actions2
            else:
                pawn_with_possible_actions2 = sorted(pawn_with_possible_actions[k].items(), key=lambda x: x[1])
                pawn_with_possible_actions[k] = pawn_with_possible_actions2
        return pawn_with_possible_actions, paths, flag

    def alpha_beta_pruning(self, state, max_depth):
        v = self.max_value(state, -math.inf, math.inf, 0, max_depth)
        visited, path = self.best_start_node.jump(self.best_start_node, state, False, {}, set(), 0)
        self.best_start_node.print_path(self.best_end_node, path)

    def max_value(self, state, alpha, beta, depth, max_depth):
        if self.terminal_test(state, depth, max_depth):
            return self.utility(state)
        v = -math.inf

        pawn_with_possible_actions, child_parent_dict, flag = self.actions(state, depth)
        for start in pawn_with_possible_actions.keys():
            for end in pawn_with_possible_actions[start]:
                if end[0].further_away(start, state.player):
                    value = self.min_value(self.result(state, start, end[0], end[1], state.opponent), alpha,
                                           beta, depth + 1, max_depth)
                    if depth == 0 and v < value:
                        self.best_start_node = start
                        self.best_end_node = end[0]
                        v = value
                    elif v < value:
                        v = value
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth, max_depth):
        if self.terminal_test(state, depth, max_depth):
            return self.utility(state)
        v = math.inf
        pawn_with_possible_actions, child_parent_dict, flag = self.actions(state, depth)
        for start in pawn_with_possible_actions.keys():
            for end in pawn_with_possible_actions[start]:
                if end[0].further_away(start, state.player):
                    v = min(v, self.max_value(self.result(state, start, end[0], end[1], state.opponent), alpha, beta,
                                              depth + 1, max_depth))
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
        return v


# open the input file to read the input
input_file = open("input.txt")

# SINGLE or GAME
type = input_file.readline().strip()

# color to play with
color = input_file.readline().strip()

# total play time
total_time = input_file.readline().strip()

# search_space stores the elevation values for each site
game_board = [[c for c in line.strip('\n')] for line in input_file.readlines()]

timepass = time.time()
tt = time.gmtime(timepass).tm_hour * 3600 + time.gmtime(timepass).tm_min * 60 + time.gmtime(timepass).tm_sec

s = State(game_board, color, tt, total_time)

al = AlphaBetaPruning(s)

if type == "SINGLE":
    max_depth = 1
else:
    c = 0
    pawns_with_possible_actions, p, f = al.actions(s, 1)
    for i in pawns_with_possible_actions:
        for j in pawns_with_possible_actions[i]:
            c = c + 1

    if float(total_time) > 200:
        if c < 140:
            max_depth = 3
        else:
            max_depth = 2
    else:
        if c < 100:
            max_depth = 3
        else:
            max_depth = 2

al.alpha_beta_pruning(s, max_depth)

input_file.close()
