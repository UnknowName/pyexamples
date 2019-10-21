def bubble_sort(lst: list) -> list:
    """
    冒泡排序
    :param lst:
    :return:
    """
    length = len(lst)
    # 执行循环列表的长度次数
    while length:
        # 内层for循环，依次比较旁边的元素，将大的交换至右边
        for i in range(length - 1):
            # print(lst[i], lst[i+1])
            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i+1], lst[i]
        length -= 1
    return lst


if __name__ == '__main__':
    nums = [100, 2, 9, 12, 9, 90, 0, -2]
    print(bubble_sort(nums))
