import sys

def anagram(random_word, dictionary):
    # dictionaryの各単語をソートする
    sorted_dictionary = []
    for word in dictionary:
        sorted_dictionary.append((sorted(word), word))
    sorted_dictionary.sort(key=lambda x: x[0])
    sorted_word = sorted(random_word)
    
    anagram_list = binary_search(sorted_word, sorted_dictionary)
    
    print("\n".join(anagram_list))
    
def binary_search(sorted_word, sorted_dictionary):
    anagram_list = []
    
    low = 0
    high = len(sorted_dictionary) - 1
    mid = (low + high) // 2
    while(low < high): 
        if sorted_word == sorted_dictionary[mid][0]: # anagramをとりあえず一つみつけた
            anagram_list.append(sorted_dictionary[mid][1])
            low_anagram = mid 
            high_anagram = mid
            
            while(low_anagram != 0 and sorted_dictionary[low_anagram - 1][0] == sorted_word):
                low_anagram -= 1
                anagram_list.append(sorted_dictionary[low_anagram][1])
            while(high_anagram != len(sorted_dictionary)-1 and sorted_dictionary[high_anagram + 1][0] == sorted_word):
                high_anagram += 1
                anagram_list.append(sorted_dictionary[high_anagram][1])
            return anagram_list                 
                
        elif sorted_word < sorted_dictionary[mid][0]: # anagramがあるならmidが指す位置より前らしい
            # if high == mid: # インデックスが更新されないならおしまい
            #     return anagram_list
            high = mid -1
        else: # anagramがあるならmidが指す位置より後らしい
            # if low == mid: # インデックスが更新されないならおしまい
            #     return anagram_list
            low = mid + 1
                        
        mid = (low + high) // 2  
    
if __name__ == "__main__":
    WORDS_FILE = "./data/words.txt"
    dictionary = []
    with open(WORDS_FILE) as f:
        for line in f:
            word = line.rstrip("\n")
            dictionary.append(word)
    anagram(sys.argv[1], dictionary)