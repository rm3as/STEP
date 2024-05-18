import sys

def anagram(random_word, dictionary):
    # dictionaryの各単語をソートして、文字ごとの出現回数をカウント
    sorted_dictionary = []
    char_num_string_zero = "0" * 26
    for word in dictionary:
        # ソートして、出現回数をまとめた文字列をつくる
        char_num_string = char_num_string_zero
        for char in word:
            char_num_string[ord(char)] += 1
        sorted_dictionary.append((char_num_string, word))
    sorted_dictionary.sort(key=lambda x: x[0])
    sorted_word = sorted(random_word)
    
    anagram_list = binary_search(sorted_word, sorted_dictionary)
    print("\n".join(anagram_list))
    
def binary_search(sorted_word, sorted_dictionary):
    anagram_list = []
    
    low = 0
    high = len(sorted_dictionary) - 1
    mid = (low + high) // 2
    while(low < high): #　←もっと良い条件がある気もする
        if sorted_word == sorted_dictionary[mid][0]: # anagramをとりあえず一つみつけた
            while(1):
                if mid == 0 or \
                    sorted_dictionary[mid - 1][0] != sorted_word: # midを、最も最初にあるanagramのインデックスにずらせた
                        while(sorted_dictionary[mid][0] == sorted_word): # anagram_listにanagramを全て追加する
                            anagram_list.append(sorted_dictionary[mid][1])
                            mid += 1
                        return anagram_list
                else: # 一つ前の単語もanagram
                    mid -= 1                         
                
        elif sorted_word < sorted_dictionary[mid][0]: # anagramがあるならmidが指す位置より前らしい
            if high == mid: # インデックスが更新されないならおしまい
                return anagram_list
            high = mid
        else: # anagramがあるならmidが指す位置より後らしい
            if low == mid: # インデックスが更新されないならおしまい
                return anagram_list
            low = mid
                        
        mid = (low + high) // 2
        
if __name__ == "__main__":
    WORDS_FILE = "./data/words.txt"
    dictionary = []
    with open(WORDS_FILE) as f:
        for line in f:
            word = line.rstrip("\n")
            dictionary.append(word)
    anagram(sys.argv[1], dictionary)