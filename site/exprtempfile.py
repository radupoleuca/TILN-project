import sys
input=sys.argv[1]

data=[]
flag=False
with open('date.txt','r') as f:
    lines = f.readlines()
    for i in range(0, len(lines)):
        line = lines[i]
        if line == (str(input) + '\n'):
            indice = i
            flag=True
        if flag:
            if line != lines[indice]:
                data.append(line)
        if line.strip().endswith(']'):
            flag=False

h = open('output.txt', 'w')
h.truncate(0)
h.write(''.join(data) )
h.close() 

