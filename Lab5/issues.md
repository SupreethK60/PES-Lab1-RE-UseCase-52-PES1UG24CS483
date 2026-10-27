\# Lab 5 — Static Code Analysis Issues



\*\*Project:\*\* Insurance Premium Calculator



\## Issues Identified and Fixed



| No. | Issue | Tool / Category | Fix Applied | Priority |

|---|---|---|---|---|

| 1 | Mutable default argument could cause shared state between function calls. | Pylint — Code quality | Replaced the mutable default with `None` and initialized the value inside the function. | Medium |

| 2 | Hardcoded underwriter authentication token. | Bandit — Security | Moved the token to the `UNDERWRITER\_TOKEN` environment variable and used secure comparison. | High |

| 3 | TLS certificate verification was disabled. | Bandit — Security | Restored certificate verification and enforced HTTPS for remote rate-table requests. | High |

| 4 | Unsafe archive extraction could allow files to be written outside the intended directory. | Bandit — Security | Added archive extraction safeguards and used the data extraction filter. | High |

| 5 | Bare exception handling could hide unexpected errors. | Pylint — Error handling | Replaced broad exception handling with more specific exception handling. | Medium |

| 6 | Age calculation did not account for whether the birthday had occurred in the current year. | Functional correctness | Updated age calculation to consider the month and day of birth. | Medium |

| 7 | File handling did not consistently use a context manager. | Pylint — Code quality | Used a `with` statement to ensure proper file closure. | Low |

| 8 | Long lines and inconsistent formatting violated style guidelines. | Flake8 — Formatting | Reformatted long lines and improved naming and code organization. | Low |



\## Final Static Analysis Results



\- \*\*Pylint:\*\* 10.00/10

\- \*\*Bandit:\*\* No issues identified

\- \*\*Flake8:\*\* No violations reported



\## Conclusion



The Insurance Premium Calculator was reviewed using Pylint, Bandit, and Flake8. The identified code-quality, security, and formatting issues were addressed. The final program executed successfully with the sample inputs used during testing.



