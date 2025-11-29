# LogicMap Pro 🔬

**LogicMap Pro** is a professional-grade Karnaugh Map (K-Map) solver and visualizer built with Python and Streamlit. It is designed to help students, engineers, and educators understand and simplify Boolean logic expressions through interactive animations and clear visualizations.

## ✨ Features

- **Interactive K-Map Visualization**: Watch groups form in real-time with step-by-step animations.
- **Smart Solver**: Uses the Quine-McCluskey algorithm to find optimal prime implicants.
- **Flexible Inputs**: Support for 2, 3, and 4 variables.
- **Dual Modes**: Switch between Sum of Products (SOP) and Product of Sums (POS).
- **Don't Care Conditions**: Fully supports 'X' terms for advanced optimization.
- **Responsive Design**: Works perfectly on desktops, tablets, and mobile devices.
- **Dark/Light Mode**: Toggle between themes to suit your preference.

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/justinsaju21/logicmap-pro.git
    cd logicmap-pro
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 🛠️ Usage

1.  **Launch the App**: Open the link provided by Streamlit (usually `http://localhost:8501`).
2.  **Configure**: Use the sidebar to select the number of variables (2-4) and the mode (SOP/POS).
3.  **Input Terms**: Enter your minterms (e.g., `0, 1, 5, 7`) and optional "Don't Care" terms.
4.  **Solve**: Click **🚀 SOLVE & ANIMATE** to see the magic happen!
5.  **Analyze**: View the simplified equation, truth table, and step-by-step grouping log.

## 📦 Dependencies

-   `streamlit`
-   `pandas`
-   `matplotlib`
-   `numpy`

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve LogicMap Pro.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
