from operator import itemgetter

if __name__ == '__main__':
    arr=[]
    for _ in range(int(input())):
        name = input()
        mark = float(input())
        student=[name, mark]
        arr.append(student)
    # sorts by mark the initial array
    s = sorted(arr, key=itemgetter(1))
    # creates a dictionary with mark as a key and names as value
    mark_dict={}
    for x in s:
        if x[1] in mark_dict.keys():
            mark_dict[x[1]].append(x[0])
        else:
            mark_dict[x[1]]=[]
            mark_dict[x[1]].append(x[0])
    mark_keys = list(mark_dict.keys()) # convert dictionary keys to list
    marks_sorted=sorted(mark_dict[mark_keys[1]]) # sort for equal marks
    for name in marks_sorted:
        print(name)
