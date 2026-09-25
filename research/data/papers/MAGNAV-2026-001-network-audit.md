# MAGNAV-2026-001: Global Geophysical Navigation Network — Novelty Audit

**Date:** 2026-04-26  
**Prepared by:** magnav-auditor (theory-lead team, ghost-murmur-magnav)  
**Status:** RESEARCH COMPLETE — speculative interpretations labeled  
**Confidence:** medium-high on SOTA claims (public sources); medium on gap assessment

---

## Section 1: State of the Art

### 1.1 Airborne Magnetic Navigation (MagNav)

The field is mature at aircraft scale and accelerating fast.

**MIT Lincoln Laboratory / USAF (2023):** First real-time MagNav demonstration on a C-17A Globemaster III, May 2023, three sorties Travis AFB → Edwards AFB. Proof-of-concept: the pipeline works end-to-end in real time on a military aircraft with active interference compensation (Tolles-Lawson).

**Q-CTRL / Ironstone Opal (February 2025):** Field trials near Griffith, Australia. 6700+ km flown on a Cessna 208B. Best result: 22-meter final positioning error on a single flight (0.006% of distance). Consistent 11× advantage over velocity-aided INS across all conditions. The key advance was their "magnetic denoising" ML layer — 3× better than prior art with 15× faster learning. Published on arXiv (2504.08167). This is the current public SOTA for airborne MagNav accuracy.

**SandboxAQ / AQNav (launched June 2024):** First commercial real-time system. Five-month Airbus Acubed trial: 150+ flight hours, 44,000 km, 200 airports. Achieved RNP2 (±2 NM) full-time; RNP0.3 (±550 m) 64% of the time. Announced USAF primary-navigation flight test July 2024. Defense and commercial aviation focus. No pedestrian or ground-vehicle variant announced.

**SBQuantum:** Canadian NV-center magnetometer company. Handheld device (~quart-of-milk size), sensitivity ~400 pT/√Hz, heading error <5 nT. ESA contracts for space deployment. Field-demonstrated in Canadian Arctic, drone, and high-altitude balloon. No standalone navigation product; sensor only. No public pricing — government/contract sales only.

**Navy gravity-aided submarine navigation (SINS):** Mature classified program. Published academic literature shows 1–4 nautical mile accuracy using 1'×1' gravity anomaly reference maps and 1–2 mGal gravimeters (strapdown). Four key components: INS, gravimeter, reference map, matching algorithm (ICCP or TERCOM-style). This is entirely gravity-based, not magnetic.

**Sensor fusion architecture (SOTA):** The standard pipeline is: high-stability magnetometer → Tolles-Lawson aircraft compensation (or ML equivalent) → map-matching filter (extended Kalman or particle filter) → fused with IMU/INS. Open-source reference: MagNav.jl (MIT, Julia), the canonical public implementation. Neural network variants (Liquid Time-Constant Networks, LNNs) published 2024 on arXiv extending the compensation model.

### 1.2 Ground/Pedestrian Scale

This is the genuine gap. No peer-reviewed demonstration of outdoor pedestrian-scale MagNav against crustal anomaly maps exists in the public literature. What exists:

- Indoor pedestrian magnetic positioning: well-studied, uses *building-distorted* fields as fingerprints, not crustal anomaly maps. Accuracy 1–3 m in mapped buildings. Useless outdoors.
- Smartphone-IMU + magnetometer PDR (pedestrian dead reckoning): heading aid only. No absolute position fix.
- No published outdoor consumer-scale system matching a portable sensor to EMAG2/USGS crustal maps.

---

## Section 2: Available Data Sources

### 2.1 Magnetic Anomaly Maps

| Dataset | Resolution | Coverage | License | Notes |
|---|---|---|---|---|
| EMAG2v3 (NOAA/USGS) | 2 arc-min (~3.7 km at equator) | Global | Public domain (USG) | GeoTIFF + netCDF; crustal anomaly at 4 km altitude |
| USGS airborne surveys | 200–400 m (varies by region) | Patchy US coverage | Public domain | Higher resolution but not global |
| ESA Swarm lithospheric | ~2800 km wavelength floor | Global | Open | Only resolves features >degree 14; not useful below ~100 km scale |
| NGA CHAMP/Swarm compilations | ~30 km | Global | Varies | Higher-resolution classified versions exist |

