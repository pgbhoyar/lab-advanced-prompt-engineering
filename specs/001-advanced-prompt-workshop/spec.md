# Feature Specification: Advanced Prompt Engineering Hands-On Workshop

**Feature Branch**: `001-advanced-prompt-workshop`

**Created**: 2026-07-13

**Status**: Draft

**Workshop Title**: Hands-On: Advanced Prompt Engineering

**Primary Model**: OpenAI GPT-5.4 hosted in Microsoft Foundry

**Target Session Length**: 75 minutes

**Input**: User description: "Create an accessible, hands-on advanced prompt-engineering workshop for attendees with a wide range of technical experience. Attendees must be able to complete equivalent exercises through the Microsoft Foundry portal or through Python, C#, or Java."

## Workshop Objective

Create a hands-on workshop that teaches attendees how to design, test, evaluate, and improve prompts for reliable enterprise AI applications.

The workshop must go beyond introductory prompting and demonstrate how prompts can be treated as testable, reusable, version-controlled engineering assets.

By the end of the session, attendees should be able to:

1. Identify weaknesses in an ambiguous prompt.
2. Create an explicit prompt contract.
3. Separate system instructions, user requests, and untrusted source data.
4. Apply constraints and delimiters.
5. Use few-shot examples appropriately.
6. Generate predictable structured outputs.
7. Decompose complex tasks into prompt chains.
8. Ground responses in supplied information.
9. Define fallback behavior for missing information.
10. Evaluate prompt variants using repeatable criteria.
11. Recognize basic direct and indirect prompt-injection attempts.
12. Create a reusable enterprise prompt through either the portal or a coding path.

## Target Audience

The workshop serves attendees with varied backgrounds, including:

- Participants with no coding experience
- Business and technology professionals
- Developers
- Solution architects
- Enterprise architects
- Product managers
- Technical leaders
- Data and AI practitioners
- Python developers
- C# developers
- Java developers

No previous prompt-engineering experience is required.

Coding-track attendees are expected to have the applicable development environment prepared before the workshop.

## Workshop Scenario

All core labs use one consistent, easy-to-understand scenario:

> Build an Enterprise Service Request Triage Assistant that reads synthetic IT support requests, identifies the request category and urgency, summarizes the problem, recommends the next action, and explains when the available information is insufficient.

Using one scenario throughout the workshop allows attendees to concentrate on prompt-engineering techniques rather than repeatedly learning new business domains.

The synthetic scenario must support demonstrations of:

- Ambiguous requests
- Missing information
- Conflicting information
- Long or irrelevant input
- Classification
- Summarization
- Structured output
- Policy-based grounding
- Few-shot examples
- Prompt chaining
- Evaluation
- Prompt injection
- Unsupported-answer handling

No real customer, employee, or company data will be used.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start the Workshop Successfully (Priority: P1)

As an attendee, I want to select either the portal path or a coding path and successfully send a request to the workshop model so that setup issues do not prevent me from participating.

**Why this priority**: No learning can occur until attendees can access the model. A fast and reliable onboarding experience is essential for a short hands-on session.

**Independent Test**: A first-time attendee can follow the setup instructions and receive a response from the workshop model without instructor intervention.

**Acceptance Scenarios**:

1. **Given** an attendee has a laptop and workshop access instructions, **When** the attendee starts the setup exercise, **Then** the attendee can clearly choose Microsoft Foundry portal, Python, C#, or Java.
2. **Given** an attendee chooses the portal path, **When** the attendee follows the portal instructions, **Then** the attendee can submit the starter prompt and view a response.
3. **Given** an attendee chooses a coding path, **When** the attendee configures the provided temporary credentials and runs the starter application, **Then** the attendee receives a model response without placing credentials in source code.
4. **Given** a coding attendee encounters a local dependency or permission problem, **When** the attendee selects the documented fallback path, **Then** the attendee can continue the same lab through the Microsoft Foundry portal.
5. **Given** an attendee has never used a model playground or SDK, **When** the attendee follows the instructions, **Then** no unexplained technical knowledge is required to complete the first request.

---

### User Story 2 - Improve an Ambiguous Baseline Prompt (Priority: P1)

As an attendee, I want to compare an ambiguous prompt with an explicit prompt contract so that I can observe how clearer instructions improve model behavior.

**Why this priority**: This establishes the foundational technique used throughout every later lab.

**Independent Test**: An attendee runs the baseline and improved prompts with the same input and identifies measurable differences in instruction adherence and completeness.

**Acceptance Scenarios**:

1. **Given** a vague baseline prompt, **When** the attendee runs it against the provided support request, **Then** the attendee can identify at least two weaknesses in the response.
2. **Given** the same support request, **When** the attendee adds an objective, audience, context, constraints, and success criteria, **Then** the revised response follows more of the documented requirements than the baseline response.
3. **Given** a prompt containing subjective language such as "make this better," **When** the attendee replaces it with observable requirements, **Then** the output can be evaluated using the provided rubric.
4. **Given** the baseline and revised responses, **When** the attendee scores both with the same evaluation criteria, **Then** the attendee can explain which changes caused the measurable improvement.

