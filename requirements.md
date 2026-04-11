**Quality Plan
Stack**

1. Programming language: Python
2. Libraries: Poetry, FastAPI, SQLite, Streamlit,
3. Tools: GitHub Actions
**Team size** : 4-5 students
**Duration** : 2 weeks
**Project topic** : Team Mood tracking
**Project description:** A lightweight internal tool designed for agile teams to
monitor collective well-being. The application consists of a FastAPI backend and
a Streamlit frontend. Users can submit mood entries (emoji/rating) with
comments. The system aggregates this data to provide historical trends and
barplot visualizations, helping the team identify periods of high stress or peak
morale. The project operates without authentication, using a simple "user" field to
differentiate entries.
**Project details and expectations
Scope:** CRUD API Backend + Streamlit dashboard Frontend
**Features:**
1. Select mood/emoji/rating and provide a comment
2. Submit this mood entry (“happy”, “neutral”, “stressed”, etc.)
3. Retrieve mood entries from database
4. View historial data - changes of mood per day
5. Aggregate statistics - average mode per certain period
6. See barplots - mood distribution for a certain day and among all guys
7. Complete Filtration and sorting functionality is optional
**Constraints:**
1. No authorization
2. To differentiate guys mood has an owner (“user” field specified during
submission)


**Quality requirements
Attribute Metric Threshold Tool CI Gate?**
Maintainability Cyclomatic
complexity
<5 per function radon Yes
Style
conformance
0 PEP8 errors ruff or flake8 Yes
Code
formatting
100% black Yes
Type checking 0 errors mypy Yes
Line coverage >= 80% pytest-cov Yes
Reliability Unit tests 100% pass pytest Yes
Performance API response
time
P95 < 150ms locust or k6 No
Security High-severity
vulnerabilities
0 findings bandit Yes
Dependencies
vulnerabilities
0 vulnerabilities pip-audit or safety Yes
Documentation API endpoints
documented
100% endpoints
are visible in
Swagger UI: must
include a
summary,
description, and at
least one example
response
OpenAPI, manual
check during Code
Review
No
Inline
docstrings
100% of public
functions and
modules have
docstrings
interrogate Yes


**Quality Gates
Tools with Commands
Requirement Tool Command**
Cyclomatic complexity radon radon cc -a -s src/
Maintainability index radon radon mi -s src/
Style flake8 or ruff flake8 src/ OR ruff check src/
Formatting black black --check src/
Type checking mypy mypy src/
Coverage pytest-cov pytest –cov=src –cov-fail-under=
Unit testing pytest pytest tests/
Security (code) bandit bandit -r src/
Security (deps) pip-audit pip-audit
Performance locust Load test script, to run e.g.: locust -f
locustfile.py --headless -u 10 -r 1 -t 1m
Documentation interrogate interrogate -vv src/
**Gate When What Blocks?**
Pre-commit Before git push >0 errors from flake8 or bandit
PR (pre-merge) On Pull request
creation/update
Any failed unit test,
>0 mypy errors,
<80% coverage,
code review reject, absence of code
review from another team member (i.e.
self-review does not count)
Release Before demo Any of 6 first listed feature is missed
(feature 7 does not block), CI fails


