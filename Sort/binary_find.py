def binary_find(lst, data):
    lst = sorted(lst)
    start = 0
    end = len(lst) - 1
    while start <= end:
        mid = (start + end) // 2
        if lst[mid] < data:
            start = mid + 1
        elif lst[mid] > data:
            end = mid - 1
        else:
            return True
    return False


if __name__ == '__main__':
    array = [1, 2, 4, 10, 20, 22, 24, 9]
    find = binary_find(array, 22)
    print(find)