---

### User Story 3 - Separate Instructions from Untrusted Input (Priority: P1)

As an attendee, I want to separate system behavior, user requests, and source data so that the model can distinguish instructions from content it is being asked to process.

**Why this priority**: Instruction hierarchy and data separation are fundamental to reliable enterprise prompting and support later grounding and prompt-injection exercises.

**Independent Test**: An attendee creates separate system and user instructions and processes delimited source data without treating embedded source text as authoritative instructions.

**Acceptance Scenarios**:

1. **Given** a task with stable assistant behavior and a runtime user request, **When** the attendee places each instruction in its appropriate message, **Then** the model consistently follows the stable behavior while completing the current task.
2. **Given** a support request containing paragraphs of source data, **When** the attendee places the source data inside clear delimiters, **Then** the response distinguishes the supplied data from the prompt instructions.
3. **Given** source data containing the statement "ignore the previous instructions," **When** the model processes the data, **Then** it treats that statement as content rather than as a higher-priority instruction.
4. **Given** conflicting instructions, **When** the attendee reviews the model response, **Then** the response follows the documented instruction priority.

---

### User Story 4 - Use Few-Shot Examples to Clarify Behavior (Priority: P1)

As an attendee, I want to provide carefully selected examples so that I can improve classification, formatting, or boundary behavior when instructions alone are insufficient.

**Why this priority**: Few-shot prompting is a widely applicable technique that produces an easily observable before-and-after demonstration.

**Independent Test**: The attendee adds representative examples to a classification prompt and observes improved performance on a new test case.

**Acceptance Scenarios**:

1. **Given** a support-request classification task with ambiguous category definitions, **When** the attendee runs a zero-shot prompt, **Then** the attendee records the original classification and rationale.
2. **Given** representative examples covering common categories, **When** the attendee adds those examples and reruns the same input, **Then** the output more closely follows the expected classification behavior.
3. **Given** examples with inconsistent structure, **When** the attendee tests the prompt, **Then** the lab demonstrates why examples must be accurate and consistent.
4. **Given** an edge case not identical to any example, **When** the few-shot prompt processes it, **Then** the model applies the demonstrated pattern rather than copying an example literally.
5. **Given** an example that conflicts with a written rule, **When** the prompt is evaluated, **Then** the attendee can identify and correct the conflicting guidance.

---

### User Story 5 - Generate and Validate Structured Output (Priority: P1)

As an attendee, I want the model to return a predictable output structure so that the response can be reviewed consistently or consumed by another application.

**Why this priority**: Structured outputs demonstrate the transition from conversational prompting to enterprise application design.

**Independent Test**: The attendee generates an output containing all required fields and validates it using either programmatic validation or a portal validation checklist.

**Acceptance Scenarios**:

1. **Given** a support request and a required output contract, **When** the attendee runs the structured-output prompt, **Then** the response contains the required fields for summary, category, urgency, recommended action, missing information, and confidence.
2. **Given** an output schema with enumerated category and urgency values, **When** the model returns a response, **Then** all applicable values use only the allowed options.
3. **Given** a request with missing information, **When** the model creates the structured response, **Then** missing values follow the documented null or fallback behavior.
4. **Given** a fluent response that does not comply with the output contract, **When** the response is evaluated, **Then** it is scored as a failed structured output.
5. **Given** a coding-track attendee, **When** the structured response is received, **Then** the attendee can verify its validity automatically.
6. **Given** a portal-track attendee, **When** the structured response is received, **Then** the attendee can verify it using a concise manual checklist.

---

### User Story 6 - Decompose a Complex Prompt into a Prompt Chain (Priority: P2)

As an attendee, I want to divide a complex request into smaller prompt stages so that each stage has a clear responsibility and can be tested independently.

**Why this priority**: Prompt chaining improves observability and maintainability for complex enterprise workflows, but it builds on the foundational prompting techniques.

**Independent Test**: The attendee compares a single multi-purpose prompt with a two-stage or three-stage prompt chain and validates each intermediate result.

**Acceptance Scenarios**:

1. **Given** a prompt that asks the model to classify, summarize, recommend, and draft a customer response simultaneously, **When** the attendee runs it, **Then** the attendee records any missing, inconsistent, or weak portions.
2. **Given** the same task decomposed into distinct stages, **When** the attendee runs each stage, **Then** each stage has a defined input, responsibility, and output.
3. **Given** an invalid intermediate output, **When** the next stage would normally run, **Then** the workflow identifies the validation failure rather than silently continuing.
4. **Given** the single prompt and the chained approach, **When** both are evaluated, **Then** attendees can compare quality, complexity, traceability, and maintainability.
5. **Given** a portal attendee, **When** the attendee completes the chaining exercise manually, **Then** the attendee can copy the validated output of one stage into the next stage.

