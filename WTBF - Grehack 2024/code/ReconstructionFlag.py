tab = [214, 217, 114, 232, 148, 75, 45, 136, 199, 69, 145, 102, 148,75, 54, 100, 120]

pas = ""
for i in range(len(tab)) :
    x = (tab[i]-1)/3;
    
    if(round(x)!=x) :
        x = (tab[i]+255)/3;
    pas += chr(int(x))

print(pas)