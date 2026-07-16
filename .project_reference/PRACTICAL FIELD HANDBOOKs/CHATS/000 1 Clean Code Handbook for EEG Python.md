Clean Code Handbook for EEG Python

We need to answer the user's question: they ran (Get-Command python).Source and got C:\Users\paulo\miniconda3\python.exe. This indicates they are using the base conda environment, not the pkanda environment they mentioned earlier. The prompt shows (pkanda) but the python executable is from base miniconda3. That suggests the environment activation might be inconsistent or they haven't activated pkanda correctly. The user wants to know if it's pure or using conda. Answer: it's conda (miniconda3), but the environment pkanda is not active despite the prompt. Provide explanation and how to activate pkanda.

Thank you for running that command. The output C:\Users\paulo\miniconda3\python.exe tells us exactly what’s happening.
Answer

You are using Conda (Miniconda3), but you are NOT inside the pkanda environment – you are in the base environment.

The prompt shows (pkanda) because you (or your shell) manually set that string, but the actual Python interpreter is from the base Conda installation.
How to verify

Run this to see which Conda environment is actually active:
powershell

conda info --envs

Look for the asterisk * – that marks the active environment. You will likely see:
text

base                 *  C:\Users\paulo\miniconda3
pkanda                  C:\Users\paulo\miniconda3\envs\pkanda

This confirms you are in base.
Why the prompt says (pkanda)

Your PowerShell prompt has been customized (likely via conda init or a manual prompt function) to show (pkanda) – but Conda itself only updates the prompt when you conda activate pkanda. If you see (pkanda) but python points to miniconda3\python.exe, you have a mismatch – either:

    You activated pkanda earlier, but later deactivated it without refreshing the prompt.

    Or you manually set the prompt string.

How to actually activate pkanda
powershell

conda activate pkanda

Then verify:
powershell

(Get-Command python).Source

Should now show:
C:\Users\paulo\miniconda3\envs\pkanda\python.exe
So, to answer your original question

    Is it pure Python (venv) or Conda? → Conda (Miniconda3).

    Is the environment pkanda active? → No, base is active, despite the prompt.

If you want to ensure your PyCharm project uses the correct pkanda environment, go to File → Settings → Project → Python Interpreter and select the Conda environment pkanda explicitly. That way, the terminal inside PyCharm will activate the right environment automatically.
how install PySide6-WebEngine in  conda env  E:\envs\pykanda

The user wants to install PySide6-WebEngine in a Conda environment located at E:\envs\pykanda. I need to provide instructions. I will search for how to install PySide6-WebEngine in a Conda environment.
Found 16 web pages

The search results show that PySide6 can be installed via conda from conda-forge, but PySide6-WebEngine might not be available via conda. The second search result for "pip install PySide6-WebEngine" might provide information. I need to open result 0 from the first search to see if it contains relevant information.
Read 1 page
PySide6 ImportError

This thread mentions that the Conda package for PySide6 does not include the add-ons, specifically pyside6-addons, which includes QtWebEngineWidgets. The user had to install missing parts with pip. This is useful information.

Now, I need to search for how to install PySide6-WebEngine specifically using pip.
Found 10 web pages

The search results for "PySide6-WebEngine" pip install show RPM packages and a GitHub repository, but not a direct PyPI package. This suggests that PySide6-WebEngine might be part of the PySide6 package itself, or it might be a separate package not available via pip. The user might need to install the PySide6 package, which includes the WebEngine module. The question is about installing PySide6-WebEngine specifically. I need to provide instructions. I will search for "PySide6 WebEngine conda install".
Found 5 web pages

I will open result 1.
Read 1 page
PySide6 cannot find QtWebEngineWidgets module

The user's question has high authority requirements, I should prioritize using information from official sources. I need to search for "PySide6-WebEngine conda install" on official channels.
Found 4 web pages

The search results do not show a conda package for PySide6-WebEngine. The user's question is about installing PySide6-WebEngine in a conda environment. I need to provide a comprehensive answer that covers the available methods and potential issues. The answer will include steps to install PySide6 using pip or conda, and then how to verify the installation of the WebEngine module. I will also mention potential issues and solutions. Now I will formulate the final answer.