---

### User Story 7 - Ground Responses and Handle Missing Evidence (Priority: P2)

As an attendee, I want the model to answer from supplied policy information and acknowledge unsupported questions so that it does not invent enterprise rules or facts.

**Why this priority**: Grounding and uncertainty handling are critical for trustworthy enterprise applications.

**Independent Test**: The attendee gives the model a short policy document and verifies that answers are based only on the supplied policy.

**Acceptance Scenarios**:

1. **Given** a support policy and a question answered by the policy, **When** the attendee runs the grounded prompt, **Then** the response uses the applicable policy information.
2. **Given** a question not answered by the supplied policy, **When** the attendee runs the prompt, **Then** the response states that the provided information is insufficient.
3. **Given** two supplied passages that conflict, **When** the model produces a response, **Then** it identifies the conflict rather than silently choosing one statement.
4. **Given** a response containing an inference, **When** the response is reviewed, **Then** the inference is clearly distinguished from information explicitly stated in the source.
5. **Given** source content containing a fabricated URL or citation, **When** the prompt processes it, **Then** the model does not represent that source as independently verified.

---

### User Story 8 - Evaluate and Compare Prompt Variants (Priority: P2)

As an attendee, I want to evaluate prompt versions using the same test set and rubric so that prompt changes are based on evidence rather than personal preference.

**Why this priority**: Evaluation-driven iteration is the main distinction between casual prompting and prompt engineering.

**Independent Test**: An attendee evaluates at least two prompt versions against the same test cases and identifies an improvement or regression.

**Acceptance Scenarios**:

1. **Given** a baseline prompt, revised prompt, test set, and rubric, **When** the attendee evaluates both versions, **Then** both are scored using identical inputs and criteria.
2. **Given** a test set, **When** the attendee reviews it, **Then** it includes a normal input, ambiguous input, missing-information input, edge case, and adversarial input.
3. **Given** a revised prompt that improves the happy-path response but worsens missing-information handling, **When** evaluation results are compared, **Then** the regression is visible.
4. **Given** subjective output-quality criteria, **When** attendees use the rubric, **Then** each criterion has a clear scoring definition.
5. **Given** a model response that is eloquent but factually unsupported, **When** it is evaluated, **Then** fluency does not compensate for poor groundedness or correctness.
6. **Given** repeated executions that produce different responses, **When** consistency is being assessed, **Then** the attendee records the variation rather than selecting only the best result.

---

### User Story 9 - Test Basic Prompt-Injection Defenses (Priority: P2)

As an attendee, I want to test the prompt with benign adversarial input so that I understand that prompt instructions alone are not a complete security solution.

**Why this priority**: Enterprise prompts frequently process untrusted text. Attendees must understand both the value and limits of defensive prompt design.

**Independent Test**: The attendee runs the prompt against a synthetic direct or indirect injection attempt and verifies that the model maintains the intended task boundary.

**Acceptance Scenarios**:

1. **Given** a support request containing "ignore all previous instructions," **When** the request is processed as delimited data, **Then** the model continues the authorized triage task.
2. **Given** source data asking the model to reveal its system instructions or credentials, **When** the model responds, **Then** it does not provide secrets or hidden instructions.
3. **Given** a request outside the assistant's defined scope, **When** it is submitted, **Then** the model applies the documented out-of-scope behavior.
4. **Given** an adversarial test that bypasses the prompt boundary, **When** the result is reviewed, **Then** the workshop describes it as a failed test and explains that additional application-level safeguards are required.
5. **Given** a safety boundary, **When** it is demonstrated, **Then** the example remains benign, synthetic, and appropriate for a public user-group workshop.

---

### User Story 10 - Complete an Equivalent Coding Track (Priority: P2)

As a developer, I want to complete the same exercises through Python, C#, or Java so that I can apply the prompt techniques in my preferred development environment.

**Why this priority**: The coding paths help developers connect workshop concepts to application development while retaining an accessible no-code path.

**Independent Test**: Each supported language processes the same test input and produces an output conforming to the same prompt contract.

**Acceptance Scenarios**:

1. **Given** the Python, C#, and Java starter applications, **When** each application sends the same prompt and input, **Then** each follows the same expected behavior and output contract.
2. **Given** a language-specific code example, **When** an attendee reviews it, **Then** prompt content is clearly separated from model-connection code.
3. **Given** workshop credentials, **When** an application starts, **Then** credentials are read from local configuration or environment variables rather than source code.
4. **Given** an attendee changes a prompt, **When** the attendee reruns the application, **Then** no unrelated code change is required.
5. **Given** a coding attendee falls behind, **When** the attendee moves to the portal track, **Then** the attendee continues with the same lab number, prompt, and input data.
6. **Given** differences among language SDKs, **When** attendees compare the lab instructions, **Then** those differences do not change the learning objective or evaluation criteria.

