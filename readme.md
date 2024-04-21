# Instructiuni de utilizare

## 1. Instalati Docker
Daca sunteti pe Windows recomandarea e sa va puneti WSL si pe WSL sa instalati Docker sau sa 
va instalati Docker Desktop. <br>
Daca sunteti pe Linux il instalati normal <br>
Pt ambele metode se gasesc tutoriale, va recomand sa incercati sa va bateti capul macar un timp decent, ca e ceva de care o sa va mai loviti. Daca chiar nu reusiti, apelati la @Cristi, @Karma, @Yorknez pt tech-support (probabil, but don't rely on that!!)

## 2. Script-ul pt hostat baza de date local (`db.sh`)
Script-ul asta face urmatoarele chestii (pe linii):
- stop-ul la containere (asta e mai mult daca il rulati repetat, puteti ignora)
- liniile cu `docker run` sunt responsabile de a crea clusterele de mongo (practic sunt 3 baze de date care sunt sincronizate, necesare pt folosit db-ul local)
- exec-ul ala configureaza cele 3 clustere ca sa stie cum sa comunice unul cu altull, ar tb sa vedeti `{ ok: 1 }`

## 3. Script-ul pt populat baza de date (`populate.py`)
Pt a rula script-ul de populare sunt necesare urmatoarele:
- instalati python
- mergeti intr-un folder in care sa fie `populate.py`, `triggers.py` si `requirements.txt`
- creati un virtual env (`python3 -m venv venv` pe linux)
- `source venv/bin/activate` (pe windows ar tb sa fie ceva similar, look it up)
- `pip install -r requirements.txt` (sau `venv/bin/pip install -r requirements.txt` daca cu `source`-ul de mai sus nu merge)
- `python3 populate.py`

Dupa toti pasii astia, ar tb sa aveti baza de date facuta cu date mockuite si cu validari puse (TOT TREBUIE FACUTE IN BACKEND VALIDARI REGARDLESS) <br>
Daca e cineva curios, script-ul poate fi configurat ca sa fie modificat output-ul, sunt niste params ce tb schimbati daca chiar vreti
