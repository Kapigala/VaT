import pandas as pd
from def_base import car_miss,car_size,vat_i_brutto_fix,account_pull,odlicz,transfer_grosza,podsumowanie
from datetime import date
pd.options.mode.chained_assignment = None  # default='warn'

#Listy,Słowniki
attribute={'OLEJ NAPĘDOWY': 'PALIWO', 'LPG': 'PALIWO', 'GAZ PLYNNY       LTR': 'PALIWO',
               'BENZYNA EUROSUPER 95':'PALIWO','OLEJ NAPĘDOWY VERVA':'PALIWO','OLEJ NAPEDOWY    LTR':'PALIWO',
               'Opłata za korzystanie z karty':'OPŁATA MANIPULACYJNA/ OPŁATA ZA KORZYSTANIE Z KARTY',
               'Opłata manipulacyjna - droga płatna':'OPŁATA MANIPULACYJNA/ OPŁATA ZA KORZYSTANIE Z KARTY',
               'OPL. DROGOWE SZT':'VIATOLL/OPŁATY DROGOWE/AUTOSTRADY',
               'OPŁATY ZA AUTOSTRADY':'VIATOLL/OPŁATY DROGOWE/AUTOSTRADY',
           'VIATOLL/AUTO - OPŁATA DROGOWA':'VIATOLL/OPŁATY DROGOWE/AUTOSTRADY',
           'INNE PRODUKTY/TIS PL SZT':'PŁYNY EKSPLOATACYJNE/OLEJE SILNIKOWE/INNE PRODUKTY',
           'PŁYNY EKSPLOATACYJNE':'PŁYNY EKSPLOATACYJNE/OLEJE SILNIKOWE/INNE PRODUKTY',
           'KOSMETYKI SAMOCHODOWE':'PŁYNY EKSPLOATACYJNE/OLEJE SILNIKOWE/INNE PRODUKTY',
           'AKCESORIA SAMOCHODOWE':'PŁYNY EKSPLOATACYJNE/OLEJE SILNIKOWE/INNE PRODUKTY',
           'USŁUGI SAMOCHODOWE':'MYJNIA'}
card_code={78971516571135926: 'EL6T641', 201924: 'WW094SE', 78971516571135892: 'WB2733U',
           78971516571151378:'WZ977OY', 78971516571135918:'EL6T639', 219777:'DW1JY97',
           78971516571151386:'WW094SE', 78971516571135900:'WB2734U', 78971516724804410:'DW1JY97', 78971516571135884:'EL8G506',
           196405:'WB2734U', 196371:'WE769UX', 196389:'EL8G506', 196397:'WB2733U', 196413:'EL6T639', 196421:'EL6T641',
           213937:'WZ977OY', 78971516571135876:'WE769UX', 196413:'EL6T639'}
car=['WE769UX', 'WB2733U', 'WB2734U', ]
truck=['EL8G506', 'EL6T639', 'EL6T641', 'WZ977OY', 'WW094SE', 'DW1JY97', 'EL6T639']

#Wczytywanie danych
plik='../Flotex/raw.xls'
#try:
    df_full=pd.read_excel(plik)
#except:
 #   print('Błąd:\nPlik powinien posiadać nazwę: raw.xls')
  #  exit()
df_full=pd.read_excel(plik)
df_full=df_full.rename(columns={'Wartosc netto po rabacie':'Wartosc netto'})
df=df_full[['Numer karty','Nr rejestracyjny / Imię i nazwisko','Grupa produktowa','Ilosc','Jednostka',
           'Cena za jednostke','Wartosc netto','Stopa VAT','Brutto']]

#Operacje na źródle
car_miss(df, card_code)
car_size(df, car, truck)
vat_i_brutto_fix(df)
account_pull(df, attribute)
df=odlicz(df)
transfer_grosza(df)
#------------------------------------------------------
#Dane prezentowane
work=df[['Konto', 'Grupa produktowa', 'Stopa VAT', 'Netto', 'Vat', 'Brutto', 'Odliczenie']]
work=work.sort_values(['Konto', 'Brutto', 'Odliczenie'], ascending=[True, True, False])

#Data do tytułu
today = date.today()
today.strftime("%b-%d-%Y")

#Lista do pliku 2
lista=podsumowanie(work)
tablica=pd.DataFrame(lista,columns=['Konto','Stopa VAT','Cecha','Wartość'])

#Zapisywanie
work.to_excel('Sandra_{}.xlsx'.format(today))
tablica.to_excel('Sumy_{}.xlsx'.format(today))

print('Raport gotowy')