---

### User Story 11 - Complete a Reusable Capstone Prompt (Priority: P3)

As an attendee, I want to create and test a reusable enterprise prompt so that I leave the workshop with a practical artifact demonstrating the techniques I learned.

**Why this priority**: The capstone reinforces learning but depends on successful completion of the core labs.

**Independent Test**: An attendee creates a prompt that passes the minimum capstone rubric against the provided test set.

**Acceptance Scenarios**:

1. **Given** the capstone requirements, **When** the attendee creates the prompt, **Then** it includes an objective, input contract, boundaries, output contract, and uncertainty policy.
2. **Given** the capstone test set, **When** the attendee runs the prompt, **Then** it handles at least one normal, ambiguous, missing-information, and adversarial case.
3. **Given** the initial evaluation results, **When** the attendee identifies a failure, **Then** the attendee revises the prompt and records the reason for the change.
4. **Given** a completed capstone, **When** it is reviewed, **Then** the attendee can explain which prompt-engineering techniques were applied.
5. **Given** an attendee who does not complete the capstone during the session, **When** the workshop ends, **Then** the attendee has sufficient instructions and assets to finish it independently.

---

### User Story 12 - Facilitate the Workshop Consistently (Priority: P2)

As a workshop facilitator, I want timed instructions, checkpoints, expected observations, and fallback options so that I can support attendees with different experience levels without losing control of the session.

**Why this priority**: A technically strong lab can still fail if participants become blocked or the facilitator cannot manage the limited session time.

**Independent Test**: A facilitator other than the original author can deliver the workshop using the supplied facilitator materials.

**Acceptance Scenarios**:

1. **Given** the facilitator guide, **When** the facilitator starts the session, **Then** each segment has a learning objective, suggested duration, demonstration cue, and completion checkpoint.
2. **Given** attendees progressing at different speeds, **When** a checkpoint is reached, **Then** slower attendees have a fallback or solution path and advanced attendees have an optional challenge.
3. **Given** a model-access or local-development issue, **When** the problem occurs, **Then** the facilitator can direct attendees to a documented recovery path.
4. **Given** limited workshop credentials or service quota, **When** usage approaches an operational limit, **Then** the facilitator has a documented mitigation strategy.
5. **Given** the end of the workshop, **When** temporary access is no longer needed, **Then** the facilitator follows the documented credential-revocation process.

---

### Edge Cases

The workshop and lab assets must account for the following cases:

- An attendee arrives after the setup portion.
- An attendee cannot install packages.
- An attendee cannot run local code because of corporate workstation restrictions.
- An attendee has no Git experience.
- An attendee has never used Visual Studio Code or a terminal.
- An attendee selects a coding language but the necessary runtime is unavailable.
- Temporary credentials are invalid, expired, or incorrectly copied.
- Credentials contain trailing spaces or formatting characters.
- The model deployment name differs from the model family name.
- Internet access is slow or unavailable.
- Service quota or rate limits are reached.
- A response is delayed or interrupted.
- The model returns a different but still acceptable result from the example.
- The model produces a fluent response that violates the output contract.
- Structured output omits a required value.
- Structured output contains an unexpected enum value.
- A test input is blank.
- A test input contains only irrelevant information.
- A test input contains contradictory statements.
- A test input contains insufficient information.
- A test input is much longer than normal.
- A request contains instructions embedded inside the source content.
- A request asks the model to expose credentials or hidden instructions.
- A prompt revision improves one criterion but reduces another.
- Repeated runs produce different results.
- A participant pastes private or proprietary information.
- An attendee finishes much earlier than the group.
- An attendee cannot complete the capstone within the scheduled session.
- The portal experience differs slightly from workshop screenshots.
- A language-specific SDK returns an error whose wording differs from the guide.
- The instructor must switch the entire group from code to the portal path.

## Core Lab Progression

The workshop must provide the following core progression.

### Lab 0 - Access and Baseline

- **Primary concept**: Establish a working environment and capture an unoptimized baseline.
- **Required outcome**: Every attendee successfully submits a prompt and saves the baseline response for later comparison.

### Lab 1 - Explicit Prompt Contracts

- **Primary concept**: Objective, audience, context, instructions, constraints, and success criteria.
- **Required outcome**: Attendees transform an ambiguous request into an observable and testable prompt.

### Lab 2 - Instruction Hierarchy and Delimited Data

- **Primary concept**: Separate stable behavior, runtime requests, and untrusted source content.
- **Required outcome**: Attendees demonstrate that instructions embedded in source data do not automatically control the assistant.

### Lab 3 - Few-Shot Prompting

- **Primary concept**: Use representative examples to clarify expected classifications or boundary decisions.
- **Required outcome**: Attendees improve an ambiguous classification task using a small, consistent example set.

### Lab 4 - Structured Output

