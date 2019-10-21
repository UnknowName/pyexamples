def insert_sort(lst: list) -> list:
    length = len(lst)
    # 第一层循环，从第二位开始，因为第一位认为已排序
    for i in range(1, length):
        # 第二层循环，从已排好充的列表中依次比较当前值，如果比它小，交换位置
        for j in range(i):
            if lst[i] < lst[j]:
                lst[i], lst[j] = lst[j], lst[i]
    return lst


if __name__ == '__main__':
    nums = [2, 9, 8, 7, 12, 0, -1, 7]
    print(insert_sort(nums))
