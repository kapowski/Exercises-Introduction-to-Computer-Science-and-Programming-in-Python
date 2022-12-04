# Problem Set 4A
# Name: jkantypowicz
# Collaborators: Youtube, Google, StackOverflow
# Time Spent: Too Much

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    #program if word length is only 1
    if len(sequence) == 1:
        return [sequence]
    
    ''' This next line is the recursive section for all permutations for the 
    length of word - 1.
    
    The "word[1:] returns the word missing the first letter (eg. from 'abc'
    this will return 'bc').
    
    This is the string equivelent of a the concept of n-1 used in solving 
    factorial recursion with integers.'''
    perms = get_permutations(sequence[1:])
    
    #saves first letter of word
    letter = sequence[0]
    
    #all possible permutations list
    perms_list = []
    
    #itterates through all permutations of word length n-1
    for perm in perms:
        #iterates through the characters of each permutation in perms list
        for i in range(len(perm)+1):
            #this takes the first letter (word[0]) and places it in every possible position in a given permutation
            perms_list.append(perm[:i] + letter + perm[i:])
            
    return perms_list

# word = 'abc'
# print(permutations(word))
   

if __name__ == '__main__':
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'bac', 'bca', 'acb', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
    example_input = 'cat'
    print('Input:', example_input)
    print('Expected Output:', ['cat', 'act', 'atc', 'cta', 'tca', 'tac'])
    print('Actual Output:', get_permutations(example_input))
    
    example_input = 'bad'
    print('Input:', example_input)
    print('Expected Output:', ['bad', 'abd', 'adb', 'bda', 'dba', 'dab'])
    print('Actual Output:', get_permutations(example_input))
    

