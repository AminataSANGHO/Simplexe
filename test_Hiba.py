import re
import numpy as np

def get_equation():
    b=[]
    liste2=[]
    liste_pour_les_ecarts = dict()
    a=input('entrez max ou min') #si max les parametres entres seront affectees a la fonction simpl max
    fct_obj= re.split(r'[+]', a)
    lis_fct_obj=list()
    for i in range(len(fct_obj)):
        if fct_obj[i]=='':
            continue
        if fct_obj[i][0]=='-':
            a=int(fct_obj[i][:fct_obj[i].index('x')])
        else:
            a = int(fct_obj[i][:fct_obj[i].index('x')])
        lis_fct_obj.append(a)

    a=input('entrez votre equation')
    s=0
    while a!='q':
        if '>' in a:
            liste_pour_les_ecarts[s]=True
        if '<' in a:
            liste_pour_les_ecarts[s]=False
        result = re.split(r'[<>+=]|>=|<=', a)
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
        a=input('entrez equation ou q pour terminer : ')
    
    taille_contra=len(liste2[0])
    liste_indice_ajout_zerneg=[]
    n=len(liste2)
    nbr_var_hors_base=len(liste2[0])
    zer=np.eye(n, dtype=int)

    for k,v in liste_pour_les_ecarts.items():
        if v == False:
            liste2[k].extend(zer[k])
        else:
            liste2[k].extend(-zer[k])
            liste_indice_ajout_zerneg.append(k)

    l=len(liste_indice_ajout_zerneg)
    #zero=[[1,0,0],[0,1,0],[0,0,1]]
    nbr_e=len(liste2[0])-nbr_var_hors_base

    if l != 0:
        #mi = iter(liste_indice_ajout_zerneg)
        for k in liste_indice_ajout_zerneg:
            for j in range(n):
                liste2[j].append(zer[j][k])
                
    z=np.zeros(len(liste2[0])-len(lis_fct_obj),dtype=int)
    lis_fct_obj.extend(z) 
    nbr_var_a=len(liste2[0])-nbr_var_hors_base-nbr_e
    return np.array(liste2),np.array(b),np.array(lis_fct_obj),n,taille_contra,nbr_var_hors_base,nbr_e,nbr_var_a,liste_indice_ajout_zerneg


get_equation()