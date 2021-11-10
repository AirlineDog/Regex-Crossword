import sre_yield
import sys
import string


def find_max_letters(res):
    """ Return the maximum number of letters of a word in the crossword """
    max_letters = 0
    for i in range(len(res)):
        if max_letters < len(res[i]):
            max_letters = len(res[i])
    return max_letters


def find_min_letters(res):
    """ Return the minimum number of letters of a word in the crossword """
    min_letters = len(res[0])
    for i in range(1, len(res)):
        if min_letters > len(res[i]):
            min_letters = len(res[i])
    return min_letters


def find_next_word(res):
    """ Return next word to find based in percentage of letters filled """
    max_score = -1
    returning_word_number = -1
    # possible words to search
    numbers = []
    for i in range(len(res)):
        if not (isinstance(res[i], str)):  # when word is found res[i] will be a string
            numbers.append(i)

    for i in numbers:
        known = 0  # number of known letters
        unknown = 0  # number of unknown letters
        for letter in res[i]:
            if letter == ".":
                unknown += 1
            else:
                known += 1
        if unknown == 0:
            returning_word_number = i
            break
        percentage = known / unknown  # known letters percentage
        if max_score < percentage:
            max_score = percentage
            returning_word_number = i
    return returning_word_number


def update_cross():
    """ Update crossword csv input to show letters in intersections"""
    # Save who is connected with who and where (Adjacency lists)
    connection_words = []  # words connected [[word number, connections+++],[word number, connections+++]]
    connection_places = []  # place of connection [[word number, places+++],[word number, places+++]]
    for x in range(len(crossword)):  # for every word
        temp_words = [crossword[x][0]]  # First element the word's number
        temp_places = [crossword[x][0]]  # First element the word's number
        for i in range(2, len(crossword[x]), 2):
            temp_words.append(int(crossword[x][i]))  # Add connected words
            temp_places.append(int(crossword[x][i + 1]))  # Add place of connection
        connection_words.append(temp_words)
        connection_places.append(temp_places)

    for j in range(len(connection_words)):  # for every word with connections
        all_connections = connection_words[j]  # word's connections list
        for y in range(1, len(all_connections)):  # for every word which is connected with
            connection = all_connections[y]  # connected word
            for x in range(2, len(crossword[connection]), 2):  # connection place in csv
                if all_connections[0] == int(crossword[connection][x]):  # if they are connected fill the letters
                    # new strings for known letters
                    if crossword[all_connections[0]][1][int(crossword[connection][x + 1])] != ".":
                        crossword[connection][1] = \
                            crossword[connection][1][:(connection_places[j][y])] + \
                            crossword[all_connections[0]][1][int(crossword[connection][x + 1])] + \
                            crossword[connection][1][(connection_places[j][y] + 1):]
                    elif crossword[connection][1][connection_places[j][y]] != ".":
                        crossword[all_connections[0]][1] = \
                            crossword[all_connections[0]][1][:(int(crossword[connection][x + 1]))] + \
                            crossword[connection][1][connection_places[j][y]] + \
                            crossword[all_connections[0]][1][(int(crossword[connection][x + 1]) + 1):]


def update_result():
    """ Update results list"""
    # Find who is connected with who and where (Adjacency lists)
    connected_words = []  # words connected [[word_number, connections+++],[word, connections+++]]
    connection_places = []  # place of connection [[word_number, places+++],[word, places+++]]
    for x in range(len(result)):  # for every word
        word = result[x]
        # if word is completed
        is_full = isinstance(word, str)  # if word not complete -> ['.','.','A','.']
        if is_full:
            temp_words = [crossword[x][0]]  # First element is the word's number
            temp_places = [crossword[x][0]]  # First element is the word's number
            for i in range(2, len(crossword[x]), 2):
                temp_words.append(int(crossword[x][i]))  # Add connected words
                temp_places.append(int(crossword[x][i + 1]))  # Add place of connection
            connected_words.append(temp_words)
            connection_places.append(temp_places)

    for j in range(len(connected_words)):  # for every word with letters known
        for line in crossword:  # for every other word
            for x in range(2, len(line), 2):  # Adjacency list
                if connected_words[j][0] == int(line[x]):  # if they are connected fill the letters
                    for i in range(1, len(connected_words[j])):
                        if connected_words[j][i] == line[0] and \
                                not (isinstance(result[connected_words[j][i]], str)):
                            result[connected_words[j][i]][connection_places[j][i]] = \
                                result[int(line[x])][int(line[x + 1])]


