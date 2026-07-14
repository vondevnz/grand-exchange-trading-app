import { useState, useEffect } from "react";
import "./App.css"

function App() {
  // data holds { items, total, page, page_size, total_pages }
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  useEffect(() => {

    const timeoutId = setTimeout(() => {

      const params = new URLSearchParams({
        page: page,
        page_size: pageSize
      });
      if (searchTerm) params.set("search", searchTerm);

      fetch(`http://localhost:8000/api/prices/latest?${params.toString()}`)
        .then((res) => res.json())
        .then((json) => setData(json))
        .catch((err) => setError(err.message));
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [searchTerm, page, pageSize]);

  // Reset to page 1 whenever searching
  useEffect(() => {
    setPage(1);
  }, [searchTerm, pageSize]);

  if (error) return <div>Error: {error}</div>;

  return (
    <div className="ge-container">
      <div className="ge-header">
        <h1>Grand Exchange Prices</h1>
        <span className="ge-subtitle">Live OSRS item data</span>
      </div>

      <div className="ge-controls-row">
        <div className="ge-search-row">
          <input
            type="text"
            className="ge-search"
            placeholder="Search items..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="ge-page-size">
          <label htmlFor="pageSize">Show</label>
          <select
            id="pageSize"
            value={pageSize}
            onChange={(e) => setPageSize(Number(e.target.value))}
          >
            <option value={20}>20</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
          <span>per page</span>
        </div>
      </div>

      {!data ? (
        <div>Loading...</div>
      ) : (
        <>
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
                {data.items.map((item) => (
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

          <Pagination
            page={data.page}
            totalPages={data.total_pages}
            onPageChange={setPage}
          />
        </>
      )}
    </div>
  );
}

function Pagination({ page, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  // Show a limited window of page numbers around the current page,
  // rather than every page number when there are hundreds of pages.
  const windowSize = 2;
  const start = Math.max(1, page - windowSize);
  const end = Math.min(totalPages, page + windowSize);
  const pageNumbers = [];
  for (let p = start; p <= end; p++) pageNumbers.push(p);

  return (
    <div className="ge-pagination">
      <button disabled={page <= 1} onClick={() => onPageChange(page - 1)}>
        Prev
      </button>

      {start > 1 && (
        <>
          <button onClick={() => onPageChange(1)}>1</button>
          {start > 2 && <span className="ge-ellipsis">…</span>}
        </>
      )}

      {pageNumbers.map((p) => (
        <button
          key={p}
          className={p === page ? "ge-page-active" : ""}
          onClick={() => onPageChange(p)}
        >
          {p}
        </button>
      ))}

      {end < totalPages && (
        <>
          {end < totalPages - 1 && <span className="ge-ellipsis">…</span>}
          <button onClick={() => onPageChange(totalPages)}>{totalPages}</button>
        </>
      )}

      <button disabled={page >= totalPages} onClick={() => onPageChange(page + 1)}>
        Next
      </button>
    </div>
  );
}

export default App;