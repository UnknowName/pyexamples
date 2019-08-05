import collections
import operator


def main():
    words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 's', 'ss', 'a', 'a', 'a', 'b', 'b', 'c', 'c']
    word_count = collections.Counter(words)
    # 打印出现频率最高的三个字母，如果不带参数，默认从出现最多到最小排序。输出元组
    print(word_count.most_common(3))
    # 打印指定字符串出现的次数,返回整型
    print(type(word_count['a']))
    rows = [
        {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
        {'fname': 'Arian', 'lname': 'Baeazley', 'uid': 1004},
        {'fname': 'Crian', 'lname': 'Clesses', 'uid': 1001},
        {'fname': 'Drian', 'lname': 'Jones', 'uid': 1002}
    ]
    # 按fname值排序
    rows_by_fname = sorted(rows, key=operator.itemgetter('fname'))
    # 按UID值排序
    rows_by_uid = sorted(rows, key=operator.itemgetter('uid'))
    print(rows_by_fname)
    print(rows_by_uid)


if __name__ == '__main__':
    main()
