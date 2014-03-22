hand_names = ['High Card','Pair','2 pair',
              '3 of a kind','Straight','Flush',
              'Full House','4 of a kind','Straight Flush']

# Function hand percentages
# Prints probability for possible hands in poker game
def hand_percentages(n):
    "Sample n random hands and print a table of percentages for each type of hand"
    counts = [0]*9
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print "%14s: %7.2f %%" % (hand_names[i], 100.*counts[i]/n)

# Write a function, deal(numhands, n=5, deck), that 
# deals numhands hands with n cards each.
#
import random # this will be a useful library for shuffling

# This builds a deck of 52 cards. 
mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 

def deal(numhands, n=5, deck=mydeck):
    random.shuffle(deck)
    hands = [deck[n*i:n*(1+i)] for i in range(numhands)]
    return hands
    
# allmax(iterable, key=None) returns
# a list of all items equal to the max of the iterable, 
# according to the function specified by key. 
def poker(hands):
    # Example of hands: [['6C', '7C', '8C', '9C', 'TC'], ['6D', '7D', '8D', '9D', 'TD'], 
    # ['9D', '9H', '9S', '9C', '7D'], ['TD', 'TC', 'TH', '7C', '7D']]
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result

# There is a newer implementation of hand_rank
hand_rank_old = """ hand_rank old
def hand_rank(hand):
    "Return a value indicating the ranking of a hand in a tuple."
    ranks = card_ranks(hand) 
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)
"""

def hand_rank(hand):
    "Return a value indicating the ranking of a hand in a tuple."
    # counts is the count of each rank; rank lists corresponding ranks
    # e.g. '7 T 7 9 7' => counts = (3,1,1); ranks = (7,10,9)
    groups = group(card_ranks(hand))
    counts, ranks = unzip(groups)
    return (9 if (5,) == counts else # 5 of a kind -> 4 of a kind plus joker
            8 if straight(ranks) and flush(hand) else
            7 if (4,1) == counts else
            6 if (3,2) == counts else
            5 if flush(hand) else
            4 if straight(ranks) else
            3 if (3,1,1) == counts else
            2 if (2,2,1) == counts else
            1 if (2,1,1,1) == counts else
            0), ranks

def group(items):
    # items is the card ranks -> [6, 7, 8, 9, 10]
    # Returns a list of [(count,x)...] highest count first, then highest x first."
    # Example:
    # If the input is [6,7,8,9,10], the output is [(1, 10), (1, 9), (1, 8), (1, 7), (1, 6)]
    # If the input is [10, 10, 10, 7, 7], the output is [(3, 10), (2, 7)]
    groups = [(items.count(x),x) for x in set(items)]
    return sorted(groups, reverse=True)

def unzip(pairs):
    # Example:
    # input:  [(1, 10), (1, 9), (1, 8), (1, 7), (1, 6)]
    # output:  [(1, 1, 1, 1, 1), (10, 9, 8, 7, 6)]
    # input: [(3, 10), (2, 7)]
    # output: [(3, 2), (10, 7)]
    return zip(*pairs)

# Input is a hand of cards, that is a list
# of pair rank and suit string, example: ['AC', '3D', '4S', 'KH']
# Output is the numeric rank of cards sorted descending
# example: ['AC', '3D', '4S', 'KH'] should output [14, 13, 4, 3]
def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r,s in cards]
    ranks.sort(reverse=True)    
    return [5,4,3,2,1] if (ranks == [14,5,4,3,2]) else ranks

# Input: a list of card ranks, example: [10,9,8,7,6]
# Output: True if ranks form a straight hand, false otherwise
def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return ((max(ranks)-min(ranks)==4) and len(set(ranks))==5)

# Input: a list of cards in a hand, example: ['6C','9C','8C','7C','6C']
# Output: True if the hand form a flush hand, false otherwise
def flush(hand):
    "Return True if all the cards have the same suit."
    return len(set([s for r,s in hand]))==1   

# Input:
# n -> the hand has exactly n of
# ranks -> a list of card ranks
# Output:
# if the hand is "9D 9H 9S 9C 7D"
# ranks -> [9,9,9,9,7]
# if we call kind(4,ranks), it should return 9,
# because the hand has 4 of 9
def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for rank in ranks:
        if ranks.count(rank) == n:
            return rank
    return None

# Input: a list of card ranks, example: [10,9,8,7,6]
# Output: returns a tuple of the two ranks (high,low), None otherwise
def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    pair = kind(2, ranks)
    twopair = kind(2, list(reversed(ranks)))
    if pair and twopair != pair:
        return (pair, twopair)
    return None

def test():
 
    al = "AC 2D 4H 3D 5S".split() # Ace-Low Straight
    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "9D 9H 8S 8D KH".split() # Two Pair
    pair = ['AC', '3D', '4S', 'KH', 'KS']
    al = "AC 2D 4H 3D 5S".split() # Ace-Low Straight
     
    assert poker([sf1, sf2, fk, al]) == [sf1, sf2] 

    assert straight(card_ranks(al)) == True 
    
    assert card_ranks(sf) == [10,9,8,7,6]
    assert card_ranks(fk) == [9,9,9,9,7]
    assert card_ranks(fh) == [10,10,10,7,7]
    assert card_ranks(pair) == [14,13,13,4,3]    
    
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf) == True
    assert flush(fk) == False

    assert two_pair(card_ranks(tp)) == (9,8)
    assert two_pair(card_ranks(pair)) == None

    fkranks = card_ranks(fk)
     
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    
    print deal(3)
    #hand_percentages(10000)

    print 'Test Passed'
    return True

test()
