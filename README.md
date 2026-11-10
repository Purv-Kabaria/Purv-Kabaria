### Hi, I'm Purv.

I build the unglamorous parts of software that keep the glamorous parts alive: queues that don't lose jobs, retries that don't double-charge, and models whose accuracy survives contact with real data. Final-year CS at NIT Surat, founding engineer intern at [Career Passport](https://www.careerpassport.ai/) last summer, and occasionally found arguing with Codeforces about what "easy" means.

**Open to:** 6-month SDE / backend / AI engineering internships from January 2027, remote or on-site · [resume](https://purvkabaria.netlify.app/resume.pdf) · [portfolio](https://purvkabaria.netlify.app)

#### What I work with

| | |
|---|---|
| **Languages** | Python, TypeScript, JavaScript, Java, SQL, C++ |
| **Backend** | Node.js, NestJS, FastAPI, Django, Spring Boot, REST APIs, Server-Sent Events |
| **Queues and data** | PostgreSQL, MongoDB, Redis, BullMQ, Redis Streams, Prisma, Qdrant, Meilisearch, Firestore, MinIO |
| **ML** | PyTorch, LightGBM, XGBoost, scikit-learn, Hugging Face Transformers, LoRA fine-tuning, ONNX Runtime |
| **LLM systems** | RAG, retrieval evaluation, rerankers, embeddings, Langfuse, LangChain, Ollama, Groq and Gemini APIs |
| **Frontend** | Next.js, React, Tailwind CSS |
| **Infra** | Docker, Linux, Git, GitHub Actions, AWS, GCP, SLURM on A100/H100 clusters |

#### Achievements

- **Winner**, Adani Powermind Hackathon 2026 (team): energy-demand forecasting
- **Rank 94** of 19,900+, Amazon ML Challenge 2026: entity resolution over 10M records
- **Top 15** (solo), EEG/EMG Foundation Challenge, NeurIPS 2026 workshop
- **Top 10** (solo), WWT Unravel 2026
- **1st runner-up**, WebOsmotic AI/ML Hackathon 2025
- **Top 100**, ZS Tech Challenge · finalist at 12 national hackathons
- Chairperson, Cutting Edge Visionaries (Fintech Club), SVNIT · Developer, ACM SVNIT

<!-- competitive starts -->
[Codeforces](https://codeforces.com/profile/OldmanGalaxy): **1415**, Specialist (max 1415)

[CodeChef](https://www.codechef.com/users/oldmangalaxy): **1669**, 3★ (max 1669)

[LeetCode](https://leetcode.com/u/oldmangalaxy/): **1550**, 507 solved
<!-- competitive ends -->

#### Currently learning and exploring

- **Foundation models for brain signals:** decoding EEG for people a model has never seen, from Riemannian geometry to LoRA fine-tuning (my NeurIPS 2026 challenge entry)
- **Evaluating retrieval honestly:** benchmarking every stage of a RAG pipeline on held-out questions (keyword fusion lost, so it shipped off)
- **Distributed job processing:** at-least-once delivery, idempotent consumers, and what actually happens when a worker dies mid-job
- **Java and Spring Boot**, by building something with them rather than reading about them

#### Things worth opening

| | What | Why it's interesting |
|---|---|---|
| [Distributed RAG](https://github.com/Purv-Kabaria/Distributed-RAG) | Self-hosted RAG over PDFs, scans, audio and video, split into 5 services | Retrieval benchmarked stage by stage (nDCG@10 0.706 to 0.724 on held-out questions), duplicate chunks cut from 17% of top results to 0%, and a queue where a crashed worker can't lose a document |
| [FinBridge](https://github.com/Purv-Kabaria/FinBridge) | Offline-first lead capture and call review for field sales (team project) | INT8 sentiment model measured 2.74x faster on CPU with identical labels, and a check for when someone's tone contradicts their words |
| [Business Entity Resolution](https://github.com/Purv-Kabaria/business-entity-resolution) | Amazon ML Challenge 2026, rank 94 of 19,900+ | Matching 10M messy records without comparing 6.7 trillion pairs, and a decision rule built around the metric |
| [Jobs180](https://github.com/Purv-Kabaria/Jobs180) | Spring Boot job tracker | Ten concurrent retries of the same request create exactly one record, and there's a test that proves it |
| [AssetFlow](https://github.com/Purv-Kabaria/Odoo-2026) | Asset management (team hackathon project) | Role checks on every request, Ctrl+K search, and real-time notifications that replay what you missed |
| [Prometheus](https://github.com/Purv-Kabaria/prometheus) | Adani Powermind Hackathon winner (team) | I built the forecaster, then found the leak in my own validation and published the honest number |

[Portfolio](https://purvkabaria.netlify.app) · [LinkedIn](https://www.linkedin.com/in/purv-kabaria/) · purvkabaria@gmail.com
