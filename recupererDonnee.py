#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 21:13:01 2017
Qqs fonction pour formater les adresses
peut-être inutile...
@author: romain
"""
import classeProjet as cP
import pandas as pd
import unidecode


class ListeError(FileNotFoundError):
    def __init__(self,file,typeP):
        FileNotFoundError.__init__(self)
        self.file = file
        self.typeP = typeP
    
    def __str__(self):
        return ("le fichier %s  pour créer la liste %s n'existe pas"%(self.file,self.typeP))
    
class ListeEtuError(ListeError):
    def __init__(self,file):
        ListeError.__init__(self,file,"d'étudiants")
        
class ListeFormError(ListeError):
    def __init__(self,file):
        ListeError.__init__(self,file,"de formateurs")
        
class PasAuNorme(KeyError):
    def __init__(self, file, typeP,forma):
        KeyError.__init__(self)
        self.file = file
        self.typeP = typeP
        self.format = forma
    
    def __str__(self):
        return ("le fichier %s pour creer des %s doit avoir la forme: %s,tc,stage"%(self.file,self.typeP,self.format))
    
class PasAuNormeEtu(PasAuNorme):
    def __init__(self,file):
        PasAuNorme.__init__(self,file,"étudiants","nomE,adresseE")
        
class PasAuNormeForm(PasAuNorme):
    def __init__(self,file):
        PasAuNorme.__init__(self,file,"formateurs","nomF,adresseF")
        


def _formater2(s):
    tmp = s
    enlever =['(',')',';',':']
    for elem in enlever:
        tmp = tmp.replace(elem,'')
    tmp = tmp.split(' ')
    res = tuple((float(x) for x in tmp if x != '' ))
    if len(res) != 2:
        raise ValueError
    return res

def _formater(s):
    res = unidecode.unidecode(s)
    res = res.replace(' ','+')
    return res
        
"""
def formaterAdresse(L):
    res = []
    for elem in L:
        res.append(_formater(elem))
    return res
"""

def makeListeEtudiant(fichier):
    try:
        txt = pd.read_excel(fichier,sep=',')
    except FileNotFoundError:
        raise ListeEtuError(fichier)
    try:
        stage = list(map(int,txt['stage']))
        nom = list(txt['Nom E'])
        prenom = list(txt["Prenom E"])
#        adresse = list(map(_formater,txt['adresseE']))
        adresse = list(txt['Adresse E'])
        ville = list(txt['Ville E'])
        typeClasse = list(txt['TC'])
    except KeyError:
        raise PasAuNormeEtu(fichier)
    donne = zip(nom,adresse,ville,typeClasse,stage,prenom)
    res = list()
    for n,a,v,t,s,p in donne:
        if str(a) == 'nan':
            a = ''
        res.append(cP.Etudiant(n+ ' '+p,a+ ' ' + v,t,s))
    return res

def makeListeFormateur(fichier):
    try:
        txt = pd.read_excel(fichier,sep=',')
    except FileNotFoundError:
        raise ListeFormError(fichier)
    try:
        stage = list(map(int,txt['stage']))
        nom = list(txt['Nom F'])
        ville = list(txt['Ville F'])
        typeClasse = list(txt['TC'])
        priorite = list(txt['priorite'])
    except KeyError:
        raise PasAuNormeForm(fichier)
    donne = zip(nom,ville,typeClasse,stage,priorite)
    res = list()
    for n,v,t,s,p in donne:
        res.append(cP.Formateur(n,v,t,s,p))
    return res

def makeStage2(fichierE, fichierF):
    listeE = makeListeEtudiant(fichierE)
    listeF = makeListeFormateur(fichierF)
    res=dict()
    for i in range(1,7):
        try:
            res[i]=cP.Stage(i,listeE[i],listeF[i])
        except KeyError:
            try:
                res[i]=cP.Stage(i,None,listeF[i])
            except KeyError:
                try:
                    res[i]=cP.Stage(i,listeE[i],None)
                except KeyError:
                    res[i]=cP.Stage(i,None,None)
    return res

def makeStage(*args):
    lE = []
    lF = []
    for arg in args:
        try:
            etu = makeListeEtudiant(arg)
            lE += etu
        except PasAuNormeEtu:
            try:
                form = makeListeFormateur(arg)
                lF += form
            except PasAuNormeForm:
                raise ValueError("le fichier %s n'est pas aux normes, rappel "%(arg) +  
                                " pour un étudiant nome E,adresse E,TC,stage" + 
                                " pour un formateur nom F,adresse F,TC,stage ")
    return cP.Stages(lE,lF)


if __name__ == '__main__':

#    E = makeListeEtudiant('stage4E.txt')
#    F = makeListeFormateur('stage4F.txt')
#    print("etu",E)
#    print("-"*30)
#    print("form",F)
#    print(_formater('(2  1)'))
#    print(makeStage2('stage4E.txt','stage4F.txt'))
    print(_formater("savièse"))
#    test= pd.read_excel('liste adresse.xlsx')
#    for x in test:
#        print(x)
#    print(test['TC'])