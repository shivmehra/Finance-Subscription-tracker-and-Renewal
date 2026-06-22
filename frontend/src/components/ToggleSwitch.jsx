// Dumb presentational atom: a controlled active/paused switch.
// Knows nothing about subscriptions — just checked state + an onChange callback.
export default function ToggleSwitch({ checked, onChange, label }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-label={label}
      className={`toggle ${checked ? "toggle--on" : "toggle--off"}`}
      onClick={onChange}
    >
      <span className="toggle__track">
        <span className="toggle__thumb" />
      </span>
      <span className="toggle__label">{checked ? "Active" : "Paused"}</span>
    </button>
  );
}
