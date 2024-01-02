import { useState } from "react";
import { BarChart, XAxis, YAxis, Bar } from "recharts";

function timeout(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function Track({ img, title, artists, preview, active, handleClick }) {
  return (
    <div
      onClick={handleClick}
      className={`track ${active ? " track--active" : ""}`}
    >
      <img src={img} className="track__img" />
      <p className="track__title">{title}</p>
      <p className="track__artists">{artists}</p>
      <audio className="track__audio" src={preview} controls />
    </div>
  );
}

function TrackList({ tracks, handleSelection, activeId }) {
  const track = [];
  for (let i = 0; i < 5; i++) {
    if (tracks[i]) {
      track.push(tracks[i]);
    } else {
      track.push(null);
    }
  }

  return (
    <div className="track-list">
      {track.map((row, idx) =>
        row !== null ? (
          <Track
            img={row.img}
            title={row.title}
            artists={row.artists}
            preview={row.preview}
            active={activeId === row.id}
            handleClick={() => {
              handleSelection(row.id);
            }}
            key={`${row.title}-${idx}`}
          />
        ) : (
          <div className="track--empty" key={idx} />
        )
      )}
    </div>
  );
}

function App() {
  const [activeId, setActiveId] = useState("");
  const [searchResponse, setSearchResponse] = useState({ tracks: [] });
  const [predictResponse, setPredictResponse] = useState({
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

  const search = async () => {
    setActiveId("");
    const res = await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: title,
      }),
    }).then((res) => res.json());

    setSearchResponse(res);
  };

  const handlePrediction = async () => {
    setStatus("calculating_metrics");

    const res = await fetch("/api/predict_popularity", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: activeId,
      }),
    }).then((res) => res.json());

    await timeout(1500);
    setStatus("calculating_popularity");
    setPredictResponse({
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
    setPredictResponse({
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
          className="searchbar"
          onChange={(e) => {
            setTitle(e.target.value);
          }}
          value={title}
        />
        <button onClick={search} disabled={title.length < 3}>
          Search
        </button>
        <button onClick={handlePrediction} disabled={activeId === ""}>
          Predict
        </button>
      </div>
      <TrackList
        tracks={searchResponse.tracks}
        activeId={activeId}
        handleSelection={(id) => {
          setActiveId(id);
        }}
      />
      <div
        className="loader"
        style={{ opacity: status === "stale" ? 0 : 1 }}
      ></div>
      <BarChart
        width={1000}
        height={500}
        margin={{ top: 0, right: 0, left: 0, bottom: 100 }}
        style={{ opacity: status !== "calculating_metrics" ? 1 : 0.2 }}
        data={[
          { name: "Danceability", value: predictResponse.metrics.danceability },
          { name: "Energy", value: predictResponse.metrics.energy },
          { name: "Loudness", value: predictResponse.metrics.loudness },
          { name: "Speechiness", value: predictResponse.metrics.speechiness },
          { name: "Acousticness", value: predictResponse.metrics.acousticness },
          {
            name: "Instrumentalness",
            value: predictResponse.metrics.instrumentalness,
          },
          { name: "Liveness", value: predictResponse.metrics.liveness },
          { name: "Valence", value: predictResponse.metrics.valence },
          { name: "Tempo", value: predictResponse.metrics.tempo },
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
      {predictResponse.title && status === "stale" && (
        <p>
          Predicted popularity of{" "}
          <span className="italic bold">
            &quot;{predictResponse.title}&quot;
          </span>{" "}
          is <span className="bold">{predictResponse.popularity}</span>.
        </p>
      )}
      {!predictResponse.title && status === "stale" && (
        <p className="bold">‎</p>
      )}
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
