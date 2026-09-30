/**
 * Automated Playwright Choreography for Hackathon Demo Video.
 * Records screen capture of browser at 1440x900, synchronized with voiceover.
 */

const path = require('path');
const fs = require('fs');
const { chromium } = require(path.resolve(__dirname, '../frontend/node_modules/playwright'));

async function recordWalkthrough() {
  const videoDir = path.resolve(__dirname, '../docs/submission/raw_video');
  if (!fs.existsSync(videoDir)) {
    fs.mkdirSync(videoDir, { recursive: true });
  }

  // Clear previous recordings
  const oldFiles = fs.readdirSync(videoDir);
  for (const f of oldFiles) {
    if (f.endsWith('.webm') || f.endsWith('.mp4')) {
      fs.unlinkSync(path.join(videoDir, f));
    }
  }

  console.log('Launching Chrome with video recording...');
  const browser = await chromium.launch({
    channel: 'chrome',
    headless: false,
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    recordVideo: {
      dir: videoDir,
      size: { width: 1440, height: 900 },
    },
  });

  const page = await context.newPage();
  const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  console.log('Scene 1: Introduction & The Problem (0:00 - 0:18)');
  await page.goto('http://localhost:8000/#/', { waitUntil: 'networkidle' });
  await wait(2000);
  await page.hover('.hero-title');
  await wait(3000);
  await page.hover('.metric-card:nth-child(1)');
  await wait(3000);
  await page.hover('.metric-card.highlight-holds');
  await wait(4000);
  await page.hover('.judge-banner');
  await wait(4000);

  console.log('Scene 2: Exploring AI Study & Playground (0:18 - 0:38)');
  const aiStudyBtn = page.locator('button:has-text("AI Study")');
  if (await aiStudyBtn.count()) {
    await aiStudyBtn.click();
    await wait(3000);
    await page.evaluate(() => {
      const modal = document.querySelector('.ai-study-modal');
      if (modal) modal.scrollTop = 250;
    });
    await wait(4000);
    const closeBtn = page.locator('.study-close-btn');
    if (await closeBtn.count()) await closeBtn.click();
    await wait(1500);
  }

  const trapBtn = page.locator('button:has-text("Trap Playground")').first();
  if (await trapBtn.count()) {
    await trapBtn.click();
    await wait(2500);
    const runBtn = page.locator('button:has-text("Execute 50 Differential Probes")');
    if (await runBtn.count()) {
      await runBtn.click();
      await wait(3500);
    }
    const doneBtn = page.locator('.done-btn');
    if (await doneBtn.count()) {
      await doneBtn.click();
    } else {
      await page.keyboard.press('Escape');
    }
    await wait(2000);
  }

  console.log('Scene 3: Specimen Inspection (0:38 - 1:02)');
  await page.evaluate(() => window.scrollBy({ top: 380, behavior: 'smooth' }));
  await wait(2500);

  const inspectBtn = page.locator('.trap-inspect-btn').first();
  if (await inspectBtn.count()) {
    await inspectBtn.click();
    await wait(5000);
  }

  // Hover over the trap code block
  await page.hover('.trap-code-block');
  await wait(4000);

  console.log('Scene 4: Launching Verification Run in Cockpit (1:02 - 1:28)');
  await page.goto('http://localhost:8000/#/run/2407642b-b5aa-4bfe-844d-81301c86beaf', {
    waitUntil: 'networkidle',
  });
  await wait(2500);

  // Cockpit inspection
  await page.hover('.cockpit-rail');
  await wait(4000);

  // Hover planted bugs tripwires
  await page.hover('.strength-widget');
  await wait(5000);

  console.log('Scene 5: Plumb Graph Physics & Candidate Deflection (1:28 - 2:00)');
  try {
    await page.hover('.plumb-tick-strip', { force: true, timeout: 5000 });
  } catch {}
  await wait(5000);

  // Hover candidate bobs
  const candidateA = page.locator('.plumb-candidate:nth-child(1)');
  if (await candidateA.count()) {
    try {
      await candidateA.hover({ force: true, timeout: 5000 });
    } catch {}
    await wait(6000);
  }

  const candidateB = page.locator('.plumb-candidate:nth-child(2)');
  if (await candidateB.count()) {
    try {
      await candidateB.hover({ force: true, timeout: 5000 });
    } catch {}
    await wait(7000);
  }

  // Hover verdict banner
  try {
    await page.hover('.plumb-verdict-banner', { timeout: 5000 });
  } catch {}
  await wait(5000);

  // Switch tabs in cockpit right panel
  const ledgerTab = page.locator('button:has-text("Ledger")');
  if (await ledgerTab.count()) {
    await ledgerTab.click();
    await wait(4000);
  }

  const testsTab = page.locator('button:has-text("Tests")');
  if (await testsTab.count()) {
    await testsTab.click();
    await wait(4000);
  }

  console.log('Scene 6: Verification Dossier & Certificate (2:00 - 2:32)');
  await page.goto('http://localhost:8000/#/dossier/2407642b-b5aa-4bfe-844d-81301c86beaf', {
    waitUntil: 'networkidle',
  });
  await wait(3000);

  // Certificate banner
  await page.hover('.certificate-seal-banner');
  await wait(4000);

  // Scroll through verified change
  await page.evaluate(() => window.scrollBy({ top: 350, behavior: 'smooth' }));
  await wait(5000);

  // Scroll through evidence report
  await page.evaluate(() => window.scrollBy({ top: 400, behavior: 'smooth' }));
  await wait(5000);

  // Scroll through caveats
  await page.evaluate(() => window.scrollBy({ top: 350, behavior: 'smooth' }));
  await wait(5000);

  // Hover export certificate button
  await page.hover('.export-cert-btn');
  await wait(4000);

  console.log('Scene 7: Benchmarks Modal & Closing (2:32 - 2:53)');
  const benchBtn = page.locator('button:has-text("Benchmarks")');
  if (await benchBtn.count()) {
    await benchBtn.click();
    await wait(6000);
    const closeBench = page.locator('.benchmarks-close-btn');
    if (await closeBench.count()) {
      await closeBench.click();
    } else {
      await page.keyboard.press('Escape');
    }
    await wait(2000);
  }

  await page.goto('http://localhost:8000/#/', { waitUntil: 'networkidle' });
  await wait(2000);
  await page.hover('.navbar__brand');
  await wait(4000);

  console.log('Closing browser to save video...');
  await page.close();
  await context.close();
  await browser.close();

  console.log('Video recording completed successfully!');
}

recordWalkthrough().catch((err) => {
  console.error('Walkthrough recording error:', err);
  process.exit(1);
});
