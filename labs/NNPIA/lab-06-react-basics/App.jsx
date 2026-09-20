// App.jsx — starter root component: composition, props, list rendering.
// Rendered by index.html (Babel standalone, no build step).

function App() {
  const [name, setName] = React.useState("NNPIA");
  const counters = [
    { label: "clicks", start: 0, step: 1 },
    { label: "fives", start: 10, step: 5 },
  ];
  return (
    <main>
      <h1>Hello, {name || "stranger"}!</h1>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="your name"
      />
      {counters.map((c) => (
        <Counter key={c.label} label={c.label} start={c.start} step={c.step} />
      ))}
    </main>
  );
}
