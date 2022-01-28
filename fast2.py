from pandas import read_csv, DataFrame,concat
from itertools import product, combinations
import numpy as np
import time

start = time.process_time()
def search(guess_list, dataframe, A_dic, B_dic):
    IsAvailable = bool()
    result = []
    for word in guess_list:
        for row in dataframe.index:
            if dataframe.loc[row,0] == word:
                IsAvailable = True
                for i in B_dic:                     # i = letter ex.'r'
                    for num in B_dic[i]:
                        if word[ num ] == i:
                            IsAvailable = False
                for j in A_dic:                   
                    for num in A_dic[j]:
                        if word[ num ] != j:
                            IsAvailable = False
                if IsAvailable:
                    # print(final_dataframe.loc[row,0])
                    result.append(dataframe.loc[row,0])
    return result

def tup_to_string( tups ):
    l = []
    for tup in tups:
        l.append( list(tup) )
    string_lsit =[]
    for lists in l:
        string_lsit.append(''.join(lists) )
    return string_lsit

def main():
    dataframe_guesses = read_csv('wordle-allowed-guesses.txt', sep = '\n\n', header = None, engine = 'python')
    dataframe_answers = read_csv('wordle-answers-alphabetical.txt', sep = '\n\n', header = None, engine = 'python')
    final_dataframe = concat([dataframe_guesses, dataframe_answers], axis=0)
    final_dataframe.sort_values(0 , inplace = True)
    final_dataframe.reset_index(drop = True, inplace=True)
    five_letter_guess = []

    from tools import alphabet_counts
    A_dic = {}
    B_dic = {}
    ava_dataframe = DataFrame.from_dict(
        alphabet_counts, orient='index'
    ).rename(columns={0:'Available'})

    guess = input('Enter first three guesses without comma: ').lower()
    result =input('Enter 15 results without comma.(A,B,or X): ').lower()


    while True:
        for i in range(len(result)):
            if result[i] == 'x':
                if guess[i] not in A_dic.keys() and guess[i] not in B_dic.keys():
                    final_dataframe = final_dataframe[~final_dataframe[0].str.contains( guess[i] )]
            elif result[i] == 'a':
                try:
                    if i not in A_dic[ guess[i] ]:
                        A_dic[ guess[i] ].append( i%5 ) 
                        if guess[i] in B_dic:
                            del B_dic[guess[i]]
                except:
                    A_dic[ guess[i] ] =  [i%5] 
                    if guess[i] in B_dic:
                        del B_dic[guess[i]]
            elif result[i] == 'b':
                try:
                    B_dic[ guess[i] ].append(i%5) 
                except:
                    B_dic[ guess[i] ] =  [i%5] 
                # final_dataframe = final_dataframe[~final_dataframe[0].str.contains( guess[i] )]

        for i in alphabet_counts:
            alphabet_counts[i] = False

        for row in final_dataframe.index:
            for letter in final_dataframe.loc[row , 0]:
                alphabet_counts[letter] = True
        ava_dataframe = DataFrame.from_dict(
            alphabet_counts, orient='index'
        ).rename(columns={0:'Available'})
        ava_dataframe =  ava_dataframe.loc[~(ava_dataframe==False).all(axis=1)]

        ult_list = []
        for i in ava_dataframe.index:
            ult_list.append(i)
        AorB_list = []
        AorB_list = list(A_dic.keys()) + list(B_dic.keys())
        ult_list = [ i for i in ult_list if i not in AorB_list]

        remaining_tups = list(combinations(''.join(ult_list), 5 - len(A_dic.keys()) - len(B_dic.keys()) ))     
        # print(len(remaining_tups))

        remaining_list = tup_to_string( remaining_tups )
        # print(remaining_list)

        five_letter_list = []
        for i in remaining_list:
            five_letter_list.append( i + ''.join(AorB_list))

        five_letter_guess = []
        for i in five_letter_list:
            five_letter_tups = list(product( i, repeat = 5 ))
            l = []
            l2 = []
            for tup in five_letter_tups:
                l.append( list(tup) )   
            for word in l:
                if set(''.join(AorB_list)) <= set(word):
                    l2.append(word)
            for lists in l2:                                   
                five_letter_guess.append(''.join(lists) )
        five_letter_guess = list(set(five_letter_guess))
        # print(len(five_letter_guess))
        # flg_array = np.array(five_letter_guess)
        result = search(five_letter_guess, final_dataframe, A_dic, B_dic)
        if len(result) == 1:
            print(f'Answer: {result}')
            break
        else:
            print(f'Guess: {result[0]}')
            print(result)
            guess = result[0]
            result = input('Enter the result: ').lower()

main()
end = time.process_time()

print(f'Process time:{end-start} sec')
