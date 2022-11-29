# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : JKantypowicz
# Collaborators : Google, Stack Overflow
# Time spent    : Too Much

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
WILD_CARD = '*'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word = word.lower()   
    word_length = len(word)
    # print(word_length)
    second_componant = 7 * word_length - 3 * (n - word_length)
    # print(second_componant)
    word_points = 0
    
    for value in word:
        # print(SCRABBLE_LETTER_VALUES[value])
        word_points += SCRABBLE_LETTER_VALUES[value]
    # print(word_points)
    
    if second_componant > 1:
        return word_points * second_componant
    else:
        return word_points * 1
        
# Tester code for function:    
# word = 'h*ney'
# n = 7
# print(get_word_score(word, n))


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    #print(hand.keys())
    
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line


# Tester code for function:  
# hand = {'a':1, 'x':2, 'l':3, 'e':1}
# print(display_hand(hand))

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 4))
    # print(num_vowels)

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(1):
        x = WILD_CARD
        hand[x] = hand.get(x, 0) + 1
        for i in range(num_vowels, n - 1):    
            x = random.choice(CONSONANTS)
            hand[x] = hand.get(x, 0) + 1
  
    return hand

# Tester code for function:  
# print(deal_hand(HAND_SIZE))

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    
    word = word.lower() 
    hand_copy = {}
    new_hand = {}
    
    #makes copy/helper hand
    for key, value in hand.items():
        hand_copy.update({key : value})
    
    #identifies letters from word to not be included in new hand and sets hand_copy dictionary key values to zero
    for letter in word:
        if letter in hand_copy.keys():
            hand_copy[letter] -= 1
    
    #adds all non zero key value dictionary items to new_hand
    for key, value in hand_copy.items():
        if hand_copy[key] > 0:
            new_hand.update({key : value})
    
    return new_hand


# Tester code for function:  
# hand = {'j':2, 'o':1, 'l':1, 'w':1, 'n':2}
# word = 'jolly'
# display_hand(hand)
# hand = update_hand(hand, word)
# print(hand)
# display_hand(hand)




#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    word = word.lower()
    hand_copy_dict = hand.copy()
    hand_letters_list = []
    
    #checks word for wildcard usage, if so finds all possibile words that can be used with that wildcare usage. May not use exact word but points should be the same due to game rules (all vowels worth the same) so irrelevent.
    
    for letter in word:
        if letter == WILD_CARD:
            for letter in VOWELS:
                wild_card_word = word.replace('*', letter)
                # print(wild_card_word)
                if wild_card_word in word_list:
                    if letter in word:
                        hand_copy_dict[letter] += 1
                    else:
                        hand_copy_dict[letter] = 1
                    word = wild_card_word
                    break
     
        #checks to see if the word entered actually contains the letters from the hand played
        else:
            if letter not in hand_copy_dict:
                return False
    
    #if all potential wildcard words are not in the word list returns function as false
    if word not in word_list:
        return False
       
    #a) subtracts value of letter from hand_copy_dict for later in function
    #b) appends letter to hand_letters_list if in word for later in function
    for letter in word:
        if letter in hand_copy_dict:
            hand_copy_dict[letter] -=1
            hand_letters_list.append(letter)
    # print(hand_letters_list)
    # print(hand_copy_dict)
    
    
    #same as above but just for the wildcard value. Ensures that there isnt a double entry of wildcard values or a letter    
    for letter in hand_copy_dict:
        if letter == WILD_CARD and len(hand_letters_list) != len(word):
            hand_copy_dict[letter] -=1
            hand_letters_list.append(letter)
    

    # print(word)    
    # print(hand_copy_dict)
    # print(hand_letters_list)
    
    # loop in line 278 if statment subtracted value tally for each word used. If hand had only one of a letter where two are required in the word, value in hand_copy_dict would be -1.
    # this loop checks for negative values and if one is found returns function as False (i.e hand {'a': 1, 'b': 1, 'e': 1} would not allow you to submit the word 'abbe')
    for value in hand_copy_dict.values():
        if value < 0 :
            return False
    # if no negative values are found, len of hand_letters_list is compared to len of word to ensure all letters required were used. If so, word is valid.
    if len(hand_letters_list) != len(word):
        return False       
    else:
        return True
        


