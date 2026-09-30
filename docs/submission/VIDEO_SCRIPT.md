# Plumbline: Demonstration Video Storyboard & Script

- **Target Video Duration:** 2 minutes 45 seconds (Limit: 3:00)
- **Narration Pace:** ~140 words per minute (~385 words total)
- **Audio:** Clear English voiceover, zero background music.
- **Visuals:** Real 1080p screen capture of browser at 1440×900 in light theme.

---

## Storyboard & Narration

### Scene 1: The Legacy Problem & Introduction (0:00 – 0:15)
- **On Screen:** Clean view of the Plumbline Home screen (`http://localhost:8000`). Mouse hovers over the headline *"Refactor old code without changing what it does."*
- **Voiceover:**
  > "Every engineering team has legacy code they are afraid to touch. When developers use AI to refactor it, the code looks great and passes the tests the model just wrote—yet silently breaks in production. We built Plumbline to replace vibes with experimental proof."

---

### Scene 2: Selecting a Specimen & Starting the Run (0:15 – 0:40)
- **On Screen:** Mouse clicks on the `invoice_totals.py` specimen card. The description highlights the subtle trap: *"Rounds prices two ways (banker's vs half-up)"*. Mouse clicks **Start run**. Screen navigates smoothly into the Run Cockpit.
- **Voiceover:**
  > "Here, we select a 232-line invoice calculation module. We choose our modernization goal and hit Start Run. Everything that happens next executes in completely isolated Nebius Token Factory Sandboxes—nothing runs on our host machine."

---

### Scene 3: Recording Pins & Planted Bug Tripwires (0:40 – 1:10)
- **On Screen:** Cockpit view. Stage 1 completes as Nemotron 3 Ultra maps out code risks. Stage 2 executes as Nemotron 3 Super writes 14 characterization tests with hermetic fixtures. Stage 3 activates: the horizontal tick strip on the Plumb Graph begins filling with green checkmarks as 20 mutants are tested across 30 parallel sandbox forks.
- **Voiceover:**
  > "First, Nemotron 3 Ultra analyzes the module's behavior. Then, Nemotron 3 Super writes characterization tests in an isolated sandbox. But we don't just trust the tests: our AST mutator plants 20 tripwires. Token Factory Sandboxes fork 30 environments in parallel, and our tests catch 100% of the planted bugs."

---

### Scene 4: Refactor Candidates & The Plumb Graph Divergence (1:10 – 1:50)
- **On Screen:** Stage 4 begins. Candidate A (Conservative) and Candidate B (Balanced) appear on the Plumb Graph. In Stage 5, cables extend downward. Candidate A hangs straight down at 0.0 drift. Candidate B swings out to the right with an orange divergence badge as differential probes run.
- **Voiceover:**
  > "Now, two refactoring candidates run in parallel forks under strict test hash-locking. In Stage 5, Nemotron Nano generates 50 unseen numerical inputs. Look at the Plumb Graph: Candidate A stays true on the vertical baseline. But Candidate B swung out—it fell into the trap by unifying rounding to Python's standard `round()`, changing pennies on 7 probe invoices!"

---

### Scene 5: The Verdict & The Verification Dossier (1:50 – 2:20)
- **On Screen:** The damped spring animation plays: Candidate A settles true on the plumb baseline. The green verdict banner appears: *"Verdict: HOLDS - Candidate A held true on all behavior tests and 50/50 differential probes."* Mouse clicks **View Dossier**. The Dossier screen opens, showing the verified unified diff patch and the *"What this does not prove"* boundary disclaimer.
- **Voiceover:**
  > "The plumb line settles. Candidate A holds true. Clicking View Dossier reveals the verified change, the complete quantitative evidence report, and critically: an explicit statement of what this does not prove. No hallucinations, no false guarantees."

---

### Scene 6: Token Factory Acceleration & The Ledger (2:20 – 2:45)
- **On Screen:** Navigating to the Ledger and the repository README. Cursor points to the measured benchmark table showing the **11.2x sandbox fork speedup** (1.64 ms vs 18.4 ms) and token consumption.
- **Voiceover:**
  > "By leveraging Token Factory's copy-on-write sandbox checkpointing, forking environments took just 1.64 milliseconds—over 11 times faster than a cold container rebuild. The entire run cost less than five cents."

---

### Scene 7: Conclusion & Links (2:45 – 2:55)
- **On Screen:** Title card showing:
  - **Plumbline**
  - GitHub: `github.com/YOUR_USERNAME/plumbline`
  - Built for Nebius × NVIDIA Global AI Hackathon
  - Open Source (MIT License)
- **Voiceover:**
  > "Plumbline: refactor legacy code without changing behavior, and see the evidence. Thank you."
