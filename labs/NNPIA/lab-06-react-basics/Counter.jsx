// Counter.jsx — starter component: props + state + event.
// Read-only in this lab (no build); rendered by index.html via Babel standalone.

function Counter({ label, start = 0, step = 1 }) {
  const [count, setCount] = React.useState(start);
  return (
    <div>
      <span>
        {label}: {count}
      </span>{" "}
      <button onClick={() => setCount((c) => c + step)}>+{step}</button>
      <button onClick={() => setCount(start)}>reset</button>
    </div>
  );
}
