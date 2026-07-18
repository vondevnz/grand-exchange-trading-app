import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export function PriceHistoryChart({ history, loading }) {
  if (loading) return <div className="ge-chart-status">Loading price history...</div>;

  if (!history || history.length === 0) {
    return <div className="ge-chart-status">No historical data available for this item.</div>;
  }

  const chartData = history.map((point) => ({
    time: timeAgoFromUnix(point.timestamp),
    High: point.avgHighPrice,
    Low: point.avgLowPrice,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#26304a" />
        <XAxis dataKey="time" stroke="#8a93a8" fontSize={11} tickLine={false} />
        <YAxis 
          stroke="#8a93a8"
          fontSize={11}
          tickLine={false}
          domain={[
            (dataMin) => Math.floor(dataMin * 0.985),
            (dataMax) => Math.ceil(dataMax * 1.015),
          ]} 
        />
        <Tooltip
          contentStyle={{ background: "#161d2e", border: "1px solid #26304a", borderRadius: 8 }}
          labelStyle={{ color: "#e4e8f1" }}
        />
        <Line type="monotone" dataKey="High" stroke="#4CAF50" dot={false} strokeWidth={2} connectNulls/>
        <Line type="monotone" dataKey="Low" stroke="#E91E63" dot={false} strokeWidth={2} connectNulls/>
      </LineChart>
    </ResponsiveContainer>
  );
}

function timeAgoFromUnix(unixSeconds) {
  const then = new Date(unixSeconds * 1000);
  const now = new Date();
  const diffSeconds = Math.floor((now - then) / 1000);

  if (diffSeconds < 60) return "just now";

  const diffMinutes = Math.floor(diffSeconds / 60);
  if (diffMinutes < 60) return `${diffMinutes}m ago`;

  const diffHours = Math.floor(diffMinutes / 60);
  if (diffHours < 24) return `${diffHours}h ago`;

  const diffDays = Math.floor(diffHours / 24);
  return `${diffDays}d ago`;
}