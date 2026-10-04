# Full Spectrum — Job Assessment Prep Bootcamp

An interactive, adaptive, all-encompassing prep bootcamp built to prepare **any candidate** to dominate job assessments — "full spectrum dominance" across every assessment type employers actually use.

**Live:** https://enmanueldmejia.com/assessments/
**AI Practice Companion:** https://enmanueldmejia.com/assessments/chat/

## What's inside

| Module | Content |
|---|---|
| Technical troubleshooting simulations | 24 scored hands-on scenarios: Windows, networking, Active Directory, PowerShell, Windows registry, Linux, ticketing/ServiceNow ITSM workflows, hardware diagnostics |
| Situational judgment tests | 16 work-simulation scenarios: customer service, prioritization, incident response, teamwork |
| Cognitive aptitude drills | 24 timed items: logical, numerical, and verbal reasoning with method-teaching explanations |
| Behavioral interview prep | 20 classic prompts with STAR-method frameworks, model talking points, and pitfalls |
| Work-style assessment guidance | 6 honest guides — how these are scored, authentic preparation, no gaming |
| Timed full simulation | 180-minute, 12-incident mixed simulation across all domains |
| AI Practice Companion | Conversational role-play interviewer with keyword-based feedback (`chat.html`) |

## How it works

- **Interactive** — every scenario is a hands-on scored decision, not reading material.
- **Adaptive** — the drill queue targets your weakest domains first; per-domain mastery is tracked in your browser (localStorage, nothing leaves your device).
- **Honest** — work-style guidance teaches genuine self-knowledge, not deceptive test-gaming. All scenario content is original.

## Run it

The bootcamp is two self-contained HTML files with zero dependencies:

- `index.html` — the full bootcamp (open in any browser)
- `chat.html` — the AI practice companion

Source content lives in `content/` as JSON (`technical.json`, `situational.json`, `cognitive.json`, `behavioral.json`, `workstyle.json`).

## Deploy

Deployed as a standalone Cloudflare Worker (`full-spectrum-bootcamp`) serving `index.html` at `/assessments/*` and `chat.html` at `/assessments/chat/*`, routed on:

- `enmanueldmejia.com/assessments/*`
- `interstitiumlabs.dev/assessments/*`
- `learn.interstitiumlabs.dev/assessments/*`

See `deploy.py` for the full worker-upload + route-creation flow (Cloudflare API).

## Evidence boundary

Assessment formats described here are general industry patterns. No vendor test content is reproduced; all scenarios, questions, and explanations are original. Vendor documentation may be linked as reference, never copied.

Built by [Interstitium Labs](https://interstitiumlabs.dev) — Enmanuel D. Mejia, Founder.
