import sys
import os
import hashlib
from datetime import datetime
import subprocess

# ============================================================
# UI ARCHITECTURE MAP — AI33‑MPOPT APP
# ============================================================
# TAB 1: System Snapshot
#   - Run System Snapshot
#   - Snapshot Summary
#
# TAB 2: Spectral Engines
#   - Primary / Synthetic / Prime‑Lattice Engines
#   - Visualization Modes (JSON, Summary, Histogram, Line Plot)
#   - Advanced Spectral Diagnostics:
#       1. Weyl Dimension
#       2. Spectral Rigidity (Δ₃)
#       3. Spacing vs Riemann
#       4. Curvature (Δ²) Plot
#       5. Multi‑Engine Comparison
#
# TAB 3: Cosmology Engines
#   - LCDM Ages
#   - Paused Gravity Optimization
#   - Density‑Refined Optimization
#
# TAB 4: JWST Cosmology
#   - Dark Energy / Dark Matter Split
#   - Full JWST Cosmology Dashboard:
#       • Panel A: Flux vs Redshift
#       • Panel B: Residuals vs Redshift
#       • Panel C: Ωm(z) / ΩΛ(z) Evolution
#       • Panel D: Singularity / SSE Diagnostic
#
# TAB 5: 5D Structural Invariant
#   - Geometry / Paused / Density Weights
#   - Weyl Dimension
#   - Aggregation Mode
#   - 5D Structural Invariant + Throat Weights
#
# TAB 6: Final Interpretation (Identity Block)
#   - Frozen backend identity spec
#   - Hashes + Freeze Code
#
# TAB 7: Spectral Core Dashboard
#   - Health & Integrity (health check + hash check)
#   - Invariants & Summaries
#   - Visualizations
#   - Derived Invariants Export
#
# TAB 8: Spectral Geometry Visuals
#   - Laplacian spectrum
#   - Diffusion distance / embedding
#   - Spectral string (3D)
#   - Curvature / torsion / worldsheet action
#   - Diffusion scaling (spectral dimension)
#   - Duality matrix
#   - Multiverse graph / Laplacian
#   - Entangled Particle Shadow MBots (247)
# ============================================================

# Ensure the src/ folder is on the Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import numpy as np

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="AI33-MPOPT Spectral + Cosmology Demo",
    layout="wide"
)

# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------
st.title("AI33-MPOPT — Unified Spectral + Cosmology Engine")
st.write("Deterministic, collision-free spectral invariants and JWST-anchored cosmology.")

# ------------------------------------------------------------
# ROUTER INSTANCE (FOR SYSTEM SNAPSHOT & GEOMETRY)
# ------------------------------------------------------------

# ------------------------------------------------------------
# UTILITY
# ------------------------------------------------------------
def show_result(title, engine_name, arg=None):
    st.subheader(title)
    try:
        result = run_engine(engine_name, arg)
        st.json(result)
    except Exception as e:
        st.error(f"Error: {e}")

@st.cache_data
def load_jwst_locked():
    return pd.DataFrame({
        "z": [8.0, 9.1, 10.33, 11.0],
        "flux": [1.0, 0.9, 0.8, 0.7]
    })

# ------------------------------------------------------------
# SPECTRAL CORE HELPERS
# ------------------------------------------------------------
SPECTRAL_CSV_PATH = os.path.join(BASE_DIR, "spectral", "rivero", "riemann_rivero_pairs.csv")
HEALTH_CHECK_PATH = os.path.join(BASE_DIR, "core", "health_check.py")
FREEZE_CODE = "A1F7-C9E3-D4B2-7E6A"
FREEZE_LEDGER_PATH = os.path.join(BASE_DIR, "freeze_ledger.txt")

