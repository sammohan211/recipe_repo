# AGENTS.md

## Purpose

You are helping build a lean MVP for a personal inventory-driven cooking assistant.

Your job is to act like a strong product-minded engineer:
- respect scope
- prefer simple solutions
- do not overengineer
- do not invent extra features outside the PRD
- keep code understandable and modular
- make progress in small, testable steps

This project is being developed with AI assistance and should remain easy to iterate on.

---

## Product Summary

This app allows a user to:

- scan UPC barcodes with a phone camera
- identify grocery products
- map products to simple ingredient names
- maintain a household inventory using ingredient presence only
- get AI-generated recipe suggestions based on current inventory
- see recipes grouped into:
  - can make now
  - missing a few ingredients
- maintain a manual grocery list

This is a **personal tool MVP** that may later evolve into a broader consumer app.

---

## MVP Scope

### Must build

- barcode scanning from phone browser
- UPC/product lookup
- product-to-ingredient mapping
- user editing of ingredient name at scan time
- remembered mapping for future scans
- simple ingredient inventory
- present / absent toggle
- pantry staples assumed present
- AI recipe suggestions
- recipe links only
- grouped recipe results:
  - recipes you can make now
  - recipes missing 2-3 ingredients
- manual grocery list
- local-first architecture
- offline inventory support
- multi-device access through browser on local network

### Must NOT add in MVP

Do **not** add any of the following unless explicitly requested:

- quantity tracking
- expiry tracking
- nutrition tracking
- meal planning
- recipe storage/database
- user accounts
- cloud sync
- voice input
- receipt scanning
- image recognition beyond barcode
- local LLM integration
- automatic grocery suggestions
- advanced ontology/taxonomy systems
- complex categorization
- chat-based AI UI

If a possible improvement conflicts with MVP simplicity, do not implement it by default.

---

## Product Principles

When making decisions, optimize for:

1. simplicity
2. reliability
3. low friction
4. human correction over AI guessing
5. clear UX over feature richness
6. local-first design
7. buildability for a solo developer

Prefer:
- editable text over heavy automation
- explicit flows over magic behavior
- small services over deep abstractions
- practical defaults over configurable complexity

---

## Development Principles

### General

- make the smallest reasonable change
- keep files organized and readable
- avoid premature abstraction
- avoid speculative architecture
- prefer boring, maintainable solutions
- add comments only where they add real value
- keep naming clear and literal

### Code style

- write clean, straightforward code
- prefer functions and services with single responsibilities
- avoid large monolithic files
- avoid hidden side effects
- use type hints where practical
- keep logic easy to test

### Architecture

Prefer a clean, simple structure such as:

- `app/api/` for routes
- `app/services/` for business logic
- `app/models/` for DB models / schemas
- `app/templates/` or frontend folder for UI
- `tests/` for tests
- `docs/` for product and architecture docs

Do not introduce microservices, event buses, background workers, or complex plugin systems for MVP.

---

## Tech Preferences

### Backend
- FastAPI

### Database
- SQLite

### ORM / models
- SQLModel or lightweight SQLAlchemy usage

### Frontend
- simple server-rendered HTML or lightweight web UI
- HTMX is acceptable if it reduces complexity
- minimal JavaScript is preferred unless more is clearly needed

### Barcode scanning
Use practical browser-compatible scanning tools.

### AI integration
- keep provider integration simple
- use a thin abstraction layer only if helpful
- do not overbuild a provider framework up front

### Tooling
- use `uv`
- keep setup simple
- prefer `pytest`
- prefer `ruff`

---

## Inventory Rules

Inventory is intentionally simple.

### Inventory behavior
- ingredients are tracked as present / absent only
- no quantities in MVP
- no expiry in MVP
- no nutrition in MVP

### Ingredient mapping flow
When a barcode is scanned:

1. resolve UPC to product name
2. suggest ingredient name if possible
3. allow user to edit ingredient immediately
4. save the product-to-ingredient mapping
5. reuse that mapping on future scans
6. if similar ingredient already exists, suggest merge rather than forcing a duplicate

### Ingredient data model
Use simple free-text ingredient names.

Do not introduce a complex taxonomy for MVP.

---

## Pantry Staple Rules

Assume pantry staples are always available.

Examples may include:
- salt
- pepper
- oil
- water
- butter

These should not count against missing ingredients in recipe suggestions.

Keep pantry staples simple in MVP.

---

## Recipe Rules

### Recipe generation
- recipes are generated or found dynamically through AI/provider integration
- do not store recipes in a local recipe database for MVP
- recipe output should include links, not a full recipe management system

### Recipe grouping
Group recipe suggestions into:
- recipes you can make now
- recipes missing a few ingredients

### Missing ingredient rule
- allow recipes with up to 2-3 missing ingredients
- ignore pantry staples when counting missing items

### Important
Do not turn the app into a recipe catalog, meal planner, or nutrition engine.

---

## Grocery List Rules

Grocery list in MVP is manual only.

Allowed:
- add item
- remove item
- mark purchased if useful

Not allowed in MVP:
- AI-generated grocery suggestions
- auto-building list from recipes by default
- shopping intelligence systems

Keep it basic.

---

## Offline / Network Rules

### Offline
Inventory functionality must work offline.

### Online dependency
Recipe suggestions may require internet access.

### Network model
Assume a local-first setup:
- FastAPI app runs on a home machine
- phone accesses it through browser on local network

Do not assume cloud infrastructure for MVP.

---

## UX Rules

When making UX decisions:

- reduce taps/clicks
- keep workflows obvious
- make scan flow fast
- let users correct data immediately
- prefer explicit labels over clever UI
- keep screens focused

Recommended primary screens:
- Inventory
- Scan
- Ingredient Edit / Confirm
- Recipes
- Grocery List

Do not introduce a chat-first UI for MVP.

---

## Testing Expectations

When adding meaningful logic, include tests where reasonable.

Priority areas for tests:
- product-to-ingredient mapping logic
- merge suggestion logic
- pantry staple exclusion
- recipe grouping logic
- inventory toggle behavior
- API/service boundaries

Do not create excessive test scaffolding before real logic exists.

---

## Documentation Expectations

When asked to generate docs:
- keep them concise
- reflect actual implemented behavior
- do not describe speculative features as if already decided
- clearly separate MVP vs future ideas

Useful docs include:
- PRD
- architecture notes
- setup instructions
- API notes
- implementation checklist

---

## How to Work

When asked to build something:

1. restate the specific task in practical terms
2. check it against MVP scope
3. implement the smallest complete version
4. keep structure clean
5. note assumptions
6. avoid expanding into adjacent features

When asked for plans:
- break work into small milestones
- prefer sequenced implementation steps
- identify dependencies clearly

When uncertain:
- choose the simpler solution
- do not silently add complexity
- flag the tradeoff clearly

---

## What Good Looks Like

A good output for this repo is:

- small
- clear
- working
- easy to test
- easy to extend later
- faithful to the MVP
- not overdesigned

A bad output is:

- feature creep
- speculative architecture
- heavy abstractions
- unnecessary frameworks
- hidden complexity
- solving future problems too early

---

## Final Rule

Respect the PRD and MVP boundaries.

This project succeeds by being:
- useful
- simple
- local-first
- AI-assisted
- realistically buildable

Do not optimize for impressiveness over usability.
