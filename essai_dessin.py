import matplotlib.pyplot as plt
import re
import copy
import numpy as np
from IPyton import get_ipython
get_ipython().run_line_magic('matplotlib','qt')


def traitement_dessin(max_min,f_obj,liste_contraintes):
    
    
    b=[]
    liste2=[]
    liste_pour_les_ecarts = dict()
    liste_inf_super=[]    
    
    #Traitement sur la fonction obj : extraction des couts
    fct_obj= re.split(r'[+]', f_obj)
    lis_fct_obj=list()
    for i in range(len(fct_obj)):
        if fct_obj[i]=='':
            continue
        if fct_obj[i][0]=='-':
            a=int(fct_obj[i][:fct_obj[i].index('x')])
        else:
            a = int(fct_obj[i][:fct_obj[i].index('x')])
        lis_fct_obj.append(a)
        
    #Traitement sur les contraintes  : extraction des coeffs
    
    s=0
    for contr in liste_contraintes:
        if '=' in contr:
            liste_pour_les_ecarts[s]=2
        if '>=' in contr:
            liste_pour_les_ecarts[s]=True
            liste_inf_super.append('>')
        if '<=' in contr:
            liste_pour_les_ecarts[s]=False
            liste_inf_super.append('<')

        result = re.split(r'[<>+=]|>=|<=', contr)
        b.append(int(result[-1]))
        result1=result.pop(-1)
        l=list()
        for i in range(len(result)):
            if result[i]=='':
                continue
            if result[i][0]=='-':
                a=int(result[i][:result[i].index('x')])
            else:
                a = int(result[i][:result[i].index('x')])
            l.append(a)
        liste2.append(l)
        s=s+1
        
    A=copy.deepcopy(liste2)
    v=np.array(A)
    trans=v.T
    p=trans.shape[1]
    for su in range(p):
        if trans[1,su]<0:
            if liste_inf_super[su]=='<':
                liste_inf_super[su]='>'
            else:
                liste_inf_super[su]='<'
                
    return A,b,liste_inf_super,liste_contraintes





