def binary_search_with_upper_bound(arr, target):
    """
    Двійковий пошук для дробових чисел.
    Повертає кортеж: (кількість ітерацій, верхня межа).
    """
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            # Знайшли точне співпадіння
            return (iterations, arr[mid])
        elif arr[mid] < target:
            left = mid + 1
        else:
            # arr[mid] > target, кандидат на верхню межу
            upper_bound = arr[mid]
            right = mid - 1

    # Якщо точного збігу немає, повертаємо верхню межу
    return (iterations, upper_bound)


# Приклад використання 
array = [1.2, 3.5, 5.7, 7.9, 9.3, 11.5, 14.8]
target = 8.0

result = binary_search_with_upper_bound(array, target)
print(f"Ітерацій: {result[0]}")
print(f"Верхня межа: {result[1]}")
