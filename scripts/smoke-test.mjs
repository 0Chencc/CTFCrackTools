#!/usr/bin/env node
// Windows smoke test: launch built exe, attach via WebView2 remote debugging,
// fail if any uncaught JS exception appears or if #root never mounts.
//
// Usage: node scripts/smoke-test.mjs <path-to-exe>

import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const exePath = process.argv[2];
if (!exePath) {
  console.error('Usage: node scripts/smoke-test.mjs <path-to-exe>');
  process.exit(2);
}

const DEBUG_PORT = 9222;
const STARTUP_TIMEOUT_MS = 30_000;
const COLLECT_WINDOW_MS = 5_000;

const env = {
  ...process.env,
  WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS: `--remote-debugging-port=${DEBUG_PORT}`,
};

console.log(`[smoke] launching: ${exePath}`);
const child = spawn(exePath, [], { env, stdio: 'ignore', detached: false });
let killed = false;
function killApp() {
  if (killed) return;
  killed = true;
  try { child.kill('SIGKILL'); } catch { /* noop */ }
}
process.on('exit', killApp);
process.on('SIGINT', () => { killApp(); process.exit(130); });

async function waitForDebugger() {
  const deadline = Date.now() + STARTUP_TIMEOUT_MS;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(`http://localhost:${DEBUG_PORT}/json`);
      if (res.ok) {
        const pages = await res.json();
        const page = pages.find((p) => p.type === 'page' && p.webSocketDebuggerUrl);
        if (page) return page;
      }
    } catch { /* connection refused while starting */ }
    await sleep(500);
  }
  throw new Error(`Debugger did not become reachable within ${STARTUP_TIMEOUT_MS}ms`);
}

function attach(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let nextId = 0;
    const pending = new Map();
    const exceptions = [];

    function send(method, params = {}) {
      const id = ++nextId;
      return new Promise((res) => {
        pending.set(id, res);
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    ws.addEventListener('open', async () => {
      await send('Runtime.enable');
      await send('Log.enable');

      await sleep(COLLECT_WINDOW_MS);

      const rootCheck = await send('Runtime.evaluate', {
        expression: 'document.getElementById("root")?.innerHTML?.length || 0',
      });
      const rootSize = rootCheck?.result?.result?.value ?? 0;

      ws.close();
      resolve({ exceptions, rootSize });
    });

    ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        const res = pending.get(msg.id);
        pending.delete(msg.id);
        res(msg);
      } else if (msg.method === 'Runtime.exceptionThrown') {
        exceptions.push(msg.params?.exceptionDetails);
      } else if (msg.method === 'Log.entryAdded' && msg.params?.entry?.level === 'error') {
        exceptions.push({ source: 'log', text: msg.params.entry.text, url: msg.params.entry.url });
      }
    });

    ws.addEventListener('error', (e) => reject(new Error(`WS error: ${e.message || e}`)));
  });
}

try {
  const page = await waitForDebugger();
  console.log(`[smoke] attached to ${page.url}`);

  const { exceptions, rootSize } = await attach(page.webSocketDebuggerUrl);

  console.log(`[smoke] #root innerHTML length: ${rootSize}`);
  console.log(`[smoke] uncaught exceptions: ${exceptions.length}`);

  let failed = false;
  if (exceptions.length > 0) {
    failed = true;
    console.error('[smoke] FAIL: uncaught exceptions detected');
    for (const e of exceptions) {
      const desc = e?.exception?.description || e?.text || JSON.stringify(e);
      console.error(`  - ${desc}`);
    }
  }
  if (rootSize === 0) {
    failed = true;
    console.error('[smoke] FAIL: React did not mount (#root is empty)');
  }

  killApp();
  process.exit(failed ? 1 : 0);
} catch (err) {
  console.error(`[smoke] FAIL: ${err.message}`);
  killApp();
  process.exit(1);
}
