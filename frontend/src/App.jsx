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
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>High</th>
            <th>Low</th>
          </tr>
        </thead>
        <tbody>
          {prices.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.name}</td>
              <td>{item.high ?? "-"}</td>
              <td>{item.low ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;