Here’s how to get the WebEngine module working in your pykanda environment:
1. Understand the Incompatibility

It's best to stick to one package manager to avoid conflicts. The PySide6 package from the conda-forge channel often doesn't include the WebEngine add-ons, which will cause an import error.
2. The Recommended Path: Create a Fresh pip Environment

To get a functional WebEngine module, the cleanest approach is to create a fresh environment and install PySide6 exclusively with pip.

Step 1: Create a New Environment
Open your terminal and run this command to create a new environment named pykanda with Python 3.12:
bash

conda create -n pykanda python=3.12 -y

Step 2: Activate the New Environment
bash

conda activate pykanda

Step 3: Install PySide6 with pip
bash

pip install pyside6

This command will install the complete PySide6 suite, including the PySide6.QtWebEngineWidgets module.

Step 4: Verify the Installation
To confirm the installation was successful, run the following Python code:
python

from PySide6.QtWebEngineWidgets import QWebEngineView
print("WebEngine module imported successfully!")

If you see the success message without errors, you're ready to go.
3. If You Must Use Your Existing conda Environment

If you want to use your existing conda environment, you can still try installing the required components with pip.

Step 1: Activate Your Target Environment
bash

conda activate pykanda

Step 2: Install with pip
bash

pip install pyside6

Step 3: Verify the Installation
Run the same verification code as above. If you encounter any import or platform plugin errors, you may need to run conda update --all to resolve dependencies.
4. Troubleshooting Common pip Installation Issues

If the installation using pip is slow or fails, you can use a faster mirror:
bash

pip install pyside6 -i https://pypi.tuna.tsinghua.edu.cn/simple

💎 Summary for Your Project

For this project, I strongly recommend Option 2 (The Recommended Path). It ensures you have a stable, complete environment for your PySide6 work from the start, eliminating potential headaches down the line. After creating the environment, the final step in PyCharm is to configure the project interpreter to use this new pykanda environment.
This response is AI-generated, for reference only.
Unresolved reference 'Qt'

We need to diagnose the "Unresolved reference 'Qt'" error in PySide6. This typically means the import is missing or the module structure is wrong. In PySide6, Qt is a top-level module but often you need to import from PySide6.QtCore. The user might be trying to use Qt.AlignCenter or similar. Let me provide a clear solution.

The error Unresolved reference 'Qt' in PySide6 usually means you're trying to use Qt without the correct import. Here's how to fix it.
Common cause

You wrote something like:
python

label.setAlignment(Qt.AlignCenter)   # ❌ Qt not imported

Solution 1 – Import Qt from QtCore
python

from PySide6.QtCore import Qt

label.setAlignment(Qt.AlignCenter)   # ✅ works

Solution 2 – Use the full namespace
python

from PySide6 import QtCore

label.setAlignment(QtCore.Qt.AlignCenter)

Full example showing correct imports
python

import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central = QWidget()
        layout = QVBoxLayout(central)
        label = QLabel("Hello")
        label.setAlignment(Qt.AlignCenter)   # now works
        layout.addWidget(label)
        self.setCentralWidget(central)

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())

Other common Qt enums

    Qt.AlignLeft, Qt.AlignRight

    Qt.Horizontal, Qt.Vertical

    Qt.Red, Qt.blue (for colors in some contexts)

    Qt.Drawer, Qt.Window (window flags)

Always import Qt from PySide6.QtCore when you need these constants. If the error persists, check that you have installed PySide6 correctly:
bash

pip show pyside6

And ensure your IDE is using the correct Python interpreter (the one with PySide6 installed).


Clean Code Book Overview
do you konw a book callled clean code ?

The user is asking about the book "Clean Code". I need to provide information about it. I will search for relevant sources.
Found 26 web pages

