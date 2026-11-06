# Lab 01 — RAG w BigQuery

## Cel
Zbudować pierwszy działający RAG w całości w BigQuery: PDF-y w GCS → Object Table → ekstrakcja tekstu (Gemini) → chunking → embeddingi → `VECTOR_SEARCH` → odpowiedź Gemini. Zrozumieć każdy etap i jego koszt.

## Kroki
- [x] 1.0 Dane testowe (syntetyczne PDF-y)
- [ ] 1.1 Fundament w `infra/main.tf`
- [ ] 1.2 Object Table
- [ ] 1.3 Ekstrakcja tekstu przez Gemini
- [ ] 1.4 Chunking w SQL
- [ ] 1.5 Embeddingi
- [ ] 1.6 `VECTOR_SEARCH` + odpowiedź Gemini
- [ ] 1.7 Mini-ewaluacja (baseline)
- [ ] 1.8 Przegląd kosztów i sprzątanie

## Dane testowe (1.0)
10 PDF-ów fikcyjnej firmy Lumen Logistics. Źródło prawdy w gicie, PDF-y są artefaktem builda (gitignored).

| Plik | Rola |
|---|---|
| `test_data/documents.yaml` | treść wszystkich dokumentów |
| `test_data/facts.yaml` | znane fakty + tagi trudności → przyszły golden set (1.7, lab 04) |
| `scripts/generate_pdfs.py` | YAML → PDF (fpdf2; skan jako obraz przez Pillow) |
| `data/*.pdf` | wygenerowane PDF-y (nie w gicie) |

Co testuje korpus: dystraktory („14 dni” ×3), sprzeczne wersje polityki (2024 vs 2026), tabela, liczby, multi-hop (cennik + umowa), fakt przecięty sekcjami, skan bez warstwy tekstowej (OCR), dokument po angielsku, sprzeczność między dokumentami (800 vs 1000 kg), fikcyjne PII (lab 05), pytanie bez odpowiedzi.

Wszystkie dane osobowe są fikcyjne: e-maile w `example.com`, PESEL-e z błędną sumą kontrolną (skrypt to sprawdza i przerywa, gdy trafi na poprawny), konta `PL00 0000 ...`.

### Regeneracja
```bash
py -3 -m venv .venv
.venv/Scripts/python -m pip install -r labs/01-rag-bigquery/requirements.txt
.venv/Scripts/python labs/01-rag-bigquery/scripts/generate_pdfs.py
```
Domyślne fonty to Arial z `C:/Windows/Fonts`; na innym systemie podaj `--font` i `--font-bold` (dowolny TTF z polskimi znakami, np. DejaVu Sans).

## Wnioski
- Dane testowe RAG projektuje się jak fixture'y: znane fakty w znanych miejscach + celowo trudne przypadki.
- Wbudowane fonty PDF są Latin-1 — polskie znaki wymagają osadzonego TTF (analogia: encoding przy ładowaniu CSV).
- PDF „skan” nie ma warstwy tekstowej; parser tekstu zwróci pusty wynik — tylko model multimodalny/OCR go odczyta.

## Koszt
| Krok | Koszt |
|---|---|
| 1.0 | 0 USD (lokalnie) |
