import { useState } from "react";

// Controlled onboarding form. Holds only its own draft state; on submit it
// hands a clean payload to the parent via onAdd() and resets.
const EMPTY = {
  name: "",
  cost: "",
  billing_cycle: "Monthly",
  renewal_date: "",
};

export default function EntryForm({ onAdd }) {
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (!form.name.trim() || !form.cost || !form.renewal_date) {
      setError("Please fill in every field.");
      return;
    }

    setSubmitting(true);
    try {
      await onAdd({
        name: form.name.trim(),
        cost: parseFloat(form.cost),
        billing_cycle: form.billing_cycle,
        renewal_date: form.renewal_date,
      });
      setForm(EMPTY);
    } catch (err) {
      setError(err.message || "Failed to add subscription.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="entry-form" onSubmit={handleSubmit}>
      <h2 className="section-title">Add a subscription</h2>

      <div className="entry-form__grid">
        <label className="field">
          <span className="field__label">Service name</span>
          <input
            type="text"
            placeholder="e.g. Spotify"
            value={form.name}
            onChange={(e) => update("name", e.target.value)}
          />
        </label>

        <label className="field">
          <span className="field__label">Cost</span>
          <div className="field__currency">
            <span className="field__currency-symbol">$</span>
            <input
              type="number"
              min="0"
              step="0.01"
              placeholder="0.00"
              value={form.cost}
              onChange={(e) => update("cost", e.target.value)}
            />
          </div>
        </label>

        <label className="field">
          <span className="field__label">Billing cycle</span>
          <select
            value={form.billing_cycle}
            onChange={(e) => update("billing_cycle", e.target.value)}
          >
            <option value="Monthly">Monthly</option>
            <option value="Yearly">Yearly</option>
          </select>
        </label>

        <label className="field">
          <span className="field__label">Next renewal date</span>
          <input
            type="date"
            value={form.renewal_date}
            onChange={(e) => update("renewal_date", e.target.value)}
          />
        </label>
      </div>

      {error && <p className="entry-form__error">{error}</p>}

      <button type="submit" className="btn-primary" disabled={submitting}>
        {submitting ? "Adding…" : "Add Subscription"}
      </button>
    </form>
  );
}