The search results provide information about the book. I need to provide a comprehensive answer. I'll open some of the relevant results.
Read 6 pages
代码整洁之道
Clean Code by Uncle Bob - Book Review - Must read for Java Programmers
MPG.eBooks - 职员浏览: Clean code
Robert C. Martin Series- Clean Code | 9780135398579 | Robert Martin | Boeken | bol
https://www.library.nu.edu.eg/cgi-bin/koha/opac-export.pl?op=export&bib=125&format=isbd
View All

I have gathered information from multiple sources. I will now provide a comprehensive answer.

Yes, you've likely come across one of the most influential books in software development: Clean Code: A Handbook of Agile Software Craftsmanship by the renowned software expert Robert C. Martin (often affectionately called "Uncle Bob").

It is widely considered a must-read reference for producing high-quality, maintainable code.
📖 The Core Philosophy

The central idea is that code quality is directly linked to its readability and maintainability. The book argues that "clean code" is code that is easy to understand, easy to change, and a joy to work with. It's not just about whether the code works; it's about how it communicates its intent to other developers.
📚 What's Inside the Book?

Over the course of its 400+ pages, the book provides a systematic approach to writing good code. The original version is structured into three main parts, each building on the last:

    Part 1: The Principles, Patterns, and Practices - This section introduces the fundamental rules and guidelines for writing clean code.

    Part 2: The Case Studies - Here, you'll see the principles in action. Uncle Bob walks you through the process of cleaning up and refactoring real, messy code into something clean and efficient.

    Part 3: The Heuristics and "Smells" - The final part is a handy reference list of code "smells" (indicators of potential problems) and heuristics (rules of thumb) to guide your own code reviews and improvements.

🗺️ A Guide to the Core Chapters

The book is packed with practical advice, covering a wide range of topics. The table below provides a quick overview of the key chapters:
Category	Chapter	Core Idea
The Basics	Meaningful Names	Choosing clear, intention-revealing names for variables, functions, and classes.
	Functions	Keeping functions small, focused on a single task, and with minimal arguments.
	Comments	The best comment is a well-written code; comments should explain why, not what.
Code Structure	Formatting	Using consistent formatting (like vertical density and horizontal spacing) for readability.
	Objects & Data Structures	The important distinction between exposing data and hiding data structures.
Advanced Topics	Error Handling	Treating error handling as a distinct, separate concern that doesn't obscure code logic.
	Boundaries	Learning to cleanly integrate third-party code into your own system.
	Unit Tests	Keeping tests as clean and maintainable as production code; using the Test-Driven Development (TDD) pattern, Build-Operate-Check.
Systems & Design	Classes	The class organization and the "Single Responsibility Principle" (SRP).
	Systems	Separating the construction logic of a system from its runtime usage.
	Emergence	How a design with simple rules (e.g., "runs all tests, contains no duplication") naturally emerges into a clean structure.
Deep Dive	Concurrency	Writing clean, thread-safe code in multi-threaded environments.
✨ What About the New Edition?

It's important to note that there is a Second Edition of Clean Code, published in 2026, which is a comprehensive rewrite. While it retains the core philosophy, the new edition expands its scope significantly:

    Updated Languages: It now includes examples in modern languages like Go, Python, Clojure, C#, and C alongside Java and JavaScript.

    Modern Practices: It delves deeper into testing disciplines, design and architecture principles, and the effective use of AI tools for coding.

    New Structure: The content is reorganized into four parts, covering basic coding practices, design principles, high-level architecture, and even the ethics of software craftsmanship.

Both editions of Clean Code have left a profound mark on the industry and continue to shape how developers think about the craft of writing code. Are you interested in learning about some of the specific concepts from the book, or perhaps how to apply them in a particular programming language?
-----------------PROMPT

