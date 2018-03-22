def expr(lis):
    l=list(lis)

    for k in range(0,len(l)):

        #logical operations:
        if(l[k]=='>' and l[k]=='='):
            if(l[k-1]>=l[k+1]):
                return True
            else:
                return False
        elif(l[k]=='<' and l[k+1]=='='):
            if(l[k-1]<=l[k+1]):
                return True
            else:
                return False
        elif(l[k]=='>'):
            if(l[k-1]>l[k+1]):
                return True
            else:
                return False

        elif(l[k]=='<'):
            if(l[k-1]<l[k+1]):
                return True
            else:
                return False

        elif(l[k]=='='):
            if(l[k+1]=='='):
                if(l[k-1]==l[k+2]):
                    return True
                else:
                    return False





