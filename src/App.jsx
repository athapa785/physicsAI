import { useEffect, useMemo, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, Atom, BookOpen, Check, Pause, Play, RotateCcw, Search, Send, Settings, Target, X } from "lucide-react";
import ReactMarkdown from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkMath from "remark-math";

const studentSession = (() => {
  const existing = window.sessionStorage.getItem("physicsatlas_student_session");
  if (existing) return existing;
  const created = window.crypto.randomUUID();
  window.sessionStorage.setItem("physicsatlas_student_session", created);
  return created;
})();

const api = {
  async get(path) {
    const response = await fetch(path);
    if (!response.ok) throw new Error("Could not load this part of the atlas.");
    return response.json();
  },
  async ask(topic, question, apiKey, lab = null, state = {}, history = []) {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Student-Session": studentSession,
        ...(apiKey ? { "X-OpenAI-API-Key": apiKey } : {}),
      },
      body: JSON.stringify({ topic, question, lab, state, history }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "The tutor is unavailable.");
    return data;
  },
};

function splitSections(markdown) {
  const parts = markdown.split(/(?=^##\s+)/gm).filter((part) => part.trim());
  return parts.length ? parts : [markdown];
}

function Library({ catalog, onOpen }) {
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [searching, setSearching] = useState(false);
  const chapters = catalog?.chapters || [];
  const total = chapters.reduce((sum, chapter) => sum + chapter.topics.length, 0);

  useEffect(() => {
    const trimmed = query.trim();
    if (trimmed.length < 2) {
      setSearchResults(null);
      setSearching(false);
      return undefined;
    }
    setSearching(true);
    const controller = new AbortController();
    const timer = window.setTimeout(async () => {
      try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(trimmed)}`, { signal: controller.signal });
        if (!response.ok) throw new Error();
        setSearchResults((await response.json()).results);
      } catch (error) {
        if (error.name !== "AbortError") setSearchResults([]);
      } finally {
        setSearching(false);
      }
    }, 220);
    return () => { window.clearTimeout(timer); controller.abort(); };
  }, [query]);

  return (
    <main className="library">
      <section className="hero">
        <p className="eyebrow">Physics course library</p>
        <h1>Undergraduate physics,<br /><em>clearly organized.</em></h1>
        <p className="hero-copy">Browse 18 lessons across mechanics, thermodynamics, waves, electromagnetism, optics, and modern physics.</p>
        <div className="search-box">
          <Search size={20} />
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search topics and lesson content…" aria-label="Search topics and lesson content" />
          <kbd>{searching ? "searching" : `${searchResults?.length ?? total} results`}</kbd>
        </div>
      </section>

      {searchResults !== null ? (
        <section className="search-results" aria-label="Corpus search results">
          <div className="results-heading"><span>Corpus results</span><span>{searchResults.length} found</span></div>
          {searchResults.map((result) => (
            <button key={result.slug} onClick={() => onOpen(result.slug)}>
              <div><span>{result.chapter}</span><h2>{result.title}</h2><p>{result.snippet}</p></div>
              <ArrowRight size={20} />
            </button>
          ))}
          {!searching && !searchResults.length && <p className="empty-results">No lesson contains all of those words.</p>}
        </section>
      ) : <section className="chapter-grid" aria-label="Physics chapters">
        {chapters.map((chapter) => {
          return (
            <article className="chapter-card" key={chapter.number}>
              <div className="chapter-heading"><span>0{chapter.number}</span><h2>{chapter.title}</h2></div>
              <div className="topic-list">
                {chapter.topics.map((topic) => (
                  <button key={topic.slug} onClick={() => onOpen(topic.slug)}>
                    <span>{topic.title}</span><ArrowRight size={17} />
                  </button>
                ))}
              </div>
            </article>
          );
        })}
      </section>}
    </main>
  );
}

function Tutor({ lesson, onClose, apiKey, openSettings }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    if (!question.trim()) return;
    setBusy(true); setError(""); setAnswer("");
    try {
      const data = await api.ask(lesson.slug, question.trim(), apiKey);
      setAnswer(data.answer);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <aside className="tutor-panel">
      <header><div><span>AI study companion</span><h2>Ask the atlas</h2></div><button onClick={onClose} aria-label="Close tutor"><X /></button></header>
      <p>Ask about <strong>{lesson.title}</strong>. Answers are grounded in the local course notes.</p>
      {!apiKey && <button className="configure-key" onClick={openSettings}><Settings size={16} /> Configure an API key first</button>}
      <form onSubmit={submit}>
        <textarea value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Why does this happen?" rows="4" />
        <button disabled={busy || !question.trim()}>{busy ? "Thinking…" : "Ask question"}<Send size={16} /></button>
      </form>
      {error && <div className="tutor-message error">{error}</div>}
      {answer && <div className="tutor-message markdown"><ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>{answer}</ReactMarkdown></div>}
    </aside>
  );
}

function Reader({ lesson, onBack, apiKey, openSettings }) {
  const sections = useMemo(() => splitSections(lesson.content), [lesson.content]);
  const [section, setSection] = useState(0);
  const [tutorOpen, setTutorOpen] = useState(false);
  useEffect(() => setSection(0), [lesson.slug]);

  return (
    <main className={`reader ${tutorOpen ? "with-tutor" : ""}`}>
      <aside className="reader-rail">
        <button className="back-button" onClick={onBack}><ArrowLeft size={17} /> Library</button>
        <div className="rail-meta"><span>{lesson.chapter}</span><h1>{lesson.title}</h1></div>
        <nav aria-label="Lesson sections">
          {sections.map((content, index) => {
            const title = content.match(/^##\s+(.+)$/m)?.[1] || `Overview ${index + 1}`;
            return <button className={index === section ? "active" : ""} onClick={() => setSection(index)} key={title}><span>{String(index + 1).padStart(2, "0")}</span>{title}</button>;
          })}
        </nav>
      </aside>
      <article className="lesson-page">
        <div className="lesson-kicker"><BookOpen size={16} /> Lesson {section + 1} of {sections.length}</div>
        <div className="markdown"><ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>{sections[section]}</ReactMarkdown></div>
        <footer>
          <button disabled={section === 0} onClick={() => setSection((value) => value - 1)}><ArrowLeft size={17} /> Previous</button>
          <span>{section + 1} / {sections.length}</span>
          <button disabled={section === sections.length - 1} onClick={() => setSection((value) => value + 1)}>Next <ArrowRight size={17} /></button>
        </footer>
      </article>
      <button className="ask-fab" onClick={() => setTutorOpen(true)}><Atom size={19} /> Ask a question</button>
      {tutorOpen && <Tutor lesson={lesson} apiKey={apiKey} openSettings={openSettings} onClose={() => setTutorOpen(false)} />}
    </main>
  );
}

function ProjectileLab({ onContext }) {
  const [speed, setSpeed] = useState(24);
  const [angle, setAngle] = useState(45);
  const [height, setHeight] = useState(2);
  const [gravity, setGravity] = useState(9.81);
  const [time, setTime] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [prediction, setPrediction] = useState(55);
  const [revealed, setRevealed] = useState(false);
  const frameRef = useRef(null);
  const lastRef = useRef(null);

  const physics = useMemo(() => {
    const radians = angle * Math.PI / 180;
    const vx = speed * Math.cos(radians);
    const vy0 = speed * Math.sin(radians);
    const flight = (vy0 + Math.sqrt(vy0 ** 2 + 2 * gravity * height)) / gravity;
    const range = vx * flight;
    const peakTime = vy0 / gravity;
    const maxHeight = height + (vy0 ** 2) / (2 * gravity);
    return { vx, vy0, flight, range, peakTime, maxHeight };
  }, [speed, angle, height, gravity]);

  useEffect(() => onContext({
    initial_speed_m_s: speed,
    launch_angle_deg: angle,
    initial_height_m: height,
    gravity_m_s2: gravity,
    time_s: time.toFixed(2),
    horizontal_position_m: x?.toFixed?.(2) ?? "0.00",
    vertical_position_m: y?.toFixed?.(2) ?? height.toFixed(2),
    horizontal_velocity_m_s: physics.vx.toFixed(2),
    vertical_velocity_m_s: (physics.vy0 - gravity * time).toFixed(2),
    predicted_range_m: physics.range.toFixed(2),
  }), [speed, angle, height, gravity, time, physics, onContext]);

  useEffect(() => {
    setTime(0); setPlaying(false); setRevealed(false);
  }, [speed, angle, height, gravity]);

  useEffect(() => {
    if (!playing) { lastRef.current = null; return undefined; }
    function tick(timestamp) {
      if (lastRef.current === null) lastRef.current = timestamp;
      const delta = (timestamp - lastRef.current) / 1000;
      lastRef.current = timestamp;
      setTime((current) => {
        const next = current + delta;
        if (next >= physics.flight) { setPlaying(false); return physics.flight; }
        return next;
      });
      frameRef.current = requestAnimationFrame(tick);
    }
    frameRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frameRef.current);
  }, [playing, physics.flight]);

  const x = physics.vx * time;
  const y = Math.max(0, height + physics.vy0 * time - 0.5 * gravity * time ** 2);
  const vy = physics.vy0 - gravity * time;
  const plotW = 900, plotH = 410, pad = 48;
  const xMax = Math.max(physics.range * 1.08, 10);
  const yMax = Math.max(physics.maxHeight * 1.18, 5);
  const sx = (value) => pad + value / xMax * (plotW - pad * 2);
  const sy = (value) => plotH - pad - value / yMax * (plotH - pad * 2);
  const samples = Array.from({ length: 81 }, (_, index) => {
    const t = physics.flight * index / 80;
    return [physics.vx * t, Math.max(0, height + physics.vy0 * t - .5 * gravity * t ** 2)];
  });
  const trajectory = samples.map(([px, py]) => `${sx(px)},${sy(py)}`).join(" ");
  const timeX = (value) => 42 + value / physics.flight * 358;
  const heightY = (value) => 150 - value / yMax * 118;
  const velocityLimit = Math.max(Math.abs(physics.vy0), Math.abs(physics.vy0 - gravity * physics.flight), 1);
  const velocityY = (value) => 91 - value / velocityLimit * 58;
  const heightPlot = Array.from({ length: 61 }, (_, index) => {
    const t = physics.flight * index / 60;
    return `${timeX(t)},${heightY(Math.max(0, height + physics.vy0*t - .5*gravity*t*t))}`;
  }).join(" ");
  const velocityPlot = Array.from({ length: 61 }, (_, index) => {
    const t = physics.flight * index / 60;
    return `${timeX(t)},${velocityY(physics.vy0-gravity*t)}`;
  }).join(" ");

  function reset() { setPlaying(false); setTime(0); }
  function toggle() { if (time >= physics.flight) setTime(0); setPlaying((value) => !value); }

  return (
    <main className="lab-page">
      <section className="lab-title">
        <div><span>Interactive lab 01</span><h1>Projectile motion</h1></div>
        <p>Change the launch conditions. The trajectory, vectors, equations, and plots stay synchronized.</p>
      </section>

      <section className="lab-layout">
        <aside className="lab-controls">
          <h2>Launch conditions</h2>
          <label>Initial speed <output>{speed} m/s</output><input type="range" min="5" max="50" value={speed} onChange={(event) => setSpeed(Number(event.target.value))} /></label>
          <label>Launch angle <output>{angle}°</output><input type="range" min="5" max="85" value={angle} onChange={(event) => setAngle(Number(event.target.value))} /></label>
          <label>Initial height <output>{height} m</output><input type="range" min="0" max="20" step="0.5" value={height} onChange={(event) => setHeight(Number(event.target.value))} /></label>
          <label>Gravity <output>{gravity.toFixed(2)} m/s²</output><input type="range" min="1.6" max="24.8" step="0.01" value={gravity} onChange={(event) => setGravity(Number(event.target.value))} /></label>
          <div className="control-buttons"><button className="play-button" onClick={toggle}>{playing ? <Pause size={17}/> : <Play size={17}/>} {playing ? "Pause" : "Run"}</button><button onClick={reset}><RotateCcw size={17}/> Reset</button></div>
        </aside>

        <div className="simulation-area">
          <div className="live-readout"><span>t <strong>{time.toFixed(2)} s</strong></span><span>x <strong>{x.toFixed(1)} m</strong></span><span>y <strong>{y.toFixed(1)} m</strong></span><span>v<sub>y</sub> <strong>{vy.toFixed(1)} m/s</strong></span></div>
          <svg className="trajectory-plot" viewBox={`0 0 ${plotW} ${plotH}`} role="img" aria-label={`Projectile at ${x.toFixed(1)} metres horizontal and ${y.toFixed(1)} metres high`}>
            <defs><marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" /></marker><marker id="arrow-red" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" /></marker></defs>
            {[0,.25,.5,.75,1].map((fraction) => <g key={fraction}><line className="grid-line" x1={pad} x2={plotW-pad} y1={sy(yMax*fraction)} y2={sy(yMax*fraction)} /><text x={pad-9} y={sy(yMax*fraction)+4} textAnchor="end">{(yMax*fraction).toFixed(0)}</text></g>)}
            <line className="axis" x1={pad} x2={plotW-pad} y1={sy(0)} y2={sy(0)} />
            <polyline className="trajectory-line" points={trajectory} />
            <line className="velocity-vector" x1={sx(x)} y1={sy(y)} x2={sx(x)+physics.vx*2.2} y2={sy(y)-vy*2.2} markerEnd="url(#arrow-blue)" />
            <line className="gravity-vector" x1={sx(x)} y1={sy(y)} x2={sx(x)} y2={sy(y)+58} markerEnd="url(#arrow-red)" />
            <circle className="projectile" cx={sx(x)} cy={sy(y)} r="10" />
            <text className="vector-label" x={sx(x)+physics.vx*1.2} y={sy(y)-vy*1.2-9}>v</text>
            <text className="gravity-label" x={sx(x)+9} y={sy(y)+48}>g</text>
            <text className="axis-label" x={plotW-pad} y={plotH-12} textAnchor="end">horizontal distance (m)</text>
            <text className="axis-label" x={14} y={pad} transform={`rotate(-90 14 ${pad})`}>height (m)</text>
          </svg>
          <div className="timeline"><input aria-label="Simulation time" type="range" min="0" max={physics.flight} step="0.01" value={time} onChange={(event) => {setPlaying(false); setTime(Number(event.target.value));}} /><span>{physics.flight.toFixed(2)} s</span></div>
        </div>
      </section>

      <section className="lab-analysis">
        <div className="equation-panel"><span>Position model</span><div>x(t) = ({physics.vx.toFixed(1)})t</div><div>y(t) = {height} + ({physics.vy0.toFixed(1)})t − ½({gravity.toFixed(2)})t²</div><p>Horizontal velocity is constant. Vertical velocity changes by −g every second.</p></div>
        <div className="mini-plots">
          <div><h3>Height vs. time</h3><svg viewBox="0 0 430 175" role="img" aria-label="Height versus time plot"><line className="mini-axis" x1="42" y1="150" x2="400" y2="150"/><polyline className="mini-line" points={heightPlot}/><line className="plot-cursor" x1={timeX(time)} x2={timeX(time)} y1="24" y2="150"/><circle cx={timeX(time)} cy={heightY(y)} r="5" /></svg></div>
          <div><h3>Vertical velocity vs. time</h3><svg viewBox="0 0 430 175" role="img" aria-label="Vertical velocity versus time plot"><line className="zero-line" x1="42" y1={velocityY(0)} x2="400" y2={velocityY(0)}/><line className="mini-axis" x1="42" y1="150" x2="400" y2="150"/><polyline className="mini-line velocity" points={velocityPlot}/><line className="plot-cursor" x1={timeX(time)} x2={timeX(time)} y1="24" y2="150"/><circle cx={timeX(time)} cy={velocityY(vy)} r="5" /></svg></div>
        </div>
      </section>

      <section className="challenge-panel">
        <div className="challenge-copy"><span><Target size={16}/> Prediction challenge</span><h2>Where will it land?</h2><p>Make a prediction before revealing the calculated range. Then adjust the angle and see whether your intuition still holds.</p></div>
        <div className="prediction-control"><label>Your prediction <output>{prediction} m</output><input type="range" min="0" max={Math.max(120, Math.ceil(physics.range*1.4))} value={prediction} onChange={(event) => {setPrediction(Number(event.target.value));setRevealed(false);}} /></label><button onClick={() => setRevealed(true)}>Check prediction</button>{revealed && <p>Actual range: <strong>{physics.range.toFixed(1)} m</strong> · Error: <strong>{Math.abs(prediction-physics.range).toFixed(1)} m</strong></p>}</div>
      </section>
    </main>
  );
}

function ForcesLab({ onContext }) {
  const [mass,setMass]=useState(8),[angle,setAngle]=useState(28),[muStatic,setMuStatic]=useState(.35),[muKinetic,setMuKinetic]=useState(.22),[applied,setApplied]=useState(0),[distance,setDistance]=useState(0),[velocity,setVelocity]=useState(0),[playing,setPlaying]=useState(false);
  const g=9.81,radians=angle*Math.PI/180,weight=mass*g,parallel=weight*Math.sin(radians),normal=weight*Math.cos(radians),drive=parallel-applied,maxStatic=muStatic*normal;
  const held=Math.abs(velocity)<.001&&Math.abs(drive)<=maxStatic;
  const direction=Math.abs(velocity)>.001?Math.sign(velocity):Math.sign(drive||1);
  const frictionForce=held?Math.abs(drive):muKinetic*normal;
  const signedFriction=held?drive:direction*frictionForce;
  const net=held?0:drive-signedFriction;
  const acceleration=net/mass;
  useEffect(()=>{if(muKinetic>muStatic)setMuKinetic(muStatic)},[muStatic,muKinetic]);
  useEffect(()=>{setDistance(0);setVelocity(0);setPlaying(false)},[mass,angle,muStatic,muKinetic,applied]);
  useEffect(()=>{if(!playing||held)return undefined;const timer=window.setInterval(()=>setVelocity(current=>{setDistance(s=>Math.max(-3,Math.min(3,s+current*.03+.5*acceleration*.03**2)));return current+acceleration*.03}),30);return()=>window.clearInterval(timer)},[playing,held,acceleration]);
  useEffect(() => onContext({mass_kg:mass,incline_angle_deg:angle,static_friction_coefficient:muStatic,kinetic_friction_coefficient:muKinetic,applied_uphill_force_N:applied,weight_N:weight.toFixed(2),normal_force_N:normal.toFixed(2),downhill_gravity_component_N:parallel.toFixed(2),friction_force_N:frictionForce.toFixed(2),net_force_downhill_N:net.toFixed(2),acceleration_downhill_m_s2:acceleration.toFixed(2),velocity_downhill_m_s:velocity.toFixed(2),state:held?'held by static friction':velocity>=0?'moving downhill':'moving uphill'}),[mass,angle,muStatic,muKinetic,applied,weight,normal,parallel,frictionForce,net,acceleration,velocity,held,onContext]);
  const low={x:190,y:355},length=500,up={x:Math.cos(radians),y:-Math.sin(radians)},out={x:-Math.sin(radians),y:-Math.cos(radians)},high={x:low.x+length*up.x,y:low.y+length*up.y},along=.52-distance/10,contact={x:low.x+length*along*up.x,y:low.y+length*along*up.y},center={x:contact.x+38*out.x,y:contact.y+38*out.y};
  const forceMax=Math.max(weight,normal,parallel,applied,frictionForce,1),vec=value=>Math.min(120,Math.abs(value)/forceMax*120),frictionDirection=held?Math.sign(drive||1):direction;
  return <LabFrame number="02" title="Forces on an incline" description="Resolve weight into components and see when friction can no longer hold the block.">
    <ControlPanel title="System parameters">
      <Range label="Mass" value={mass} setValue={setMass} min={1} max={20} step={1} unit="kg" />
      <Range label="Incline angle" value={angle} setValue={setAngle} min={0} max={45} step={1} unit="°" />
      <Range label="Static friction μₛ" value={muStatic} setValue={setMuStatic} min={0} max={.9} step={.01} unit="" />
      <Range label="Kinetic friction μₖ" value={muKinetic} setValue={setMuKinetic} min={0} max={Math.min(muStatic,.8)} step={.01} unit="" />
      <Range label="Applied force uphill" value={applied} setValue={setApplied} min={0} max={120} step={1} unit="N" />
      <div className="control-buttons"><button className="play-button" onClick={()=>setPlaying(value=>!value)} disabled={held}>{playing?<Pause size={17}/>:<Play size={17}/>} {playing?'Pause':'Run'}</button><button onClick={()=>{setPlaying(false);setDistance(0);setVelocity(0)}}><RotateCcw size={17}/> Reset</button></div>
    </ControlPanel>
    <div className="concept-visual">
      <div className="live-readout"><span>F<sub>net, ∥</sub> <strong>{net.toFixed(1)} N</strong></span><span>a<sub>∥</sub> <strong>{acceleration.toFixed(2)} m/s²</strong></span><span>friction <strong>{held?'static':'kinetic'} · {frictionForce.toFixed(1)} N</strong></span><span>state <strong>{held?'held':velocity>=0?'downhill':'uphill'}</strong></span></div>
      <svg viewBox="0 0 900 430" role="img" aria-label={`Free body diagram for a ${mass} kilogram block on a ${angle} degree incline`}>
        <polygon className="incline" points={`${low.x},${low.y} ${high.x},${high.y} ${high.x},${low.y}`} />
        <g transform={`translate(${center.x} ${center.y}) rotate(${-angle})`}><rect className="block" x="-45" y="-36" width="90" height="72" rx="4" /></g>
        <line className="force weight" x1={center.x} y1={center.y} x2={center.x} y2={center.y+vec(weight)} markerEnd="url(#force-red)" />
        <line className="force normal" x1={center.x} y1={center.y} x2={center.x+out.x*vec(normal)} y2={center.y+out.y*vec(normal)} markerEnd="url(#force-blue)" />
        <line className="force friction" x1={center.x} y1={center.y} x2={center.x+up.x*vec(frictionForce)*frictionDirection} y2={center.y+up.y*vec(frictionForce)*frictionDirection} markerEnd="url(#force-purple)" />
        {applied>0&&<line className="force applied" x1={center.x} y1={center.y} x2={center.x+up.x*vec(applied)} y2={center.y+up.y*vec(applied)} markerEnd="url(#force-green)" />}
        <defs><marker id="force-red" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z"/></marker><marker id="force-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z"/></marker><marker id="force-purple" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z"/></marker><marker id="force-green" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z"/></marker></defs>
        <text x={center.x+10} y={center.y+vec(weight)-5}>mg</text><text x={center.x+out.x*vec(normal)} y={center.y+out.y*vec(normal)-8}>N</text><text x={low.x} y="385">θ = {angle}°</text>
      </svg>
      <ForceBars values={[['gravity ∥',parallel],['friction',frictionForce],['applied',applied],['|net|',Math.abs(net)]]} max={Math.max(parallel,frictionForce,applied,1)} />
    </div>
  </LabFrame>;
}

function EnergyLab({ onContext }) {
  const [mass,setMass]=useState(2),[startHeight,setStartHeight]=useState(12),[initialSpeed,setInitialSpeed]=useState(0),[friction,setFriction]=useState(0),[position,setPosition]=useState(0),[playing,setPlaying]=useState(false);
  const g=9.81,trackHeight=s=>startHeight*(.12+.88*(1-s)**2+.35*s**4),trackX=s=>30*s;
  const samples=useMemo(()=>Array.from({length:101},(_,index)=>{const s=index/100;return{s,x:trackX(s),h:trackHeight(s)}}),[startHeight]);
  let accumulated=0;const track=samples.map((point,index)=>{if(index){const previous=samples[index-1];accumulated+=Math.hypot(point.x-previous.x,point.h-previous.h)}return{...point,arc:accumulated}}),totalArc=track.at(-1).arc;
  const initialEnergy=mass*g*trackHeight(0)+.5*mass*initialSpeed**2;
  let reachable=1;for(const point of track){const available=initialEnergy-friction*mass*g*point.arc-mass*g*point.h;if(available<-.001){reachable=Math.max(0,point.s-.01);break}}
  const actualS=Math.min(position/100,reachable),index=Math.round(actualS*100),point=track[index],lost=friction*mass*g*point.arc,mechanical=Math.max(0,initialEnergy-lost),potential=mass*g*point.h,kinetic=Math.max(0,mechanical-potential),velocity=Math.sqrt(2*kinetic/mass);
  useEffect(()=>{setPosition(0);setPlaying(false)},[mass,startHeight,initialSpeed,friction]);
  useEffect(()=>{if(!playing)return undefined;const timer=window.setInterval(()=>setPosition(current=>{const next=current+Math.max(.15,velocity/totalArc*100*.04);if(next>=reachable*100){setPlaying(false);return reachable*100}return next}),40);return()=>window.clearInterval(timer)},[playing,velocity,totalArc,reachable]);
  useEffect(() => onContext({mass_kg:mass,initial_height_m:startHeight,initial_speed_m_s:initialSpeed,friction_coefficient:friction,track_progress_percent:(actualS*100).toFixed(1),current_height_m:point.h.toFixed(2),potential_energy_J:potential.toFixed(2),kinetic_energy_J:kinetic.toFixed(2),thermal_energy_J:lost.toFixed(2),initial_total_energy_J:initialEnergy.toFixed(2),speed_m_s:velocity.toFixed(2),maximum_reachable_progress_percent:(reachable*100).toFixed(1)}),[mass,startHeight,initialSpeed,friction,actualS,point,potential,kinetic,lost,initialEnergy,velocity,reachable,onContext]);
  const svgPoints=track.map(item=>`${80+item.s*740},${360-item.h/(startHeight*1.5)*290}`).join(' '),px=80+actualS*740,py=360-point.h/(startHeight*1.5)*290;
  return <LabFrame number="03" title="Energy conservation" description="Move a cart along the track and watch potential energy convert into kinetic energy.">
    <ControlPanel title="Cart and track"><Range label="Cart mass" value={mass} setValue={setMass} min={.5} max={10} step={.5} unit="kg"/><Range label="Start height" value={startHeight} setValue={setStartHeight} min={3} max={25} step={1} unit="m"/><Range label="Initial speed" value={initialSpeed} setValue={setInitialSpeed} min={0} max={12} step={.5} unit="m/s"/><Range label="Track friction μ" value={friction} setValue={setFriction} min={0} max={.25} step={.01} unit=""/><Range label="Track position" value={position} setValue={setPosition} min={0} max={100} step={.2} unit="%"/><div className="control-buttons"><button className="play-button" onClick={()=>setPlaying(value=>!value)}>{playing?<Pause size={17}/>:<Play size={17}/>} {playing?'Pause':'Run'}</button><button onClick={()=>{setPlaying(false);setPosition(0)}}><RotateCcw size={17}/> Reset</button></div></ControlPanel>
    <div className="concept-visual"><div className="live-readout"><span>height <strong>{point.h.toFixed(1)} m</strong></span><span>speed <strong>{velocity.toFixed(1)} m/s</strong></span><span>mechanical E <strong>{mechanical.toFixed(0)} J</strong></span><span>thermal E <strong>{lost.toFixed(0)} J</strong></span></div>
      <svg viewBox="0 0 900 430" role="img" aria-label={`Cart at ${point.h.toFixed(1)} metres with speed ${velocity.toFixed(1)} metres per second`}><polyline className="track" points={svgPoints}/><circle className="cart" cx={px} cy={py} r="18"/><line className="height-guide" x1={px} x2={px} y1={py} y2="360"/><text x={px+9} y={(py+360)/2}>{point.h.toFixed(1)} m</text>{reachable<1&&<><line className="reach-limit" x1={80+reachable*740} x2={80+reachable*740} y1="55" y2="365"/><text x={80+reachable*740+7} y="75">turning point</text></>}</svg>
      <div className="energy-bars"><div><span>Potential</span><i style={{height:`${potential/initialEnergy*100}%`}}/><strong>{potential.toFixed(0)} J</strong></div><div><span>Kinetic</span><i className="kinetic" style={{height:`${kinetic/initialEnergy*100}%`}}/><strong>{kinetic.toFixed(0)} J</strong></div><div><span>Thermal</span><i className="thermal" style={{height:`${lost/initialEnergy*100}%`}}/><strong>{lost.toFixed(0)} J</strong></div><div><span>Initial total</span><i className="total" style={{height:'100%'}}/><strong>{initialEnergy.toFixed(0)} J</strong></div></div>
    </div>
  </LabFrame>;
}

function OscillationLab({ onContext }) {
  const [mass,setMass]=useState(1.5),[spring,setSpring]=useState(18),[amplitude,setAmplitude]=useState(.6),[phase,setPhase]=useState(0),[playing,setPlaying]=useState(false);
  const omega=Math.sqrt(spring/mass),period=2*Math.PI/omega,time=phase/100*period,x=amplitude*Math.cos(omega*time),velocity=-amplitude*omega*Math.sin(omega*time),total=.5*spring*amplitude**2,potential=.5*spring*x**2,kinetic=total-potential;
  const acceleration=-(omega**2)*x,force=-spring*x;
  useEffect(()=>{setPhase(0);setPlaying(false)},[mass,spring,amplitude]);
  useEffect(()=>{if(!playing)return undefined;const timer=window.setInterval(()=>setPhase(value=>(value+.6)%100),30);return()=>window.clearInterval(timer)},[playing]);
  useEffect(()=>onContext({mass_kg:mass,spring_constant_N_m:spring,amplitude_m:amplitude,time_s:time.toFixed(2),period_s:period.toFixed(2),angular_frequency_rad_s:omega.toFixed(2),displacement_m:x.toFixed(3),velocity_m_s:velocity.toFixed(3),acceleration_m_s2:acceleration.toFixed(3),restoring_force_N:force.toFixed(3),kinetic_energy_J:kinetic.toFixed(3),potential_energy_J:potential.toFixed(3),total_energy_J:total.toFixed(3)}),[mass,spring,amplitude,phase,time,period,omega,x,velocity,acceleration,force,kinetic,potential,total,onContext]);
  const cx=450+x/amplitude*260;
  const plotX=p=>42+p/100*758,centerY=115,curve=(fn)=>Array.from({length:101},(_,index)=>`${plotX(index)},${centerY-fn(index/100*2*Math.PI)*70}`).join(' ');
  return <LabFrame number="04" title="Simple harmonic motion" description="Scrub through one cycle and connect displacement, velocity, restoring force, and energy.">
    <ControlPanel title="Oscillator"><Range label="Mass" value={mass} setValue={setMass} min={.5} max={5} step={.1} unit="kg"/><Range label="Spring constant" value={spring} setValue={setSpring} min={5} max={60} step={1} unit="N/m"/><Range label="Amplitude" value={amplitude} setValue={setAmplitude} min={.1} max={1} step={.05} unit="m"/><Range label="Cycle" value={phase} setValue={setPhase} min={0} max={100} step={.1} unit="%"/><div className="control-buttons"><button className="play-button" onClick={()=>setPlaying(value=>!value)}>{playing?<Pause size={17}/>:<Play size={17}/>} {playing?'Pause':'Run'}</button><button onClick={()=>{setPlaying(false);setPhase(0)}}><RotateCcw size={17}/> Reset</button></div></ControlPanel>
    <div className="concept-visual"><div className="live-readout"><span>x <strong>{x.toFixed(2)} m</strong></span><span>v <strong>{velocity.toFixed(2)} m/s</strong></span><span>a <strong>{acceleration.toFixed(2)} m/s²</strong></span><span>F <strong>{force.toFixed(1)} N</strong></span><span>T <strong>{period.toFixed(2)} s</strong></span></div>
      <svg viewBox="0 0 900 430" role="img" aria-label={`Spring mass displaced ${x.toFixed(2)} metres`}><line className="equilibrium" x1="450" x2="450" y1="80" y2="340"/><path className="spring" d={`M80 215 ${Array.from({length:20},(_,i)=>`${80+(cx-115)*i/19},${i%2?190:240}`).join(' ')} ${cx-35} 215`}/><rect className="mass-block" x={cx-35} y="170" width="70" height="90"/><line className="restore-arrow" x1={cx} x2={450} y1="290" y2="290" markerEnd="url(#restore)"/><defs><marker id="restore" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z"/></marker></defs><text x="425" y="365">equilibrium</text><text x={(cx+450)/2} y="315">F = −kx</text></svg>
      <svg className="oscillation-plot" viewBox="0 0 850 250" role="img" aria-label="Displacement, velocity, and acceleration over one oscillation cycle"><line className="zero-line" x1="42" x2="800" y1={centerY} y2={centerY}/><polyline className="x-curve" points={curve(t=>Math.cos(t))}/><polyline className="v-curve" points={curve(t=>-Math.sin(t))}/><polyline className="a-curve" points={curve(t=>-Math.cos(t))}/><line className="plot-cursor" x1={plotX(phase)} x2={plotX(phase)} y1="35" y2="195"/><text x="55" y="32">x/A</text><text x="105" y="32">v/vₘₐₓ</text><text x="180" y="32">a/aₘₐₓ</text><text x="800" y="220" textAnchor="end">one period</text></svg>
      <div className="energy-composition"><div><span>Kinetic</span><i style={{width:`${kinetic/total*100}%`}}/></div><div><span>Potential</span><i className="potential" style={{width:`${potential/total*100}%`}}/></div><p>K + U = {total.toFixed(2)} J</p></div>
    </div>
  </LabFrame>;
}

function ElectricFieldLab({ onContext }) {
  const [q1,setQ1]=useState(3),[q2,setQ2]=useState(-3),[separation,setSeparation]=useState(4);
  const k=8.99e9,d=separation,force=k*Math.abs(q1*q2)*1e-12/(d*d),fieldMid=(k*q1*1e-6/((d/2)**2))-(k*q2*1e-6/((d/2)**2));
  useEffect(()=>onContext({left_charge_microC:q1,right_charge_microC:q2,separation_m:separation,force_magnitude_N:force.toFixed(5),interaction:q1*q2<0?'attractive':'repulsive',electric_field_at_midpoint_N_C:fieldMid.toFixed(2)}),[q1,q2,separation,force,fieldMid,onContext]);
  const left=450-separation*45,right=450+separation*45;
  const arrows=[]; for(let gy=90;gy<=350;gy+=65) for(let gx=100;gx<=800;gx+=70){let ex=0,ey=0;[[left,215,q1],[right,215,q2]].forEach(([qx,qy,q])=>{const dx=gx-qx,dy=gy-qy,r2=Math.max(dx*dx+dy*dy,500),r=Math.sqrt(r2);ex+=q*dx/(r2*r);ey+=q*dy/(r2*r)});const mag=Math.hypot(ex,ey)||1;arrows.push(<line key={`${gx}-${gy}`} className="field-arrow" x1={gx-ex/mag*12} y1={gy-ey/mag*12} x2={gx+ex/mag*12} y2={gy+ey/mag*12} markerEnd="url(#field-tip)"/>)}
  return <LabFrame number="05" title="Electric fields" description="Change two source charges and inspect how their vector fields combine everywhere in space.">
    <ControlPanel title="Source charges"><Range label="Left charge" value={q1} setValue={setQ1} min={-6} max={6} step={1} unit="μC"/><Range label="Right charge" value={q2} setValue={setQ2} min={-6} max={6} step={1} unit="μC"/><Range label="Separation" value={separation} setValue={setSeparation} min={2} max={7} step={.5} unit="m"/></ControlPanel>
    <div className="concept-visual"><div className="live-readout"><span>interaction <strong>{q1*q2<0?'attraction':'repulsion'}</strong></span><span>|F| <strong>{force.toFixed(4)} N</strong></span><span>E at midpoint <strong>{fieldMid.toFixed(0)} N/C</strong></span></div>
      <svg viewBox="0 0 900 430" role="img" aria-label={`Electric field around charges ${q1} and ${q2} microcoulombs`}><defs><marker id="field-tip" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z"/></marker></defs>{arrows}<circle className={q1>=0?'charge positive':'charge negative'} cx={left} cy="215" r="29"/><circle className={q2>=0?'charge positive':'charge negative'} cx={right} cy="215" r="29"/><text className="charge-label" x={left} y="221" textAnchor="middle">{q1>=0?'+':''}{q1}</text><text className="charge-label" x={right} y="221" textAnchor="middle">{q2>=0?'+':''}{q2}</text></svg>
    </div>
  </LabFrame>;
}

function Range({label,value,setValue,min,max,step,unit}) { return <label>{label}<output>{typeof value==='number'&&step<1?value.toFixed(step<.1?2:1):value} {unit}</output><input type="range" min={min} max={max} step={step} value={value} onChange={event=>setValue(Number(event.target.value))}/></label>; }
function ControlPanel({title,children}) { return <aside className="lab-controls"><h2>{title}</h2>{children}</aside>; }
function LabFrame({number,title,description,children}) { return <main className="lab-page"><section className="lab-title"><div><span>Interactive lab {number}</span><h1>{title}</h1></div><p>{description}</p></section><section className="lab-layout">{children}</section></main>; }
function ForceBars({values,max}) { return <div className="force-bars">{values.map(([label,value])=><div key={label}><span>{label}</span><i style={{width:`${value/max*100}%`}}/><strong>{value.toFixed(1)} N</strong></div>)}</div>; }

function LabTutor({ lab, state, apiKey, openSettings }) {
  const [open,setOpen]=useState(false),[question,setQuestion]=useState(''),[messages,setMessages]=useState([]),[busy,setBusy]=useState(false),[error,setError]=useState('');
  useEffect(()=>{setMessages([]);setQuestion('');setError('');},[lab.id]);
  async function submit(event){event.preventDefault();if(!question.trim()||busy)return;if(!apiKey){openSettings();return;}const user={role:'user',content:question.trim()};setMessages(items=>[...items,user]);setQuestion('');setBusy(true);setError('');try{const data=await api.ask(lab.topic,user.content,apiKey,lab.title,state,messages);setMessages(items=>[...items,{role:'assistant',content:data.answer}]);}catch(requestError){setError(requestError.message);}finally{setBusy(false)}}
  if(!open)return <button className="lab-tutor-fab" onClick={()=>setOpen(true)}><Atom size={18}/> Ask the lab coach</button>;
  return <aside className="lab-tutor"><header><div><span>State-aware AI coach</span><h2>{lab.title}</h2></div><button aria-label="Close lab coach" onClick={()=>setOpen(false)}><X/></button></header><p>The coach can see the current sliders and calculated values.</p><div className="coach-prompts"><button onClick={()=>setQuestion('Walk me through what the visualization is showing right now.')}>Explain this state</button><button onClick={()=>setQuestion('Give me a prediction challenge using the current settings.')}>Challenge me</button><button onClick={()=>setQuestion('Help me solve a related problem one step at a time.')}>Solve with me</button></div><div className="coach-messages">{messages.map((message,index)=><div className={message.role} key={index}>{message.role==='assistant'?<ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>{message.content}</ReactMarkdown>:message.content}</div>)}{busy&&<div className="assistant">Thinking about the current state…</div>}{error&&<div className="coach-error">{error}</div>}</div><form onSubmit={submit}><textarea rows="3" value={question} onChange={event=>setQuestion(event.target.value)} placeholder={apiKey?'Ask about the graph, equation, or problem…':'Configure an API key in Settings first.'}/><button disabled={!question.trim()||busy}><Send size={16}/> Send</button></form></aside>;
}

const LABS=[
  {id:'projectile',title:'Projectile motion',topic:'kinematics-1d'},
  {id:'forces',title:'Forces on an incline',topic:'forces-newtons-laws'},
  {id:'energy',title:'Energy conservation',topic:'work-energy'},
  {id:'oscillation',title:'Simple harmonic motion',topic:'simple-harmonic-motion'},
  {id:'fields',title:'Electric fields',topic:'electric-fields'},
];

function Labs({apiKey,openSettings}){
  const [selected,setSelected]=useState(LABS[0]);
  const [context,setContext]=useState({});
  const contextHandler=useMemo(()=>state=>setContext(state),[]);
  let visual;
  if(selected.id==='projectile')visual=<ProjectileLab onContext={contextHandler}/>;
  else if(selected.id==='forces')visual=<ForcesLab onContext={contextHandler}/>;
  else if(selected.id==='energy')visual=<EnergyLab onContext={contextHandler}/>;
  else if(selected.id==='oscillation')visual=<OscillationLab onContext={contextHandler}/>;
  else visual=<ElectricFieldLab onContext={contextHandler}/>;
  return <><div className="lab-switcher" aria-label="Choose a lab">{LABS.map((lab,index)=><button className={lab.id===selected.id?'active':''} onClick={()=>setSelected(lab)} key={lab.id}><span>0{index+1}</span>{lab.title}</button>)}</div>{visual}<LabTutor lab={selected} state={context} apiKey={apiKey} openSettings={openSettings}/></>;
}

function SettingsDialog({ apiKey, onSave, onClose }) {
  const [value, setValue] = useState(apiKey);
  function submit(event) {
    event.preventDefault();
    onSave(value.trim());
    onClose();
  }
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="settings-dialog" role="dialog" aria-modal="true" aria-labelledby="settings-title">
        <header><div><span>Student settings</span><h2 id="settings-title">AI tutor access</h2></div><button onClick={onClose} aria-label="Close settings"><X /></button></header>
        <p>Enter an OpenAI API key to ask questions about lesson material. It stays in this browser session and is sent only with your tutor requests.</p>
        <form onSubmit={submit}>
          <label htmlFor="api-key">OpenAI API key</label>
          <input id="api-key" type="password" autoComplete="off" value={value} onChange={(event) => setValue(event.target.value)} placeholder="sk-…" />
          <div className="settings-actions"><button type="button" onClick={() => setValue("")}>Clear</button><button type="submit"><Check size={16} /> Save settings</button></div>
        </form>
      </section>
    </div>
  );
}

export default function App() {
  const [catalog, setCatalog] = useState(null);
  const [lesson, setLesson] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [apiKey, setApiKey] = useState(() => window.sessionStorage.getItem("physicsatlas_openai_key") || "");
  const [view, setView] = useState("lab");

  useEffect(() => { api.get("/api/catalog").then(setCatalog).catch((err) => setError(err.message)).finally(() => setLoading(false)); }, []);

  async function openLesson(slug) {
    setLoading(true); setError("");
    try { setLesson(await api.get(`/api/lessons/${slug}`)); setView("library"); window.scrollTo(0, 0); }
    catch (err) { setError(err.message); }
    finally { setLoading(false); }
  }

  function saveApiKey(value) {
    setApiKey(value);
    if (value) window.sessionStorage.setItem("physicsatlas_openai_key", value);
    else window.sessionStorage.removeItem("physicsatlas_openai_key");
  }

  return (
    <div className="app-shell">
      <header className="site-header"><button className="brand" onClick={() => {setView("lab");setLesson(null);}}><Atom /><span>PHYSICS<em>LAB</em></span></button><nav className="main-nav"><button className={view === "lab" ? "active" : ""} onClick={() => {setView("lab");setLesson(null);}}>Lab</button><button className={view === "library" ? "active" : ""} onClick={() => {setView("library");setLesson(null);}}>References</button></nav><button className="settings-button" onClick={() => setSettingsOpen(true)}><Settings size={17} /><span>Settings</span>{apiKey && <i aria-label="API key configured" />}</button></header>
      {loading && view === "library" && <div className="loading"><Atom /><span>Loading references…</span></div>}
      {error && <div className="global-error">{error}</div>}
      {view === "lab" && <Labs apiKey={apiKey} openSettings={() => setSettingsOpen(true)} />}
      {view === "library" && !loading && !lesson && <Library catalog={catalog} onOpen={openLesson} />}
      {view === "library" && !loading && lesson && <Reader lesson={lesson} apiKey={apiKey} openSettings={() => setSettingsOpen(true)} onBack={() => setLesson(null)} />}
      {settingsOpen && <SettingsDialog apiKey={apiKey} onSave={saveApiKey} onClose={() => setSettingsOpen(false)} />}
    </div>
  );
}
