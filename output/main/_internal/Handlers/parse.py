def parse(func):
        vars=[]
        l=len(func)
        i=0
        while i<l:
            if ord(func[i])==ord('x'):
                j=i+2
                while j<l and ord(func[j])>=ord('0') and ord(func[j])<=ord('9'):
                    j+=1
                j+=1
                if func[i:j] not in vars:
                    vars.append(func[i:j])
                i=j
            i+=1
        return sorted(vars)