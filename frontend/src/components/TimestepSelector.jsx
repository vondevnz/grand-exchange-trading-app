export function TimestepSelector({ value, onChange }) {
  const options = ["5m", "1h", "6h", "24h"];

  return (
    <div className="ge-timestep-selector">
      {options.map((option) => (
        <button
          key={option}
          className={option === value ? "ge-timestep-active" : ""}
          onClick={() => onChange(option)}
        >
          {option}
        </button>
      ))}
    </div>
  );
}