You are a senior software engineer and technical educator with 20+ years of
hands-on experience. Your task is to produce a PRACTICAL FIELD HANDBOOK of
the following work:

  TITLE  : [BOOK / PAPER / FRAMEWORK / SPECIFICATION TITLE]
  AUTHOR : [AUTHOR(S)]
  DOMAIN : [e.g. Python, System Design, ML, DevOps, Architecture, Security]
  MY LEVEL: [beginner / intermediate / advanced]
  MY CONTEXT: [e.g. "I write Python backend APIs solo", "I lead a 5-person team",
               "I'm preparing for system design interviews"]:
            MY CONTEXT: "I write Python backend APIs solo",  
            "I'm neurophysiologst specialist in EEG and  a hobbist programmer in python, 
            now turning in to a prompt programer because it spare me time". 
            The important thing to me is create perfect architectured EEg apps for Quantitative EEG,
            and I intend to learn this matherial while doing "you tube classes" in python code for 
            neurophysiologists with no idea about python programming or quantitative EEG, 
            but that urge learning creating apps for qEEG to extract EEg information from that using python. 
            So probably the content you create about the book will become a "series" or course in "you tube"

────────────────────────────────────────────────────────────────────
HANDBOOK STRUCTURE  (follow this order exactly)
────────────────────────────────────────────────────────────────────

1. ONE-PARAGRAPH ESSENCE
   What is the core thesis of this work in plain language?
   Why does it matter TODAY, not just when it was written?

2. MENTAL MODEL MAP
   The 5–8 central concepts as a hierarchy or dependency map.
   Show how they connect. Text-diagram is fine.

3. CHAPTER-BY-CHAPTER FIELD NOTES
   For each major chapter or section:
   - Core idea in ONE sentence
   - The single most actionable rule or pattern
   - A minimal, realistic code or config example in [DOMAIN]
   - One "anti-pattern" — what this chapter tells you to STOP doing
   - Difficulty to apply in practice: [Easy / Medium / Hard]

4. THE DAILY CHECKLIST
   A single-page checklist a developer can paste above their desk.
   Organized by: Writing Code / Reviewing Code / Designing / Debugging

5. THE DIRTY DOZEN
   The 12 most commonly violated principles from this work,
   with one-line fixes for each.

6. PATTERN QUICK-REFERENCE TABLE
   | Pattern/Rule | What it solves | Red flag it fixes | One-line example |

7. COMMON MISCONCEPTIONS
   What do people often get WRONG about this book's advice?
   What advice is CONTEXT-DEPENDENT and when should you ignore it?

8. EVOLUTION SINCE PUBLICATION
   What has aged well? What has been superseded by modern tooling,
   language features, or paradigms? (Be honest, not reverential.)

9. COMPANION RESOURCES
   3–5 books, talks, or tools that pair best with this work.
   One sentence on WHY each one pairs well.

10. 30-DAY ADOPTION PLAN
    Week 1: What to read and internalize.
    Week 2: What to audit in existing code.
    Week 3: What to refactor.
    Week 4: What to automate or enforce via tooling/linting/CI.

────────────────────────────────────────────────────────────────────
OUTPUT RULES  (non-negotiable)
────────────────────────────────────────────────────────────────────

- Prioritize PRACTICAL over THEORETICAL throughout.
- All code examples must be in [DOMAIN] and reflect CURRENT best practices
  for [CURRENT YEAR], not the book's original language or era.
- Use concrete, realistic naming — no foo/bar/baz.
- Be opinionated. Say "prefer X over Y because Z", not "some people think".
- Never pad. If a section is genuinely short, keep it short.
- If the answer exceeds your comfortable output window, STOP cleanly
  after completing the current section, print exactly:

      ── PAUSED: ready for Section [N] — reply GO to continue ──

  Do NOT rush, truncate mid-thought, or summarize early to fit. If tolkens are finishing for a answer just ask 
- can I continue?   Wait for GO, continue. Quality over completeness-in-one-shot.

We need to produce a practical field handbook for "Clean Code" by Robert C. Martin. Domain: Python (since user writes Python backend APIs, and for EEG apps). User's level: intermediate? Actually they are a hobbyist programmer turning into prompt programmer, neurophysiologist specialist in EEG, wants to create perfect architected EEG apps for quantitative EEG. They will teach on YouTube to neurophysiologists with no Python or qEEG knowledge. So examples should be EEG-related in Python (using libraries like MNE, NumPy, etc.). Current year: 2026. The book has a second edition 2026, but we should likely focus on timeless principles while adapting to modern Python.

