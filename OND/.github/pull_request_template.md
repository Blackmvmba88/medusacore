# PR Checklist

- [ ] `.github/copilot-instructions.md` is up to date and accurate
- [ ] WebSocket contract test (`tests/test_ws_contract.py`) passes locally and in CI
- [ ] If the WS message schema changed, both client and server are updated and golden examples are added to the instructions
- [ ] Manual QA: server runs, UI renders, and "Nota"/"RMS" update in both demo and mic modes
- [ ] For performance changes: include before/after notes (fps/memory)
- [ ] For visual changes: include before/after screenshots

---

Describe what this PR does and why:

- ...
