import sys

def file_contents_letters(file_name):
    """
    Takes a file name as input and returns a string consisting of the file's contents
    with all non-letter characters removed.
    
    Parameters:
        file_name: The name of the file.
    
    Returns:
        A string with the contents of <file_name> but with all non-letter characters removed.
    """

    f = open(file_name, "r")
    file_contents = f.read()
    f.close()
    return "".join([c for c in file_contents if c.isalpha()])
    
def edit_distance(s1, s2, ci = 1, cd = 1, cm = 1):
    """
    Computes the edit distance between two strings, s1 and s2.
    
    Parameters:
        s1: The first string.
        s2: The second string.
        ci: The cost of an insertion (1 by default).
        cd: The cost of a deletion (1 by default).
        cm: The cost of a mutation (1 by default).
    
    Returns:
        The edit distance between s1 and s2.
    """
    # Initialization (m + 1)x(n + 1) array edit. Note: m = len(s2), n = len(s1)
    edit = []
    for i in range(len(s2) + 1):
        row = []
        for j in range(len(s1) + 1):
            row.append(0)
        edit.append(row)

    # Fill matrix for m
    for i in range(len(s2) + 1):
        edit[i][0] = i

    # Fill matrix for n
    for j in range(len(s1) + 1):
        edit[0][j] = j

    # Nested for loops for Tabulation algorithm
    for i in range(1, len(s2) + 1):
        for j in range(1, len(s1) + 1):
            # Matching characters
            if s2[i - 1] == s1[j - 1]:
                edit[i][j] = edit[i - 1][j - 1]
            # Calculate the minimum cost of which change to make (ci = insertion, cd = deletion, cm = mutation)
            else:
                edit[i][j] = min(edit[i - ci][j] + 1, edit[i][j - cd] + 1, edit[i - cm][j - cm] + 1)

    # Return "bottom right" element of the matrix
    return edit[len(s2)][len(s1)]
    
def lcs(s1, s2):
    """
    Computes the length of the longest common subsequence between two strings, s1 and s2.
    
    Parameters:
        s1: The first string.
        s2: The second string.
    
    Returns:
        The length of the longest common subsequence between s1 and s2.
    """
    # Initialization of (m + 1)x(n + 1) array LCS. m = len(s1), n = len(s2)
    lcsMatrix = []
    for i in range(len(s1) + 1):
        row = []
        for j in range(len(s2) + 1):
            row.append(0)
        lcsMatrix.append(row)

    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            # Case 1: first column, first row always 0
            if i == 0 or j == 0:
                lcsMatrix[i][j] = 0
            # Case 2: Diagonal arrows to find LCS itself
            elif s1[i - 1] == s2[j - 1]:
                lcsMatrix[i][j] = lcsMatrix[i - 1][j - 1] + 1
            # Case 3: set the max length number between the left index and top index
            else:
                lcsMatrix[i][j] = max(lcsMatrix[i - 1][j], lcsMatrix[i][j - 1])

    # Return bottom right index of the LCS matrix for length of LCS
    return lcsMatrix[len(s1)][len(s2)]

def lcs3(s1, s2, s3):
    """
    Computes the length of the longest common subsequence between three strings: s1, s2, and s3.
    
    Parameters:
        s1: The first string.
        s2: The second string.
        s3: The third string.
    
    Returns:
        The length of the longest common subsequence between s1, s2, and s3.
    """
    # Initialize (m + 1)x(n + 1)x(o + 1)
    lcsArray = []
    for i in range(len(s1) + 1):
        s1Array = []
        for j in range(len(s2) + 1):
            s1s2Array = []
            for k in range(len(s3) + 1):
                s1s2Array.append(0)
            s1Array.append(s1s2Array)
        lcsArray.append(s1Array)

    # Nested for loop times three for third string
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            for k in range(len(s3) + 1):
                # Edge case always will be 0
                if (i == 0 or j == 0 or k == 0):
                    lcsArray[i][j][k] = 0
                # If there is a subsequence character, add 1 to whatever their previous value was
                elif (s1[i - 1] == s2[j - 1] and s1[i - 1] == s3[k - 1]):
                    lcsArray[i][j][k] = lcsArray[i - 1][j - 1][k - 1] + 1
                # Max of all previous cases
                else:
                    lcsArray[i][j][k] = max(max(lcsArray[i - 1][j][k],lcsArray[i][j - 1][k]), lcsArray[i][j][k - 1])

    # Return final variable of the array of arrays of lengths to get final length of subsequence
    return lcsArray[len(s1)][len(s2)][len(s3)]

s1 = file_contents_letters(sys.argv[1])
s2 = file_contents_letters(sys.argv[2])
print(edit_distance(s1, s2), lcs(s1, s2))

#!!!!!!!!!!!!!!!!!ATTENTION!!!!!!!!!!!!!!!!!!ATTENTION!!!!!!!!!!!!!!!!!!#
#!  QUESTION 3 SOLUTIONS:                                              !#
#!    EDIT DISTANCE = 208                                              !#
#!    LCS = 29703                                                      !#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#