We must follow the handbook structure exactly: 1. Essence, 2. Mental Model Map, 3. Chapter-by-chapter field notes, 4. Daily Checklist, 5. Dirty Dozen, 6. Pattern Quick-Reference Table, 7. Common Misconceptions, 8. Evolution Since Publication, 9. Companion Resources, 10. 30-Day Adoption Plan.

We need to be practical, code examples in Python for EEG (e.g., loading EEG data, filtering, epoch extraction, feature calculation). Use realistic naming like raw_eeg, compute_alpha_power, reject_artifacts.

Output must be within token limits. If too long, pause. Let's start.
Practical Field Handbook: Clean Code for Python EEG Applications

TITLE: Clean Code: A Handbook of Agile Software Craftsmanship
AUTHOR: Robert C. Martin (“Uncle Bob”)
DOMAIN: Python (EEG / Quantitative EEG application development)
MY LEVEL: Intermediate (hobbyist → prompt programmer)
MY CONTEXT: Solo developer, neurophysiologist creating EEG apps for qEEG; teaching via YouTube to non‑programmer neurophysiologists.
1. ONE‑PARAGRAPH ESSENCE

Clean Code argues that readable, maintainable code is more valuable than clever, compact, or “just working” code – because most time in a software project is spent reading and changing existing code. For you as a solo neurophysiologist building EEG apps, this means your future self (and your YouTube audience) will understand why you filtered at 0.5‑40 Hz, how to safely add a new feature like connectivity analysis, and where to fix a bug in artifact rejection – without fear of breaking everything. Today, with AI‑assisted coding, clean code is even more critical: you can prompt a language model to generate entire EEG pipelines, but if the code is messy, you cannot verify, trust, or adapt it. Clean code turns your YouTube tutorials from “copy this mess” into “master this craft.”
2. MENTAL MODEL MAP
text

Readability > Cleverness
        │
        ▼
┌─────────────────────────────────────────────────┐
│  NAMES (intention‑revealing, pronounceable)     │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  FUNCTIONS (small, one thing, no side effects)  │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  COMMENTS   │    │  FORMATTING │    │   OBJECTS   │
│  (why, not  │    │ (vertical   │    │ vs. DATA    │
│   what)     │    │  density)   │    │ structures  │
└─────────────┘    └─────────────┘    └─────────────┘
        │                 │                   │
        ▼                 ▼                   ▼
┌─────────────────────────────────────────────────┐
│  ERROR HANDLING (separate from business logic)  │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  TESTS (clean, fast, isolated, one concept)     │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  CLASSES (SRP – single responsibility)          │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  SYSTEMS (separate construction from use)       │
└─────────────────────────────────────────────────┘

Key dependency: You cannot have clean tests without clean functions. You cannot have clean classes without clean tests. Start with names and functions – those are your highest leverage.
3. CHAPTER‑BY‑CHAPTER FIELD NOTES

