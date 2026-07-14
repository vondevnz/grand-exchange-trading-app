import { useState, useEffect } from "react";
import "./App.css"

function App() {
  const [prices, setPrices] = useState(null);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {

    const timeoutId = setTimeout(() => {
      const url = searchTerm
      ? `http://localhost:8000/api/prices/latest?search=${encodeURIComponent(searchTerm)}`
      : "http://localhost:8000/api/prices/latest";
    

      fetch(url)
        .then((res) => res.json())
        .then((data) => setPrices(data))
        .catch((err) => setError(err.message));
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [searchTerm]);

  if (error) return <div>Error: {error}</div>;

  return (
    <div className="ge-container">
      <div className="ge-header">
        <h1>Grand Exchange Prices</h1>
        <span className="ge-subtitle">Live OSRS item data</span>
      </div>
      
      <div className="ge-search-row">
        <input
          type="text"
          className="ge-search"
          placeholder="Search items..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      
      {!prices ? (
        <div>Loading...</div>
      ) : (
        <div className="ge-table-wrapper">
          <table className="ge-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Img</th>
                <th>Instabuy</th>
                <th>Instasell</th>
                <th>Last Instabuy</th>
                <th>Last Instasell</th>
              </tr>
            </thead>
            <tbody>
              {prices.map((item) => (
                <tr key={item.item_id}>
                  <td>{item.item_id}</td>
                  <td className="ge-name">{item.name}</td>
                  <td>
                    <img
                      className="ge-item-img"
                      src={item.item_image}
                      alt={item.name}
                      width="24"
                      height="24"
                    />
                  </td>
                  <td className="ge-price">{item.instabuy}</td>
                  <td className="ge-price">{item.instasell}</td>
                  <td className="ge-time">{item.last_instabuy_time}</td>
                  <td className="ge-time">{item.last_instasell_time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;