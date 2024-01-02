import { useState } from "react";
import { BarChart, XAxis, YAxis, Bar } from "recharts";

function timeout(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function App() {
  const [response, setResponse] = useState({
    title: "",
    popularity: 0,
    metrics: {
      danceability: 0,
      energy: 0,
      loudness: 0,
      speechiness: 0,
      acousticness: 0,
      instrumentalness: 0,
      liveness: 0,
      valence: 0,
      tempo: 0,
    },
  });
  const [status, setStatus] = useState("stale");
  const [title, setTitle] = useState("");
  const [genre, setGenre] = useState("pop");

  const search = async () => {
    const res = await fetch("api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: title,
      }),
    }).then((res) => res.json());

    console.log(res);
  };

  const handlePrediction = async () => {
    setStatus("calculating_metrics");

    const res = await fetch("/api/predict_popularity", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        genre: genre,
        title: title,
      }),
    }).then((res) => res.json());

    await timeout(1500);
    setStatus("calculating_popularity");
    setResponse({
      popularity: res.popularity,
      title: "",
      metrics: {
        danceability: res.metrics.danceability,
        energy: res.metrics.energy,
        loudness: res.metrics.loudness,
        speechiness: res.metrics.speechiness,
        acousticness: res.metrics.acousticness,
        instrumentalness: res.metrics.instrumentalness,
        liveness: res.metrics.liveness,
        valence: res.metrics.valence,
        tempo: res.metrics.tempo,
      },
    });

    await timeout(3000);
    setStatus("stale");
    setResponse({
      popularity: res.popularity,
      title: res.title,
      metrics: {
        danceability: res.metrics.danceability,
        energy: res.metrics.energy,
        loudness: res.metrics.loudness,
        speechiness: res.metrics.speechiness,
        acousticness: res.metrics.acousticness,
        instrumentalness: res.metrics.instrumentalness,
        liveness: res.metrics.liveness,
        valence: res.metrics.valence,
        tempo: res.metrics.tempo,
      },
    });
  };

  return (
    <main className="page-container">
      <div className="input-container">
        <input
          onChange={(e) => {
            setTitle(e.target.value);
          }}
          value={title}
        />
        <select
          onChange={(e) => {
            setGenre(e.target.value);
          }}
          value={genre}
        >
          <option value="pop">Pop</option>
          <option value="rock">Rock</option>
          <option value="hiphop">Hip-hop/Rap</option>
          <option value="electronic">Electronic</option>
          <option value="country">Country</option>
          <option value="rb">R&B</option>
          <option value="classical">Classical</option>
          <option value="jazz">Jazz</option>
        </select>
        <button onClick={search} disabled={title.length < 3}>
          Search
        </button>
        <button onClick={handlePrediction} disabled={title.length < 3}>
          Predict
        </button>
      </div>
      <div
        className="loader"
        style={{ opacity: status === "stale" ? 0 : 1 }}
      ></div>
      <BarChart
        width={700}
        height={500}
        margin={{ top: 0, right: 0, left: 0, bottom: 100 }}
        style={{ opacity: status !== "calculating_metrics" ? 1 : 0.2 }}
        data={[
          { name: "Danceability", value: response.metrics.danceability },
          { name: "Energy", value: response.metrics.energy },
          { name: "Loudness", value: response.metrics.loudness },
          { name: "Speechiness", value: response.metrics.speechiness },
          { name: "Acousticness", value: response.metrics.acousticness },
          {
            name: "Instrumentalness",
            value: response.metrics.instrumentalness,
          },
          { name: "Liveness", value: response.metrics.liveness },
          { name: "Valence", value: response.metrics.valence },
          { name: "Tempo", value: response.metrics.tempo },
        ]}
      >
        <XAxis
          dataKey="name"
          angle={-45}
          offset={50}
          textAnchor="end"
          stroke="#eee"
        />
        <YAxis stroke="#eee" domain={[0, 100]} />
        <Bar dataKey="value" fill="#42a676" />
      </BarChart>
      {response.title && status === "stale" && (
        <p>
          Predicted popularity of{" "}
          <span className="italic bold">&quot;{response.title}&quot;</span> is{" "}
          <span className="bold">{response.popularity}</span>.
        </p>
      )}
      {!response.title && status === "stale" && <p className="bold">‎</p>}
      {status === "calculating_metrics" && (
        <p>Calculating track&apos;s metrics...</p>
      )}
      {status === "calculating_popularity" && (
        <p>Predicting track&apos;s popularity...</p>
      )}
    </main>
  );
}

export default App;
