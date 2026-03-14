# Product Requirements Document (PRD)
# AI Pantry Inventory & Recipe Assistant

## 1. Product Overview

This project is a personal inventory-driven cooking assistant that allows a user to scan groceries, maintain a simple ingredient inventory, and receive AI-generated recipe suggestions based on available ingredients.

The primary goal is personal utility with a clean MVP design. The system prioritizes simplicity, accuracy, and usability over automation or complex modeling.

This is intentionally designed as a lean MVP that can later evolve into a broader consumer application.

---

## 2. Problem Statement

Users often:
- Forget what ingredients they already have
- Buy duplicate groceries
- Struggle to decide what to cook
- Cannot easily find recipes matching available ingredients

Existing apps are either:
- Recipe databases
- Grocery planners
- Nutrition trackers

But none focus on **inventory-driven cooking decisions** with minimal friction.

---

## 3. Product Goals

### Primary Goals

- Maintain a simple inventory of household ingredients
- Allow fast barcode scanning of groceries
- Normalize products into usable ingredients
- Suggest recipes based on inventory
- Show missing ingredients clearly
- Keep system simple and fast

### Secondary Goals

- Provide foundation for AI experimentation
- Allow future expansion into shopping intelligence
- Support multi-device use on local network

---

## 4. Non-Goals (Explicit MVP Exclusions)

The following are intentionally excluded from MVP:

- Quantity tracking
- Expiry tracking
- Nutrition tracking
- Meal planning
- Recipe storage
- User accounts
- Cloud sync
- Voice input
- Receipt scanning
- Image recognition beyond barcode
- Local LLM integration
- Automated grocery suggestions
- Ingredient ontology systems
- Complex categorization

---

## 5. Target User

Primary user:
Single household technical user managing groceries and meals.

Secondary future users:
Households wanting a simple cooking assistant.

---

## 6. Core User Workflow

Primary workflow (happy path — error paths documented in feature sections):

User scans groceries
→ Product identified
→ User confirms or edits ingredient
→ Ingredient added to inventory
→ User views recipes
→ Spoonacular returns recipe suggestions
→ System shows missing ingredients
→ User manages grocery list manually

---

## 7. Core Features

## 7.1 Inventory Management

### Features

- Barcode scanning using phone camera
- Product name lookup from UPC
- Manual ingredient editing
- Ingredient mapping memory
- Simple ingredient list
- Presence only tracking
- Toggle present / absent
- Pantry staples assumed present

### UPC Lookup Cascade

Scan UPC
→ Query Open Food Facts (primary — free, no key required)
→ Found? Use product name
→ Not found? Query UPCitemdb (fallback — free, 100 req/day)
→ Found? Use product name
→ Not found? Prompt user for manual entry
→ Save UPC → product name mapping locally (never fails twice)

### Ingredient Mapping Flow

Scan UPC
→ Detect product name (via lookup cascade above)
→ Suggest ingredient
→ User edits if needed
→ Save mapping

Example:

Great Value Whole Milk  
→ Suggested: Milk  
→ User confirms  
→ Stored: Milk

Future scans auto suggest mapping.

### Error States

**Barcode scan fails** (bad lighting, damaged barcode, unrecognized format)
→ Show "couldn't read barcode" message with manual text entry field
→ No retry loop — go straight to manual entry

**UPC not found** (after full OFF → UPCitemdb → cache lookup)
→ Prompt manual product name entry
→ Save locally by UPC on confirmation

**Duplicate scan** (UPC already present in inventory)
→ Show "already in inventory" notification
→ No action taken — do not toggle off accidentally

---

## 7.2 Recipe Discovery

### Features

- Spoonacular API returns real recipe URLs with titles, matched ingredient counts, and missing ingredients
- Results filtered using `diet=ketogenic` and optional `maxCarbs` parameter
- Ingredient match filtering

### Recipe Grouping

Results grouped as:

**Recipes you can make now**

Example:
- Keto omelette
- Egg scramble

**Recipes missing few ingredients**

Example:
- Keto broccoli casserole  
Missing: broccoli

### Matching Rules

- Maximum 2–3 missing ingredients
- Pantry staples ignored in missing count
- Ingredient presence only (no quantities)

### Fallback: Google Search

If Spoonacular results are unsatisfactory or the user wants broader options:

- Recipe screen shows a "Search Google" button
- Button constructs a Google search from current ingredients (e.g. `keto recipes with chicken eggs butter`) and opens it in a new browser tab
- No backend involvement — frontend builds the URL from inventory state
- Always visible as a secondary action beneath API results

### Error States

**Recipe API unavailable or times out**
→ Show "recipe suggestions unavailable" message
→ Show "Search Google" button so user can still find recipes
→ Inventory view remains fully functional — do not block the screen

**Zero results returned**
→ Show "no recipes found for current ingredients" empty state
→ Show "Search Google" button as the next step
→ No automatic filter relaxation — keep behavior predictable

---

## 7.3 Grocery List

### MVP Scope

Manual grocery list only.

Features:

Add item  
Remove item  
Mark purchased  

Future versions may include:
Recipe derived lists
AI suggestions

---

## 7.4 Pantry Staples

System assumes default pantry items exist.

Example:

Salt  
Pepper  
Oil  
Water  
Butter  

Future feature:
User editable staples list.

---

## 8. Platform Requirements

### Backend

FastAPI

### Database

SQLite

### Frontend

Simple web interface

Accessible from:
Phone browser
Desktop browser

### Phone access

No app installation required. The app runs in the phone browser.

Setup steps:
1. Raspberry Pi runs FastAPI server on home network
2. Phone navigates to Pi's local IP (e.g. `http://192.168.1.50:8000`)
3. Browser "Add to Home Screen" creates an icon that opens the app in one tap

