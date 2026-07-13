import { useEffect, useState } from "react";
import { api } from "./api.js";

function KpiCard({ label, value }) {
  return (
    <div className="kpi">
      <div className="kpi-value">{value}</div>
      <div className="kpi-label">{label}</div>
    </div>
  );
}

export default function App() {
  const [days, setDays] = useState(7);
  const [summary, setSummary] = useState(null);
  const [skus, setSkus] = useState([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    setErr("");
    Promise.all([api.summary(days), api.topSkus(30, 10)])
      .then(([s, t]) => {
        setSummary(s);
        setSkus(t);
      })
      .catch((e) => setErr(String(e)));
  }, [days]);

  return (
    <div className="app">
      <header>
        <h1>OzonPulse · 运营看板</h1>
        <select value={days} onChange={(e) => setDays(Number(e.target.value))}>
          <option value={7}>近 7 天</option>
          <option value={14}>近 14 天</option>
          <option value={30}>近 30 天</option>
        </select>
      </header>

      {err && <p className="err">加载失败：{err}</p>}

      {summary && (
        <section className="kpis">
          <KpiCard label="GMV" value={`¥${summary.gmv.toLocaleString()}`} />
          <KpiCard label="订单数" value={summary.orders} />
          <KpiCard label="客单价" value={`¥${summary.avg_order_value}`} />
          <KpiCard label="动销率" value={`${(summary.active_sku_ratio * 100).toFixed(1)}%`} />
        </section>
      )}

      <section>
        <h2>畅销 SKU Top10（近 30 天）</h2>
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>商品</th>
              <th>销量</th>
              <th>GMV</th>
            </tr>
          </thead>
          <tbody>
            {skus.map((s) => (
              <tr key={s.sku}>
                <td>{s.sku}</td>
                <td>{s.title}</td>
                <td>{s.units}</td>
                <td>¥{s.gmv.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