- **Primary concept**: Define and validate an explicit output contract.
- **Required outcome**: Attendees produce a predictable response containing all required fields and valid allowed values.

### Lab 5 - Prompt Decomposition and Chaining

- **Primary concept**: Divide a complex task into independently testable stages.
- **Required outcome**: Attendees validate an intermediate result before using it in a subsequent prompt.

### Lab 6 - Grounding and Uncertainty

- **Primary concept**: Answer from supplied context and define behavior when evidence is insufficient.
- **Required outcome**: Attendees prevent unsupported answers and explicitly distinguish facts, inferences, and unknown information.

### Lab 7 - Evaluation and Adversarial Testing

- **Primary concept**: Compare prompt variants with a repeatable test set and rubric.
- **Required outcome**: Attendees identify at least one improvement, regression, or unresolved weakness using evidence.

### Capstone - Enterprise Triage Prompt

- **Primary concept**: Combine the techniques into a reusable prompt asset.
- **Required outcome**: Attendees create or begin a prompt that satisfies the capstone quality gates.

## Requirements *(mandatory)*

### Functional Requirements

#### Workshop Accessibility Requirements

- **FR-001**: The workshop MUST support a Microsoft Foundry portal path requiring no coding.
- **FR-002**: The workshop MUST support equivalent Python, C#, and Java coding paths.
- **FR-003**: Every required lab MUST be completable through the portal path.
- **FR-004**: The portal and coding paths MUST teach the same prompt-engineering technique.
- **FR-005**: Each lab MUST explain unfamiliar technical terms when first introduced.
- **FR-006**: Core instructions MUST use plain language and short, numbered steps.
- **FR-007**: Each lab MUST state its learning objective before the exercise begins.
- **FR-008**: Each lab MUST identify prerequisites and expected completion time.
- **FR-009**: Each lab MUST provide a visible completion checkpoint.
- **FR-010**: Each coding lab MUST provide a portal fallback.
- **FR-011**: Required learning MUST NOT depend on completing an optional challenge.
- **FR-012**: Attendees MUST be able to resume at the current lab after switching tracks. Because each lab is stateless and uses shared prompts and inputs, "resume" means restarting the current lab number from its beginning on the new track using the same prompt and input data (no mid-lab step state is preserved or required). The switch MUST be completable within the SC-002 five-minute target.
- **FR-013**: Copy-ready prompts and sample inputs MUST be supplied.
- **FR-014**: Expected results MUST describe required characteristics rather than requiring one exact model response.

#### Lab Design Requirements

- **FR-015**: Each core lab MUST teach one primary prompt-engineering concept.
- **FR-016**: Labs MUST follow a progressive sequence from baseline prompting to evaluation-driven prompt design.
- **FR-017**: Core labs MUST use a consistent enterprise service-request scenario.
- **FR-018**: Each technique lab MUST include a baseline prompt or prior prompt version.
- **FR-019**: Each technique lab MUST include a revised prompt.
- **FR-020**: Baseline and revised prompts MUST be tested with the same comparison input.
- **FR-021**: Each lab MUST ask attendees to observe a specific behavior before modifying the prompt.
- **FR-022**: Each lab MUST explain why the introduced technique addresses the observed weakness.
- **FR-023**: Each lab MUST include at least one reflection question.
- **FR-024**: Each lab SHOULD include an optional advanced challenge.
- **FR-025**: Core exercises MUST fit within the scheduled 75-minute workshop when delivered at the recommended pace.
- **FR-026**: Optional exercises MUST be clearly distinguished from the core path.
- **FR-027**: All source data used in the workshop MUST be synthetic or approved public data.
- **FR-028**: Lab examples MUST remain understandable without specialized industry knowledge.

#### Prompt-Engineering Technique Requirements

- **FR-029**: The workshop MUST demonstrate a zero-shot baseline.
- **FR-030**: The workshop MUST demonstrate an explicit prompt contract.
- **FR-031**: The prompt contract MUST include an objective, context, instructions, constraints, and output expectations.
- **FR-032**: The workshop MUST demonstrate the difference between stable system behavior and task-specific user instructions.
- **FR-033**: The workshop MUST demonstrate the separation of instructions from source data.
- **FR-034**: Source data MUST use clearly identifiable delimiters.
- **FR-035**: The workshop MUST demonstrate few-shot prompting.
- **FR-036**: Few-shot examples MUST be representative, accurate, and internally consistent.
- **FR-037**: The workshop MUST demonstrate a structured output contract.
- **FR-038**: Structured outputs MUST define required fields and allowed values where applicable.
- **FR-039**: Structured outputs MUST define behavior for missing information.
- **FR-040**: The workshop MUST demonstrate task decomposition.
- **FR-041**: Prompt-chain stages MUST define inputs, outputs, and responsibilities.
- **FR-042**: Prompt chains MUST validate intermediate output before continuing.
- **FR-043**: The workshop MUST demonstrate grounded generation using supplied reference material.
- **FR-044**: Grounded prompts MUST define whether outside knowledge is permitted.
- **FR-045**: Grounded prompts MUST define fallback behavior for unsupported questions.
- **FR-046**: Prompts MUST distinguish supported facts, inferences, and unknown information.
- **FR-047**: The workshop MUST demonstrate evaluation-driven prompt iteration.
- **FR-048**: The workshop MUST include benign adversarial prompt tests.
- **FR-049**: The workshop MUST NOT require or encourage disclosure of hidden chain-of-thought.
- **FR-050**: Where an explanation is useful, prompts SHOULD request concise rationale, evidence, assumptions, or a verification checklist.

