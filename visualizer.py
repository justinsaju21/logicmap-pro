import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class KMapVisualizer:
    def __init__(self, num_vars, minterms, dont_cares, groups, theme='dark'):
        self.num_vars = num_vars
        self.minterms = set(minterms)
        self.dont_cares = set(dont_cares)
        self.groups = groups
        self.theme = theme
        
        # Configuration based on vars
        if num_vars == 2:
            self.rows = 2
            self.cols = 2
            self.row_labels = ['0', '1']
            self.col_labels = ['0', '1']
            self.row_vars = "A"
            self.col_vars = "B"
        elif num_vars == 3:
            self.rows = 2
            self.cols = 4
            self.row_labels = ['0', '1']
            self.col_labels = ['00', '01', '11', '10']
            self.row_vars = "A"
            self.col_vars = "BC"
        elif num_vars == 4:
            self.rows = 4
            self.cols = 4
            self.row_labels = ['00', '01', '11', '10']
            self.col_labels = ['00', '01', '11', '10']
            self.row_vars = "AB"
            self.col_vars = "CD"
            
        # Gray code indices for mapping
        self.row_indices = [0, 1] if self.rows == 2 else [0, 1, 3, 2]
        self.col_indices = [0, 1] if self.cols == 2 else [0, 1, 3, 2]

    def _get_cell_coords(self, minterm):
        # Returns (row, col) in the grid (0-indexed)
        bin_str = format(minterm, f'0{self.num_vars}b')
        
        if self.num_vars == 2:
            r_val = int(bin_str[0], 2)
            c_val = int(bin_str[1], 2)
        elif self.num_vars == 3:
            r_val = int(bin_str[0], 2)
            c_val = int(bin_str[1:], 2)
        elif self.num_vars == 4:
            r_val = int(bin_str[:2], 2)
            c_val = int(bin_str[2:], 2)
            
        r = self.row_indices.index(r_val)
        c = self.col_indices.index(c_val)
        return r, c

    def draw(self, show_grid=True, show_indices=False, visible_values=None, visible_groups=None):
        # visible_values: list of minterms/indices to show values for
        # visible_groups: list of groups to draw
        
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        # Adjusted limits to prevent clipping of labels
        ax.set_xlim(-1.5, self.cols + 0.5)
        ax.set_ylim(-1.5, self.rows + 0.5)
        ax.invert_yaxis() # 0 at top
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Theme-based colors
        if self.theme == 'dark':
            BG_COLOR = 'black'
            GRID_COLOR = 'white'
            LABEL_COLOR = '#FFFF00'
            TEXT_COLOR = '#E0FFFF'
            MINTERM_NUM_COLOR = '#CCCCCC'
        else:
            BG_COLOR = 'white'
            GRID_COLOR = '#333333'
            LABEL_COLOR = '#004E89'
            TEXT_COLOR = '#1F1F1F'
            MINTERM_NUM_COLOR = '#666666'
        
        # Set background
        fig.patch.set_facecolor(BG_COLOR)
        ax.set_facecolor(BG_COLOR)
        
        if show_grid:
            # Draw Grid Lines with rounded style
            for r in range(self.rows + 1):
                ax.plot([0, self.cols], [r, r], color=GRID_COLOR, lw=2.5, alpha=0.9)
            for c in range(self.cols + 1):
                ax.plot([c, c], [0, self.rows], color=GRID_COLOR, lw=2.5, alpha=0.9)
                
            # Draw Diagonal Split
            ax.plot([0, -0.6], [0, -0.6], color=GRID_COLOR, lw=2.5, alpha=0.9)
            
            # Variable Labels
            ax.text(-0.7, 0.2, self.row_vars, ha='right', va='center', fontsize=18, 
                    color=LABEL_COLOR, fontweight='bold')
            ax.text(-0.1, -0.7, self.col_vars, ha='center', va='bottom', fontsize=18, 
                    color=LABEL_COLOR, fontweight='bold')
            
            # Row Headers
            for i, label in enumerate(self.row_labels):
                ax.text(-0.1, i + 0.5, label, ha='right', va='center', fontsize=16, 
                       color=LABEL_COLOR, fontweight='bold', fontfamily='monospace')
                
            # Col Headers
            for i, label in enumerate(self.col_labels):
                ax.text(i + 0.5, -0.1, label, ha='center', va='bottom', fontsize=16, 
                       color=LABEL_COLOR, fontweight='bold', fontfamily='monospace')

        # Fill Content (Values and Minterm Indices)
        for r in range(self.rows):
            for c in range(self.cols):
                r_val = self.row_indices[r]
                c_val = self.col_indices[c]
                
                if self.num_vars == 2:
                    minterm = (r_val << 1) | c_val
                elif self.num_vars == 3:
                    minterm = (r_val << 2) | c_val
                elif self.num_vars == 4:
                    minterm = (r_val << 2) | c_val
                
                # Minterm Number (Top Right)
                if show_indices:
                    ax.text(c + 0.88, r + 0.18, str(minterm), ha='right', va='top', 
                           fontsize=10, color=MINTERM_NUM_COLOR, fontweight='normal')
                
                # Value (Center)
                if visible_values is not None and minterm in visible_values:
                    val_text = "0"
                    val_color = TEXT_COLOR
                    if minterm in self.minterms:
                        val_text = "1"
                        val_color = '#00FF00' if self.theme == 'dark' else '#00AA00'
                    elif minterm in self.dont_cares:
                        val_text = "X"
                        val_color = '#FF00FF' if self.theme == 'dark' else '#AA00AA'
                    
                    ax.text(c + 0.5, r + 0.55, val_text, ha='center', va='center', 
                           fontsize=26, color=val_color, fontweight='bold')

        # Draw Groups
        if visible_groups:
            colors = ['#FFD700', '#FF69B4', '#00FFFF', '#ADFF2F', '#FF4500', '#9370DB']
            for i, group in enumerate(visible_groups):
                group_color = colors[i % len(colors)]
                self._draw_group(ax, group, group_color)

        # Explicitly set margins to ensure labels (AB, CD) are not clipped
        # left/bottom provide space for the negative coordinate labels
        # Increased top/left margins to fix clipping
        plt.subplots_adjust(left=0.25, right=0.95, top=0.85, bottom=0.1)
        return fig

    def _draw_group(self, ax, group, color):
        coords = [self._get_cell_coords(m) for m in group]
        rows = [r for r, c in coords]
        cols = [c for r, c in coords]
        
        # Identify clusters to handle wrapping
        r_clusters = self._get_clusters(rows, self.rows)
        c_clusters = self._get_clusters(cols, self.cols)
        
        for r_start, r_end in r_clusters:
            for c_start, c_end in c_clusters:
                width = c_end - c_start + 1
                height = r_end - r_start + 1
                pad = 0.06
                
                # Rounded Rectangle with enhanced styling
                rect = patches.FancyBboxPatch(
                    (c_start + pad, r_start + pad),
                    width - 2*pad,
                    height - 2*pad,
                    boxstyle="round,pad=0.12,rounding_size=0.25",
                    linewidth=3.5,
                    edgecolor=color,
                    facecolor='none',
                    alpha=0.95
                )
                ax.add_patch(rect)

    def _get_clusters(self, indices, size):
        unique_indices = sorted(list(set(indices)))
        if not unique_indices: return []
        
        clusters = []
        start = unique_indices[0]
        prev = start
        
        for i in range(1, len(unique_indices)):
            curr = unique_indices[i]
            if curr != prev + 1:
                clusters.append((start, prev))
                start = curr
            prev = curr
        clusters.append((start, prev))
        
        return clusters
