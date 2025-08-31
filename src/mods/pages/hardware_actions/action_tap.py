from playwright.sync_api import Page

# DOES NOR WORK PROPERLY YET

def allow_tap(page: Page) -> None:
  action_container = page.locator('#wf-hw-actions')
  actions = action_container.locator('[id*="wf-hwa"]')

  print(f"Found {actions.count()} hardware actions")

  page.evaluate("""
  () => {
    const SELECTOR = '#wf-hw-actions [id*="wf-hwa"]';

    // Idempotent binding guard using a WeakSet (survives across binds without touching dataset)
    const bound = (window.__tapBoundEls ||= new WeakSet());

    // Keep originals so we can restore after our synthetic click
    const originalSetTimeout = window.setTimeout;
    const originalSetInterval = window.setInterval;

    function withFastLongPress(fn) {
      // Temporarily patch timers so any long-press waits (e.g., 8–10s) become instant
      window.setTimeout = function (cb, delay, ...args) {
        try {
          if (delay != null && Number(delay) >= 8000) {
            // Collapse long delays to 0 to trigger immediately on this tick
            return originalSetTimeout(cb, 0, ...args);
          }
        } catch {}
        return originalSetTimeout(cb, delay, ...args);
      };
      window.setInterval = function (cb, delay, ...args) {
        try {
          if (delay != null && Number(delay) >= 8000) {
            return originalSetInterval(cb, 0, ...args);
          }
        } catch {}
        return originalSetInterval(cb, delay, ...args);
      };

      try {
        fn();
      } finally {
        // Always restore
        window.setTimeout = originalSetTimeout;
        window.setInterval = originalSetInterval;
      }
    }

    document.querySelectorAll(SELECTOR).forEach((el) => {
      if (bound.has(el)) return;

      el.addEventListener('click', (e) => {
        // Don't interfere with modified clicks
        if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        e.preventDefault();

        // Run whatever the long-press would eventually run, but instantly
        withFastLongPress(() => {
          // Most long-press implementations wire on pointer/mouse down + internal setTimeout
          // We synthesize the same sequence so their code path executes, but with collapsed timers
          const down = new MouseEvent('mousedown', { bubbles: true, cancelable: true, buttons: 1 });
          const up   = new MouseEvent('mouseup',   { bubbles: true, cancelable: true, buttons: 0 });

          el.dispatchEvent(down);
          el.dispatchEvent(up);

          // Some UIs gate on click after long-press sets internal flags; fire a click too.
          const clickEvt = new MouseEvent('click', { bubbles: true, cancelable: true });
          el.dispatchEvent(clickEvt);
        });
      }, { capture: true });

      bound.add(el);
    });
  }
  """)