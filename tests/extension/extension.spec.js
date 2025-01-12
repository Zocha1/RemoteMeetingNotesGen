// tests/extension/extension.spec.js
import { test, chromium } from '@playwright/test';
const path = require('path');

test('should load the extension and interact with it', async () => {
    const pathToExtension = path.join(__dirname, '../../extension'); // Update with the actual path
    const browser = await chromium.launch({
      headless: true,
      args: [
        `--disable-extensions-except=${pathToExtension}`,
        `--load-extension=${pathToExtension}`,
        '--disable-gpu',
        '--no-sandbox'
      ],
    });
      const context = await browser.newContext();
      const page = await context.newPage();
      await page.goto('https://example.com');

     // Open extension popup
     const extensionId = (await context.browser().contexts())[0]._options.args[0].match(/chrome-extension:\/\/([a-z]+)\//)[1];
    
        const extensionPage = await context.newPage();
        await extensionPage.goto(`chrome-extension://${extensionId}/index.html`);


      // Example: Start recording
      await extensionPage.locator('#start-recording').click()
      await extensionPage.waitForTimeout(2000);
      // Example: Stop recording
      await extensionPage.locator('#stop-recording').click()

      // Example: take screenshot
      await extensionPage.locator('#take-screenshot').click()
       await extensionPage.waitForTimeout(2000)
       
      // Additional assertions here
        await extensionPage.evaluate(() => {
            return new Promise((resolve) => {
                 chrome.runtime.onMessage.addListener((message) => {
                  if (message.type === "recording-finished" || message.type === "recording-started" || message.type === "recording-stopped" )
                    resolve(true)
                 });
             })
          })



    await browser.close();
  });