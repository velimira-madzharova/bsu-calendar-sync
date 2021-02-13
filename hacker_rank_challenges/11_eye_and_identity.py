import numpy as n
n.set_printoptions(legacy='1.13')

if __name__ == '__main__':
    a = list(input().split())

print(n.eye(int(a[0]), int(a[1]), k = 0))