import streamlit as st
import time
import math
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="Pomodoro Timer",
    page_icon="🍅",
    layout="centered"
)

# CSS pour le style abysse et animations
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .main-container {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
        padding: 2rem;
        gap: 3rem;
    }
    
    .timer-section {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .controls-section {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        min-width: 150px;
        justify-content: center;
        align-items: center;
        height: 300px;
    }
    
    .timer-circle {
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: #1a1a2e;
        border: 3px solid #2d4a6b;
        position: relative;
        margin: 2rem 0;
        overflow: hidden;
        box-shadow: 
            inset 0 0 50px rgba(0, 100, 200, 0.1),
            0 0 30px rgba(0, 100, 200, 0.3);
    }
    
    .water-fill {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(
            0deg,
            #003366 0%,
            #004d99 30%,
            #0066cc 60%,
            #3399ff 100%
        );
        transition: height 1s ease-in-out;
        animation: wave 3s ease-in-out infinite;
    }
    
    @keyframes wave {
        0%, 100% {
            transform: translateY(0px);
            filter: hue-rotate(0deg);
        }
        50% {
            transform: translateY(-10px);
            filter: hue-rotate(20deg);
        }
    }
    
    .time-display {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        z-index: 10;
    }
    
    .control-buttons {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2d4a6b, #1a365d);
        color: white;
        border: 2px solid #4a90e2;
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4a90e2, #2d4a6b);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.5);
    }
    
    .phase-indicator {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        text-align: center;
        color: #4a90e2;
        text-shadow: 0 0 10px rgba(74, 144, 226, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if 'timer_state' not in st.session_state:
    st.session_state.timer_state = 'stopped'  # 'running', 'paused', 'stopped'
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'remaining_time' not in st.session_state:
    st.session_state.remaining_time = 25 * 60  # 25 minutes par défaut
if 'current_phase' not in st.session_state:
    st.session_state.current_phase = 'work'  # 'work' ou 'break'
if 'work_duration' not in st.session_state:
    st.session_state.work_duration = 25
if 'break_duration' not in st.session_state:
    st.session_state.break_duration = 5

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_progress_percentage():
    if st.session_state.current_phase == 'work':
        total_time = st.session_state.work_duration * 60
    else:
        total_time = st.session_state.break_duration * 60
    
    elapsed = total_time - st.session_state.remaining_time
    return min((elapsed / total_time) * 100, 100)

# Interface principale
st.title("🌊 Pomodoro Timer")

# Calcul du temps restant si le timer est en marche
if st.session_state.timer_state == 'running' and st.session_state.start_time:
    elapsed = time.time() - st.session_state.start_time
    st.session_state.remaining_time = max(0, st.session_state.remaining_time - elapsed)
    st.session_state.start_time = time.time()
    
    # Vérifier si le timer est fini
    if st.session_state.remaining_time <= 0:
        # Changer de phase
        if st.session_state.current_phase == 'work':
            st.session_state.current_phase = 'break'
            st.session_state.remaining_time = st.session_state.break_duration * 60
        else:
            st.session_state.current_phase = 'work'
            st.session_state.remaining_time = st.session_state.work_duration * 60
        
        st.session_state.timer_state = 'stopped'
        st.balloons()

# Affichage de la phase actuelle
phase_text = "🎯 Concentration" if st.session_state.current_phase == 'work' else "☕ Pause"
st.markdown(f'<div class="phase-indicator">{phase_text}</div>', unsafe_allow_html=True)

# Interface avec timer et contrôles côte à côte
col1, col2 = st.columns([2, 1])

with col1:
    # Cercle de progression
    progress = get_progress_percentage()
    
    st.markdown(f"""
    <div class="timer-section">
        <div class="timer-circle">
            <div class="water-fill" style="height: {progress}%;"></div>
            <div class="time-display">{format_time(st.session_state.remaining_time)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Espace pour centrer verticalement
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    
    # Bouton principal (Start/Pause/Resume)
    if st.session_state.timer_state == 'stopped':
        if st.button("▶️ Démarrer", key="start_btn", use_container_width=True):
            st.session_state.timer_state = 'running'
            st.session_state.start_time = time.time()
            st.rerun()
    elif st.session_state.timer_state == 'running':
        if st.button("⏸️ Pause", key="pause_btn", use_container_width=True):
            st.session_state.timer_state = 'paused'
            st.rerun()
    else:  # paused
        if st.button("▶️ Reprendre", key="resume_btn", use_container_width=True):
            st.session_state.timer_state = 'running'
            st.session_state.start_time = time.time()
            st.rerun()
    
    # Bouton Reset
    if st.button("🔄 Reset", key="reset_btn", use_container_width=True):
        st.session_state.timer_state = 'stopped'
        st.session_state.start_time = None
        if st.session_state.current_phase == 'work':
            st.session_state.remaining_time = st.session_state.work_duration * 60
        else:
            st.session_state.remaining_time = st.session_state.break_duration * 60
        st.rerun()

# Auto-refresh si le timer est en marche
if st.session_state.timer_state == 'running':
    time.sleep(1)
    st.rerun()