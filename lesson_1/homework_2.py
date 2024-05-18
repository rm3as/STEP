import sys
from collections import Counter

def main():
    selected_file = sys.argv[1]
    if selected_file == "small" or selected_file == "medium":
        func_key = "subset"
    elif selected_file == "large":
        func_key = "count"
    else:
        print("正しいtxtファイルを、small, medium, largeの中から選んでください。")
        
    sort_functions = {
        "subset": sort_dictionary_subset,
        "count": sort_dictionary_count
    }
    anagram_functions = {
        "subset": anagram_subset,
        "count": anagram_count
    }
    
    sort_func = sort_functions[func_key]
    anagram_func = anagram_functions[func_key]
    
    
    ANSWER_FILE = f"./answer/{selected_file}_answer.txt"
    best_anagram_list = []
    
    DICTIONARY_FILE = "./data/words.txt"
    dictionary = []
    with open(DICTIONARY_FILE) as f1:
        for line in f1:
            word = line.rstrip("\n")
            dictionary.append(word)
    print("辞書ファイルの読み込み完了")
    
    RANDOM_WORDS_FILE = f"./data/{selected_file}.txt"
    random_words = []
    with open(RANDOM_WORDS_FILE) as f2:
        for line in f2:
            random_word = line.rstrip("\n")
            random_words.append(random_word)
    print("random_wordファイルの読み込み完了")
    
    # sorted_dictionaryをここでつくっちゃう
    sorted_dictionary = sort_func(dictionary)
    
    for random_word in random_words:
        print(random_word)
        best_anagram = anagram_func(random_word, sorted_dictionary)
        best_anagram_list.append(best_anagram)
        print(best_anagram)
    with open(ANSWER_FILE, "r+") as f3:
        f3.truncate(0)
        for best_anagram in best_anagram_list:
            f3.write(best_anagram + "\n")
    
def sort_dictionary_subset(dictionary):
    sorted_dictionary = []
    for word in dictionary:
        sorted_dictionary.append((sorted(word), word))
    sorted_dictionary.sort(key=lambda x: x[0])
    return sorted_dictionary

def sort_dictionary_count(dictionary):
    sorted_and_counted_dictionary = []
    for word in dictionary:
        char_count = Counter(sorted(word))
        sorted_and_counted_dictionary.append((sorted(word), word, char_count))
    sorted_and_counted_dictionary.sort(key=lambda x: x[0])
    return sorted_and_counted_dictionary  
        
def anagram_subset(random_word, sorted_dictionary):
    # 入力ワードをソートする
    sorted_word = sorted(random_word)
    subsequences = generate_subsequences(sorted_word)
    
    best_anagram = ""
    best_score = 0
    for subset in subsequences:
        if binary_search(subset, sorted_dictionary) is not None:
            subset_best_anagram, subset_best_score = binary_search(subset, sorted_dictionary)
            if subset_best_score > best_score:
                best_score = subset_best_score
                best_anagram = subset_best_anagram
                
    return best_anagram
    
def binary_search(sorted_word, sorted_dictionary):
    best_anagram = ""
    best_score = 0
    
    low = 0
    high = len(sorted_dictionary) - 1
    mid = (low + high) // 2
    while(low < high): #　←もっと良い条件がある気もする
        if sorted_word == sorted_dictionary[mid][0]: # anagramをとりあえず一つみつけた
            while(1):
                if mid == 0 or \
                    sorted_dictionary[mid - 1][0] != sorted_word: # midを、最も最初にあるanagramのインデックスにずらせた
                        while(sorted_dictionary[mid][0] == sorted_word): # anagram_listにanagramを全て追加する
                            current_score = calculate_score(sorted_dictionary[mid][1])
                            if current_score > best_score:
                                best_anagram = sorted_dictionary[mid][1]
                                best_score = current_score
                            mid += 1
                        
                        return best_anagram, best_score
                else: # 一つ前の単語もanagram
                    mid -= 1                         
                
        elif sorted_word < sorted_dictionary[mid][0]: # anagramがあるならmidが指す位置より前らしい
            if high == mid: # インデックスが更新されないならおしまい
                return best_anagram, best_score
            high = mid
        else: # anagramがあるならmidが指す位置より後らしい
            if low == mid: # インデックスが更新されないならおしまい
                return best_anagram, best_score
            low = mid
                        
        mid = (low + high) // 2  

def generate_subsequences(sorted_word):
    def backtrack(start, subsequence):
        subsequences.append(subsequence.copy())
        for i in range(start, len(sorted_word)):
            subsequence.append(sorted_word[i])
            backtrack(i+1, subsequence)
            subsequence.pop()

    subsequences = []
    backtrack(0, [])
    return subsequences

def anagram_count(random_word, sorted_dictionary):
    random_word_count = Counter(sorted(random_word)) # random_wordのカウンターつくる
    
    best_anagram = ""
    best_score = 0

    for word in sorted_dictionary:
        is_anagram = True
        char_count = word[2]
        for char in char_count:
            if char_count[char] > random_word_count[char]:
                is_anagram = False
                break
        if not is_anagram:
            continue
        # このwordはanagramだった！
        current_score = calculate_score(word[1])
        if current_score > best_score:
            best_score = current_score
            best_anagram = word[1]
    return best_anagram
        
    
def calculate_score(word):
    SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score

if __name__ == "__main__":
    main()
    