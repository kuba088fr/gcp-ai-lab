# Roadmapa gcp-ai-lab

Odhaczaj `- [x]` po zakończeniu kroku. Szczegóły każdego kroku: `docs/postepy.md` i README labu.

---

## 00 Koncepcje (tylko rozmowa, bez kodu)
- [x] 0.0 LLM, embeddingi, chunking, podobieństwo wektorów, RAG, agent, MCP, A2A
- [x] 0.1 Budżet i alerty kosztowe (ręcznie w konsoli GCP) ⭐ *zmiana*

## 01 RAG w BigQuery
- [ ] 1.0 Dane testowe: 5–20 syntetycznych PDF-ów (część z fikcyjnymi danymi osobowymi) ⭐ *zmiana*
- [ ] 1.1 Fundament w `infra/main.tf`
  - włączenie potrzebnych API
  - bucket GCS na surowe PDF-y w EU (`force_destroy = true`, bez dostępu publicznego, uniform bucket-level access, bez wersjonowania i soft delete)
  - dataset BigQuery `ai_poc` w EU
  - BigQuery Cloud Resource Connection `vertex_conn` w EU
  - SA połączenia: `roles/aiplatform.user` na projekcie + `roles/storage.objectViewer` (projekt vs bucket — omówić różnicę i zawęzić)
  - outputy: URI bucketa, ID połączenia, konto serwisowe
  - krótkie komentarze przy każdym bloku
- [ ] 1.2 Object Table na kilku PDF-ach
- [ ] 1.3 Ekstrakcja tekstu z PDF przez Gemini w SQL
- [ ] 1.4 Chunking w SQL
- [ ] 1.5 Embeddingi (`ML.GENERATE_EMBEDDING`)
- [ ] 1.6 `VECTOR_SEARCH` + odpowiedź Gemini — pierwszy działający RAG
- [ ] 1.7 Mini-ewaluacja (baseline): 5–10 pytań z oczekiwanymi odpowiedziami ⭐ *zmiana*
- [ ] 1.8 Przegląd kosztów i sprzątanie ⭐ *zmiana*

## 02 Agenci (Google ADK, lokalnie)
- [ ] 2.1 Agent z jednym prostym narzędziem
- [ ] 2.2 Agent z RAG (lab 01) jako narzędziem
- [ ] 2.3 Pamięć (sesja vs pamięć długoterminowa)
- [ ] 2.4 Wielu agentów (orkiestracja w ADK) + A2A ⭐ *zmiana: A2A jawnie*
- [ ] 2.5 Porównanie z innym frameworkiem (ten sam agent, inna biblioteka)
- [ ] 2.6 Przegląd kosztów

## 03 MCP
- [ ] 3.1 Własny serwer MCP (lokalnie, stdio) wystawiający RAG jako narzędzie
- [ ] 3.2 Podłączenie do agenta ADK
- [ ] 3.3 Podłączenie do Claude Code
- [ ] 3.4 Przegląd kosztów

## 04 Ewaluacja
- [ ] 4.1 Rozbudowa zestawu pytań testowych z 1.7 (golden set)
- [ ] 4.2 Metryki retrieval (trafność: hit rate, recall@k, MRR)
- [ ] 4.3 Metryki odpowiedzi + LLM-as-judge
- [ ] 4.4 Ewaluacja agenta (trajektoria: czy użył właściwego narzędzia)
- [ ] 4.5 Eksperyment: zmiana chunkingu / modelu i porównanie wyników
- [ ] 4.6 Przegląd kosztów

## 05 Data governance ⭐ *zmiana: ustalona kolejność*
- [ ] 5.1 Inwentaryzacja danych osobowych w chunkach (skąd się wzięły, gdzie lądują)
- [ ] 5.2 Policy tags i maskowanie kolumn
- [ ] 5.3 Uprawnienia agenta: SA agenta vs SA połączenia, co agent może zobaczyć
- [ ] 5.4 Lineage (PDF → tekst → chunki → embeddingi → odpowiedź)
- [ ] 5.5 Dataplex: katalog, jakość danych
- [ ] 5.6 Przegląd kosztów i sprzątanie całości

---

## Uzasadnienie zmian względem wersji pierwotnej

| Zmiana | Dlaczego |
|---|---|
| **0.1 Budżet i alerty** | Free Trial to jedyne zabezpieczenie przed pomyłką. Alerty na np. 5/10/25 USD to darmowy bezpiecznik. Ręcznie w konsoli, bo `google_billing_budget` w Terraform wymaga uprawnień na koncie rozliczeniowym, a to osobny temat. Uwaga: budżet tylko **powiadamia**, nie blokuje wydatków. |
| **1.0 Dane testowe** | Własne, syntetyczne PDF-y: zero ryzyka prawnego, pełna kontrola nad treścią (łatwiej układać pytania testowe), a fikcyjne PII daje gotowy materiał do labu 05. |
| **1.3 — notka techniczna** | Ekstrakcja przez Gemini multimodalnie, **nie** `ML.PROCESS_DOCUMENT` (to Document AI = zakazane bez zgody). Przed krokiem sprawdzimy w dokumentacji, czy lepsze są nowsze funkcje `AI.GENERATE*` niż `ML.GENERATE_TEXT`. |
| **1.7 Mini-ewaluacja** | Bez punktu odniesienia nie da się powiedzieć, czy zmiana chunkingu coś poprawiła. Kilka pytań od razu po pierwszym RAG-u = baseline; lab 04 rozbudowuje gotowy zestaw. Analogia: testy danych w Dataform piszesz razem z modelem, nie na końcu projektu. |
| **x.8 / x.6 Przegląd kosztów** | Na koniec labu: co zostało w chmurze, ile kosztowało (raport billingowy, `INFORMATION_SCHEMA.JOBS`). Nawyk, który chroni budżet. |
| **2.4 A2A jawnie** | A2A było w celach, ale nie w krokach. |
| **05 kolejność** | Od problemu do narzędzia: najpierw zobaczyć, gdzie PII wycieka do RAG-a, potem je chronić (policy tags), potem ograniczyć agenta, a dopiero na końcu narzędzia katalogowe (lineage, Dataplex), które to wszystko opisują. |
