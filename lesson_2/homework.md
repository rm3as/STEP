# 第二回目
## 宿題1
>ほぼ O(1) で動くハッシュテーブルを自分で実装してみよう
### delete関数の実装
```
def delete(self, key):
    assert type(key) == str
    bucket_index = calculate_hash(key) % selfbucket_size
    item = self.buckets[bucket_index]
    prev_item = None
    while item:
        if item.key == key:
            if prev_item:
                prev_item.next = item.next
            else:
                self.buckets[bucket_index] = item.next
            self.item_count -= 1
            return True
        prev_item = item
        item = item.next
    return False
```
1. deleteの対象Itemがどこのbucketに入っているか、bucketの中のどこにあるか調べる
2. 削除対象Itemが見つかったら、該当Item前後のnextポインタが指すものを書き換える。
3. item_countを1つ減らしてTrueを返して終了。
4. bucketsの中に削除対象Itemが見つからなければFalseを返して終了。

### 再ハッシュの実装
要素数がテーブルサイズの 70% を上回ったら、テーブルサイズを 2 倍に拡張するようにした。
```
def spread_buckets(self):
    prev_bucket_size = self.bucket_size
    self.bucket_size = self.bucket_size * 2 + 1
    new_buckets = [None] * self.bucket_size
    for i in range(prev_bucket_size):
        item = self.buckets[i]
        while item:
            next_item = item.next
            new_bucket_index = calculate_hash(item.key) % self.bucket_size
            item.next = new_buckets[new_bucket_index]
            new_buckets[new_bucket_index] = item
            item = next_item
    self.buckets = new_buckets
```
要素数がテーブルサイズの 30% を下回ったら、テーブルサイズを半分に縮小するようにした。
```
def shrink_busckets(self):
    prev_bucket_size =  self.bucket_size
    self.bucket_size = (self.bucket_size + 1) // 2 -1
    new_buckets = [None] * self.bucket_size
    for i in range(prev_bucket_size):
        item = self.buckets[i]
        while item:
            next_item = item.next
            new_bucket_index = calculate_hash(item.key) % self.bucket_size
            item.next = new_buckets[new_bucket_index]
            new_buckets[new_bucket_index] = item
            item = next_item
    self.buckets = new_buckets
```
### ハッシュ関数を変更した
衝突をできるだけ避けるため、keyの文字列を素数の掛け算として表した(各文字が素数になっている)。
```
def calculate_hash_multiply(key):
    
    assert type(key) == str
    hash = 1
    for i in key:
        hash *= prime_number_list[ord(i)]
    return hash

calculate_hash = calculate_hash_multiply
```
ただ、これだとanagramに対しては同じハッシュ値が出力される。
prime_number_list[ord(i) * (文字の出現順番)]とすることで解消されるとは思ったが、prime_number_listのメモリ消費量がかなり増えるため、そこまでする価値があるか分からなかった。

## 宿題2
>木構造を使えば O(log N)、ハッシュテーブルを使えばほぼ O(1) で検索・追加・削除を実現することができて、これだけ見ればハッシュテーブルのほうが優れているように見える。ところが現実の大規模なデータベースでは、ハッシュテーブルではなく木構造が使われることが多い。その理由を考えよ。

1. 拡張性に優れている \
木構造なら、データ量の増加に伴い、徐々にデータ構造を拡張していくことができるが、ハッシュテーブルを利用すると再ハッシュが必要になる（もしくは探索にとても時間がかかるようになる）。

2. 順序関係がデータ構造に反映される \
これはハッシュ値の求め方によって一部解消できるのかもしれないが、基本的にハッシュテーブルではデータ間の類似性・近さは考慮されない。木構造は考慮される。これにより、キャッシュヒット率の向上などのメリットがある。
3. メモリ消費量が少ない　\
ハッシュテーブルはbucketが指すポインタの分だけメモリ消費量が大きい。

## 宿題3
以下のように、縦軸を「いくつ前に参照されたページか」、横軸を「ページのハッシュ値」とするようなテーブルで管理すればよい。

|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| 1 |   |   |   | d.com:ページd |   |   |   |
| 2 |   |   |   |   |   |   | g.com:ページg |
| 3 | a.com:ページa |   |   |   |   |   |   |

## 宿題4
homework_4.py参照。
