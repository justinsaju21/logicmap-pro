import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from kmap_logic import KMapSolver
from visualizer import KMapVisualizer

# Page Config
st.set_page_config(
    page_title="LogicMap Pro - K-Map Solver",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Theme colors
if st.session_state.theme == 'dark':
    PRIMARY_BG = '#0E1117'
    SECONDARY_BG = '#1a1a2e'
    TEXT_COLOR = '#E0FFFF'
    ACCENT_1 = '#FFD700'
    ACCENT_2 = '#FF69B4'
    ACCENT_3 = '#00FFFF'
    CARD_BG = '#16213e'
    PLOT_BG = 'black'
    GRID_COLOR = 'white'
    LABEL_COLOR = '#FFFF00'
else:
    PRIMARY_BG = '#FFFFFF'
    SECONDARY_BG = '#F0F2F6'
    TEXT_COLOR = '#1F1F1F'
    ACCENT_1 = '#FF6B35'
    ACCENT_2 = '#004E89'
    ACCENT_3 = '#1A659E'
    CARD_BG = '#E8EAF6'
    PLOT_BG = 'white'
    GRID_COLOR = 'black'
    LABEL_COLOR = '#004E89'

# Custom CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, {PRIMARY_BG} 0%, {SECONDARY_BG} 100%);
        color: {TEXT_COLOR};
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3 {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }}
    
    .main-title {{
        background: linear-gradient(45deg, {ACCENT_1}, {ACCENT_2}, {ACCENT_3});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8em;
        text-align: center;
        margin-bottom: 0.2em;
        animation: fadeInDown 1s ease-in;
    }}
    
    .subtitle {{
        text-align: center;
        color: {TEXT_COLOR};
        opacity: 0.8;
        font-size: 1.2em;
        margin-bottom: 2em;
        animation: fadeIn 1.5s ease-in;
    }}
    
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    .feature-card {{
        background: {CARD_BG};
        border-radius: 15px;
        padding: 2em;
        margin: 1em 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: slideInRight 0.8s ease-in;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    }}
    
    .stButton>button {{
        background: linear-gradient(45deg, {ACCENT_1}, {ACCENT_2});
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-size: 1.1em;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }}
    
    .theme-toggle {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        background: {CARD_BG};
        border-radius: 50px;
        padding: 10px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.05);
    }}
    
    .status-message {{
        background: {CARD_BG};
        border-left: 4px solid {ACCENT_1};
        padding: 1em;
        border-radius: 8px;
        margin: 0.5em 0;
        animation: slideInRight 0.5s ease;
    }}
    
    .scrollable-container {{
        max-height: 58vh;
        overflow-y: auto;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .dataframe {{
        font-family: 'Courier New', monospace;
        border-radius: 10px;
        overflow: hidden;
    }}
    
    .hero-section {{
        text-align: center;
        padding: 3em 2em;
        animation: fadeIn 1s ease-in;
    }}
    
    .cta-button {{
        display: inline-block;
        background: linear-gradient(45deg, {ACCENT_1}, {ACCENT_3});
        color: white;
        padding: 1em 3em;
        border-radius: 30px;
        font-size: 1.2em;
        font-weight: 600;
        text-decoration: none;
        margin: 2em 0;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }}
    
    .cta-button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }}
    
    /* Responsive K-Map Scaling & Centering */
    div[data-testid="stImage"] {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }}
    
    div[data-testid="stImage"] > img {{
        max-height: 58vh !important;
        width: auto !important;
        max-width: 100% !important;
        object-fit: contain !important;
    }}
    
    /* Reduce top padding of the main container */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
    }}
    
    /* Center Equation */
    .equation-text {{
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: {ACCENT_3};
    }}

    /* Mobile Responsiveness */
    @media (max-width: 768px) {{
        .main-title {{
            font-size: 2em !important;
        }}
        
        div[data-testid="stImage"] > img {{
            max-height: 50vh !important;
        }}
        
        .feature-card {{
            padding: 1em !important;
        }}
        
        .scrollable-container {{
            max-height: 300px !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar Footer (Theme & Navigation)
def render_sidebar_footer(show_back=False):
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        # Theme Toggle
        theme_icon = "🌙" if st.session_state.theme == 'dark' else "☀️"
        if st.button(f"{theme_icon} Toggle Theme", key="theme_toggle_footer"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
            
        # Back Button (if requested)
        if show_back:
            st.markdown("---")
            if st.button("⬅️ Back to Home", key="back_home_footer"):
                st.session_state.page = 'home'
                st.rerun()

# Homepage
def show_homepage():
    # Logo
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("C:/Users/justi/.gemini/antigravity/brain/a9aa5f87-8f95-4f13-aba9-b808c2d661c9/logic_map_pro_logo_1764410271837.png", use_container_width=True)
    
    st.markdown('<h1 class="main-title">LogicMap Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Professional Karnaugh Map Solver & Visualizer</p>', unsafe_allow_html=True)
    
    # Hero Section
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown("""
        <div class="hero-section">
            <h2>🔬 Simplify Digital Logic Like Never Before</h2>
            <p style="font-size: 1.1em; margin: 1.5em 0;">
                Experience the most intuitive and powerful K-Map solver designed for students,
                educators, and engineers. Watch your Boolean expressions simplify in real-time
                with stunning visualizations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Centered Button using columns
        # Using [1, 2, 1] ratio to give the button column more width relative to spacers
        c1, c2, c3 = st.columns([1, 2, 1]) 
        with c2:
            # Use a container to help with centering if needed, but the column ratio should do it
            if st.button("🚀 Launch Solver", key="launch_main", use_container_width=True):
                st.session_state.page = 'solver'
                st.rerun()
    
    # Features
    st.markdown("## ✨ Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Smart Grouping</h3>
            <p>Automatically finds optimal prime implicants using the Quine-McCluskey algorithm.
            Groups are ordered by size (8→4→2) for educational clarity.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎬 Live Animation</h3>
            <p>Step-by-step visualization shows exactly how groups are formed, making
            complex concepts easy to understand.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Complete Analysis</h3>
            <p>View truth tables, simplified equations, and visual groupings all in one
            professional interface.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Info
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎓 Perfect For
        - Students learning digital logic
        - Professors teaching circuit design
        - Engineers verifying simplifications
        - Anyone working with Boolean algebra
        """)
    
    with col2:
        st.markdown("""
        ### 🛠️ Capabilities
        - 2, 3, and 4-variable K-Maps
        - Sum of Products (SOP) mode
        - Product of Sums (POS) mode
        - Don't Care term optimization
        - Gray code compliance
        """)
        
    # Render Footer
    render_sidebar_footer(show_back=False)

# Solver Page
def show_solver():
    # Logo (Smaller)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image("C:/Users/justi/.gemini/antigravity/brain/a9aa5f87-8f95-4f13-aba9-b808c2d661c9/logic_map_pro_logo_1764410271837.png", width=100)
        
    st.markdown('<h1 class="main-title">LogicMap Pro Solver</h1>', unsafe_allow_html=True)
    
    st.sidebar.title("🎛️ Configuration")
    
    num_vars = st.sidebar.radio("Number of Variables", [2, 3, 4], index=2)
    mode = st.sidebar.radio("Mode", ["SOP (Sum of Products)", "POS (Product of Sums)"], index=0)
    mode_short = "SOP" if "SOP" in mode else "POS"
    
    # Speed Control
    st.sidebar.markdown("### ⏱️ Animation Speed")
    speed_mode = st.sidebar.select_slider(
        "Select Speed",
        options=["Educational (Slow)", "Fast", "Instant"],
        value="Educational (Slow)"
    )
    
    # Map speed to delay
    if speed_mode == "Educational (Slow)":
        step_delay = 1.0
        value_delay = 0.3
        phase_delay = 2.0
    elif speed_mode == "Fast":
        step_delay = 0.3
        value_delay = 0.05
        phase_delay = 0.5
    else:
        step_delay = 0
        value_delay = 0
        phase_delay = 0
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Input Terms")
    
    # Helper to parse input
    def parse_input(input_str):
        if not input_str.strip():
            return []
        try:
            return [int(x.strip()) for x in input_str.split(',') if x.strip().isdigit()]
        except:
            return []
    
    minterm_label = "Minterms (1s)" if mode_short == "SOP" else "Maxterms (0s)"
    minterms_input = st.sidebar.text_input(f"Enter {minterm_label}", "0, 1, 5, 7, 8, 9, 13, 15", 
                                           help="Comma-separated numbers")
    dont_cares_input = st.sidebar.text_input("Don't Cares (Optional)", "3, 11",
                                             help="Terms that can be either 0 or 1")
    
    minterms = parse_input(minterms_input)
    dont_cares = parse_input(dont_cares_input)
    
    # Validation
    max_val = 2**num_vars - 1
    valid_minterms = [m for m in minterms if 0 <= m <= max_val]
    valid_dont_cares = [d for d in dont_cares if 0 <= d <= max_val]
    
    # Check for overlap
    overlap = set(valid_minterms) & set(valid_dont_cares)
    if overlap:
        st.sidebar.error(f"⚠️ Terms {overlap} cannot be both {minterm_label} and Don't Care!")
        st.stop()
    
    # Go Button
    if st.sidebar.button("🚀 SOLVE & ANIMATE"):
        # Solve
        solver = KMapSolver(num_vars, valid_minterms, valid_dont_cares, mode=mode_short)
        truth_table = solver.get_truth_table()
        equation, logic_parts, groups = solver.solve()
        
        visualizer = KMapVisualizer(num_vars, valid_minterms, valid_dont_cares, groups, 
                                     st.session_state.theme)
    
    
        # Layout: K-Map (Left, Large) | Tabs (Right, Info)
        col_kmap, col_info = st.columns([2, 1], gap="medium")
        
        with col_kmap:
            st.subheader("📊 K-Map Visualization")
            # Equation Display
            st.markdown(f'<div class="equation-text">F = {equation}</div>', unsafe_allow_html=True)
            plot_placeholder = st.empty()
            
        with col_info:
            st.subheader("ℹ️ Details")
            tab_steps, tab_table = st.tabs(["📝 Steps", "📋 Truth Table"])
            
            with tab_steps:
                st.markdown("**Solution Log**")
                # Container for logs
                log_placeholder = st.empty()
                # JS Placeholder for auto-scroll
                js_placeholder = st.empty()
                
            with tab_table:
                def highlight_output(val):
                    if val == 1:
                        return 'color: #00FF00; font-weight: bold'
                    elif val == 0:
                        return 'color: #FF5733'
                    elif val == 'X':
                        return 'color: #FF00FF; font-weight: bold'
                    return ''

                st.dataframe(
                    truth_table.style.applymap(highlight_output, subset=['Output']),
                    use_container_width=True,
                    height=500
                )

        # Log State
        logs = []
        
        def add_log(message, icon="ℹ️"):
            # Append to list (Oldest First -> Newest Last)
            logs.append(f'<div class="status-message">{icon} {message}</div>')
            
            # Wrap in scrollable container div with a unique ID for JS targeting
            log_content = "".join(logs)
            log_placeholder.markdown(
                f'<div id="log-container" class="scrollable-container">{log_content}</div>', 
                unsafe_allow_html=True
            )
            
            # Inject JS to scroll to bottom
            js_placeholder.markdown(
                """
                <script>
                    var container = window.parent.document.getElementById("log-container");
                    if (container) {
                        container.scrollTop = container.scrollHeight;
                    }
                </script>
                """,
                unsafe_allow_html=True
            )
        
        # --- Phase 1: Setup & Plotting ---
        if speed_mode != "Instant":
            # 1. Construct Grid
            add_log("<b>Phase 1:</b> Constructing Grid (Gray Code)", "🏗️")
            fig = visualizer.draw(show_grid=True, show_indices=False, visible_values=None, visible_groups=None)
            plot_placeholder.pyplot(fig, use_container_width=True)
            plt.close(fig)
            time.sleep(step_delay)
            
            # 2. Show Indices
            add_log("<b>Phase 1:</b> Marking Cell Indices", "🔢")
            fig = visualizer.draw(show_grid=True, show_indices=True, visible_values=None, visible_groups=None)
            plot_placeholder.pyplot(fig, use_container_width=True)
            plt.close(fig)
            time.sleep(step_delay)
            
            # 3. Plot Terms
            add_log("<b>Phase 1:</b> Plotting Terms (1s, 0s, Xs)", "✍️")
            visible_vals = []
            for i in range(2**num_vars):
                visible_vals.append(i)
                if speed_mode == "Educational (Slow)" or i % 2 == 0 or i == 2**num_vars - 1:
                    fig = visualizer.draw(show_grid=True, show_indices=True, visible_values=visible_vals, visible_groups=None)
                    plot_placeholder.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                    time.sleep(value_delay)
            time.sleep(phase_delay)
        
        # --- Phase 2: Grouping Strategy ---
        add_log("<b>Phase 2:</b> Grouping Strategy (Greedy Search)", "🧠")
        
        if not groups:
            add_log("No Groups Found", "❌")
            time.sleep(step_delay)
        else:
            visible_groups = []
            for i, group in enumerate(groups):
                visible_groups.append(group)
                group_size = len(group)
                
                # Determine group type text
                if group_size == 16: g_type = "16 (All)"
                elif group_size == 8: g_type = "Octet (8)"
                elif group_size == 4: g_type = "Quad (4)"
                elif group_size == 2: g_type = "Pair (2)"
                else: g_type = "Single (1)"
                
                add_log(f"Found <b>{g_type}</b> - Group {i+1}", "🔍")
                
                if speed_mode != "Instant":
                    fig = visualizer.draw(show_grid=True, show_indices=True, visible_values=list(range(2**num_vars)), visible_groups=visible_groups)
                    plot_placeholder.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                    time.sleep(step_delay * 1.5)
            time.sleep(phase_delay)
        
        # --- Phase 3: Extraction (Detailed) ---
        add_log("<b>Phase 3:</b> Term Extraction", "🧪")
        
        colors = ['#FFD700', '#FF69B4', '#00FFFF', '#ADFF2F', '#FF4500', '#9370DB']
        
        if speed_mode != "Instant":
            for i, group in enumerate(groups):
                term = logic_parts[i]
                color = colors[i % len(colors)]
                
                # Highlight specific group
                fig = visualizer.draw(show_grid=True, show_indices=True, visible_values=list(range(2**num_vars)), visible_groups=[group])
                plot_placeholder.pyplot(fig, use_container_width=True)
                plt.close(fig)
                
                add_log(f"Group {i+1} (<span style='color:{color}'>■</span>) covers {list(group)} <br>→ Term: <b>{term}</b>", "📝")
                time.sleep(step_delay * 2)
        
        # Final State
        add_log(f"<b>Final Equation:</b> F = {equation}", "✅")
        fig = visualizer.draw(show_grid=True, show_indices=True, visible_values=list(range(2**num_vars)), visible_groups=groups)
        plot_placeholder.pyplot(fig, use_container_width=True)
        plt.close(fig)
    
    else:
        st.info("👈 Configure your inputs in the sidebar and click **SOLVE & ANIMATE**")
        
    # Render Footer
    render_sidebar_footer(show_back=True)

# Main App Router
if st.session_state.page == 'home':
    show_homepage()
else:
    show_solver()
