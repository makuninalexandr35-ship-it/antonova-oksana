Always use FSDB Protocol in ./.agent_memory/ before answering

FSDB Protocol:
- Read relevant files in .agent_memory/ before working on a request.
- Before the final answer, append new significant facts to the appropriate memory file.
- Preserve existing entries; do not rewrite whole files for routine updates.
- If a file exceeds 100 lines, compact older entries while retaining current facts and decisions.
- On requests to check or update memory, immediately reread the memory files.
- Verify remembered facts against current files when they may have changed.
