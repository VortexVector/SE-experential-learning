# Requirements Table
### Faculty Research Grant & Publication Tracker
**Course:** Requirements Engineering & UML Use-Case Modelling — Lab 1
**Problem Statement #09 — Campus & Academic Operations**
**Actors:** Faculty Researcher, Research Dean

---

## Functional Requirements

### FR-001 — Grant Budget & Expense Tracking
| Field | Detail |
|---|---|
| **Priority** | High |
| **Description** | The system shall track grant fund allocations, allow faculty to log equipment procurement expenses, and compute remaining budgetary balance. |
| **Acceptance Criteria** | **Pass:** Balance updates accurately and blocks expenses exceeding the grant cap. **Fail:** Overdraft is allowed without an admin override. |
| **Rationale** | Ensures fiscal accountability and prevents overspending of sponsored research funds. |

### FR-002 — Publication Record & Citation Metrics Tracking
| Field | Detail |
|---|---|
| **Priority** | High |
| **Description** | The system shall allow faculty researchers to register journal/conference publications and record their indexing status (e.g., Scopus/SCI/Web of Science) and citation counts, refreshed from linked bibliometric sources. |
| **Acceptance Criteria** | **Pass:** A publication's citation count and indexing status reflect the latest available source data within 24 hours of a source update. **Fail:** Stale or missing citation data persists beyond the refresh window without being flagged. |
| **Rationale** | Enables accurate assessment of faculty research output for annual appraisals, promotions, and institutional rankings. |

### FR-003 — Co-Author Approval Workflow
| Field | Detail |
|---|---|
| **Priority** | Medium |
| **Description** | The system shall notify all listed co-authors when a new publication entry is created and require each co-author to approve or dispute the authorship/contribution details before the publication is marked "Verified." |
| **Acceptance Criteria** | **Pass:** Publication status remains "Pending" until every listed co-author responds, and any dispute is routed to the Research Dean for resolution. **Fail:** A publication is marked "Verified" while co-authors have not all responded. |
| **Rationale** | Prevents authorship disputes and preserves the integrity of collaborative research records. |

### FR-004 — Grant Proposal Submission & Dean Approval
| Field | Detail |
|---|---|
| **Priority** | High |
| **Description** | The system shall allow faculty to submit new grant proposals with a budget breakdown, and shall allow the Research Dean to review the proposal and approve, reject, or request revisions. |
| **Acceptance Criteria** | **Pass:** Proposal state transitions correctly (Submitted → Under Review → Approved / Revision Requested / Rejected) with a timestamped decision log. **Fail:** A grant is activated and funded without a recorded Dean approval. |
| **Rationale** | Enforces institutional governance and accountability for sponsored fund commitments. |

### FR-005 — Fund Burn-Up Analytics Dashboard
| Field | Detail |
|---|---|
| **Priority** | Medium |
| **Description** | The system shall generate a burn-up chart per grant showing cumulative expenditure against the allocated budget over time, filterable by expense category and time period, and exportable as a report. |
| **Acceptance Criteria** | **Pass:** The chart accurately reflects logged expenses and updates as new expenses are approved. **Fail:** Chart totals diverge from the underlying ledger by more than a defined rounding tolerance. |
| **Rationale** | Gives faculty and administrators visibility into spending trends to support timely, informed budget decisions. |

---

## Non-Functional Requirements

### NFR-001 — Audit Ledger Integrity
| Field | Detail |
|---|---|
| **Type** | Security & Auditability |
| **Priority** | High |
| **Description** | The system shall maintain an immutable, tamper-evident audit ledger for all financial approvals and publication/journal status modifications. |
| **Acceptance Criteria** | **Pass:** Benchmarking tests confirm target latency and security standards under simulated peak load, and independent hash-chain verification detects any record tampering. **Fail:** A modification to a historical record goes undetected by the verification process. |
| **Rationale** | Sponsored-fund audits and academic-integrity reviews require verifiable, non-repudiable historical records. |

### NFR-002 — Performance & Scalability
| Field | Detail |
|---|---|
| **Type** | Performance & Scalability |
| **Priority** | Medium |
| **Description** | The system shall support at least 500 concurrent faculty/dean sessions, with publication-metric queries and dashboard rendering completing within 2 seconds under normal load. |
| **Acceptance Criteria** | **Pass:** Load testing at 500 concurrent users shows a 95th-percentile response time ≤ 2 seconds. **Fail:** Response times exceed the threshold, or errors occur under the load test. |
| **Rationale** | Ensures the portal stays usable during peak periods such as annual appraisal cycles and grant renewal deadlines. |
