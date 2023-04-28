
def decListToBinaryList(listValues):
    s = ""
    for v in listValues:
        s += format(v, 'b')[-1]
    with open('lichtschranke.txt', 'w') as f:
        f.write(s)
    
    