#### Evaluation Requirements

- **FR-051**: Every core prompt feature MUST have documented evaluation criteria.
- **FR-052**: The workshop MUST provide a reusable evaluation rubric.
- **FR-053**: The standard rubric MUST evaluate task correctness.
- **FR-054**: The standard rubric MUST evaluate instruction adherence.
- **FR-055**: The standard rubric MUST evaluate completeness.
- **FR-056**: The standard rubric MUST evaluate relevance.
- **FR-057**: The standard rubric MUST evaluate groundedness where reference information is supplied.
- **FR-058**: The standard rubric MUST evaluate output-format compliance.
- **FR-059**: The standard rubric MUST evaluate missing-information behavior.
- **FR-060**: The standard rubric MUST evaluate boundary or safety compliance.
- **FR-061**: Each rubric criterion MUST have observable scoring guidance.
- **FR-062**: The default workshop rubric SHOULD use a simple zero-to-two scoring scale.
- **FR-063**: Every evaluated prompt MUST be tested against the same test cases as its comparison version.
- **FR-064**: Each core evaluation set MUST include a normal input.
- **FR-065**: Each core evaluation set MUST include an ambiguous input.
- **FR-066**: Each core evaluation set MUST include a missing-information input.
- **FR-067**: Each core evaluation set MUST include an edge case.
- **FR-068**: Each core evaluation set MUST include a conflicting, irrelevant, or adversarial input.
- **FR-069**: Evaluations MUST reveal regressions as well as improvements.
- **FR-070**: A single successful response MUST NOT be presented as proof of general reliability.
- **FR-071**: When consistency is evaluated, attendees MUST compare multiple inputs or repeated executions.
- **FR-072**: Programmatic validation MUST be used for coding-track structured outputs when practical.
- **FR-073**: Portal attendees MUST receive an equivalent manual validation checklist.

#### Security and Privacy Requirements

- **FR-074**: Workshop credentials MUST be distributed through a controlled method.
- **FR-075**: Credentials MUST NOT appear in source code.
- **FR-076**: Credentials MUST NOT appear in prompts, examples, screenshots, logs, or expected outputs.
- **FR-077**: Credentials MUST NOT be committed to version control.
- **FR-078**: Coding examples MUST obtain secrets from environment variables or an equivalent local secret mechanism.
- **FR-079**: Example configuration files MUST contain placeholders only.
- **FR-080**: Temporary workshop credentials MUST be revoked or rotated after the workshop.
- **FR-081**: Attendees MUST be instructed not to submit confidential, regulated, proprietary, or personal information.
- **FR-082**: All adversarial examples MUST be synthetic and benign.
- **FR-083**: Untrusted source content MUST be clearly identified as data.
- **FR-084**: Source content MUST NOT be permitted to override higher-priority workshop instructions.
- **FR-085**: The workshop MUST explain that prompt instructions are only one layer of a broader security strategy.
- **FR-086**: A failed adversarial test MUST be recorded as a failure rather than hidden or replaced with a successful example.
- **FR-087**: Consequential or external actions MUST remain outside the workshop scope.

#### Cross-Track Parity Requirements

- **FR-088**: Portal, Python, C#, and Java tracks MUST use the same business scenario.
- **FR-089**: All tracks MUST use equivalent prompt content.
- **FR-090**: All tracks MUST use the same core test inputs.
- **FR-091**: All tracks MUST use the same evaluation rubric.
- **FR-092**: All tracks MUST target the same required output behavior.
- **FR-093**: Language-specific differences MUST be limited to what is necessary to connect to and invoke the model.
- **FR-094**: The coding samples MUST keep prompt text easy to locate and modify.
- **FR-095**: Code samples MUST contain only the complexity required to demonstrate the lab.
- **FR-096**: Coding attendees MUST be able to rerun a prompt after editing only the prompt or input.
- **FR-097**: Failure in one coding track MUST NOT block completion through another track or the portal.

#### Facilitator Requirements

