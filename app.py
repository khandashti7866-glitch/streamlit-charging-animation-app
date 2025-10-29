import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Charging Animation", page_icon="🔋", layout="centered")

st.title("🔋 Charging Animation")

# Controls
col1, col2 = st.columns([2, 1])
with col1:
    color = st.color_picker("Battery color", "#00cc66")
    bg = st.color_picker("Background color", "#0f172a")
    size = st.slider("Size (width px)", 120, 500, 240)
    show_percent = st.checkbox("Show numeric %", True)
with col2:
    speed = st.slider("Speed (seconds to fill)", 2.0, 20.0, 6.0, step=0.5)
    initial = st.slider("Start percent", 0, 100, 0)
    loop = st.checkbox("Loop animation", True)

# Start / Restart button (re-renders html to restart animation)
if st.button("Start / Restart"):
    st.experimental_rerun()

# Prepare HTML/CSS/JS. We'll inject the parameters to control animation-duration, color, etc.
html = dedent(f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {{
    --battery-color: {color};
    --bg-color: {bg};
    --width: {size}px;
    --height: calc(var(--width) * 0.55);
    --duration: {speed}s;
    --start-pct: {initial}%;
    --show-percent: {'block' if show_percent else 'none'};
  }}
  html,body {{
    margin:0;
    padding:0;
    background: var(--bg-color);
    height:100%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  }}
  .battery {{
    width: var(--width);
    height: var(--height);
    border-radius: 8px;
    padding: 8px;
    box-sizing: border-box;
    position: relative;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0.06));
    border: 2px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 25px rgba(2,6,23,0.6), inset 0 2px 4px rgba(255,255,255,0.02);
  }}
  .battery::after {{
    content: "";
    position: absolute;
    right: -10px;
    top: 30%;
    width: calc(var(--width) * 0.06);
    height: calc(var(--height) * 0.4);
    background: rgba(255,255,255,0.06);
    border-radius: 3px;
  }}
  .inner {{
    width: 100%;
    height: 100%;
    background: rgba(255,255,255,0.03);
    border-radius: 6px;
    overflow: hidden;
    position: relative;
  }}
  .level {{
    position: absolute;
    left: 0;
    bottom: 0;
    height: 100%;
    width: var(--start-pct);
    background: linear-gradient(90deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)), var(--battery-color);
    box-shadow: 0 0 20px rgba(0,0,0,0.2) inset;
    transform-origin: left center;
    border-right: 1px solid rgba(0,0,0,0.08);
    transition: width 0.3s linear;
  }
  /* Charging bars (visual shimmer) */
  .shimmer {{
    position: absolute;
    top:0;
    bottom:0;
    left: -50%;
    width: 200%;
    background: linear-gradient(90deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0.12) 50%, rgba(255,255,255,0.02) 100%);
    animation: glide var(--duration) linear infinite;
    mix-blend-mode: overlay;
    opacity: 0.6;
  }}
  @keyframes glide {{
    0% {{ transform: translateX(-25%); }}
    100% {{ transform: translateX(25%); }}
  }}

  .percent {{
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    font-weight: 700;
    display: var(--show-percent);
    color: white;
    text-shadow: 0 2px 10px rgba(0,0,0,0.6);
    letter-spacing: 0.6px;
    font-size: calc(var(--height) * 0.35);
  }}

  /* small responsive */
  @media (max-width: 480px) {{
    :root {{ --width: 200px; }}
  }}
</style>
</head>
<body>
  <div class="battery" role="img" aria-label="Battery charging animation">
    <div class="inner">
      <div id="level" class="level"></div>
      <div class="shimmer" id="shimmer"></div>
      <div id="percent" class="percent"></div>
    </div>
  </div>

<script>
(function() {{
  const level = document.getElementById('level');
  const percentEl = document.getElementById('percent');
  let startPct = Number(getComputedStyle(document.documentElement).getPropertyValue('--start-pct').trim().replace('%','')) || 0;
  const duration = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--duration')) || {speed};
  const loop = {"true" if loop else "false"};

  // Use JS to animate width from startPct to 100 over `duration` seconds.
  function animateTo(targetPct, timeSec) {{
    const fps = 60;
    const steps = Math.max(1, Math.round(timeSec * fps));
    const from = startPct;
    const to = targetPct;
    let step = 0;
    const delta = (to - from) / steps;
    const interval = 1000 / fps;
    percentEl.textContent = Math.round(from) + "%";
    const t = setInterval(() => {{
      step++;
      const cur = from + delta * step;
      level.style.width = cur + "%";
      percentEl.textContent = Math.round(cur) + "%";
      if (step >= steps) {{
        clearInterval(t);
        startPct = to;
        if (loop) {{
          // small pause then restart
          setTimeout(() => {{
            startPct = 0;
            animateTo(100, duration);
          }}, 350);
        }}
      }}
    }}, interval);
  }}

  // Kick off
  animateTo(100, duration);
}})();
</script>
</body>
</html>
""")

# Render HTML component
st.components.v1.html(html, height=int(size * 0.7) + 80, scrolling=False)
st.write("Tip: Adjust **speed**, **size**, and **color**, then press **Start / Restart** to re-run the animation.")
st.write("Run with: `streamlit run app.py`")
