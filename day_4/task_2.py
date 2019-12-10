def passwordGenerator(n, end):
  while (n <= end):
    arr, double, group = list(str(n)), False, 1
    for i in range(1, len(arr)):
      if (arr[i] < arr[i-1]): arr[i] = arr[i-1]
      if (arr[i] == arr[i-1]): group += 1
      else:
        if (group == 2): double = True
        group = 1
    n = int(''.join(arr))
    if (n <= end and (double or group == 2)): yield n
    n += 1

inpRange = (372304, 847060)
numbers = list(passwordGenerator(*inpRange))
print(len(numbers))