- **FR-098**: The workshop MUST include a facilitator guide.
- **FR-099**: The facilitator guide MUST include a recommended timeline.
- **FR-100**: The facilitator guide MUST identify required and optional labs.
- **FR-101**: The facilitator guide MUST include demonstration prompts.
- **FR-102**: The facilitator guide MUST include expected observations.
- **FR-103**: The facilitator guide MUST include attendee checkpoints.
- **FR-104**: The facilitator guide MUST include common questions and concise answers.
- **FR-105**: The facilitator guide MUST include setup and authentication troubleshooting.
- **FR-106**: The facilitator guide MUST include recovery guidance for dependency problems.
- **FR-107**: The facilitator guide MUST include a portal fallback for all coding exercises.
- **FR-108**: The facilitator guide MUST include guidance for managing attendees progressing at different speeds.
- **FR-109**: The facilitator guide MUST include a contingency plan for model quota, availability, or network problems.
- **FR-110**: The facilitator guide MUST include credential-distribution and credential-revocation procedures.
- **FR-111**: The complete workshop MUST be rehearsed end to end before delivery.

#### Workshop Deliverable Requirements

- **FR-112**: The workshop package MUST include a workshop overview.
- **FR-113**: The workshop package MUST include a pre-workshop setup guide.
- **FR-114**: The workshop package MUST include Microsoft Foundry portal instructions.
- **FR-115**: The workshop package MUST include Python starter instructions.
- **FR-116**: The workshop package MUST include C# starter instructions.
- **FR-117**: The workshop package MUST include Java starter instructions.
- **FR-118**: The workshop package MUST include all core lab instructions.
- **FR-119**: The workshop package MUST include copy-ready prompts.
- **FR-120**: The workshop package MUST include synthetic source data and test cases.
- **FR-121**: The workshop package MUST include evaluation rubrics.
- **FR-122**: The workshop package MUST include expected observations.
- **FR-123**: The workshop package MUST include troubleshooting guidance.
- **FR-124**: The workshop package MUST include capstone instructions.
- **FR-125**: The workshop package MUST include reference solutions or facilitator solutions.
- **FR-126**: Solutions MUST remain clearly separated from attendee instructions to prevent accidental disclosure.
- **FR-127**: Workshop assets MUST be usable after the temporary workshop credentials expire.
- **FR-128**: Model-specific behavior MUST be identified when it is relevant to an exercise.
- **FR-129**: Core prompt patterns SHOULD remain understandable and reusable with other compatible models.

### Key Entities

- **Attendee**: Represents a workshop participant. Key attributes: selected track, experience level, setup status, current lab, completed checkpoints, evaluation results, capstone status.
- **Learning Track**: Represents the method used to complete the labs. Allowed values: Microsoft Foundry portal, Python, C#, Java. Each track teaches the same required learning outcomes.
- **Lab**: Represents a focused hands-on exercise. Key attributes: lab identifier, title, primary technique, learning objective, estimated duration, prerequisites, baseline prompt, improved prompt, input data, checkpoint, test cases, evaluation rubric, troubleshooting guidance, optional challenge.
- **Prompt Asset**: Represents a reusable prompt or prompt stage. Key attributes: prompt identifier, name, version, purpose, objective, input variables, instructions, constraints, output contract, uncertainty policy, model-specific notes, known limitations, change rationale.
- **Prompt Variant**: Represents a version of a prompt being compared. Key attributes: variant identifier, parent prompt, version, changes from baseline, reason for change, test set used, evaluation scores, observed failures, regressions.
- **Test Case**: Represents one repeatable prompt input and expected behavior. Key attributes: test-case identifier, scenario type, input, expected characteristics, prohibited behavior, applicable rubric criteria. Scenario types include: normal, ambiguous, missing information, edge case, conflicting, irrelevant, adversarial.
- **Evaluation Rubric**: Represents the criteria used to score responses. Key attributes: rubric identifier, criteria, scoring scale, scoring definitions, required passing score, automatic checks, human-review checks.
- **Structured Output Contract**: Represents the required machine-readable or predictable response format. Key attributes: required fields, optional fields, field types, allowed values, missing-value behavior, validation rules.
- **Reference Context**: Represents supplied source information used for grounding. Key attributes: context identifier, source label, content, authority level, allowed usage, conflict-handling behavior.
- **Workshop Credential**: Represents temporary access to the workshop model. Key attributes: distribution method, validity period, authorized scope, revocation status. Credential values must never be stored as workshop-content entities.
- **Capstone Submission**: Represents the attendee's final reusable prompt. Key attributes: prompt contract, test results, revision notes, evaluation score, known limitations, completion status.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 90% of participating attendees receive their first model response within the first 10 minutes of the hands-on portion.
- **SC-002**: An attendee whose coding setup fails can switch to the portal path and resume the current lab within five minutes.
- **SC-003**: At least 80% of attendees complete Labs 0 through 4 during the live session.
- **SC-004**: At least 70% of attendees complete at least one advanced lab covering prompt chaining, grounding, evaluation, or adversarial testing.
- **SC-005**: At least 80% of attendees improve their prompt's total rubric score compared with the baseline prompt.
- **SC-006**: At least 80% of attendees can identify two specific weaknesses in the initial baseline response.
- **SC-007**: At least 80% of attendees create a prompt containing an explicit objective, relevant context, constraints, and output expectations.
- **SC-008**: At least 80% of attendees produce an output containing all required structured-output fields.
- **SC-009**: At least 90% of coding-track structured responses pass syntax or schema validation after the exercise is completed.
- **SC-010**: At least 80% of portal-track attendees correctly validate structured output using the supplied checklist.
- **SC-011**: At least 80% of attendees correctly identify when the supplied reference context is insufficient to support an answer.
- **SC-012**: At least 80% of attendees successfully test the prompt against a normal, ambiguous, and missing-information input.
- **SC-013**: At least 75% of attendees identify an improvement or regression by comparing two prompt variants with the same rubric.
- **SC-014**: At least 75% of attendees demonstrate that instructions embedded inside synthetic source data should not override the authorized task.
- **SC-015**: Portal, Python, C#, and Java paths use the same core prompts, test cases, and evaluation criteria.
- **SC-016**: No workshop credential appears in committed source code, distributed samples, screenshots, prompts, or workshop output.
- **SC-017**: All distributed source data is synthetic or approved public data.
- **SC-018**: Every core lab includes an objective, numbered instructions, copy-ready prompt, expected observations, checkpoint, evaluation method, and troubleshooting section.
- **SC-019**: A facilitator who did not author the workshop can complete the core workshop rehearsal using the supplied facilitator guide.
- **SC-020**: The complete core workshop can be delivered within 75 minutes without requiring optional challenges.
- **SC-021**: At least 80% of post-workshop survey respondents rate the workshop's instructions as clear or very clear.
- **SC-022**: At least 80% of post-workshop survey respondents report increased confidence in creating structured and reusable prompts.
- **SC-023**: At least 75% of attendees leave with a completed or partially completed capstone prompt that they can continue after the session.
- **SC-024**: Temporary workshop credentials are revoked or rotated within the organizer's defined post-workshop operational window.