*Based on the 1st edition chapters (timeless structure), adapted to Python 3.12+ and MNE‑EEG examples.*
Chapter 1: Clean Code
Aspect	Description
Core idea	Code is clean if it’s easy to understand by other humans (including your future self), not just the computer.
Actionable rule	Before writing any EEG processing step, ask: “If I see this code 6 months from now, can I change it without fear?”
Example	Instead of eeg = mne.io.read_raw_edf('pat1.edf', preload=True), wrap with intention: def load_subject_eeg(subject_id: str) -> mne.io.Raw:
Anti‑pattern	“It works, so I’ll commit and move on” – ignoring readability for speed.
Difficulty	Easy (conceptual)
Chapter 2: Meaningful Names
Aspect	Description
Core idea	Every variable, function, class name must reveal its intent, not just its type or value.
Actionable rule	Replace any name that could mean two things – e.g., data → raw_voltage_microvolts.
Example	alpha = np.mean(power[8:13]) → alpha_power_microvolts_squared = calculate_band_power(psd, freq_band=(8, 13))
Anti‑pattern	Hungarian notation in Python (freq_list, i_subject, dict_data). Or one‑letter names except loop indices.
Difficulty	Easy – requires only discipline
Chapter 3: Functions
Aspect	Description
Core idea	Functions should be small (≤5 lines ideally, ≤20 lines in Python), do one thing, and have no side effects.
Actionable rule	If you need a comment inside a function to explain a “step”, extract that step into a named function.
Example	Instead of a 30‑line preprocess(raw), do:
raw = filter_standard_eeg(raw)
raw = interpolate_bad_channels(raw)
raw = apply_reference(raw, ref='average')
Anti‑pattern	Functions that both compute and plot, or that modify a global list of rejected epochs.
Difficulty	Medium – requires practice to break habits
Chapter 4: Comments
Aspect	Description
Core idea	Comments are failures of expression. Use code to say what, comments only for why (business rules, quirks of EEG).
Actionable rule	If you write a comment, first try to rename the function or add a small helper. Only comment if that fails.
Example	❌ # filter between 0.5 and 40 Hz → rename to bandpass_filter_eeg(raw, lowcut=0.5, highcut=40)
Anti‑pattern	Commented‑out code (“old way of artifact rejection”) – delete it, git remembers.
Difficulty	Easy – but developers love to over‑comment
Chapter 5: Formatting
Aspect	Description
Core idea	Vertical density (few empty lines) and consistent horizontal spacing make code scan like a newspaper – most important concepts first.
Actionable rule	Group related functions vertically; separate different concerns with a single blank line. Use Black formatter.
Example	Top of module: imports, constants (sample rate, band limits), then public functions, then helpers.
Anti‑pattern	Long files (>500 lines) with no logical grouping.
Difficulty	Easy – automate with Ruff/Black
Chapter 6: Objects and Data Structures
Aspect	Description
Core idea	Prefer data structures (simple containers like dataclasses) for transferring EEG data, and objects (classes with methods) for complex behavior like filtering.
Actionable rule	Use @dataclass for EEG metadata (subject ID, sampling frequency, channel names). Use classes for signal processing algorithms.
Example	class EEGPreprocessor: with methods .apply_bandpass(), .detect_bad_channels(), but returning plain numpy arrays or dataclasses.
Anti‑pattern	A class named EEGData with both properties and methods that modify the data – violates separation.
Difficulty	Medium – many tutorials mix concerns
Chapter 7: Error Handling
Aspect	Description
Core idea	Error handling is one distinct concern. Don’t obscure normal logic with try/except; wrap external calls.
Actionable rule	For file I/O or network (e.g., loading EDF files), catch exceptions at the boundary, convert to domain‑specific exceptions or result objects.
Example	Instead of raw = mne.io.read_raw_edf(file) everywhere, define def load_eeg_safe(path: Path) -> Optional[mne.io.Raw]: that logs and returns None or raises a custom EEGLoadError.
Anti‑pattern	Using except: (bare except) or putting try/except around every line.
Difficulty	Easy – once you remember that Python can raise everywhere
Chapter 8: Boundaries
Aspect	Description
Core idea	Isolate third‑party libraries (MNE, NumPy, SciPy) behind your own interfaces, so you can change them or mock them in tests.
Actionable rule	Create a thin wrapper around MNE’s filtering function – that wrapper is the only place you call mne.filter.filter_data.
Example	def apply_bandpass(signal, sfreq, low, high): return mne.filter.filter_data(signal, sfreq, low, high) – now you can swap to SciPy later without changing 100 files.
Anti‑pattern	Directly importing mne in 20 different EEG processing modules.
Difficulty	Medium – requires foresight, pays off after first library upgrade
Chapter 9: Unit Tests
Aspect	Description
Core idea	Tests must be as clean as production code, follow the same naming/function rules, and test one concept per test.
Actionable rule	For each EEG function, write a test using pytest that compares output to a known small synthetic EEG signal.
Example	def test_compute_alpha_power_returns_positive(): generate 10 Hz sine wave, compute power, assert > 0.
Anti‑pattern	Tests that are long, full of comments, or that depend on real EDF files on disk.
Difficulty	Hard for beginners – but critical for qEEG accuracy
Chapter 10: Classes
Aspect	Description
Core idea	Classes should have a single responsibility (SRP). A class called EEGAnalyzer that loads, filters, computes features, and plots – does too much.
Actionable rule	Split into: EEGLoader, EEGFilter, FeatureExtractor, EEGPlotter. Each has one reason to change.
Example	class AlphaPowerExtractor: only extract(raw) -> float.
Anti‑pattern	“God class” with 50 methods and 10 responsibilities.
Difficulty	Medium – requires practice to identify responsibilities
Chapter 11: Systems
Aspect	Description
Core idea	Separate construction (how objects are wired) from use (how they work). Use dependency injection.
Actionable rule	Don’t create dependencies inside functions – pass them as arguments or use a simple DI container.
Example	Instead of extractor = AlphaPowerExtractor() inside process_patient(), do def process_patient(extractor: AlphaPowerExtractor, raw: Raw) -> float:.
Anti‑pattern	Hard‑coded file paths, global configuration, or if __name__ == "__main__" doing both setup and processing.
Difficulty	Hard for solo devs who start with scripts – but invaluable for reusable YouTube code
Chapter 12: Emergence
Aspect	Description
Core idea	Simple rules (tests pass, no duplication, expressive names, minimal classes) naturally lead to clean design – you don’t need upfront big architecture.
Actionable rule	Whenever you copy‑paste EEG code between notebooks, extract it into a function. Duplication is the enemy.
Example	You wrote np.mean(psd[8:13]) twice – create band_power(psd, fmin, fmax).
Anti‑pattern	“We’ll refactor later” – later never comes.
Difficulty	Easy to start, hard to maintain discipline
Chapter 13: Concurrency
Aspect	Description
Core idea	Keep concurrent code (e.g., processing many EEG files in parallel) separate, simple, and thread‑safe with immutable data.
Actionable rule	Use concurrent.futures.ProcessPoolExecutor for CPU‑bound EEG processing, and pass only immutable arrays (no shared state).
Example	with ProcessPoolExecutor() as executor: results = list(executor.map(compute_alpha, raw_list))
Anti‑pattern	Using threads (GIL limitation) or sharing Python objects between processes.
Difficulty	Hard – but Python’s ProcessPoolExecutor makes it easier than Java
Chapter 14: Successive Refinement (Case Study)
Aspect	Description
Core idea	Writing clean code is iterative. First get it working (messy), then refactor (clean). Never commit messy code to main.
Actionable rule	After finishing an EEG feature extraction that works, take 10 minutes to rename variables, split long functions, and remove duplication.
Example	Start with def a(x): return np.sum((x-mean(x))**2) → refine to def compute_variance(signal: np.ndarray) -> float: with clear steps.
Anti‑pattern	“I’ll clean it tomorrow” – leads to irreversible technical debt.
Difficulty	Medium – requires self‑discipline
Chapter 15: JUnit internals (skip for Python)
Aspect	Description
Core idea	Not directly applicable – but the lesson is: even framework code should be clean.
Actionable rule	If you write a decorator or context manager in Python, apply the same naming/function rules.
Difficulty	N/A
Chapter 16: Refactoring the case study
Aspect	Description
Core idea	Refactoring is not rewriting; it’s small, behavior‑preserving transformations.
Actionable rule	Use PyCharm or VSCode refactoring tools: extract method, rename, inline variable – one at a time.
Anti‑pattern	Refactoring and adding new EEG features in the same commit.
Difficulty	Medium
Chapter 17: Smells and Heuristics
Aspect	Description
Core idea	A catalogue of “code smells” (like long parameter lists, dead code, speculative generality) – use as a diagnostic checklist.
Actionable rule	Once a week, pick one smell (e.g., “Too many arguments”) and scan your EEG codebase for it.
Example	def process(raw, lowcut, highcut, notch, reject, interpolate, montage, ...) → wrap parameters in a ProcessingConfig dataclass.
Anti‑pattern	Ignoring smells because “the code is small”.
Difficulty	Easy once you internalize the smells

─ PAUSED: ready for Section 4 (The Daily Checklist) — reply GO to continue ──
