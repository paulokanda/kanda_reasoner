Address the AI you're consulting as: "You are a Python specialist with
20 years of experience refactoring large-scale, multi-layered,
architecturally complex codebases. I need you to audit my
implementation plan before we write code." Then give it: (1) a short
summary of the task, (2) my proposed file/module breakdown with each
module's responsibility and how they interface. State this hard
constraint explicitly: every file, including helpers, must be strictly
more than 100 lines and strictly less than 500 lines — no tiny/trivial
modules (merge them into related ones) and no oversized files (split
along logical boundaries). Ask it to reply covering: structural
soundness, risks, concrete improvements, corrections/anti-patterns,
explicit compliance check against the 100–500 line rule (naming any
violating files), and its recommended final implementation logic.
Then return its full response to me for review.