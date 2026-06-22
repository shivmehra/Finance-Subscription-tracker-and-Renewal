// Two KPI cards. Pure presentation — values are computed server-side and
// passed down as props.
function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value ?? 0);
}

export default function MetricsRow({ burnRate, urgentCount }) {
  return (
    <div className="metrics-row">
      <div className="card card--primary">
        <div className="card__label">Total Monthly Burn Rate</div>
        <div className="card__value">{formatCurrency(burnRate)}</div>
        <div className="card__sub">across all active subscriptions</div>
      </div>

      <div className={`card ${urgentCount > 0 ? "card--alert" : ""}`}>
        <div className="card__label">Upcoming Renewals Alert</div>
        <div className="card__value">{urgentCount ?? 0}</div>
        <div className="card__sub">
          {urgentCount === 1 ? "renewal" : "renewals"} within 7 days
        </div>
      </div>
    </div>
  );
}