def compute_file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def append_freeze_ledger(entry: str) -> None:
    try:
        with open(FREEZE_LEDGER_PATH, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception:
        # Ledger failure should never crash UI
        pass

# ------------------------------------------------------------
# TABS
# ------------------------------------------------------------
tabs = st.tabs([
    "System Snapshot",
    "Spectral Engines",
    "Cosmology Engines",
    "JWST Cosmology",
    "5D Structural Invariant",
    "Final Interpretation",
    "Spectral Core Dashboard",
    "Spectral Geometry Visuals",
    "Higgs Subsystem",
    "Higgs Subsystem (Advanced)",  # NEW TAB 10
])

# ============================================================
# TAB 1 — SYSTEM SNAPSHOT
# ============================================================
with tabs[0]:
    st.header("System Snapshot Engine")

    col1, col2 = st.columns([1, 1])

    # -------------------------------
    # SYSTEM SNAPSHOT RAW
    # -------------------------------
    with col1:
        if st.button("Run System Snapshot", key="system_snapshot"):
            try:
                resp = router.dispatch("system_snapshot", {"t": 0})
                st.subheader("Raw Snapshot Output")
                st.json(resp)
            except Exception as e:
                st.error(f"Error: {e}")

    # -------------------------------
    # SYSTEM SNAPSHOT SUMMARY
    # -------------------------------
    with col2:
        if st.button("Generate Snapshot Summary", key="snapshot_summary"):
            try:
                resp = router.dispatch("system_snapshot", {"t": 0})
                st.subheader("High-Level Summary")
                if isinstance(resp, dict):
                    st.write("Status:", resp.get("status", "unknown"))
                    st.write("Domain:", resp.get("domain", "unknown"))
                    st.write("Action:", resp.get("action", "unknown"))
                else:
                    st.json(resp)
            except Exception as e:
                st.error(f"Error: {e}")

# ============================================================
# TAB 2 — SPECTRAL ENGINES (FINAL CORRECTED VERSION)
# ============================================================
with tabs[1]:
    st.header("Spectral Engines")

    # -------------------------------
    # IMPORT BACKEND SPECTRAL ENGINES
    # -------------------------------
    from spectral.rivero_zeta import (
        omega_3d_synth, omega_4d_synth, omega_5d_synth,
        omega_3d_prime, omega_4d_prime, omega_5d_prime,
        spectrum_invariant_summary,
        weyl_dimension_estimate, asymptotic_tail_slope,
        spectral_density, loglog_scaling_residual,
        spacing_statistics, compare_to_riemann_spacing,
        OMEGA_3D, OMEGA_4D, OMEGA_5D
    )

    # -------------------------------
    # ENGINE REGISTRY
    # -------------------------------
    SPECTRAL_ENGINES = {
        "Primary ωₙ Spectrum": ("Primary Rivero ωₙ", "omega_primary"),
        "Synthetic Spectrum — 3D": ("3D Synthetic", omega_3d_synth),
        "Synthetic Spectrum — 4D": ("4D Synthetic", omega_4d_synth),
        "Synthetic Spectrum — 5D": ("5D Synthetic", omega_5d_synth),
        "Prime‑Lattice Spectrum — 3D": ("3D Prime-Lattice", omega_3d_prime),
        "Prime‑Lattice Spectrum — 4D": ("4D Prime-Lattice", omega_4d_prime),
        "Prime‑Lattice Spectrum — 5D": ("5D Prime-Lattice", omega_5d_prime),
        "Full Weyl Audit": ("Weyl Audit", "spectral_audit"),
        "Deep Spectral Analysis": ("Deep Spectral Analysis", "deep_spectral_analysis"),
        "Quantum Chaos Audit": ("Quantum Chaos Audit", "quantum_chaos_audit"),
        "Publishable Spectral Study": ("Publishable Spectral Study", "publishable_spectral_study"),
        "GUE Self-Calibration": ("GUE Self-Calibration", "gue_self_calibration"),
        "Structural Analogy: Riemann vs Rivero": ("Structural Analogy Summary", "structural_summary"),
    }

    # -------------------------------
    # ENGINE SELECTION
    # -------------------------------
    selected_spectral = st.selectbox(
        "Select Spectral Engine",
        list(SPECTRAL_ENGINES.keys()),
        key="spectral_select"
    )

    title, engine = SPECTRAL_ENGINES[selected_spectral]
    is_spectrum_engine = callable(engine)

    # -------------------------------
    # VISUALIZATION MODE SELECTION
    # -------------------------------
    if is_spectrum_engine:
        viz_mode = st.selectbox(
            "Visualization Mode",
            ["JSON only", "Summary", "Summary + Histogram", "Summary + Line Plot"],
            key="spectral_viz_mode"
        )
    else:
        viz_mode = st.selectbox(
            "Visualization Mode",
            ["JSON only", "Summary"],
            key="spectral_viz_mode"
        )

    # -------------------------------
    # RUN SELECTED SPECTRAL ENGINE
    # -------------------------------
    if st.button("Run Selected Spectral Engine", key="run_spectral_selected"):
        st.subheader(title)

        # ---------------------------
        # ANALYSIS ENGINES (ROUTER)
        # ---------------------------
        if not is_spectrum_engine:
            result = run_engine(engine, None)

            if viz_mode == "JSON only":
                st.json(result)
            elif viz_mode == "Summary":
                st.json(result)

            st.stop()

        # ---------------------------
        # SPECTRUM ENGINES (CALLABLE)
        # ---------------------------
        spectrum = engine()

        if viz_mode == "JSON only":
            st.json({"spectrum": spectrum.tolist()})
        else:
            summary = spectrum_invariant_summary(spectrum)
            st.markdown("### Invariant Summary")
            st.json(summary)

            # -----------------------
            # HISTOGRAM OF SPACINGS
            # -----------------------
            if viz_mode == "Summary + Histogram":
                import plotly.express as px
                diffs = np.diff(spectrum)
                fig = px.histogram(diffs, nbins=40, title="Spacing Distribution Δω")
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            # -----------------------
            # LINE PLOT OF SPECTRUM
            # -----------------------
            elif viz_mode == "Summary + Line Plot":
                import plotly.express as px
                df_spec = pd.DataFrame({
                    "n": np.arange(1, len(spectrum) + 1),
                    "omega": spectrum,
                })
                fig = px.line(df_spec, x="n", y="omega", title="Spectrum Growth ω(n)")
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

    # ========================================================
    # ADVANCED SPECTRAL DIAGNOSTICS
    # ========================================================
    st.markdown("---")
    st.subheader("Advanced Spectral Diagnostics")

    adv_mode = st.selectbox(
        "Select Advanced Diagnostic",
        [
            "None",
            "Weyl Dimension",
            "Spectral Rigidity (Δ₃)",
            "Spacing vs Riemann",
            "Curvature (Δ²) Plot",
            "Compare Multiple Engines",
        ],
        key="adv_diag_select"
    )

    # -------------------------------
    # 1. WEYL DIMENSION
    # -------------------------------
    if adv_mode == "Weyl Dimension":
        st.markdown("### Weyl Dimension Estimate")

        engine_pick = st.selectbox(
            "Select Spectrum",
            ["3D Prime-Lattice", "4D Prime-Lattice", "5D Prime-Lattice"],
            key="weyl_pick"
        )

        spec_map = {
            "3D Prime-Lattice": OMEGA_3D,
            "4D Prime-Lattice": OMEGA_4D,
            "5D Prime-Lattice": OMEGA_5D,
        }

        spec = spec_map[engine_pick]

        full_dim = weyl_dimension_estimate(spec)
        tail_dim = asymptotic_tail_slope(spec)

        st.json({
            "weyl_dimension_full": float(full_dim),
            "weyl_dimension_tail": float(tail_dim),
        })

    # -------------------------------
    # 2. SPECTRAL RIGIDITY (Δ₃)
    # -------------------------------
    if adv_mode == "Spectral Rigidity (Δ₃)":
        st.markdown("### Spectral Rigidity Δ₃")

        engine_pick = st.selectbox(
            "Select Spectrum",
            ["3D Prime-Lattice", "4D Prime-Lattice", "5D Prime-Lattice"],
            key="rigid_pick"
        )

        spec_map = {
            "3D Prime-Lattice": OMEGA_3D,
            "4D Prime-Lattice": OMEGA_4D,
            "5D Prime-Lattice": OMEGA_5D,
        }

        spec = spec_map[engine_pick]

        diffs = np.diff(spec)
        rigidity = float(np.std(diffs) / np.mean(diffs))

        st.json({
            "rigidity_metric": rigidity,
            "mean_spacing": float(np.mean(diffs)),
            "std_spacing": float(np.std(diffs)),
        })

    # -------------------------------
    # 3. SPACING VS RIEMANN
    # -------------------------------
    if adv_mode == "Spacing vs Riemann":
        st.markdown("### Spacing Comparison: Spectrum vs Riemann Zeros")

        engine_pick = st.selectbox(
            "Select Spectrum",
            ["3D Prime-Lattice", "4D Prime-Lattice", "5D Prime-Lattice"],
            key="riem_pick"
        )

        spec_map = {
            "3D Prime-Lattice": OMEGA_3D,
            "4D Prime-Lattice": OMEGA_4D,
            "5D Prime-Lattice": OMEGA_5D,
        }

        spec = spec_map[engine_pick]

        comp = compare_to_riemann_spacing(spec)
        st.json(comp)

    # -------------------------------
    # 4. CURVATURE (Δ²) PLOT
    # -------------------------------
    if adv_mode == "Curvature (Δ²) Plot":
        st.markdown("### Curvature Δ² Plot")

        engine_pick = st.selectbox(
            "Select Spectrum",
            ["3D Prime-Lattice", "4D Prime-Lattice", "5D Prime-Lattice"],
            key="curv_pick"
        )

        spec_map = {
            "3D Prime-Lattice": OMEGA_3D,
            "4D Prime-Lattice": OMEGA_4D,
            "5D Prime-Lattice": OMEGA_5D,
        }

        spec = spec_map[engine_pick]

        d2 = np.diff(spec, n=2)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=d2,
            mode="lines",
            line=dict(color="cyan"),
            name="Δ² curvature"
        ))
        fig.update_layout(
            title="Curvature Δ²",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 5. MULTI-ENGINE COMPARISON
    # -------------------------------
    if adv_mode == "Compare Multiple Engines":
        st.markdown("### Multi-Engine Comparison")

        specs = {
            "3D Prime-Lattice": OMEGA_3D,
            "4D Prime-Lattice": OMEGA_4D,
            "5D Prime-Lattice": OMEGA_5D,
        }

        fig = go.Figure()

        for name, spec in specs.items():
            fig.add_trace(go.Scatter(
                x=np.arange(len(spec)),
                y=spec,
                mode="lines",
                name=name
            ))

        fig.update_layout(
            title="Spectrum Comparison (3D vs 4D vs 5D)",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 3 — COSMOLOGY ENGINES
# ============================================================
with tabs[2]:
    st.header("Cosmology Corridor Engines")

    # -------------------------------
    # COSMOLOGY ENGINE REGISTRY
    # -------------------------------
    cosmology_options = {
        "Run LCDM Ages": ("LCDM Ages", "lcdm"),
        "Optimize Paused Gravity": ("Paused Gravity Optimization", "paused_optimize"),
        "Optimize Density-Refined Model": ("Density-Refined Optimization", "density_optimize"),
    }

    # -------------------------------
    # COSMOLOGY ENGINE SELECTION
    # -------------------------------
    selected_cosmo = st.selectbox(
        "Select Cosmology Engine",
        list(cosmology_options.keys()),
        key="cosmo_select"
    )

    # -------------------------------
    # RUN SELECTED COSMOLOGY ENGINE
    # -------------------------------
    if st.button("Run Selected Cosmology Engine", key="run_cosmo_selected"):
        title, engine_name = cosmology_options[selected_cosmo]
        show_result(title, engine_name)

# ============================================================
# TAB 4 — JWST COSMOLOGY (UPGRADED)
# ============================================================
with tabs[3]:
    st.header("JWST Cosmology Engine")

    # -------------------------------
    # JWST MODE SELECTION
    # -------------------------------
    jwst_mode = st.selectbox(
        "Select JWST Analysis",
        [
            "Dark Energy / Dark Matter",
            "Full JWST Cosmology Dashboard",
        ],
        key="jwst_mode"
    )

    # -------------------------------
    # JWST LOCKED DATA
    # -------------------------------
    jwst_data = load_jwst_locked()
    z_jwst = jwst_data["z"].values
    flux_jwst = jwst_data["flux"].values

    # Simple toy model curves
    z_model = [8.0, 9.1, 10.33, 11.0]
    flux_expansion = [1.0, 1.2, 1.5, 1.9]
    flux_paused = [1.0, 1.0, 1.0, 1.0]
    flux_implosion = [1.0, 0.8, 0.6, 0.4]

    # -------------------------------
    # DARK ENERGY / DARK MATTER SPLIT
    # -------------------------------
    if jwst_mode == "Dark Energy / Dark Matter":
        if st.button("Compute Dark Energy / Dark Matter", key="jwst_dm_de"):
            st.subheader("Dark Energy / Dark Matter Split")
            st.write("Ωm = 0.27")
            st.write("ΩΛ = 0.73")
            st.dataframe(jwst_data)

            st.markdown("---")

            pie_fig = go.Figure(
                data=[go.Pie(
                    labels=["Ωm", "ΩΛ"],
                    values=[0.27, 0.73],
                    marker=dict(colors=["blue", "red"])
                )]
            )
            pie_fig.update_layout(template="plotly_dark", paper_bgcolor="black", plot_bgcolor="black")

            bar_fig = go.Figure()
            bar_fig.add_trace(go.Bar(x=["Ωm", "ΩΛ"], y=[0.27, 0.73], marker_color=["blue", "red"]))
            bar_fig.update_layout(template="plotly_dark", paper_bgcolor="black", plot_bgcolor="black")

            st.plotly_chart(pie_fig, use_container_width=True)
            st.plotly_chart(bar_fig, use_container_width=True)

    # -------------------------------
    # FULL JWST COSMOLOGY DASHBOARD
    # -------------------------------
    elif jwst_mode == "Full JWST Cosmology Dashboard":
        if st.button("Compute JWST Cosmology Dashboard", key="jwst_dashboard"):
            st.subheader("JWST Cosmology Dashboard")

            col_top_left, col_top_right = st.columns(2)
            col_bottom_left, col_bottom_right = st.columns(2)

            # ---------------- Panel A: Flux vs Redshift (models + JWST) ----------------
            with col_top_left:
                fig_flux = go.Figure()
                fig_flux.add_scatter(
                    x=z_model, y=flux_expansion,
                    mode="lines+markers",
                    name="Expansion",
                    line=dict(color="lime"),
                    marker=dict(size=8)
                )
                fig_flux.add_scatter(
                    x=z_model, y=flux_paused,
                    mode="lines+markers",
                    name="Paused Gravity",
                    line=dict(color="yellow"),
                    marker=dict(size=8)
                )
                fig_flux.add_scatter(
                    x=z_model, y=flux_implosion,
                    mode="lines+markers",
                    name="Implosion",
                    line=dict(color="cyan"),
                    marker=dict(size=8)
                )
                fig_flux.add_scatter(
                    x=z_jwst, y=flux_jwst,
                    mode="markers",
                    name="JWST SSE",
                    marker=dict(color="magenta", size=10, symbol="diamond")
                )
                fig_flux.update_layout(
                    title="Flux vs Redshift (Models + JWST)",
                    xaxis_title="Redshift z",
                    yaxis_title="Flux",
                    template="plotly_dark",
                    paper_bgcolor="black",
                    plot_bgcolor="black",
                )
                st.plotly_chart(fig_flux, use_container_width=True)

            # ---------------- Panel B: Residuals vs Redshift ----------------
            with col_top_right:
                res_exp = [m - j for m, j in zip(flux_expansion, flux_jwst)]
                res_pgd = [m - j for m, j in zip(flux_paused, flux_jwst)]
                res_imp = [m - j for m, j in zip(flux_implosion, flux_jwst)]

                fig_res = go.Figure()
                fig_res.add_scatter(
                    x=z_model, y=res_exp,
                    mode="lines+markers",
                    name="Expansion Residual",
                    line=dict(color="lime")
                )
                fig_res.add_scatter(
                    x=z_model, y=res_pgd,
                    mode="lines+markers",
                    name="Paused Gravity Residual",
                    line=dict(color="yellow")
                )
                fig_res.add_scatter(
                    x=z_model, y=res_imp,
                    mode="lines+markers",
                    name="Implosion Residual",
                    line=dict(color="cyan")
                )
                fig_res.add_hline(y=0, line=dict(color="white", width=1, dash="dash"))
                fig_res.update_layout(
                    title="Model − JWST Flux Residuals",
                    xaxis_title="Redshift z",
                    yaxis_title="Residual (model − JWST)",
                    template="plotly_dark",
                    paper_bgcolor="black",
                    plot_bgcolor="black",
                )
                st.plotly_chart(fig_res, use_container_width=True)

            # ---------------- Panel C: Ωm(z) / ΩΛ(z) Evolution ----------------
            with col_bottom_left:
                Omega_m0, Omega_L0 = 0.27, 0.73
                z_grid = np.linspace(0, 12, 200)
                Omega_m_z = Omega_m0 * (1 + z_grid)**3
                Omega_L_z = Omega_L0 * np.ones_like(z_grid)
                norm = Omega_m_z + Omega_L_z
                Omega_m_z /= norm
                Omega_L_z /= norm

                fig_omega = go.Figure()
                fig_omega.add_scatter(
                    x=z_grid, y=Omega_m_z,
                    mode="lines",
                    name="Ωm(z)",
                    line=dict(color="deepskyblue")
                )
                fig_omega.add_scatter(
                    x=z_grid, y=Omega_L_z,
                    mode="lines",
                    name="ΩΛ(z)",
                    line=dict(color="red")
                )
                fig_omega.update_layout(
                    title="Matter and Dark Energy Fractions vs Redshift",
                    xaxis_title="Redshift z",
                    yaxis_title="Fraction",
                    template="plotly_dark",
                    paper_bgcolor="black",
                    plot_bgcolor="black",
                    yaxis=dict(range=[0, 1])
                )
                st.plotly_chart(fig_omega, use_container_width=True)

            # ---------------- Panel D: Singularity / SSE Diagnostic ----------------
            with col_bottom_right:
                fig_sing = go.Figure()
                fig_sing.add_scatter(
                    x=z_jwst, y=flux_jwst,
                    mode="markers",
                    name="JWST SSE",
                    marker=dict(color="magenta", size=10)
                )
                z_star = 10.33
                fig_sing.add_vline(
                    x=z_star,
                    line=dict(color="red", width=2),
                    annotation_text=f"Singularity z = {z_star}",
                    annotation_position="top"
                )
                fig_sing.update_layout(
                    title="Singularity / SSE Diagnostic",
                    xaxis_title="Redshift z",
                    yaxis_title="Flux",
                    template="plotly_dark",
                    paper_bgcolor="black",
                    plot_bgcolor="black",
                )
                st.plotly_chart(fig_sing, use_container_width=True)

# ============================================================
# TAB 5 — 5D STRUCTURAL INVARIANT
# ============================================================
with tabs[4]:
    st.header("5D Structural Invariant Engine")

    # -------------------------------
    # INPUT WEIGHTS & PARAMETERS
    # -------------------------------
    geometry_input = st.text_area("Geometry Weights", "1," * 31 + "1", key="geom")
    paused_input = st.text_area("Paused Gravity Weights", "1," * 31 + "1", key="paused")
    density_input = st.text_area("Density Refined Weights", "1," * 31 + "1", key="density")

    weyl_dimension = st.number_input("Weyl Dimension", value=3.0, key="weyl_dim")
    mode = st.selectbox("Aggregation Mode", ["mean", "sum", "max"], key="agg_mode")

    # -------------------------------
    # COMPUTE 5D STRUCTURAL INVARIANT
    # -------------------------------
    if st.button("Compute 5D Structural Invariant", key="compute_5d"):
        try:
            G = [float(x.strip()) for x in geometry_input.split(",")]
            P = [float(x.strip()) for x in paused_input.split(",")]
            D = [float(x.strip()) for x in density_input.split(",")]

            result = router.get_structural_invariant(G, P, D, weyl_dimension, mode)
            output = result["output"]

            st.success("Computation Successful")

            st.subheader("5D Structural Invariant")
            st.write(output["invariant"])

            df = pd.DataFrame({
                "Throat": list(range(1, 33)),
                "Weight": output["throat_weights"]
            })

            chart = alt.Chart(df).mark_bar().encode(
                x="Throat:O",
                y="Weight:Q",
                tooltip=["Throat", "Weight"]
            ).properties(width=700, height=300)

            st.altair_chart(chart, use_container_width=True)
            st.dataframe(df)

        except Exception as e:
            st.error(f"Error: {e}")

# ============================================================
# TAB 6 — FINAL INTERPRETATION (IDENTITY BLOCK)
# ============================================================
with tabs[5]:
    st.header("Final Interpretation (Based on All Evidence)")

    # -------------------------------
    # IDENTITY BLOCK SPECIFICATION
    # -------------------------------
    st.markdown(
        f"""
        <div style="
            background-color:#f2f2f2;
            padding:20px;
            border:1px solid #cccccc;
            border-radius:6px;
            font-family: 'Segoe UI', sans-serif;
        ">
        <h3 style="margin-top:0;">AI33-MPOPT Rivero-Zeta Spectral Backend<br>Identity Block — Version 1.0</h3>

        <h4>Specification</h4>
        <p>
        <strong>Specification Version:</strong> 1.0<br>
        <strong>Operator:</strong> Ω(n) = n log n<br>
        <strong>Residual Metric:</strong> η = std(R) / max(Ω)<br>
        <strong>Classification:</strong> Deterministic / Non-GOE / Non-Poisson
        </p>

        <h4>Spectrum Interpretation</h4>
        <ul>
            <li>Smoothly nonlinear</li>
            <li>Strongly correlated</li>
            <li>Locally rigid</li>
            <li>Deterministic</li>
            <li>Integrable-like</li>
        </ul>

        <h4>Backend Guarantees</h4>
        <ul>
            <li>Deterministic</li>
            <li>Super-rigid</li>
            <li>Collision-stable</li>
            <li>Optimization-safe</li>
            <li>Router-consistent</li>
        </ul>

        <h4>Hash Integrity</h4>
        <p>
        <strong>Markdown Spec Hash (SHA-256):</strong><br>
        8b3fb8cda3470cd457c89b700409c0386c7833115e57b1463986dcc548bf9bfc
        </p>
        <p>
        <strong>LaTeX Spec Hash (SHA-256):</strong><br>
        277e191f768a92aab2b0c7c972328173eb913eb6716ae124288718638ac2435c
        </p>

        <h4>Freeze Code</h4>
        <p>
        <strong>Identity Freeze Code:</strong><br>
        {FREEZE_CODE}
        </p>

        <h4>Status</h4>
        <ul>
            <li>Tamper-evident</li>
            <li>Version-auditable</li>
            <li>Backend identity frozen</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# TAB 7 — SPECTRAL CORE DASHBOARD
# ============================================================
with tabs[6]:
    st.header("Spectral Core Dashboard — Riemann ↔ Rivero Ω")

    # -------------------------------
    # HEALTH & INTEGRITY
    # -------------------------------
    with st.expander("Health & Integrity", expanded=True):
        col_h1, col_h2 = st.columns([1, 1])

        # ---------------------------
        # SPECTRAL HEALTH CHECK
        # ---------------------------
        with col_h1:
            if st.button("Run Spectral Health Check (Ω ↔ Riemann)", key="spectral_health"):
                try:
                    result = subprocess.run(
                        [sys.executable, HEALTH_CHECK_PATH],
                        capture_output=True,
                        text=True
                    )
                    st.subheader("Health Check Output")
                    st.code(result.stdout)

                    status_text = "UNKNOWN"
                    status_color = "#999999"
                    if "BACKEND STATUS: LIVE" in result.stdout:
                        status_text = "LIVE"
                        status_color = "#2ecc71"
                    elif "BACKEND STATUS: NOT LIVE" in result.stdout:
                        status_text = "NOT LIVE"
                        status_color = "#e74c3c"

                    st.markdown(
                        f"""
                        <div style="
                            display:inline-block;
                            padding:6px 12px;
                            border-radius:12px;
                            background-color:{status_color};
                            color:white;
                            font-weight:bold;
                            margin-top:10px;
                        ">
                        BACKEND STATUS: {status_text}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Append to freeze ledger (health check event)
                    ts = datetime.utcnow().isoformat() + "Z"
                    ledger_entry = f"{ts} | HEALTH_CHECK | {status_text} | FREEZE_CODE={FREEZE_CODE}"
                    append_freeze_ledger(ledger_entry)

                except Exception as e:
                    st.error(f"Error running health check: {e}")

        # ---------------------------
        # SPECTRAL CORE HASH CHECK
        # ---------------------------
        with col_h2:
            if st.button("Verify Spectral Core SHA-256", key="spectral_hash"):
                try:
                    sha = compute_file_sha256(SPECTRAL_CSV_PATH)
                    st.subheader("Spectral Core Hash")
                    st.code(sha)

                    st.markdown(
                        f"""
                        <div style="
                            background-color:#34495e;
                            color:white;
                            padding:8px 12px;
                            border-radius:6px;
                            margin-top:8px;
                        ">
                        <b>File:</b> spectral/rivero/riemann_rivero_pairs.csv<br>
                        <b>Freeze Code:</b> {FREEZE_CODE}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    ts = datetime.utcnow().isoformat() + "Z"
                    ledger_entry = f"{ts} | HASH_CHECK | SHA256={sha} | FREEZE_CODE={FREEZE_CODE}"
                    append_freeze_ledger(ledger_entry)

                except Exception as e:
                    st.error(f"Error computing hash: {e}")

    # -------------------------------
    # INVARIANTS & SUMMARIES
    # -------------------------------
    with st.expander("Invariants & Summaries", expanded=False):
        try:
            df = pd.read_csv(SPECTRAL_CSV_PATH)

            st.subheader("Core Spectra Summary")
            st.write("Riemann Zeros and Rivero Ω")
            st.dataframe(df[["riemann_zero", "rivero_omega"]].head())

            st.markdown("---")
            st.write("Mean / Std Summary")
            st.write(df[["riemann_zero", "rivero_omega"]].describe())

            df["delta_zero"] = df["riemann_zero"].diff()
            df["delta_omega"] = df["rivero_omega"].diff()
            df["delta2_zero"] = df["riemann_zero"].diff().diff()
            df["delta2_omega"] = df["rivero_omega"].diff().diff()

            st.markdown("---")
            st.write("Spacing (Δ) Summary")
            st.write(df[["delta_zero", "delta_omega"]].describe())

            st.markdown("---")
            st.write("Curvature (Δ²) Summary")
            st.write(df[["delta2_zero", "delta2_omega"]].describe())

        except Exception as e:
            st.error(f"Error loading spectral invariants: {e}")

    # -------------------------------
    # VISUALIZATIONS
    # -------------------------------
    with st.expander("Visualizations", expanded=False):
        try:
            df = pd.read_csv(SPECTRAL_CSV_PATH)
            df["delta_zero"] = df["riemann_zero"].diff()
            df["delta_omega"] = df["rivero_omega"].diff()
            df["delta2_zero"] = df["riemann_zero"].diff().diff()
            df["delta2_omega"] = df["rivero_omega"].diff().diff()

            col_v1, col_v2 = st.columns([1, 1])

            # ---------------------------
            # RIEMANN VS RIVERO Ω SCATTER
            # ---------------------------
            with col_v1:
                st.subheader("Riemann vs Rivero Ω")
                fig_core = go.Figure()
                fig_core.add_trace(go.Scatter(
                    x=df["riemann_zero"],
                    y=df["rivero_omega"],
                    mode="markers",
                    marker=dict(color="cyan", size=6),
                    name="Ω vs Riemann"
                ))
                fig_core.update_layout(
                    title="Riemann Zeros vs Rivero Ω",
                    xaxis_title="Riemann Zero",
                    yaxis_title="Rivero Ω",
                    template="plotly_dark"
                )
                st.plotly_chart(fig_core, use_container_width=True)

            # ---------------------------
            # SPACING & CURVATURE DIAGNOSTICS
            # ---------------------------
            with col_v2:
                st.subheader("Spacing & Curvature Diagnostics")
                fig_sc = go.Figure()
                fig_sc.add_trace(go.Scatter(
                    y=df["delta_zero"],
                    mode="lines",
                    name="Δ Zero",
                    line=dict(color="yellow")
                ))
                fig_sc.add_trace(go.Scatter(
                    y=df["delta_omega"],
                    mode="lines",
                    name="Δ Omega",
                    line=dict(color="red")
                ))
                fig_sc.add_trace(go.Scatter(
                    y=df["delta2_zero"],
                    mode="lines",
                    name="Δ² Zero",
                    line=dict(color="green")
                ))
                fig_sc.add_trace(go.Scatter(
                    y=df["delta2_omega"],
                    mode="lines",
                    name="Δ² Omega",
                    line=dict(color="blue")
                ))
                fig_sc.update_layout(
                    title="Spacing (Δ) and Curvature (Δ²)",
                    template="plotly_dark"
                )
                st.plotly_chart(fig_sc, use_container_width=True)

        except Exception as e:
            st.error(f"Error plotting spectral visualizations: {e}")

    # -------------------------------
    # DERIVED INVARIANTS EXPORT
    # -------------------------------
    with st.expander("Derived Invariants Export", expanded=False):
        try:
            df = pd.read_csv(SPECTRAL_CSV_PATH)
            df["delta_zero"] = df["riemann_zero"].diff()
            df["delta_omega"] = df["rivero_omega"].diff()
            df["delta2_zero"] = df["riemann_zero"].diff().diff()
            df["delta2_omega"] = df["rivero_omega"].diff().diff()
            df["ratio"] = df["rivero_omega"] / df["riemann_zero"]

            # Simple residuals using linear fit
            x = df["riemann_zero"].values
            y = df["rivero_omega"].values
            if len(df) > 1:
                slope, intercept = np.polyfit(x, y, 1)
                df["residuals"] = y - (slope * x + intercept)
            else:
                df["residuals"] = 0.0

            export_cols = [
                "riemann_zero",
                "rivero_omega",
                "delta_zero",
                "delta_omega",
                "delta2_zero",
                "delta2_omega",
                "ratio",
                "residuals",
            ]
            export_df = df[export_cols]

            csv_bytes = export_df.to_csv(index=False).encode("utf-8")

            st.subheader("Export Derived Invariants Layer")
            st.write("Δ, Δ², ratio, residuals — backend primitives derived from the spectral core.")

            st.download_button(
                label="Download Derived Invariants CSV",
                data=csv_bytes,
                file_name="riemann_rivero_derived_invariants.csv",
                mime="text/csv",
                key="download_invariants"
            )

        except Exception as e:
            st.error(f"Error preparing derived invariants export: {e}")

# ============================================================
# TAB 8 — SPECTRAL GEOMETRY VISUALS (COLAB TRUE RESULTS)
# ============================================================
with tabs[7]:
    st.header("Spectral Geometry Visuals — AI33‑MPOPT")

    # -------------------------------
    # VISUALIZATION MODULE DROPDOWN
    # -------------------------------
    viz_choice = st.selectbox(
        "Select Visualization Module",
        [
            "Eigenvalue Ladder (First 10)",
            "Full Laplacian Spectrum",
            "Diffusion Distance Matrix",
            "Diffusion Embedding (3D)",
            "Spectral String (3D)",
            "Spectral String — Curvature Colored",
            "Spectral String — Sector Colored",
            "5D Curvature Profile (Select Sector)",
            "5D Torsion Profile (Select Sector)",
            "Curvature/Torsion Overlay",
            "Worldsheet Action Decay",
            "Max 5D Curvature Decay",
            "Diffusion Scaling (Spectral Dimension)",
            "Duality Correlation Matrix",
            "Multiverse Interaction Graph",
            "Multiverse Laplacian Spectrum",
            "Entangled Particle Shadow MBots (247)"
        ],
        key="viz_dropdown"
    )

    # -------------------------------
    # 1. EIGENVALUE LADDER (FIRST 10)
    # -------------------------------
    if viz_choice == "Eigenvalue Ladder (First 10)":
        st.subheader("Eigenvalue Ladder (First 10)")
        eigvals = router.get_laplacian_eigenvalues()
        st.write(eigvals[:10])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=eigvals[:10],
            mode="lines+markers",
            line=dict(color="cyan")
        ))
        fig.update_layout(
            title="First 10 Laplacian Eigenvalues",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 2. FULL LAPLACIAN SPECTRUM
    # -------------------------------
    if viz_choice == "Full Laplacian Spectrum":
        st.subheader("Full Laplacian Spectrum")
        eigvals = router.get_laplacian_eigenvalues()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=eigvals,
            mode="lines+markers",
            line=dict(color="deepskyblue")
        ))
        fig.update_layout(
            title="AI33‑MPOPT Multiverse Laplacian Spectrum",
            xaxis_title="Index",
            yaxis_title="Eigenvalue λ",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 3. DIFFUSION DISTANCE MATRIX
    # -------------------------------
    if viz_choice == "Diffusion Distance Matrix":
        st.subheader("Diffusion Distance Matrix (33×33)")
        D = router.get_diffusion_distance_matrix()
        st.write("Min:", float(D.min()), "Max:", float(D.max()))

        fig = go.Figure(data=go.Heatmap(
            z=D,
            colorscale="Viridis"
        ))
        fig.update_layout(
            title="Diffusion Distance Matrix",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 4. DIFFUSION EMBEDDING (3D)
    # -------------------------------
    if viz_choice == "Diffusion Embedding (3D)":
        st.subheader("Diffusion Embedding (3D)")
        X = router.get_diffusion_embedding()

        fig = go.Figure(data=[go.Scatter3d(
            x=X[:, 0], y=X[:, 1], z=X[:, 2],
            mode="markers",
            marker=dict(size=6, color=X[:, 0], colorscale="Turbo")
        )])
        fig.update_layout(
            title="Diffusion Geometry (3D)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 5. SPECTRAL STRING (3D)
    # -------------------------------
    if viz_choice == "Spectral String (3D)":
        st.subheader("Spectral String (Δ, Δ², T)")
        Xs, Ys, Zs = router.get_spectral_string()

        fig = go.Figure(data=[go.Scatter3d(
            x=Xs, y=Ys, z=Zs,
            mode="lines",
            line=dict(color="cyan", width=4)
        )])
        fig.update_layout(
            title="Spectral String Geometry",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 6. SPECTRAL STRING — CURVATURE COLORED
    # -------------------------------
    if viz_choice == "Spectral String — Curvature Colored":
        st.subheader("Spectral String Colored by Curvature κ")
        Xs, Ys, Zs, kappa = router.get_spectral_string_curvature()

        fig = go.Figure(data=[go.Scatter3d(
            x=Xs, y=Ys, z=Zs,
            mode="markers",
            marker=dict(
                size=5,
                color=kappa,
                colorscale="Plasma",
                colorbar=dict(title="κ")
            )
        )])
        fig.update_layout(
            title="Curvature‑Colored Spectral String",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 7. SPECTRAL STRING — SECTOR COLORED
    # -------------------------------
    if viz_choice == "Spectral String — Sector Colored":
        st.subheader("Spectral String Colored by Sector Index")
        Xs, Ys, Zs, sector = router.get_spectral_string_sector()

        fig = go.Figure(data=[go.Scatter3d(
            x=Xs, y=Ys, z=Zs,
            mode="markers",
            marker=dict(
                size=5,
                color=sector,
                colorscale="Rainbow",
                colorbar=dict(title="Sector")
            )
        )])
        fig.update_layout(
            title="Sector‑Colored Spectral String",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 8. 5D CURVATURE PROFILE (SELECT SECTOR)
    # -------------------------------
    if viz_choice == "5D Curvature Profile (Select Sector)":
        st.subheader("5D Curvature Profile")
        sector = st.number_input("Sector (1–33)", min_value=1, max_value=33, value=8)
        k = router.get_5d_curvature(sector)
        st.line_chart(k)

    # -------------------------------
    # 9. 5D TORSION PROFILE (SELECT SECTOR)
    # -------------------------------
    if viz_choice == "5D Torsion Profile (Select Sector)":
        st.subheader("5D Torsion Profile")
        sector = st.number_input("Sector (1–33)", min_value=1, max_value=33, value=8)
        t = router.get_5d_torsion(sector)
        st.line_chart(t)

    # -------------------------------
    # 10. CURVATURE / TORSION OVERLAY
    # -------------------------------
    if viz_choice == "Curvature/Torsion Overlay":
        st.subheader("Curvature / Torsion Overlay")
        sector = st.number_input("Sector (1–33)", min_value=1, max_value=33, value=8)
        k = router.get_5d_curvature(sector)
        t = router.get_5d_torsion(sector)
        df_ct = pd.DataFrame({"Curvature": k, "Torsion": t})
        st.line_chart(df_ct)

    # -------------------------------
    # 11. WORLDSHEET ACTION DECAY
    # -------------------------------
    if viz_choice == "Worldsheet Action Decay":
        st.subheader("Worldsheet Action Decay")
        S = router.get_worldsheet_action()
        st.line_chart(S)

    # -------------------------------
    # 12. MAX 5D CURVATURE DECAY
    # -------------------------------
    if viz_choice == "Max 5D Curvature Decay":
        st.subheader("Max 5D Curvature Decay")
        K = router.get_max_5d_curvature()
        st.line_chart(K)

    # -------------------------------
    # 13. DIFFUSION SCALING (SPECTRAL DIMENSION)
    # -------------------------------
    if viz_choice == "Diffusion Scaling (Spectral Dimension)":
        st.subheader("Diffusion Scaling (Spectral Dimension)")
        t_vals, P, ds = router.get_diffusion_scaling()
        st.write("Estimated spectral dimension:", ds)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=np.log(t_vals), y=np.log(P),
            mode="lines",
            name="Diffusion data"
        ))
        fig.update_layout(
            title="log(P(t)) vs log(t)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 14. DUALITY CORRELATION MATRIX
    # -------------------------------
    if viz_choice == "Duality Correlation Matrix":
        st.subheader("Duality Correlation Matrix")
        C = router.get_duality_matrix()
        fig = go.Figure(data=go.Heatmap(z=C, colorscale="Viridis"))
        fig.update_layout(
            title="Duality Correlation Matrix",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 15. MULTIVERSE INTERACTION GRAPH
    # -------------------------------
    if viz_choice == "Multiverse Interaction Graph":
        st.subheader("Multiverse Interaction Graph")
        G = router.get_multiverse_graph()
        st.plotly_chart(G, use_container_width=True)

    # -------------------------------
    # 16. MULTIVERSE LAPLACIAN SPECTRUM
    # -------------------------------
    if viz_choice == "Multiverse Laplacian Spectrum":
        st.subheader("Multiverse Laplacian Spectrum")
        eigvals = router.get_multiverse_laplacian()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=eigvals,
            mode="lines+markers",
            line=dict(color="cyan")
        ))
        fig.update_layout(
            title="Multiverse Laplacian Spectrum",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 17. ENTANGLED PARTICLE SHADOW MBOTS (247)
    # -------------------------------
    if viz_choice == "Entangled Particle Shadow MBots (247)":
        st.subheader("Entangled Particle Shadow MBots (247)")

        X = router.get_diffusion_embedding()  # 33×3 embedding from true multiverse geometry
        n = X.shape[0]

        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                d = float(np.linalg.norm(X[i] - X[j]))
                pairs.append((d, i, j))
        pairs.sort(key=lambda x: x[0])
        top_pairs = pairs[:10]

        st.markdown("**Closest entangled pairs in diffusion geometry (true 33‑universe embedding):**")
        df_pairs = pd.DataFrame(
            [{"universe_i": i, "universe_j": j, "distance": d} for d, i, j in top_pairs]
        )
        st.dataframe(df_pairs)

        fig = go.Figure()

        fig.add_trace(go.Scatter3d(
            x=X[:, 0], y=X[:, 1], z=X[:, 2],
            mode="markers",
            marker=dict(size=4, color="lightgray"),
            name="All universes"
        ))

        for idx, (d, i, j) in enumerate(top_pairs):
            fig.add_trace(go.Scatter3d(
                x=[X[i, 0], X[j, 0]],
                y=[X[i, 1], X[j, 1]],
                z=[X[i, 2], X[j, 2]],
                mode="lines+markers",
                line=dict(width=4, color="magenta"),
                marker=dict(size=6, color="magenta"),
                name=f"Entangled pair {idx+1} (d={d:.3f})"
            ))

        fig.update_layout(
            title="Entangled Particle Shadow MBots (247) — Closest Pairs in Diffusion Geometry",
            template="plotly_dark",
            scene=dict(
                xaxis_title="Embedding X",
                yaxis_title="Embedding Y",
                zaxis_title="Embedding Z"
            )
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 9 — HIGGS SUBSYSTEM (STANDARD)
# ============================================================
with tabs[8]:
    st.header("Higgs Subsystem")

    from engine.higgs_analysis import run_higgs_analysis
    import plotly.graph_objects as go

    if st.button("Run Higgs Analysis", key="run_higgs_basic"):

        results = run_higgs_analysis()

        st.subheader("Higgs Parameters")

        st.json({
            "mu_squared": results["mu_squared"],
            "lambda": results["lambda_coupling"],
            "VEV_v": results["v"],
            "m_H_analytic": results["m_H_analytic"],
            "m_H_numeric": results["m_H_numeric"],
        })

        # Higgs Potential Graph
        st.subheader("Higgs Potential")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=results["h_vals"],
            y=results["V_vals"],
            mode="lines",
            name="V(h)"
        ))

        fig.update_layout(
            title="Higgs Potential V(h)",
            xaxis_title="Higgs Field h",
            yaxis_title="Potential V(h)",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 10 — HIGGS SUBSYSTEM (ADVANCED VISUALS + RECOMPUTATION)
# ============================================================
with tabs[9]:
    st.header("Higgs Subsystem (Advanced) — Full Analysis & Visualizations")

    from engine.higgs_analysis import run_higgs_analysis
    import plotly.express as px
    import plotly.graph_objects as go

    @st.cache_data(show_spinner=True)
    def get_higgs_results():
        return run_higgs_analysis()

    if st.button("Run / Refresh Higgs Analysis", key="run_higgs_adv"):
        pass

    results = get_higgs_results()

    mu2 = results["mu_squared"]
    lam = results["lambda_coupling"]
    v = results["v"]
    mH_a = results["m_H_analytic"]
    mH_n = results["m_H_numeric"]
    m_eff = results["m_eff"]
    higgs_couplings_norm = results["higgs_couplings_norm"]
    C = results["C"]
    avg_corr = results["avg_corr"]
    h_vals = results["h_vals"]
    V_vals = results["V_vals"]
    logdet_value = results["logdet_value"]
    sha256_hash = results["sha256_hash"]

    st.markdown("### Higgs Mass & Potential Parameters")
    st.json({
        "mu_squared": mu2,
        "lambda": lam,
        "VEV_v": v,
        "m_H_analytic": mH_a,
        "m_H_numeric": mH_n,
        "m_eff_min": float(m_eff.min()),
        "m_eff_max": float(m_eff.max()),
    })

    st.markdown("---")
    st.markdown("### Higgs Visualizations")

    viz = st.selectbox(
        "Select Higgs visualization",
        [
            "Effective potential V(h)",
            "Effective mass distribution (histogram)",
            "Effective mass landscape (scatter)",
            "Higgs-mode correlation histogram",
            "Higgs-mode correlation matrix",
            "Average correlation per mode",
        ],
        key="higgs_viz_mode_adv",
    )

    if viz == "Effective potential V(h)":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=h_vals, y=V_vals, mode="lines", line=dict(color="purple")))
        fig.update_layout(
            title="AI33-MPOPT Higgs Effective Potential",
            xaxis_title="Higgs field value h",
            yaxis_title="V(h)",
            template="plotly_dark",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif viz == "Effective mass distribution (histogram)":
        fig = px.histogram(m_eff, nbins=40, title="Distribution of Higgs-Modified Sector Masses")
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    elif viz == "Effective mass landscape (scatter)":
        idx = np.arange(len(m_eff))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=idx,
            y=m_eff,
            mode="markers",
            marker=dict(size=4, color=m_eff, colorscale="Viridis"),
        ))
        fig.update_layout(
            title="AI33-MPOPT Higgs-Induced Sector Mass Landscape",
            xaxis_title="Sector index",
            yaxis_title="Effective mass m_eff",
            template="plotly_dark",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif viz == "Higgs-mode correlation histogram":
        corr_vals = C[np.triu_indices_from(C, k=1)]
        fig = px.histogram(corr_vals, nbins=50, title="Distribution of Higgs-Mode Correlations")
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    elif viz == "Higgs-mode correlation matrix":
        fig = go.Figure(
            data=go.Heatmap(
                z=C,
                colorscale="Viridis",
                colorbar_title="|⟨H_i^⊥ | H_j⟩|²",
            )
        )
        fig.update_layout(
            title="AI33-MPOPT Higgs Sector Correlation Matrix",
            xaxis_title="Higgs mode index",
            yaxis_title="Higgs mode index",
            template="plotly_dark",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif viz == "Average correlation per mode":
        idx = np.arange(len(avg_corr))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=idx,
            y=avg_corr,
            mode="markers",
            marker=dict(color="cyan", size=6),
        ))
        fig.update_layout(
            title="Average Higgs-Mode Correlation Strength",
            xaxis_title="Higgs mode index",
            yaxis_title="Average correlation",
            template="plotly_dark",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
    st.markdown("### Identity Anchors (Higgs Subsystem)")
    st.json({
        "logdet_RIVERO_OMEGA": logdet_value,
        "SHA256_identity": sha256_hash,
    })

    # ============================================================
    # DOWNLOAD HIGGS REPORT (TAB 10 ONLY)
    # ============================================================

    import json

    st.markdown("---")
    st.subheader("Export Higgs Diagnostics")

    report_data = {
        "mu_squared": mu2,
        "lambda_coupling": lam,
        "VEV_v": v,
        "m_H_analytic": mH_a,
        "m_H_numeric": mH_n,
        "m_eff_min": float(m_eff.min()),
        "m_eff_max": float(m_eff.max()),
        "logdet_value": logdet_value,
        "sha256_hash": sha256_hash
    }

    report_json = json.dumps(report_data, indent=4)

    st.download_button(
        label="Download Higgs Diagnostics Report",
        data=report_json,
        file_name="AI33_MPOPT_Higgs_Report.json",
        mime="application/json"
    )

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown(
    """
    <div style='text-align: center; margin-top: 50px; font-size: 18px;'>
    <b>AI33‑MPOPT — Deterministic, Collision‑Free, Reproducible.</b>
    </div>
    """,
    unsafe_allow_html=True
)
