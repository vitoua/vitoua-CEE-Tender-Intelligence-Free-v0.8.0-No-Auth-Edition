# CEE Tender Intelligence Free v0.8.0 No-Auth Edition

Working connectors that do not require procurement API credentials:
- TED Search API for published European notices
- Prozorro Public API 2.5 for Ukraine
- Germany Datenservice Oeffentliche Vergabe daily OCDS export
- Poland e-Zamowienia BZP notice read API

Features:
- One refresh button with country checkboxes
- Public procurement IDs in UI, including Prozorro tenderID
- TED versus national-source deduplication by external ID, deterministic fingerprint and controlled fuzzy match
- Search, current-only filter, UA/PL/EN, logout and winner analytics

Other portals are intentionally excluded from this no-auth build until a stable official anonymous endpoint and response schema are verified.
