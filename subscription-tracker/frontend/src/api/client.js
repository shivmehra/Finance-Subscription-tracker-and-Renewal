// Thin HTTP layer. No state, no side effects beyond the fetch itself.
// All URLs are relative; Vite proxies /api -> http://localhost:8000.

const JSON_HEADERS = { "Content-Type": "application/json" };

async function handle(res) {
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      /* response had no JSON body */
    }
    throw new Error(`${res.status}: ${detail}`);
  }
  // 204 No Content has no body to parse.
  if (res.status === 204) return null;
  return res.json();
}

export function getSubscriptions() {
  return fetch("/api/subscriptions").then(handle);
}

export function getMetrics() {
  return fetch("/api/metrics").then(handle);
}

export function createSubscription(sub) {
  return fetch("/api/subscriptions", {
    method: "POST",
    headers: JSON_HEADERS,
    body: JSON.stringify(sub),
  }).then(handle);
}

export function toggleSubscription(id) {
  return fetch(`/api/subscriptions/${id}/toggle`, { method: "PATCH" }).then(
    handle
  );
}

export function deleteSubscription(id) {
  return fetch(`/api/subscriptions/${id}`, { method: "DELETE" }).then(handle);
}
