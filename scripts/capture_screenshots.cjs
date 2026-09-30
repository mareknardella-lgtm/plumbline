/**
 * Captures updated 1440x900 screenshots of the Plumbline application.
 */

const path = require('path');
const fs = require('fs');
const { chromium } = require(path.resolve(__dirname, '../frontend/node_modules/playwright'));

async function capture() {
  const imgDir = path.resolve(__dirname, '../docs/images');
  if (!fs.existsSync(imgDir)) {
    fs.mkdirSync(imgDir, { recursive: true });
  }

  console.log('Launching Chrome to capture high-res 1440x900 screenshots...');
  const browser = await chromium.launch({
    channel: 'chrome',
    headless: true,
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 1,
  });

  const page = await context.newPage();
  const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  // 1. Home
  console.log('Capturing 01-home.png...');
  await page.goto('http://localhost:8000/#/', { waitUntil: 'networkidle' });
  await wait(1500);
  await page.screenshot({ path: path.join(imgDir, '01-home.png') });

  // 2. Cockpit Running
  console.log('Capturing 02-cockpit-running.png...');
  await page.goto('http://localhost:8000/#/run/2407642b-b5aa-4bfe-844d-81301c86beaf', { waitUntil: 'networkidle' });
  await wait(2000);
  await page.screenshot({ path: path.join(imgDir, '02-cockpit-running.png') });

  // 3. Graph Verdict with candidate hover telemetry
  console.log('Capturing 03-graph-verdict.png...');
  await wait(1000);
  const candidateB = page.locator('circle.cable-bob-diverged, [data-candidate="b"]').first();
  if (await candidateB.count()) {
    await candidateB.hover({ force: true });
    await wait(800);
  }
  await page.screenshot({ path: path.join(imgDir, '03-graph-verdict.png') });

  // 4. Dossier
  console.log('Capturing 04-dossier.png...');
  await page.goto('http://localhost:8000/#/dossier/2407642b-b5aa-4bfe-844d-81301c86beaf', { waitUntil: 'networkidle' });
  await wait(1500);
  await page.screenshot({ path: path.join(imgDir, '04-dossier.png') });

  // 5. Ledger
  console.log('Capturing 05-ledger.png...');
  await page.goto('http://localhost:8000/#/run/2407642b-b5aa-4bfe-844d-81301c86beaf', { waitUntil: 'networkidle' });
  await wait(1500);
  const ledgerTab = page.locator('button[role="tab"]:has-text("Ledger")');
  if (await ledgerTab.count()) {
    await ledgerTab.click();
    await wait(800);
  }
  await page.screenshot({ path: path.join(imgDir, '05-ledger.png') });

  // 6. Architecture Modal
  console.log('Capturing 06-architecture.png...');
  await page.goto('http://localhost:8000/#/', { waitUntil: 'networkidle' });
  await wait(1000);
  const archBtn = page.locator('button:has-text("Architecture")');
  if (await archBtn.count()) {
    await archBtn.click();
    await wait(800);
  }
  await page.screenshot({ path: path.join(imgDir, '06-architecture.png') });

  await browser.close();
  console.log('Screenshots captured successfully!');
}

capture().catch((err) => {
  console.error(err);
  process.exit(1);
});
