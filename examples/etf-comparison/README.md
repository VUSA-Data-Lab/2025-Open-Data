# ETF Palyginimo Pavyzdys (VWCE, EUNL, CSPX, WDEF)

Šis pavyzdys rodo, kaip **GitHub Codespaces** aplinkoje:
- Atsisiųsti ETF kainų duomenis iš `yfinance`
- Nubraižyti grafikus
- Sugeneruoti PNG failus automatiniai palyginimui

## Paleidimas

1. Atidarykite repo GitHub'e
2. Spauskite **Code → Open in Codespaces**
3. Palaukite, kol aplinka susikurs (~30–60s)
4. Atidarykite failą `analysis.py`
5. Spauskite **Run**

Sugeneruoti grafikai:
- `performance_5y.png` — penkerių metų palyginimas (normalizuota)
- `performance_1y.png` — vienerių metų palyginimas

## Naudojami ETF

| Pavadinimas | Ticker | Aprašymas |
|---|---|---|
| VWCE | VWCE.DE | Vanguard FTSE All-World UCITS (kaupiantis) |
| EUNL | EUNL.DE | iShares MSCI World UCITS |
| CSPX | CSPX.DE | iShares S&P 500 UCITS (kaupiantis) |
| WDEF | WDEF.DE | WisdomTree Europe Defence UCITS |

## Streamlit Dashboard (interaktyvus naršyklėje)

Norėdami paleisti interaktyvų ETF palyginimo grafikų dashboardą:

1. Atidarykite Codespace:
   Code → Open in Codespaces
2. Paleiskite komandą terminale:

## Keitimas studentų užduotims

Norint palyginti kitus ETF, keiskite `tickers` sąrašą `analysis.py` faile.