Recommended local access improvements:
- Assign Pi a static local IP via router (address never changes)
- Configure Pi hostname as `pantry.local` via mDNS so URL is human-readable

### Barcode scanning

Phone camera via web interface.

### Network model

Local network only.

Example:

Phone browser
→ connects to
FastAPI server running on Raspberry Pi at home.

### Security model

No authentication in MVP — intentional decision.

Assumptions:
- Server is accessible on home LAN only
- Server must NOT be exposed to the public internet (no port forwarding, no reverse proxy to external)
- All users on the home LAN are trusted
- Single-household use makes auth unnecessary for MVP

Auth becomes required if the app is ever exposed externally or expanded to multi-user.

### Deployment target

Raspberry Pi on home network. Server runs continuously — no sleep/suspend concerns.

### Offline behavior

Two distinct scenarios:

**Internet down, Raspberry Pi up (LAN reachable)**
- Inventory view, edit, and grocery list: fully functional
- Barcode scan: works; UPC lookup silently falls through to manual entry (same path as a cache miss)
- Recipe suggestions: unavailable — show "requires internet connection" message

**Raspberry Pi unreachable (server off, away from home)**
- App is inaccessible — no local copy exists on the phone
- Out of scope for MVP; document as a known limitation

---

## 9. Recipe API Responsibilities

Spoonacular API handles:

Recipe search by ingredients
Keto diet filtering (`diet=ketogenic`)
Macro filtering (`maxCarbs` parameter)
Missing ingredient identification

Spoonacular API does NOT handle:

Inventory control
Quantities
Nutrition
Meal planning
Shopping automation

---

## 10. Data Model

## Product

Fields:

UPC  
Product name  
Ingredient mapping  
Last modified date  

## Ingredient

Fields:

Name  
Present flag  

Future optional:

Category  
Tags  

## Pantry Staples

List of assumed ingredients.

## Grocery List

Manual item list.

---

## 11. Success Criteria

MVP considered successful if:

User can quickly scan groceries  
User can easily view inventory  
User can find recipes from available ingredients  
User can see missing ingredients clearly  

Success definition:

The user can answer:

What do I have?  
What can I cook?  

---

## 12. MVP Feature List

Must include:

Barcode scanning  
Manual ingredient editing  
Inventory list  
Recipe suggestions  
Missing ingredient display  
Phone access  
Offline inventory  

---

## 13. Future Enhancements (Not MVP)

Possible future features:

Ingredient categorization
Recipe ranking
Shopping suggestions
Meal planning
Local AI models
Usage learning
Nutrition integration
Cloud sync
Multi user support
Multi-provider recipe search (Edamam as secondary source)

---

## 14. Technical Stack (Proposed)

Language:
Python 3.11+

Backend:
FastAPI
SQLite
SQLModel (single class serves as both DB model and Pydantic schema — reduces boilerplate for simple CRUD; built by FastAPI author, natural fit for this stack; trade-off: thinner abstraction over SQLAlchemy, revisit if query complexity grows)
httpx (async HTTP client for Open Food Facts, UPCitemdb, and Spoonacular API calls)

Frontend:
HTML
HTMX (primary — inventory, recipes, grocery list screens)
Vanilla JS (scan screen only — required for camera API and barcode library)
Jinja2 templates (server-rendered, paired with HTMX)

Barcode:
BarcodeDetector API (primary — native browser API, zero dependencies, Android Chrome only)
Quagga2 / @ericblade/quagga2 (fallback — actively maintained, handles iOS Safari and older Android)
Strategy: detect BarcodeDetector availability at runtime, fall back to Quagga2 if unavailable

UPC Lookup:
Primary: Open Food Facts API (free, no key, food-specific, 4M+ products, 100 req/min)
Fallback: UPCitemdb (free, no key, 100 req/day, general merchandise coverage)
Local cache: SQLite UPC → product name mapping (permanent override, no API call on repeat scans)
User-Agent header required by Open Food Facts (app name + version)

Recipe API:
Primary: Spoonacular API (`diet=ketogenic`, ingredient-based search)
Abstraction: `RecipeProvider` interface with `search_by_ingredients(ingredients, diet) -> list[Recipe]`
`SpoonacularProvider` implements the interface
Upgrade path: Edamam (`health=keto-friendly`) if Spoonacular limits are hit

Dev tools:
uv
pytest
ruff

---

## 15. MVP Screens

System should contain approximately:

Inventory screen  
Scan screen  
Ingredient edit screen  
Recipe screen  
Grocery list screen  

---

## 16. Design Principles

Keep UX simple  
Avoid unnecessary automation  
Prefer correction over guessing  
Minimize user friction  
Favor reliability over features  

---

## 17. Key Risks

UPC coverage gaps for regional/store-brand products (mitigated by OFF→UPCitemdb fallback chain and manual entry with local caching)
Ingredient normalization accuracy
Recipe API relevance
Mobile camera performance
App inaccessible if Raspberry Pi is off or unreachable — known limitation, out of MVP scope

---

## 18. Open Questions

UPC provider: Open Food Facts (primary) + UPCitemdb (fallback) + local cache (resolved)
Recipe API: Spoonacular with `diet=ketogenic` filter (resolved)
Frontend framework decision
Local network discovery method
Ingredient normalization strategy

---

## 19. Development Philosophy

This project is intended to be:

AI-assisted development  
Iterative MVP driven  
Architecture first  
Feature constrained  
Expandable later  

---

## 20. Version Definition

### V1 Definition

A working system where a user can:

Scan groceries  
Maintain inventory  
Find recipes from ingredients  

Everything else is post-MVP.
