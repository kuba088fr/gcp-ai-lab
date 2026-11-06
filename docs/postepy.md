# Dziennik nauki

Nowe wpisy dopisuj na dole. Jeden wpis = jeden krok z `docs/roadmap.md`.

## Szablon wpisu

```markdown
## RRRR-MM-DD — Lab XX, krok X.Y: <tytuł>
**Co zrobione:**
**Czego się nauczyłem / wnioski:**
**Koszt (szacunek):**
**Problemy / pytania otwarte:**
**Następny krok:**
```

---

<!-- Wpisy poniżej -->

## 2026-11-06 — Lab 00, krok 0.0: Koncepcje (LLM, embeddingi, chunking, RAG)
**Co zrobione:** Szkielet repo (CLAUDE.md, .gitignore, roadmap, dziennik). Rozmowa o koncepcjach: LLM bez dostępu do moich danych, embedding jako „klucz semantyczny” (join przybliżony zamiast `=`), odległość kosinusowa, brute force vs indeks ANN, chunking jako ziarno tabeli, RAG jako dwa pipeline'y (batch indeksowanie + online zapytanie). Zapowiedź: agent, MCP, A2A.
**Czego się nauczyłem / wnioski:**
- Pytanie i dokumenty muszą mieć embeddingi z tego samego modelu; zmiana modelu = pełny backfill tabeli chunków (jak zmiana logiki klucza).
- Brak odpowiedzi w RAG może wynikać z chunkingu (ziarno, cięcie bez overlapu) albo z wyszukiwania (top-k, inny model/task type, przybliżony indeks).
- Przy setkach chunków wyszukiwanie dokładne (bez indeksu) jest tanie i daje pełny recall; indeks ANN to kompromis jakości za szybkość przy dużej skali.
**Koszt (szacunek):** 0 USD (bez operacji w chmurze).
**Problemy / pytania otwarte:** Do doczytania: wersjonowanie embeddingów (kolumna z nazwą modelu), task type w `ML.GENERATE_EMBEDDING`.
**Następny krok:** 0.1 Budżet i alerty kosztowe w konsoli GCP.

## 2026-11-06 — Lab 00, krok 0.1: Budżet i alerty kosztowe
**Co zrobione:** Repo wypchnięte na GitHub (prywatne `kuba088fr/gcp-ai-lab`). W konsoli: budżet *Alerts only* na wszystkie usługi (20 USD, progi 25/50/100% actual + 100% forecasted, kredyty odznaczone) oraz budżet *Spend cap enforcement* `lab-vertex-ai-cap` na Vertex AI (10 USD).
**Czego się nauczyłem / wnioski:**
- Budżet *Alerts only* to tylko powiadomienie (jak SLA miss w Airflow), z opóźnieniem rzędu godzin — przychodzi po fakcie.
- Spend cap (nowość) realnie pauzuje usługę, ale tylko dla 4 usług: Cloud Run, Cloud Run Functions, Gemini API, Vertex AI. **BigQuery nie jest objęte.**
- Kredyty trzeba odznaczyć w budżecie, inaczej koszt netto = 0 i alert nigdy nie przyjdzie.
- W billingu i API nadal „Vertex AI” / `aiplatform.googleapis.com`, mimo rebrandingu na Gemini Enterprise Agent Platform. Nasz ruch do modeli (BQ connection, ADK z ADC) idzie przez `aiplatform`, nie przez Gemini API (klucze).
- Free Trial blokuje edycję quot (w tym BQ „Query usage per day”). Zamiennik: `--maximum_bytes_billed` (CLI: domyślnie w `~/.bigqueryrc`, konsola: Query settings) + `--dry_run`. Bez upgrade'u konta trial sam w sobie ogranicza wydatki do kredytu.
**Koszt (szacunek):** 0 USD.
**Problemy / pytania otwarte:** Czy wywołania `ML.GENERATE_*` z BigQuery są księgowane pod Vertex AI (i blokowane przez cap)? Sprawdzić SKU w raporcie billingowym po pierwszym wywołaniu w 1.3.
**Następny krok:** 1.0 Dane testowe — syntetyczne PDF-y.

## 2026-11-06 — Lab 01, krok 1.0: Dane testowe
**Co zrobione:** Korpus 10 dokumentów fikcyjnej firmy Lumen Logistics w `labs/01-rag-bigquery/test_data/documents.yaml`, 18 znanych faktów z tagami trudności w `facts.yaml`, generator `scripts/generate_pdfs.py` (fpdf2 + Pillow). Wygenerowane PDF-y (12 stron, ~0,6 MB) w `data/` (gitignored). Lokalny `.venv` na Pythonie 3.11.
**Czego się nauczyłem / wnioski:**
- Dane testowe RAG = fixture'y: znane fakty w znanych miejscach + celowo trudne przypadki (wersje, tabele, multi-hop, skan, inny język, sprzeczności, PII, brak odpowiedzi).
- Treść (YAML) w gicie, PDF jako artefakt builda — odtwarzalny.
- Fonty wbudowane w PDF są Latin-1; polskie znaki wymagają osadzonego TTF.
- Skan nie ma warstwy tekstowej — sprawdzimy w 1.3, czy Gemini go odczyta.
- Fikcyjny PESEL: poprawny format, błędna suma kontrolna (skrypt to weryfikuje).
**Koszt (szacunek):** 0 USD (lokalnie).
**Problemy / pytania otwarte:** Na komputerze jest tylko Python 3.11 (CLAUDE.md zakłada 3.12+); generatorowi to nie przeszkadza, do sprawdzenia przed ADK w labie 02.
**Następny krok:** 1.1 Fundament w `infra/main.tf` (API, bucket, dataset, connection, IAM).
