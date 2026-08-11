# CLEANUP-2C RESEARCH — COMPLETE NON-EUROPE 1776 RULER PACKET

## 1. Result

The external historical-research phase requested after CLEANUP-2C-0 is complete.

```text
RESEARCH_QUEUE_ROWS = 140
UNIQUE_TAGS = 140
MISSING_TAGS = 0
DUPLICATE_TAGS = 0

P0_CASES = 2
P1_CASES = 135
P2_CASES = 3

STRICT_COLONY_OR_COMPANY_ROWS = 22

QUEUE_MAP_DEPENDENCY_MAJOR = 22
QUEUE_MAP_DEPENDENCY_MINOR = 31
QUEUE_MAP_DEPENDENCY_NO = 87

IDENTITY_CONFIDENCE_HIGH = 98
IDENTITY_CONFIDENCE_MEDIUM = 34
IDENTITY_CONFIDENCE_LOW = 8

DEFER_CONTAINING_DECISIONS = 40
```

The 140 rows are now represented once and only once in `RULERS_1776_NON_EUROPE_MASTER.csv`.

## 2. Critical P0/P2 decisions

- **DEI**: replace Reinier de Klerk with **Jeremias van Riemsdijk**, in office from 1775-12-28; delegated VOC Governor-General.
- **USA**: remove the anachronistic conception of **George Washington as President**. Washington is a military commander; the Second Continental Congress is the political organ and John Hancock its presiding president. The character layer may use Hancock only as a temporary `President of the Continental Congress` abstraction, while the fork's unified-USA/British-colony map/subject setup remains deferred.
- **BIC**: Warren Hastings remains historically appropriate only as a delegated East India Company Governor-General, not sovereign.
- **DUR**: Timur Shah Durrani is validated as Shah.
- **IR1**: `Omar Ahmad` is rejected in favor of **Omar Pasha**, delegated/semi-autonomous Pasha of Baghdad under Ottoman sovereignty.

## 3. Non-invention policy

No exact date was created from an approximate age or an undated ruler list. Unknown and conflicting chronologies are carried as such in `date_policy`, `notes`, and confidence fields.

The low-confidence identity set is:

```text
AGC, AIT, HAU, MJT, TGI, UZH, ARB, JMB
```

These cases are intentionally unresolved or conditional. CLEANUP-2C-1 must not turn them into fabricated historical certainty.

## 4. Structural/map deferrals

A substantial subset of the queue represents a later polity, an over-broad geographic abstraction, or a collective/confederal structure. The packet therefore uses explicit `*_DEFERRED` decisions instead of forcing one historical monarch into a false unitary tag.

Important examples include:
- ALK — Russian-American Company/settlement chronology is later than 1776.
- USA — revolutionary political structure conflicts with the fork's colony abstraction.
- ONT and NBS — later British colonial entities.
- IQU — later political abstraction.
- HAW and UNT — later/unified tags projected backward.
- DAI — 1776 Vietnam is politically divided during the Tây Sơn wars.
- LAN — Lanfang begins after the scenario start.
- MAD, BST, ORA, PHL, SIL, SOK, TRN and WTU — later or structurally incorrect centralized tags.
- CHC, CIR, BRG, PAN, SHS and others — collective/confederal structures without a safe unitary monarch.

## 5. Output packet

The historical authority packet for CLEANUP-2C-1 is:

1. `docs/research/characters/RULERS_1776_NON_EUROPE_MASTER.csv`
2. `docs/research/characters/RULERS_1776_NON_EUROPE_SOURCES.md`
3. `docs/research/characters/RULERS_1776_NON_EUROPE_CONSTITUTIONAL_NOTES.md`

This completion report may also be retained in `docs/research/characters/`.

## 6. Implementation gate

```text
NON_EUROPE_HISTORICAL_RESEARCH_COMPLETE = YES
SAFE_TO_PREPARE_CLEANUP_2C_1 = YES
CODEX_IMPLEMENTATION_PERFORMED = NO
VICTORIA3_RUNTIME_PERFORMED = NO
```

The next phase may now implement only what the MASTER authorizes. It must not redo historical research, must not invent identities for deferred rows, and must not modify map/ownership/state-region data opportunistically.
