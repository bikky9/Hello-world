values = []
for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                values.append([i,j,k,l])
def valid(i):
    if (i[0]==i[2] and i[1]==i[3] and i[0]!=i[1]):
            return False
    else:
        return True
not_valid = 0
for i in values:
    if(not valid(i)):
        not_valid+=1
total = len(values)
print "Number of boolean functions for n = 2 is " + str(total - not_valid)
values = []
not_valid = 0
for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                for m in range(2):
                    for n in range(2):
                        for o in range(2):
                            for p in range(2):
                                values.append([i,j,k,l,m,n,o,p])
ans = 0
for i in values:
    face1 = [i[0],i[1],i[2],i[3]]
    face2 = [i[2],i[3],i[4],i[5]]
    face3 = [i[4],i[5],i[6],i[7]]
    face4 = [i[1],i[2],i[5],i[6]]
    face5 = [i[0],i[3],i[4],i[7]]
    face6 = [i[0],i[1],i[6],i[7]]
    diag1 = [i[0],i[5]]
    diag2 = [i[1],i[4]]
    diag3 = [i[2],i[7]]
    diag4 = [i[3],i[6]]
    if(valid(face1) and valid(face2) and  valid(face3) and valid(face4) and valid(face5) and valid(face6) and valid([diag1[0],diag2[0],diag1[1],diag2[1]]) and valid([diag1[0],diag3[0],diag1[1],diag3[1]]) and valid([diag1[0],diag4[0],diag1[1],diag4[1]]) and  valid([diag2[0],diag3[0],diag2[1],diag3[1]]) and  valid([diag2[0],diag4[0],diag2[1],diag4[1]]) and valid([diag3[0],diag4[0],diag3[1],diag4[1]])):
        ans+=1
print "Number of boolean functions for n = 3 is " + str(ans)