def dessin(A,b,liste_inf,liste_contraintes):
    l_min_max=liste_inf
    xb = np.transpose([b])

    # combine matrices B and cb
    l = np.hstack((A, xb))
    l=np.array(l,dtype=object)
    
    x = np.linspace(0, 20, 2000)

    list_ou_zero=[]
    #l =np.array([[5,3,30],[2,3,24],[1,3,18]],dtype=object) 
    #l_min_max=['<','<','<']
    signe_sup=[]
    liste_signe_nbt=[]
    a=l.T
    p=a.shape[1]
    #print(p)
    l_min_max1=[]
    l_ind_signe=[]


    for s in range(p):
        if a[1,s]==0:
            list_ou_zero.append(s)
            signe_sup.append(l_min_max[s])

    #print(list_ou_zero)
    for e in range(len(l_min_max)): 
        if e not in list_ou_zero:
            l_min_max1.append(l_min_max[e])


    a_del=l

    cop=list_ou_zero[:]
    for k in range(1,len(cop)):
        cop[k]=cop[k]-1


    #print('apres',list_ou_zero)

    if len(cop)!=0:
        una_listamin1=[]
        una_listamax1=[]
        for j in cop:
            a_del=np.delete(a_del,j,0)

        #print(a_del)
        for m in a_del:
            m[0]=m[0]*x  


        ka1=(a_del[:,-1]-a_del[:,0])/a_del[:,1]
        i=0
        for k in ka1:       
            if l_min_max1[i]=='<':
                una_listamin1.append(k)
            elif l_min_max1[i]=='>':
                una_listamax1.append(k)
            plt.plot(x, k, label=r'y >= 2')
            i=i+1

        lu=4*np.ones(2000)
        '''
        plt.plot(lu,x, label=r'y >= 2')    
        plt.fill_between(x,lu,10,where=x>4, color='grey', alpha=0.5)    



        for u in list_ou_zero:
            #signe_sup[r]=='<':
            #una_listamin1.append(k)
            print('supprime : ',l[u])
            nbr=l[u][-1]/l[u][0]
            print(nbr)
            plt.axvline(nbr, 0, 20, label='pyplot horizontal line')
            plt.fill_between(x,100,where=x<4, color='grey', alpha=0.5) ''' 

        #print(list_ou_zero)
        r=0
        for u in list_ou_zero:
            nbr=l[u][-1]/l[u][0]
            #print(l[u])
            if signe_sup[r]=='<':
                #plt.fill_between(x,100,where=x<4, color='grey', alpha=0.5)
                liste_signe_nbt.append(('<',nbr))
            elif signe_sup[r]=='>':
                liste_signe_nbt.append(('>',nbr))
            #print('supprime : ',l[u])

            #print(nbr)
            plt.axvline(nbr, 0, 20, label='pyplot horizontal line')
            #plt.fill_between(x,100,where=x<4, color='grey', alpha=0.5)
            r=r+1



        
        plt.xlim((0, 16))
        plt.ylim((0, 11))




        maxi=10000*np.ones(2000)
        mini=np.zeros(2000)
       
        fl1=0
        fl2=0

        y5 = maxi
        for i in range(len(una_listamin1)):
            y5 = np.minimum(y5,una_listamin1[i])
            fl1=1


        y6 = mini
        for i in range(len(una_listamax1)):
            y6 = np.maximum(y6,una_listamax1[i])
            fl2=1

        #print(y5) 
         
        a=True                               
        for gh in liste_signe_nbt:
            if gh[0]=='<': 
                a=a&(x<gh[1])
            if gh[0]=='>': 
                a=a&(x>gh[1])

        if fl1==0 and fl2==1:
            plt.fill_between(x, y6,100,where=a, color='grey', alpha=0.5)
        #shi=x<4
        #print(shi)
        if fl2==0 and fl1==1:
            #y=np.linspace(0, 4, 2000)
            plt.fill_between(x, y5,0,where=a,color='grey', alpha=0.5)
        if fl1==1 and fl2==1:
            plt.fill_between(x, y5, y6, where=y5>y6, color='grey', alpha=0.5)


        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        #============================================================================================

    else:

        for m in l:
            m[0]=m[0]*x

        una_listamin=[]
        una_listamax=[]
        #print(l)
        #print(x-1)

        #l[:,0]=l[:,0]*x

        ka=(l[:,-1]-l[:,0])/l[:,1]

        i=0
        for k in ka:
            if l_min_max[i]=='<':
                una_listamin.append(k)
            elif l_min_max[i]=='>':
                una_listamax.append(k)
            plt.plot(x, k, label=liste_contraintes[i])
            i=i+1

        lu=[4,4,4,4,4,4,4,4,4,4]   
        h=np.linspace(0, 15, 10)
        #plt.plot(lu,h, label=r'y >= 2')
        #print(np.linspace(4, 15, 10))
        #t=np.linspace(4, 15, 10)
        #plt.plot(t,t, label=r'y >= 2')


        plt.xlim((0, 10))
        plt.ylim((0, 15))
        plt.xlabel(r'x')
        plt.ylabel(r'$y')


        # Fill feasible region
        maxi=10000*np.ones(2000)
        mini=np.zeros(2000)
        #print(len(una_listamin))
        #print(len(una_listamax))
        #print(mini)
        #print(maxi)
        fl1=0
        fl2=0

        y5 = maxi
        for i in range(len(una_listamin)):
            y5 = np.minimum(y5,una_listamin[i])
            fl1=1


        y6 = mini
        for i in range(len(una_listamax)):
            y6 = np.maximum(y6,una_listamax[i])
            fl2=1

        #print(y5) 
        #print(y6)    

        if fl1==0 and fl2==1:
            #plt.fill_between(x,100,where=x<4, color='grey', alpha=0.5)
            plt.fill_between(x, y6,100, color='grey', alpha=0.5)

        if fl2==0 and fl1==1:
            #plt.fill_between(x,100,where=x<4, color='grey', alpha=0.5)
            plt.fill_between(x, y5,0, color='grey', alpha=0.5)
        if fl1==1 and fl2==1:
            plt.fill_between(x, y5, y6, where=y5>y6, color='grey', alpha=0.5)


        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

max_min='min'
f_obj='3x1+-6x2'
#liste_contraintes=['5x1+3x2<=30','2x1+3x2<=24','1x1+3x2<=18']
liste_contraintes=['  -1x1+-2x2<=1','  -2x1+-1x2<=0','  -1x1+1x2<=1','-1x1+4x2<=13','4x1+-1x2<=23']
A,b,liste_inf,liste_contra=traitement_dessin(max_min,f_obj,liste_contraintes)
dessin(A,b,liste_inf,liste_contra)