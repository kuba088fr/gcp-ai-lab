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
