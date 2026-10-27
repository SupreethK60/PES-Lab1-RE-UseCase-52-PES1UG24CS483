\# Lab 5 — Static Code Analysis Reflection



\*\*Project:\*\* Insurance Premium Calculator



\## 1. What did you learn from static code analysis?



Static code analysis helps identify potential defects, security vulnerabilities, and coding-style problems without requiring the program to be executed. Pylint checks code quality, Bandit identifies common security issues, and Flake8 checks style and formatting.



\## 2. Which issues were the most important to fix, and why?



The most important issues were the hardcoded authentication token, disabled TLS certificate verification, and unsafe archive extraction. These issues could expose sensitive credentials, weaken secure communication, or allow files to be extracted to unintended locations. Addressing them improves the security of the application.



\## 3. How did static analysis improve your code?



Static analysis helped improve naming consistency, exception handling, file handling, and formatting. It also helped identify a mutable default argument and highlighted the need for safer handling of authentication credentials, network requests, and archive extraction. The age calculation was corrected to account for whether the birthday had occurred in the current year.



\## 4. What are the limitations of static code analysis?



Static analysis tools cannot guarantee that a program is completely free of defects. They may miss runtime problems, business-logic errors, or vulnerabilities that depend on the application's environment. They can also produce findings that require manual review. Therefore, static analysis should be combined with execution tests, appropriate security testing, and code review.



\## Final Results



\- Pylint score: 10.00/10

\- Bandit: No issues identified

\- Flake8: No violations reported

\- Program execution: Successful with the tested sample inputs