**Critical limitation:** EMAG2's 3.7 km resolution is the best freely available global grid. At pedestrian scale (meters), the signal you'd match against is dominated by local geology variations far smaller than the map can resolve. Aircraft fly at altitudes where the field is smoother and better-mapped. On the ground, you're in a spatial-frequency regime the maps don't cover.

### 2.2 Gravity Anomaly Maps

| Dataset | Resolution | Notes |
|---|---|---|
| EGM2020 (NGA) | 2.5 arc-min (~4.6 km); 1 arc-min version available | Spherical harmonic to degree 2190; download at earth-info.nga.mil |
| EGM2008 (public) | 2.5 arc-min | Fully public; functionally equivalent for navigation |
| IGETS network | Point measurements | Superconducting gravimeter stations, ~few-minute latency, geophysics research |

**Gravity for navigation:** Gravity anomaly varies at the ~10 mGal level globally, ~0.1–1 mGal locally. Ground-level gravimeters can resolve 0.01–0.1 mGal. The signal exists for navigation but requires very slow movement (submarine timescales) for the filter to converge — rapid pedestrian dynamics make gravity-aided nav impractical with current map resolution.

### 2.3 Stationary Observation Networks

**INTERMAGNET:** ~150 magnetic observatories globally. 1-minute and 1-second cadence data. Latency: 15 min to 1 hour depending on station, via GINs (Paris, Edinburgh, Golden CO, Kyoto). Data available for download; some near-real-time API access via INTERMAGNET and BGS. Purpose: track secular variation and space weather, not navigation. Station spacing: ~hundreds to thousands of km. Not a positioning reference grid.

**IGETS (International Geodynamics and Earth Tide Service):** Superconducting gravimeter network. Geophysics research; not designed for navigation. Station count: ~dozens globally.

**Key point:** These networks track *temporal variation* in the field — solar storms, tidal loading, secular drift. They enable correction of a navigation system's reference map for field changes over time. This correction integration is *not currently done* in commercial MagNav systems (they use static maps). This is a real gap.

---

## Section 3: User's Proposed Architecture vs SOTA

**User's proposed architecture:** Global stationary gravimeter + magnetometer network + public anomaly maps + handheld NV magnetometer = GPS-free navigation.

**Assessment: Partly reinvention, partly valid engineering extension, with one genuine novel element.**

| Component | SOTA status | User's version |
|---|---|---|
| Handheld quantum magnetometer | Exists (SBQuantum, $$$) | Same; novelty is in cost/DIY |
| Anomaly map matching | Mature for aircraft | Not demonstrated for pedestrians vs. crustal maps |
| Real-time INTERMAGNET correction | Not done in any known system | Genuine gap |
| Stationary gravimeter network as nav aid | Not done at pedestrian/ground-vehicle scale | Novel application; feasibility unclear |
| Fusion architecture (IMU + mag + gravity) | Published in theory, demonstrated at submarine/aircraft scale | Novel at ground scale |

**The reinvention part:** The aircraft-scale MagNav system already does everything the user proposes — quantum sensor, crustal anomaly map matching, sensor fusion with IMU. SandboxAQ, Q-CTRL, and MIT have all demonstrated it. If the user builds an aircraft MagNav system, it is reinvention.

**The genuine extension:** The user is implicitly targeting pedestrian or ground-vehicle scale in urban environments. This has not been demonstrated anywhere in the public literature against crustal anomaly maps. The physics reasons are clear (map resolution vs. signal scale) but it is not proven impossible either.

**The novel element:** Real-time correction of reference maps using live INTERMAGNET data. No commercial system does this. During geomagnetic storms, the crustal field is contaminated by external (ionospheric/magnetospheric) fields. INTERMAGNET data could correct this in near-real-time. This is a real architectural innovation, though its magnitude of benefit is uncertain.

---

## Section 4: Specific Novelty Gaps an Independent Researcher Could Fill

Ranked by tractability for an independent researcher:

**Gap 1 (HIGH tractability): Real-time INTERMAGNET correction integration**  
No known system integrates live observatory data to correct navigation maps during geomagnetic disturbances. INTERMAGNET data is free, has documented APIs, and the correction methodology (subtracting the external field component using a nearby observatory) is published in geophysics literature. Software-only contribution; no new hardware needed. Could meaningfully improve existing open-source MagNav stacks (MagNav.jl) during storm periods. *This is the clearest, most achievable novelty.*

