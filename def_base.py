import pandas as pd
import numpy as np
import math

def find_newcomer(df,dict1,dict2):
    fail=0
    for p in df['Numer karty'].unique():
        if p in dict1.keys():
            pass
        else:
            print('Brakujący element: {}'.format(p))
            fail=1
    for q in df['Grupa produktowa'].unique():
        if q in dict2.keys():
            pass
        elif str(q)=='nan':
            pass
        else:
            print('Brakujący element: {}'.format(q))
            fail = 1
    if fail==1:
        print('PRZERWANIE OPERACJI: Wymagane uzupełnienie')
        exit()



def car_miss(df, dict):
    l=dict.keys()
    for element in l:
        df.loc[df['Numer karty']==element,'Nr rejestracyjny / Imię i nazwisko']=dict[element]

def car_size(df, lista1, lista2):
    df['Rozmiar']=np.nan
    for element in lista1:
        df.loc[df['Nr rejestracyjny / Imię i nazwisko']==element,'Rozmiar']=0.5
    for el2 in lista2:
        df.loc[df['Nr rejestracyjny / Imię i nazwisko']==el2,'Rozmiar']=1


def vat_i_brutto_fix(df):
    df['Brutto']=df['Brutto'].str.replace(',','.')
    df['Netto'] = df['Wartosc netto'].str.replace(',', '.')
    df['Stawka Vat']=df['Stopa VAT']
    df.loc[df['Stopa VAT']=='ZW','Stawka Vat']= 0
    df.loc[df['Stopa VAT'] == 'ND', 'Stawka Vat'] = 0
    df['Stawka Vat']=pd.to_numeric(df['Stawka Vat'])
    df['Brutto']=pd.to_numeric(df['Brutto'])
    df['Netto'] = pd.to_numeric(df['Netto'])
    df['Vat']=df['Brutto']-df['Netto']

def account_pull(df, dict):
    df['Konto']=np.zeros(df['Brutto'].size)
    for el in (df['Grupa produktowa'].unique()):
        if dict[el]=='PALIWO':
            df.loc[(df['Rozmiar'] == 1) & (df['Grupa produktowa'] == el),'Konto']= '508-01-003C'
            df.loc[(df['Rozmiar'] == 0.5) & (df['Grupa produktowa'] == el), 'Konto'] = '550-01-006OSOB'
            df.loc[(df['Rozmiar'] == 1) & (df['Grupa produktowa'] == el) & (df['Nr rejestracyjny / Imię i nazwisko'] == 'EL8G506'), 'Konto'] = '503-01-01-003C'
        elif dict[el]=='OPŁATA MANIPULACYJNA/ OPŁATA ZA KORZYSTANIE Z KARTY':
            df.loc[(df['Rozmiar'] == 1) & (df['Grupa produktowa'] == el),'Konto'] = '550-02-004C'
            df.loc[(df['Rozmiar'] == 0.5) & (df['Grupa produktowa'] == el), 'Konto'] = '550-02-004OSOB'
        elif dict[el]=='VIATOLL/OPŁATY DROGOWE/AUTOSTRADY':
            df.loc[(df['Rozmiar'] == 1) & (df['Grupa produktowa'] == el),'Konto'] = '508-06-001'
            df.loc[(df['Rozmiar'] == 0.5) & (df['Grupa produktowa'] == el), 'Konto'] = '550-06-001'
            df.loc[(df['Rozmiar'] == 1) & (df['Grupa produktowa'] == el) & (df['Nr rejestracyjny / Imię i nazwisko']=='EL8G506'),'Konto']='503-01-06-002'
        elif dict[el]=='PŁYNY EKSPLOATACYJNE/OLEJE SILNIKOWE/INNE PRODUKTY':
            df.loc[(df['Rozmiar'] == 1) & (df['Grupa produktowa'] == el),'Konto'] = '508-01-004C'
            df.loc[(df['Rozmiar'] == 0.5) & (df['Grupa produktowa'] == el), 'Konto'] = '550-01-008OSOB'
            df.loc[(df['Rozmiar'] == 1) & (df['Grupa produktowa'] == el) & (df['Nr rejestracyjny / Imię i nazwisko'] == 'EL8G506'), 'Konto'] = '503-01-01-004C'
        elif dict[el]=='MYJNIA':
            df.loc[(df['Rozmiar'] == 1) & (df['Grupa produktowa'] == el),'Konto'] = '508-02-001C'
            df.loc[(df['Rozmiar'] == 0.5) & (df['Grupa produktowa'] == el), 'Konto'] = '550-02-004OSOB'
            df.loc[(df['Rozmiar'] == 1) & (df['Grupa produktowa'] == el) & (df['Nr rejestracyjny / Imię i nazwisko'] == 'EL8G506'), 'Konto'] = '503-01-02-002C'

def odlicz(df):
    df['Odliczenie'] = 'NIE'
    df.loc[(df['Rozmiar'] == 1) & (df['Stawka Vat'] !=0), 'Odliczenie'] = 'TAK'
    df.loc[(df['Rozmiar']==0.5),'Netto']=df['Netto']/2
    df.loc[(df['Rozmiar'] == 0.5), 'Brutto'] = df['Brutto'] / 2
    df.loc[(df['Rozmiar'] == 0.5), 'Vat'] = df['Vat'] / 2
    ex_natak=df.loc[(df['Rozmiar'] == 0.5)]
    ex_natak.loc[(df['Rozmiar'] == 0.5) & (df['Stawka Vat'] != 0), 'Odliczenie']='TAK'
    return pd.concat([df,ex_natak])

def transfer_grosza(df):
    df['Brutto'] = df['Brutto'].round(3)
    df['Netto'] = df['Netto'].round(3)
    df['Vat'] = df['Vat'].round(3)

    for k in ['Vat']:
        for i in df.loc[df['Odliczenie']=='NIE',k]:
            if 100*i - math.floor(100*i) == 0.005 :
                df.loc[(df['Odliczenie']=='TAK')&(df[k]==i),k]-=0.005
                df.loc[(df['Odliczenie'] == 'NIE') & (df[k] == i), k] += 0.005

def podsumowanie(df):
    tab = df
    lista = []
    kody = df['Konto'].unique()
    stawki = df['Stopa VAT'].unique()
    zasoby = ['Netto', 'Vat', 'Brutto']

    for pl in kody:
        for p in stawki:
            for k in zasoby:
                x = tab.loc[(tab['Konto'] == pl) & (tab['Stopa VAT'] == p), k].sum()
                lista.append([pl, p, k, x])
    return lista