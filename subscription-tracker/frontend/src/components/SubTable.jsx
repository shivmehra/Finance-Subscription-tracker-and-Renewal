import ToggleSwitch from "./ToggleSwitch.jsx";

// The subscription grid. Renders rows, the amber "Renewing Soon" badge for
// urgent items, greys out paused rows, and surfaces toggle + delete actions.
function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value ?? 0);
}

function renewalText(days) {
  if (days === 0) return "Today";
  if (days === 1) return "1 day";
  return `${days} days`;
}

export default function SubTable({ subscriptions, onToggle, onDelete }) {
  if (subscriptions.length === 0) {
    return (
      <div className="empty-state">
        No subscriptions yet. Add one above to start tracking your burn rate.
      </div>
    );
  }

  return (
    <div className="table-wrap">
      <table className="sub-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Cost</th>
            <th>Billing</th>
            <th>Monthly</th>
            <th>Renews</th>
            <th>Status</th>
            <th aria-label="actions" />
          </tr>
        </thead>
        <tbody>
          {subscriptions.map((sub) => (
            <tr
              key={sub.id}
              className={!sub.is_active ? "row-paused" : ""}
            >
              <td className="cell-name">
                {sub.name}
                {sub.is_active && sub.is_urgent && (
                  <span className="badge badge--soon">Renewing Soon</span>
                )}
              </td>
              <td className="num">{formatCurrency(sub.cost)}</td>
              <td>{sub.billing_cycle}</td>
              <td className="num">{formatCurrency(sub.monthly_cost)}</td>
              <td className={sub.is_urgent ? "num renews-urgent" : "num"}>
                {renewalText(sub.days_until_renewal)}
              </td>
              <td>
                <ToggleSwitch
                  checked={sub.is_active}
                  onChange={() => onToggle(sub.id)}
                  label={`Toggle ${sub.name}`}
                />
              </td>
              <td>
                <button
                  type="button"
                  className="btn-delete"
                  onClick={() => onDelete(sub.id)}
                  aria-label={`Delete ${sub.name}`}
                >
                  ✕
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
