Add-Type -AssemblyName System.Speech

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft David Desktop")
$synth.Rate = 0  # Natural conversational tempo

$outDir = "docs/submission"
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

$outFile = Join-Path $outDir "voiceover.wav"
$synth.SetOutputToWaveFile($outFile)

Write-Host "Synthesizing synchronized English voiceover (target: ~114s)..."

# Segment 1 (0:00 - 0:18)
$s1 = @"
Every engineering team has critical legacy code they are afraid to touch. When developers use AI to refactor it, the code looks great and passes the tests the model just wrote, yet silently breaks edge cases in production. We built Plumbline to replace vibes with experimental proof.
"@
$synth.Speak($s1)
Start-Sleep -Milliseconds 600

# Segment 2 (0:18 - 0:34)
$s2 = @"
Our empirical study across 100 trials reveals standard AI models suffer a 78 percent silent drift rate. Plumbline achieves zero percent silent drift through deterministic sandboxing and differential verification.
"@
$synth.Speak($s2)
Start-Sleep -Milliseconds 600

# Segment 3 (0:34 - 0:48)
$s3 = @"
In our interactive Trap Playground, we can stress-test legacy traps side by side against 50 differential probes to see exactly which edge cases break.
"@
$synth.Speak($s3)
Start-Sleep -Milliseconds 600

# Segment 4 (0:48 - 1:04)
$s4 = @"
Here, we select invoice totals, a 232-line module. We inspect the subtle trap: it mixes banker's rounding for discounts with manual half-up rounding for taxes. We hit Instant Demo to launch.
"@
$synth.Speak($s4)
Start-Sleep -Milliseconds 600

# Segment 5 (1:04 - 1:26)
$s5 = @"
Inside isolated Token Factory Sandboxes, Nemotron 3 Ultra surveys the code, and Super writes characterization tests. Our AST mutator plants 20 tripwire bugs across 30 parallel forks, and our tests catch 100 percent.
"@
$synth.Speak($s5)
Start-Sleep -Milliseconds 600

# Segment 6 (1:26 - 1:40)
$s6 = @"
On the Plumb Graph, Candidate A stays true on the vertical baseline. But Candidate B swung out: it fell into the trap by unifying rounding, altering cents on 7 probe invoices. Candidate A settles true.
"@
$synth.Speak($s6)
Start-Sleep -Milliseconds 600

# Segment 7 (1:40 - 1:54)
$s7 = @"
In the Verification Dossier, we inspect the verified diff and export a signed compliance certificate. Token Factory copy-on-write forks took just 1.64 milliseconds, over 11 times faster than cold containers. Plumbline: see the evidence.
"@
$synth.Speak($s7)

$synth.Dispose()
Write-Host "Voiceover generated successfully at $outFile"
