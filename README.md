# UdyamSathi — AI Rural Business Advisory & Finance Platform

**Team:** Catalyst  
**SIH 2026:** SIH26091  
**Prototype:** Final SIH working demo

UdyamSathi is a web-based advisory prototype for rural and semi-urban entrepreneurs. It takes **location, annual income, available margin capital and business category** and produces a detailed first-pass business decision report.

## Final demo flow
1. Select language.
2. Enter location, annual income, available margin capital and business category.
3. Every dropdown includes **Other — enter manually** where relevant.
4. If the entrepreneur has no business idea, UdyamSathi ranks 3–4 prototype options.
5. Generate a detailed report containing:
   - Executive feasibility decision
   - Hyper-local catchment and customer estimate
   - Local opportunity signals
   - Customer segments and distribution logic
   - Product-market fit and pricing strategy
   - Detailed SWOT
   - Risk → mitigation plan
   - Capital-fit analysis
   - SIH financing route
   - Indicative EMI, quarterly payment and repayment view
   - Capital allocation plan
   - Revenue, growth and break-even view
   - 90-day action plan
   - Government/official portal links
6. Multilingual UI and chatbot are available in English, Hindi, Marathi, Tamil, Telugu and Bengali.

## Important prototype note
The current demo uses **illustrative business/location profiles** so that the complete workflow works without external API keys. Population, customer, revenue and growth figures are not claimed as live market facts. The production SIH version should replace these demo profiles with verified Government/open datasets, live location/geographic data and current scheme rules.

## Run locally
```bash
cd udyamsathi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PORT=5001 python3 app.py
```
Open `http://127.0.0.1:5001`.

If port 5001 is busy, use another port, e.g. `PORT=5050 python3 app.py`.

## Suggested production architecture
**Frontend:** React/Next.js or the current HTML/CSS/JS prototype  
**Backend:** Python + Flask/FastAPI  
**AI/NLP:** LLM + multilingual/Indic-language layer  
**Data:** Government/Open Data + verified scheme data + geospatial/locality data  
**Database:** MySQL/PostgreSQL/MongoDB  
**Maps:** Maps/Geolocation API or OpenStreetMap stack

The LLM should be the reasoning/presentation layer; verified government data should remain the source of truth for scheme rules, limits and eligibility.