**Gap 2 (MEDIUM tractability): Pedestrian-scale outdoor characterization study**  
Nobody has published a systematic measurement of how well a portable magnetometer distinguishes position at pedestrian scales against EMAG2. Is the crustal anomaly signal-to-noise ratio sufficient at ground level? The answer is probably "no in cities, maybe in rural geology-rich terrain" — but this hasn't been quantified. A field measurement campaign with a ~$5k fluxgate magnetometer and GPS ground truth would settle this question. *Publication-worthy negative result or positive result.*

**Gap 3 (MEDIUM tractability): Open-source ground-vehicle MagNav stack**  
MagNav.jl is aircraft-centric (Tolles-Lawson assumes fixed-wing aircraft interference model). A ground-vehicle variant needs a different interference model (engine, suspension, ferrous chassis). No public implementation exists. Reasonably achievable in Python/Julia with a test vehicle and some logged data.

**Gap 4 (LOW tractability for independent researcher): Sub-$1k NV magnetometer**  
SBQuantum sensors are research-grade and priced accordingly. DIY NV magnetometers are being demonstrated at 400 pT/√Hz in lab settings (arXiv 2512.03106 shows an LED-based teaching lab version). Getting this to navigation-useful sensitivity in a portable form factor is a hardware PhD problem. *Not tractable alone without lab infrastructure.*

**Gap 5 (LOW tractability): Urban MagNav — solving the noise problem**  
Urban environments have 10–100 nT of human-made magnetic noise (trains, rebar, transformers). Crustal anomaly signals are 1–50 nT at ground level in quiet terrain. The SNR in cities is likely below 1 for crustal matching. Solving this requires either (a) very high sample-rate arrays to spatially resolve anthropogenic vs. crustal sources, or (b) ML discrimination trained on labeled urban data. Neither has a cheap solution.

---

## Section 5: Smallest Meaningful Demo

**Recommended minimum viable experiment:**

*Goal:* Demonstrate that a portable magnetometer can distinguish position at 100m scale in a geologically active rural area using EMAG2 or a regional airborne survey map, with and without INTERMAGNET real-time correction.

*Hardware:* A consumer-grade fluxgate triaxial magnetometer (e.g., PNI RM3100 sensor, ~$200; or a Bartington Mag-03 if budget allows ~$3k) + Raspberry Pi + GPS ground truth logger. NV magnetometer is not required for this experiment — demonstrate the concept first with classical sensors.

*Software:* Pull EMAG2 tiles for region. Pull INTERMAGNET data (BGS API or USGS). Implement EKF map-matcher in Python (port from MagNav.jl concepts). Log comparison: unaided vs. map-aided vs. INTERMAGNET-corrected.

*Cost:* $200–$500 hardware. Free data. ~2–3 months part-time for a capable programmer with physics background.

*Accuracy target:* 100–500 m absolute position fix in low-noise rural terrain. Do not attempt urban first.

*Publication threshold:* A null result (map resolution insufficient for pedestrian positioning) is publishable in NAVIGATION or IEEE Sensors Letters if the measurement methodology is careful. A positive result is more publishable still.

*Connection to worldline-MERA project:* Weak. The atom-interferometer gravimeters used in some quantum inertial navigation research use Rydberg-adjacent cold-atom physics, which is technically adjacent to the broader quantum sensing field. There is no conceptual or mathematical connection to the MERA/holography research. These are separate projects.

---

## Summary Verdict

The user's proposed architecture is **not novel at aircraft scale** — it is a precise description of SandboxAQ AQNav (2024) and Q-CTRL Ironstone Opal (2025). 

It **is** a meaningful engineering project at **pedestrian/ground scale** because that gap is real and undemonstrated in the public literature.

The **single most novel element** is real-time INTERMAGNET correction integration, which no commercial system implements and which is achievable with existing open infrastructure.

An independent researcher's highest-leverage contribution: (1) characterize whether EMAG2 provides sufficient SNR for ground-level positioning in rural terrain, and (2) build the first open-source real-time INTERMAGNET-corrected MagNav pipeline for ground vehicles. Both are tractable. Neither requires a quantum sensor to start.

*[SPECULATIVE LABEL: Section 3 gap assessment and Section 4 tractability rankings are the author's interpretation of the literature, not independently verified claims. Confidence: medium.]*