def match_words(next_word, res, words):
    """ Find best matches for a specific word """
    best_score = -1
    for word in words:  # Every regex list
        if all(word[0] != previous_regs[x] for x in range(len(previous_regs))):  # not a previous regex
            for i in range(1, len(word)):  # first element is the origin regex
                if len(word[i]) == len(res[next_word]):  # same length
                    score = 0
                    for j in range(len(word[i])):
                        if word[i][j] == res[next_word][j]:  # letter == known letter
                            score += 1
                        elif res[next_word][j] != ".":  # different letters
                            score = -2  # abort
                            break
                    if score > best_score:
                        best_score = score
                        possible_words[next_word] = [word[0], word[i]]  # [origin regex, word]
                    elif score == best_score:
                        possible_words[next_word].append(word[0])
                        possible_words[next_word].append(word[i])


def reset_state():
    """ Reset crossword to it's previous state """
    # place of the word in the possible_words[word] list
    place = len(possible_words[previous_words[- 1]]) - 1 - possible_words[previous_words[- 1]][::-1].index(
        result[previous_words[- 1]])
    previous_regs.pop()  # Don't compare last regex
    possible_words[previous_words[-1]].pop()  # pop word
    possible_words[previous_words[-1]].pop()  # pop word's origin regex
    # see if there is a different potential match for the same word
    no_diff = True
    for i in range(place - 3, -1, -2):
        if all(possible_words[previous_words[- 1]][i] != previous_regs[x] for x in range(len(previous_regs))):
            result[previous_words[-1]] = possible_words[previous_words[-1]][i + 1]
            previous_regs.append(possible_words[previous_words[-1]][i])
            no_diff = False
            update_result()
            break
    # if not, delete the word and it's connections and change the previous_words one
    if no_diff:
        # delete word
        temp_word = []
        for i in range(len(result[previous_words[- 1]])):
            temp_word.append(".")
        result[previous_words[- 1]] = temp_word
        # delete connected words
        connections = []
        for i in range(2, len(crossword[previous_words[-1]]), 2):
            if not (isinstance(result[int(crossword[previous_words[-1]][i])], str)):
                connections.append(int(crossword[previous_words[-1]][i]))
        for i in connections:
            temp_word = []
            for j in range(len(result[i])):
                temp_word.append(".")
            result[i] = temp_word
        previous_words.pop()  # delete word from previous_words tries
        reset_state()  # change the previous_words word


# read crossword csv file line by line
crossword = []
with open(sys.argv[1], "r") as csv:
    crossword = csv.read().splitlines()

# split every element
crossword = [i.split(",") for i in crossword]

# sort based on first element
for i in range(len(crossword)):
    crossword[i][0] = int(crossword[i][0])
crossword = sorted(crossword)

# Fill known letters
update_cross()

# read regex txt file line by line
regex_list = []
with open(sys.argv[2], "r") as txt:
    regex_list = txt.read().splitlines()

# all words that can be generated from regular expressions 
all_words = []
for i in range(len(regex_list)):
    all_words.append(list(sre_yield.AllStrings(regex_list[i], max_count=5, charset=string.ascii_uppercase)))

# Final result words list initialized based on csv file
result = []
for i in range(len(crossword)):
    result.append([x for x in crossword[i][1]])

# Keep words that are not too big or too small to fit the crossword
max_letters = find_max_letters(result)
min_letters = find_min_letters(result)
in_range_words = []
for i in range(len(all_words)):
    temp_words = []
    for j in range(len(all_words[i])):
        if max_letters >= len(all_words[i][j]) >= min_letters:
            temp_words.append(all_words[i][j])
    in_range_words.append(temp_words)

# Keep non duplicate generated words
words = []  # [origin regex, words+++]
for i in range(len(in_range_words)):
    regs = in_range_words[i]
    temp_line = []
    for word in regs:
        if word not in temp_line:
            temp_line.append(word)
    temp_line.insert(0, regex_list[i])
    words.append(temp_line)

possible_words = [[] for x in range(len(result))]  # List of lists with possible words
previous_words = []  # List with previous words tried
previous_regs = []  # List with previous regex tried
while len(previous_words) < len(result):  # until the results list is full
    next_word = find_next_word(result)  # next word to search
    match_words(next_word, result, words)  # find potential matches
    if len(possible_words[next_word]) >= 2:  # if there is at least one potential match
        no_different_word = True  # see if there is a fitting word
        # !!! possible_words[i] -> [origin regex, word, origin regex, word,+++]
        for i in range(int(len(possible_words[next_word]) / 2)):
            # if all patterns are different from the previous ones
            if all(possible_words[next_word][-2 + -2 * i] != previous_regs[x] for x in range(len(previous_regs))):
                previous_words.append(next_word)
                previous_regs.append(possible_words[next_word][-2 + -2 * i])
                result[next_word] = possible_words[next_word][-1 + -2 * i]
                no_different_word = False
                update_result()
                break
        if no_different_word:
            reset_state()
    else:
        reset_state()

# print final result
final = []
for i in range(len(previous_words)):
    final.append([previous_words[i], previous_regs[i], result[previous_words[i]]])

final = sorted(final)

for line in final:
    print(line[0], " ", line[1], " ", line[2])
