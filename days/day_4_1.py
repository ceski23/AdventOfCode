def passwordGenerator(n, end):
  while (n <= end):
    arr, double, group = list(str(n)), False, 0
    for i in range(1, len(arr)):
      if (arr[i] < arr[i-1]): arr[i] = arr[i-1]
      if (arr[i] == arr[i-1]): double = True
    n = int(''.join(arr))
    if (n <= end and double): yield n
    n += 1

inpRange = (372304, 847060)
numbers = list(passwordGenerator(*inpRange))

print(len(numbers))