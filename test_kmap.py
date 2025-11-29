from kmap_logic import KMapSolver
from visualizer import KMapVisualizer
import matplotlib.pyplot as plt

def test_solver():
    print("Testing Solver...")
    # Test case: 4 vars, corners
    minterms = [0, 2, 8, 10]
    dont_cares = []
    solver = KMapSolver(4, minterms, dont_cares)
    eq, parts, groups = solver.solve()
    print(f"Equation: {eq}")
    print(f"Groups: {groups}")
    
    # Expected: B'D' (if A,B,C,D) -> 0000, 0010, 1000, 1010
    # 0: 0000, 2: 0010, 8: 1000, 10: 1010
    # Binary:
    # 0000
    # 0010
    # 1000
    # 1010
    # Grouping: -0-0 -> B=0, D=0 -> B'D'
    
    if "B'" in eq and "D'" in eq:
        print("Solver Logic Passed!")
    else:
        print("Solver Logic Check Failed (Visual inspection needed)")

def test_visualizer():
    print("Testing Visualizer...")
    minterms = [0, 2, 8, 10]
    dont_cares = []
    groups = [[0, 2, 8, 10]]
    viz = KMapVisualizer(4, minterms, dont_cares, groups)
    try:
        fig = viz.draw()
        print("Visualizer Draw Passed!")
    except Exception as e:
        print(f"Visualizer Failed: {e}")

if __name__ == "__main__":
    test_solver()
    test_visualizer()
