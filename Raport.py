import pandas as pd
from def_base import car_miss,car_size,vat_i_brutto_fix,account_pull,odlicz,transfer_grosza,podsumowanie,find_newcomer
from def_base import fold
from datetime import date
pd.options.mode.chained_assignment = None  # default='warn'

print('VaT 2020 ver 1.2')
print('Kasia1 PSD     Kamila PSG')
car,truck,card_code,id_t=fold()
nazwa=input('Proszę podać nazwę pliku > ')

####TEST##3
#nazwa='raw.xls'
plik='../Flotex/{}'.format(nazwa)

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
           'USŁUGI SAMOCHODOWE':'MYJNIA','ADBLUE           SZT':'PŁYNY EKSPLOATACYJNE/OLEJE SILNIKOWE/INNE PRODUKTY',
           'AUTO MYJNIA      SZT':'MYJNIA','ADBLUE':'PŁYNY EKSPLOATACYJNE/OLEJE SILNIKOWE/INNE PRODUKTY',
	        'BEZOLOW 95       LTR':'PALIWO','ULTIMATE DIESEL  LTR':'PALIWO'}

try:
    df_full = pd.read_excel(plik)
except:
    print('PRZERWANIE OPERACJI: Wystąpił błąd pamięci Excel lub nazwa pliku jest niepoprawna.')
    print('Jeśli nazwa pliku jest poprawna, należy otworzyć plik Excel i wpisać cokolwiek w dowolnej komórce kolumny A')
    print('Następnie powtórzyć operację.')
    exit()

df_full=pd.read_excel(plik)
df_full=df_full.rename(columns={'Wartosc netto po rabacie':'Wartosc netto'})
df=df_full[['Numer karty','Nr rejestracyjny / Imię i nazwisko','Grupa produktowa','Ilosc','Jednostka',
           'Cena za jednostke','Wartosc netto','Stopa VAT','Brutto']]

#Operacje na źródle
car_miss(df, card_code)
find_newcomer(df,card_code,attribute)
car_size(df, car, truck)
vat_i_brutto_fix(df)
account_pull(df, attribute,id_t)
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
work.to_excel('{}_{}.xlsx'.format(nazwa[0:-4],today))
tablica.to_excel('Sumy_{}_{}.xlsx'.format(today,id_t))

print('Raport gotowy')
