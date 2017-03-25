from copy import deepcopy
friends_list=[]
enemies_list=[]
split_line=()
guests=0
tables=0
i=0
count=0
symbols=set()
clauses_list=[]
arrangement={}
true_values=[]
abc=""
xyz=[]
with open("input.txt", "r") as f:
    for line in f:
        #print line
        split_line=line.split()
        #print split_line
        #print i
        if(i==0):
            guests = int(split_line[0])
            tables = int(split_line[1])
            #print guests,tables
        else:
            if(split_line[2]=='F'):
                #print split_line
                del split_line[2]
                friends_list.append(tuple(split_line))
            elif(split_line[2]=='E'):
                del split_line[2]
                enemies_list.append(tuple(split_line))
        i+=1
#print friends_list
#print enemies_list

def truth(cl, model):
    val=False
    for lit in cl:
        if lit in model:
            val=model.get(lit)
            if(val==True):
                return val
    return val

def pure_symbol(clauses, symbols, model):
    pureSymbols=set()
    for clause in clauses:
        sub=set()
        flag=False
        for literal in clause:
            if literal in model:
                if (model[literal]==True):
                    flag=True
                    break
            else:
                if literal in symbols:
                    sub.add(literal)
        if (flag==False):
            pureSymbols.union(sub)
    positive_pure_symbols=set()
    negative_pure_symbols=set()
    for literal in pureSymbols:
        if(literal[0]!="~"):
            lit_complement="~"+literal
            if lit_complement in pureSymbols:
                continue
            else:
                positive_pure_symbols.add(literal)
        else:
            y=literal.split("~")
            lit_complement=y[1]
            if lit_complement in pureSymbols:
                continue
            else:
                negative_pure_symbols.add(literal)
    #print "items in positive_pure_symbols", len(positive_pure_symbols)
    #print "items in negative_pure_symbols", len(negative_pure_symbols)
    if(len(positive_pure_symbols)>0):
        return positive_pure_symbols
    elif(len(negative_pure_symbols)>0):
        return negative_pure_symbols
    else:
        return False

def unit_clause(clauses, model):
    #print "Inside unit_clause"
    for clause in clauses:
        true_or_not = truth(clause, model)
        if (true_or_not == True):
            #print true_or_not
            #print clause, "is true"
            continue
        if(len(clause)==1):  #CHECKING IF THE CLAUSE IS UNIT LENGTH
            #print clause, "i'm unit length"
            for lit in clause:
                if(lit[0]!="~"):
                    lit_complement="~"+lit
                    if lit_complement in symbols:
                        model[lit_complement]=False
                        symbols.remove(lit_complement)
                    return lit, True
                else:
                    y=lit.split("~")
                    lit_complement=y[1]
                    if lit_complement in symbols:
                        model[lit_complement]=False
                        symbols.remove(lit_complement)
                    return lit, True
        else:  #CHECKING IF ALL BUT ONE LITERAL IN CLAUSE IS FALSE
            count=0
            for literal in clause:
                if literal in model:
                    count+=1
            if(count==(len(clause)-1)):
                for literal in clause:
                    if literal in model:
                        continue
                    else:
                        if(literal[0] != "~"):
                            lit_complement = "~" + literal
                            if lit_complement in symbols:
                                model[lit_complement] = False
                                symbols.remove(lit_complement)
                            return literal, True
                        else:
                            # model[x]=True
                            y = literal.split("~")
                            lit_complement=y[1]
                            if lit_complement in symbols:
                                model[lit_complement] = False
                                symbols.remove(lit_complement)
                            return literal, True
    return None, None

def DPLL(clauses, symbols, model):
    #print "Checking if all the clauses are True in the Model"
    flag1=False
    count1=0
    for clause in clauses:
        #print clause
        flag1=False
        for literal in clause:
            if literal in model:
                if(model[literal]==True):
                    flag1=True
                    count1+=1
                    break
        #print "outside inner for"
    if((flag1==True) and (count1==len(clauses))):
        #print model
        global arrangement
        arrangement=deepcopy(model)
        #print arrangement
        abc=str(true_values)
        return True

    #print "Checking if some clause in model is false"
    flag2=True
    for clause in clauses:
        count2 = 0
        for literal in clause:
            flag2 = True
            if literal in model:
                if(model[literal]==False):
                    flag2 = False
                    count2+=1
        if((flag2==False) and (count2==len(clause))):
            return False

    pure = pure_symbol(clauses, symbols, model)
    if pure:
        for p in list(pure):
            if(p[0]!="~"):
                p_complement= "~"+p
                symbols.remove(p)
                if p_complement in symbols:
                    symbols.remove(p_complement)
            else:
                y=p.split("~")
                p_complement=y[1]
                symbols.remove(p)
                if p_complement in symbols:
                    symbols.remove(p_complement)
            model[p]=True
            model[p_complement]=False
            return DPLL(clauses, symbols, model)

    P, val = unit_clause(clauses, model)
    if P:
        symbols.remove(P)
        model[P]=val
        #print "symbols is", symbols, "and model is",model
        return DPLL(clauses, symbols, model)

    lst = list(symbols)
    #print lst
    p = lst.pop(0)
    #print "Thiiiis is p", p
    rest1 = set(lst)
    rest2 = deepcopy(rest1)
    model1 = deepcopy(model)
    model2 = deepcopy(model)

    model1[p] = True
    if (p[0] != "~"):
        p_complement = "~" + p
        #print "This is p complement", p_complement
        if p_complement in symbols:
            rest1.remove(p_complement)
    else:
        y = p.split("~")
        p_complement = y[1]
        if p_complement in symbols:
            rest1.remove(p_complement)
    model1[p_complement]=False
    flag = DPLL(clauses,rest1,model1)
    if flag == True:
        return True

    model2[p] = False
    if (p[0] != "~"):
        p_complement = "~" + p
        if p_complement in symbols:
            rest2.remove(p_complement)
    else:
        y = p.split("~")
        p_complement = y[1]
        if p_complement in symbols:
            rest2.remove(p_complement)
    model2[p_complement]=True
    flag = DPLL(clauses, rest2, model2)
    if flag == True:
        return True

    return False

