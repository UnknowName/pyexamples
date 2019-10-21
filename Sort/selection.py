def selection_sort(lst: list) -> list:
    """
    选择排序，返回升序lst
    :param lst:
    :return:
    """
    length = len(lst)
    # 第一轮循环，依次从列表中取出一个数
    for i in range(length):
        # 第二轮循环，从i+1的位置起始（因为经过一次，就比较完了一次，不需要再重新从头比较）
        # 比较剩余的元素
        for j in range(i+1, length):
            # 如果待比较的元素大于剩余里面的元素，进行位置互换。
            if lst[i] > lst[j]:
                lst[i], lst[j] = lst[j], lst[i]
    return lst


if __name__ == '__main__':
    nums = [9, 10, 23, 2, 9]
    print(selection_sort(nums))
