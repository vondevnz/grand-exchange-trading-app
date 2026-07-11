import { useState, useEffect } from "react";

function App() {
  const [prices, setPrices] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/prices/latest")
      .then((res) => res.json())
      .then((data) => setPrices(data))
      .catch((err) => setError(err.message));
  }, []);

  if (error) return <div>Error: {error}</div>;
  if (!prices) return <div>Loading...</div>;

  return (
    <div>
      <h1>OSRS Grand Exchange Prices</h1>
      <pre>{JSON.stringify(prices, null, 2)}</pre>
    </div>
  );
}

export default App;