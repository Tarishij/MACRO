import sys
import evaluate
f1=open(sys.argv[1],"r")
f3=open("namtab.txt","w")
f4=open("definetab.txt","w")
f5=open("output.txt","w")

l1=f1.read()
# reading lines of input file
s1=l1.split("\n")
l1=len(s1)


for i in range(0,l1):

    if('!#' in s1[i]):

        continue

    count=0
    #if a line contains macro definition
    if("MACRO" in s1[i]):


        p1=s1[i].split( )

        #populate name table
        f3.write(p1[0]+"\n")

        #populate define table


        for j in range(i,l1):
            if('!#' in s1[j]):
                continue

            if ("MEND" in s1[j]):

                #to count the number of levels
                count-=1

                #if outer macro's end is reached (in nested macro)
                if(count==0):
                    f4.write("...\n")       #to show ending of macro definition
                    break
            else:
              #nested macro
                if("MACRO" in s1[j]):
                    p1=s1[j].split("MACRO")

                    count+=1
                    #writing name of macro
                    f4.write(p1[0])


                    #writing arguments,if any
                    if(len(p1)>=2):

                        f4.write(p1[1])
                    f4.write("\n")


                #searching for lines containing operations on arguments
                elif("&" in s1[j]):
                    p1=s1[j].split( )
                    length=len(p1)
                    for k in range(0,length):
                        if("&" in p1[k]):

                            line=p1[k].split("&")

                            li=list(line[1])

                            kop=line[1]

                            f4.write(line[0]+"?"+li[3]+kop[4:])


                            if(k==length-1):

                                f4.write("\n")
                        else:
                            f4.write(p1[k]+" ")
                else:

                    f4.write(s1[j]+"\n")



    #writing main body in output file
    elif("Main" in s1[i]):
        f3.close()
        f4.close()
        f3=open("namtab.txt","r")
        l3=f3.read()
    #reading name table line by line
        s3=l3.split("\n")
        l3=len(s3)-1

        #entering the Main body:
        for j in range(i,l1):
            if("!#" in s1[j]):
                continue

            flag=0
            for k in range(0,l3):

                #if macro name (call) is found
                if(s3[k] in s1[j]):
                    flag=1

                    #populating argtab

                    #splitting for extracting parameters
                    word=s1[j].split( )

                    for t in range(0,len(word)):
                        if(s3[k] in word[t]):
                            break
                        else:
                            f5.write(word[t]+" ")

                    we=word[t].split(s3[k])

                    pa=list(we[1])

                    #for single line macro
                    if(len(pa)>=2 and pa[0]=="(" and pa[1]==')'):
                        f4=open("definetab.txt","r")
                        l4=f4.read()
                        s4=l4.split("\n")
                        for ik in range (0,len(s4)):
                            if(s3[k] in s4[ik]):
                                g=s4[ik].split()

                                h=we[1]

                                f5.write(we[0]+g[1]+h[2:]+"\n")



                                f4.close()
                                break


                    else:

                        len1=len(word)

                    #for parameter

                        if(len1>1):
                            f2=open("arg.txt","w")

                            m=word[1].split('(', 1)[1].split(')')[0]


                            pj=m.split(",")

                        #writing parameters in argument table
                            for n in range(0,len(pj)):

                                #for default parameters
                                if(pj[n]==''):

                                    #open define tab to get the default argument
                                    f4=open("definetab.txt","r")
                                    l4=f4.read()
                                    s4=l4.split("\n")
                                    for hu in range(0,len(s4)):

                                        #if that macro definition is found
                                        if(s3[k] in s4[hu]):
                                            t="&arg"+str(n+1)

                                            tu=s4[hu].split(t)

                                            #get the position of arg value
                                            df=list(tu[1])

                                            #get that arg value
                                            for y in range(0,len(df)):
                                                if(df[y]=='='):

                                                    #writing the default value in argument table
                                                    f2.write(df[y+1]+"\n")
                                                    break
                                            break

                                    f4.close()
                                else:
                                    f2.write(pj[n]+"\n")

                            f2.close()




                    #open definetab to expand the macro call
                    f4=open("definetab.txt","r")
                    l4=f4.read()

                    #splitting in lines
                    s4=l4.split("\n")
                    l4=len(s4)-1
                    for m in range(0,l4):

                        #searching for that macro definition in deftab
                        if s3[k] in s4[m] :
                            m=m+1
                            fr=0


                            #read defintion until macro end is not reached
                            while(s4[m]!="..."):

                                fr=0

                                for r in range (0,len(s3)-1):

                                    if(s3[r] in s4[m]):
                                        m=m+1
                                        fr=1
                                        break
                                if fr==1:
                                    continue

                                #conditional macro:
                                if("if(" in s4[m]):
                                    d=open("helper.txt","w")




                                    p4=s4[m].split( )
                                    len4=len(p4)
                                    for le in range(0,len4):
                                    #writing in helper file

                                        if "?" in p4[le] :

                                            #searching for parameter in argtable
                                            f2=open("arg.txt","r")
                                            l2=f2.read()

                                            #splitting argtab in lines
                                            s2=l2.split("\n")

                                            p=p4[le].split("?")
                                            d.write(p[0])

                                            #taking argument number
                                            kl=int(p[1][0])

                                            #specifying the parameter index
                                            d.write(s2[kl-1])

                                            d.write(p[1][1:])
                                            if(le==len4-1):
                                                d.write("\n")

                                        else:
                                            #writing the operation to be performed on parameters

                                            d.write(p4[le]+" ")
                                    m=m+1
                                    d.close()

                                    #open it in read mode
                                    d=open("helper.txt","r")

                                    sd=d.read()
                                    asd=sd.split("\n")
                                    ls=asd[0].split("if(")
                                    ls=ls[1]
                                    ls=ls[:-1]

                                    #get that expression
                                    ls=ls.replace(' ','')


                                    #function expr will evaluate the expression and returns true or false
                                    value=evaluate.expr(ls)



                                    #if condition is true:
                                    if(value):

                                        #copy the if part

                                        while (s4[m]!="else"):

                                            if("?" in s4[m]):
                                                p4=s4[m].split( )
                                                len4=len(p4)
                                                for le in range(0,len4):

                                                    if "?" in p4[le] :

                                            #searching for parameter in argtable
                                                        f2=open("arg.txt","r")
                                                        l2=f2.read()

                                            #splitting argtab in lines
                                                        s2=l2.split("\n")

                                                        p=p4[le].split("?")
                                                        f5.write(p[0])

                                             #taking argument number
                                                        kl=int(p[1][0])

                                            #specifying the parameter index
                                                        f5.write(s2[kl-1])

                                                        f5.write(p[1][1:])
                                                        #if(le==len4-1):
                                                         #   f5.write("\n")

                                                    else:
                                            #writing the operation to be performed on parameters

                                                        f5.write(p4[le]+" ")
                                                m=m+1
                                            else:
                                    #writing remaining def lines which does not reqiure parameters
                                                f5.write(s4[m]+"\n")
                                                m=m+1

                                        m=m+1

                                        #skip else part
                                        while(s4[m]!="endif"):
                                            m=m+1

                                        #skip keyword endif
                                        m=m+1

                                    #if condition is false,move to the else part
                                    else:

                                        while(s4[m]!="else"):
                                            m=m+1
                                        m=m+1

                                        while(s4[m]!="endif"):
                                            #copy else part
                                            if("?" in s4[m]):
                                                p4=s4[m].split( )
                                                len4=len(p4)
                                                for le in range(0,len4):

                                                    if "?" in p4[le] :
                                                        #searching for parameter in argtable
                                                        f2=open("arg.txt","r")
                                                        l2=f2.read()

                                                        #splitting argtab in lines
                                                        s2=l2.split("\n")

                                                        p=p4[le].split("?")
                                                        f5.write(p[0])

                                            #taking argument number
                                                        kl=int(p[1][0])

                                                      #specifying the parameter index
                                                        f5.write(s2[kl-1])

                                                        f5.write(p[1][1:])

                                                    else:
                                                        #writing the operation to be performed on parameters

                                                        f5.write(p4[le]+" ")
                                                m=m+1
                                            else:
                                                #writing remaining def lines which does not reqiure parameters
                                                f5.write(s4[m]+"\n")
                                                m=m+1

                                        m=m+1







                                #replacing parameter,if found
                                if("?" in s4[m]):
                                    p4=s4[m].split( )
                                    len4=len(p4)
                                    for le in range(0,len4):

                                        if "?" in p4[le] :

                                            #searching for parameter in argtable
                                            f2=open("arg.txt","r")
                                            l2=f2.read()

                                            #splitting argtab in lines
                                            s2=l2.split("\n")

                                            p=p4[le].split("?")
                                            f5.write(p[0])

                                            #taking argument number
                                            kl=int(p[1][0])

                                            #specifying the parameter index
                                            f5.write(s2[kl-1])

                                            f5.write(p[1][1:])
                                            if(le==len4-1):
                                                f5.write("\n")

                                        else:
                                            #writing the operation to be performed on parameters

                                            f5.write(p4[le]+" ")
                                    m=m+1
                                else:
                                    #writing remaining def lines which does not reqiure parameters
                                    f5.write(s4[m]+"\n")
                                    m=m+1
            if(flag==0) :

                #write the remaining code in output
                f5.write(s1[j]+"\n")