# Tester code for function:  
# hand = {'h': 1, 'n': 1, '*': 1, 'e': 1, 'y': 1}
# hand = deal_hand(HAND_SIZE)
# print(display_hand(hand))
# word = input('Enter word: ', )
# word_list = load_words()
# print(is_valid_word(word, hand, word_list))

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """ 
    handlen_list = []
    
    for value in hand.values():
        handlen_list.append(value)
       
    return sum(handlen_list)


# Tester code for function:  
# hand = deal_hand(HAND_SIZE)
# print(display_hand(hand))
# print(calculate_handlen(hand))    

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function  
    # Keep track of the total score
    
    total_score = 0
    
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        
        # # Display the hand
        print('Current hand:', end = ' ') 
        display_hand(hand)
               
        # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished: ', )
        
        # If the input is two exclamation points:
        if word == '!!':
            # End the game (break out of the loop)
            break
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list) is True:
                # print('yes')
                # Tell the user how many points the word earned and the updated total score
                hand_score = get_word_score(word, HAND_SIZE)
                total_score += hand_score                
                print('"' + word +'"','earned', hand_score, 'points.', 'Total:', total_score, 'points' )
            # Otherwise (the word is not valid):
            # Reject invalid word (print a message)
            else:
                print('That is not a valid word. Please choose another word')
                
        # update the user's hand by removing the letters of their inputted word
        hand = update_hand(hand, word)

            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if calculate_handlen(hand) == 0:
        print('Ran out of letters. Total score for this hand:', total_score)
        print('----------')
    elif word == '!!':
        print('Total score for this hand:', total_score)
        print('----------')
    

    # Return the total score as result of function
    return total_score



#
# Problem #6: Playing a game

# Tester code for function:   
# hand = deal_hand(HAND_SIZE)
# word_list = load_words()
# play_hand(hand, word_list)


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # creates copy of hand, consonants, vowels, and letter list for input validation
    sub_hand = hand.copy()
    con_copy = str(CONSONANTS)
    vowel_copy = str(VOWELS)
    letter_list = []
     
    #adds all consonants to letter_list
    for char in con_copy:
        letter_list.append(char)
    
    #adds all vowels to letter_list
    for char in vowel_copy:
        letter_list.append(char)
    
    # checks to see if user entered a valid letter, if not user is asked to try again
    if letter not in letter_list:
        return print('Invalid input. Please try again using letter')
    elif letter not in sub_hand:
        return print('Invalid input. Please try again using letter in hand')


    
    # identifies if letter is consonant 
    for char in con_copy:
        if char == letter:
            # removes letter from con_copy
            con_copy = con_copy.replace(char, '')
            # assigned a random letter from con_copy to x
            x = random.choice(con_copy)
        
        # if letter isnt consonant, checks to see if letter is vowel. If so does the same as above but for vowel
        elif char != letter:
            for char in vowel_copy:
                if char == letter:
                    vowel_copy = vowel_copy.replace(char, '')
                    x = random.choice(vowel_copy)


    # replaces selected letter with new random latter (x)
    sub_hand[x] = sub_hand.pop(letter)
    
    return sub_hand
    

# Tester code for function:  
# hand = {'h':1, 'e':1, 'l':2, 'o':1}  
# letter = 'l'
# sub_hand = substitute_hand(hand, letter)  
# print(sub_hand)    
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    # """
    substitutions = 1
    hand_replays = 1
    series_score = 0
    
    # Get hand amount from user
    hand_amount = int(input('Enter total number of hands: ' ))
    
    # creates loop to play the amount of hands promtped for game
    for number in range(hand_amount):
        
        # deal hand and display it to user
        hand = deal_hand(HAND_SIZE)
        print('Current hand:', end = ' ') 
        display_hand(hand)
        
        # promts for substitution once a game
        while substitutions > 0:
            sub_input = str(input('Would you like to substitute a letter? ')).lower()
            if sub_input =='yes':
                sub_letter_input = input('Which letter would you like to replace: ')
                if sub_letter_input in hand:
                    hand = substitute_hand(hand, sub_letter_input)
                    substitutions -= 1
                else:
                    print('Invalid input. PLease enter a letter from hand')
            elif sub_input == 'no':
                break
            else:
                print('Invalid input. Please enter yes or no' )
                continue
    
        # plays a hand, adds total score to series score
        total_score = play_hand(hand, word_list)
        series_score += total_score
        
        # asks user if they want to replay hand once a game
        while hand_replays > 0:
            hr_input = str(input('Would you like to replay the hand? ')).lower()
            if hr_input =='yes':
                # print('Current hand:', end = ' ') 
                # display_hand(hand)
                total_score_replay = play_hand(hand, word_list)
                if total_score_replay > total_score:
                    series_score -= total_score
                    series_score += total_score_replay
                hand_replays -= 1
            elif hr_input == 'no':
                break
            else:
                print('Invalid input. Please enter yes or no' )
                continue
    
    # indicates final score for the game
    print('Total score over all hands: ', series_score)
    # returns series score in case I want to add a high score list or something
    return series_score
            
        
            
                
        

                        
                    
            
        
    
    

    

    






#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