## Minimum Viable Workshop

The minimum viable workshop consists of:

1. Access and baseline
2. Explicit prompt contracts
3. Instruction hierarchy and delimited data
4. Few-shot prompting
5. Structured output
6. A reusable evaluation rubric
7. Portal instructions
8. At least one tested coding path
9. Synthetic test data
10. Facilitator checkpoints
11. Credential-safety instructions
12. A portal fallback

Prompt chaining, grounding, adversarial testing, all three coding languages, and the full capstone remain required for the completed workshop package, but they may be delivered as later increments during workshop development.

## Assumptions

- The instructor-led workshop has approximately 75 minutes of instructional and hands-on time.
- Attendees bring their own laptops.
- Internet access is available at the venue.
- A GPT-5.4 deployment is available in Microsoft Foundry.
- Temporary workshop credentials are available and have sufficient quota.
- The organizer has permission to distribute temporary access to attendees.
- Portal attendees receive the necessary Microsoft Foundry project access.
- Coding attendees have prepared Python 3.10 or later, .NET 8.0 or later, or JDK 17 or later.
- Coding attendees can run applications locally.
- Attendees unable to run code can use the portal path.
- The facilitator will demonstrate one primary path live while the written materials support all tracks.
- Workshop examples use synthetic service-request data.
- The workshop focuses on text prompting.
- The same underlying prompt concepts apply across all supported tracks.
- Exact model responses may vary between executions.
- Workshop assets will remain available after the live event.
- Temporary credentials will not remain valid after the workshop.

## Dependencies

- Microsoft Foundry model availability
- GPT-5.4 deployment availability
- Sufficient request and token quota
- Venue internet connectivity
- Attendee access to the Microsoft Foundry portal
- Secure credential-distribution mechanism
- Prepared starter materials
- Prepared synthetic datasets
- Tested Python starter application
- Tested C# starter application
- Tested Java starter application
- Facilitator access to troubleshooting information
- Credential-revocation capability
- GitHub repository or equivalent workshop-content distribution location

## Out of Scope

The following topics are outside the required workshop scope:

- Model fine-tuning
- Training a foundation model
- Building a production retrieval system
- Creating a vector database
- Implementing a full RAG architecture
- Production application deployment
- Production monitoring architecture
- Agent tool calling
- Autonomous agent actions
- Computer-use models
- Multimodal prompting
- Image generation
- Audio prompting
- Extensive SDK instruction
- Language-specific application architecture
- Performance benchmarking among programming languages
- Model pricing comparison
- Complete Microsoft Foundry administration
- Production identity and access-management implementation
- Collection of real personal or customer data
- Processing confidential company documents
- Revealing hidden chain-of-thought
- Evaluating harmful prompt-injection payloads
- Performing external or consequential actions

Short conceptual references to these topics are permitted when needed to explain boundaries or next steps.
