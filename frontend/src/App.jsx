import { useCallback, useEffect, useState } from "react";

import * as api from "./api/client.js";
import EntryForm from "./components/EntryForm.jsx";
import MetricsRow from "./components/MetricsRow.jsx";
import SubTable from "./components/SubTable.jsx";

// Root state owner. The server is the single source of truth: after every
// mutation we re-fetch both the list and the metrics so computed fields
// (burn rate, urgency) never drift from the backend.
export default function App() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [metrics, setMetrics] = useState({
    total_monthly_burn: 0,
    urgent_count: 0,
  });
  const [loadError, setLoadError] = useState("");

  const refresh = useCallback(async () => {
    try {
      const [subs, mets] = await Promise.all([
        api.getSubscriptions(),
        api.getMetrics(),
      ]);
      setSubscriptions(subs);
      setMetrics(mets);
      setLoadError("");
    } catch (err) {
      setLoadError(
        "Could not reach the server. Is the backend running on port 8000?"
      );
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const handleAdd = useCallback(
    async (sub) => {
      await api.createSubscription(sub);
      await refresh();
    },
    [refresh]
  );

  const handleToggle = useCallback(
    async (id) => {
      await api.toggleSubscription(id);
      await refresh();
    },
    [refresh]
  );

  const handleDelete = useCallback(
    async (id) => {
      await api.deleteSubscription(id);
      await refresh();
    },
    [refresh]
  );

  return (
    <div className="app">
      <header className="app__header">
        <h1 className="app__title">
          <span className="app__mark">◈</span> Subscription Tracker
        </h1>
        <p className="app__tagline">
          Track recurring spend, catch renewals early, simulate savings.
        </p>
      </header>

      {loadError && <div className="banner banner--error">{loadError}</div>}

      <MetricsRow
        burnRate={metrics.total_monthly_burn}
        urgentCount={metrics.urgent_count}
      />

      <EntryForm onAdd={handleAdd} />

      <section className="grid-section">
        <h2 className="section-title">Active subscriptions</h2>
        <SubTable
          subscriptions={subscriptions}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      </section>
    </div>
  );
}