def DPLL_Satisfiable(clauses):
    for i in clauses:
            for sym in i:
                symbols.add(sym)
    #print symbols
    return DPLL(clauses, symbols, {})


def cnf(guests,tables):
    temp_list=[]
    temp_clause=set()

    for i in range(1,guests+1):
        for j in range(1,tables+1):
            a="X"+str(i)+str(j)
            temp_list.append(a)
        temp_clause.add(tuple(temp_list))
        temp_list=[]
    #print temp_clause

    for i in range(1,guests+1):
        temp_list = []
        for j in range(1,tables+1):
            for k in range(j+1, tables + 1):
                a=("~"+"X"+str(i)+str(j),"~"+"X"+str(i)+str(k))
                #temp_list.append(a)
                temp_clause.add(a)
        #temp_list=[]
    #print temp_clause

    for i in friends_list:
                    for j in range(1,tables+1):

                        a="~"+"X"+str(i[0])+str(j)
                        b="X"+str(i[1])+str(j)
                        temp_list.append(a)
                        temp_list.append(b)
                        temp_clause.add(tuple(temp_list))
                        temp_list = []
                        c="~"+"X"+str(i[1])+str(j)
                        d="X"+str(i[0])+str(j)
                        temp_list.append(c)
                        temp_list.append(d)
                        temp_clause.add(tuple(temp_list))
                        temp_list = []

    #print temp_clause

    for i in enemies_list:
        for j in range(1, tables + 1):
            a = "~" + "X" + str(i[0]) + str(j)
            b = "~" + "X" + str(i[1]) + str(j)
            temp_list.append(a)
            temp_list.append(b)
            temp_clause.add(tuple(temp_list))
            temp_list =[]

    #print temp_clause
    #for i in temp_clause:
        #global count
        #count+=1
    #print count

    return DPLL_Satisfiable(temp_clause)
#print guests, tables

if(guests==0 or tables==0):
    with open("output.txt", "w") as fh:
        fh.write("no")

else:
    sol=cnf(guests,tables)




    #print "final arrangement", arrangement
    for key in arrangement:
        if(arrangement[key]==True):
            true_values.append(key)
    #print true_values
    for x in true_values:
        if(x[0]=='~'):
            continue
        else:
            xyz.append(x)
    #print xyz
    xyz.sort()
    #print xyz
    #print sol

    with open("output.txt", "w") as fh:
        if (sol==False):
            fh.write("no")
        else:
            fh.write("yes\n")
            for a in xyz:
                if (len(a) == 3):
                    fh.write(a[1]+" "+a[2])
                    fh.write("\n")
                elif ((len(a) == 4) and guests >= 10 and guests<100 and tables < 10):
                    fh.write(a[1]+a[2]+" "+a[3])
                    fh.write("\n")
                elif ((len(a) == 4) and guests < 10 and tables >= 10 and tables<100):
                    fh.write(a[1]+" "+a[2]+a[3])
                    fh.write("\n")
                elif ((len(a)==5) and guests>=10 and guests<100 and tables>=10 and tables<100):
                    fh.write(a[1]+a[2]+" "+a[3]+a[4])
                    fh.write("\n")
                elif ((len(a)==5) and guests>=100 and tables<10):
                    fh.write(a[1]+a[2]+a[3]+" "+a[4])
                    fh.write("\n")
                elif ((len(a)==5) and guests<10 and tables>=100):
                    fh.write(a[1]+" "+a[2]+a[3]+a[4])
                    fh.write("\n")
                elif ((len(a)==6) and guests>=10 and guests<100 and tables>=100):
                    fh.write(a[1]+a[2]+" "+a[3]+a[4]+a[5])
                    fh.write("\n")
                elif ((len(a) == 6) and guests>=100 and tables >= 10 and tables < 100):
                    fh.write(a[1]+a[2]+a[3]+" "+a[4]+a[5])
                    fh.write("\n")
                else:
                    fh.write(a[1]+a[2]+a[3]+" "+a[4]+a[5]+a[6])
                    fh.write("\n")






