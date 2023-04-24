
def decListToBinaryList(listValues):
    s = ""
    for v in listValues:
        s += format(v, 'b')[-1]
    print(s)
    
    