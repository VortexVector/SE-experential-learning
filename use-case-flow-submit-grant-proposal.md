# Use-Case Flow Specification

## Use Case: Submit Grant Proposal

| Field | Detail |
|---|---|
| **Use Case ID** | UC-04 |
| **Primary Actor** | Faculty Researcher |
| **Secondary Actor** | Research Dean |
| **Related Requirement** | FR-004 |
| **Includes** | Check Budget Balance |
| **Trigger** | Faculty Researcher wants to request sponsored funding for a research project. |

### Preconditions
1. The Faculty Researcher is authenticated and holds an active faculty profile in the system.
2. The Faculty Researcher has the funding agency details, requested amount, project duration, and an itemized budget breakdown ready to enter.
3. No other proposal from the same faculty member is currently "Under Review" for the same funding cycle.

### Postconditions
- **Success:** The grant proposal is stored with status **"Approved,"** a corresponding grant fund allocation record is created, and the Faculty Researcher is notified. FR-001 budget tracking becomes active for the new grant.
- **Failure / Alternate exit:** The proposal is stored with status **"Rejected"** or **"Revision Requested,"** no fund allocation is created, and the Faculty Researcher is notified with the Dean's comments.

### Main Success Scenario
1. The Faculty Researcher selects **"New Grant Proposal."**
2. The system displays a proposal form (title, funding agency, amount requested, project duration, itemized budget breakdown).
3. The Faculty Researcher completes the required fields and selects **"Submit."**
4. The system validates the entered budget breakdown against the requested amount (*includes* **Check Budget Balance**) and confirms the figures are internally consistent.
5. The system sets the proposal status to **"Submitted"** and notifies the Research Dean.
6. The Research Dean opens the proposal and reviews the budget breakdown and supporting details.
7. The Research Dean selects **"Approve."**
8. The system sets the proposal status to **"Approved,"** creates the grant fund allocation record, logs the decision (timestamp, approver) to the audit ledger, and notifies the Faculty Researcher.

### Alternate Flow A1 — Dean Requests Revision
> Branches from the Main Success Scenario at step 7.

7a. The Research Dean finds the budget breakdown incomplete or inconsistent and selects **"Request Revision"** instead of approving, attaching comments.
7b. The system sets the proposal status to **"Revision Requested,"** logs the decision, and returns the proposal to the Faculty Researcher together with the Dean's comments.
7c. The Faculty Researcher edits the proposal and resubmits it.
7d. The flow resumes at step 4 of the Main Success Scenario.

### Alternate Flow A2 — Dean Rejects the Proposal
> Branches from the Main Success Scenario at step 7.

7a. The Research Dean determines the proposal does not meet funding criteria and selects **"Reject,"** entering a reason.
7b. The system sets the proposal status to **"Rejected,"** logs the decision to the audit ledger, and notifies the Faculty Researcher with the stated reason.
7c. The use case ends without a fund allocation being created.

### Business Rules
- A proposal cannot move to **"Approved"** without a successful **Check Budget Balance** validation (FR-001 dependency).
- Every status transition is written to the immutable audit ledger (NFR-001).
