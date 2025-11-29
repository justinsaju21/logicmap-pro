import pandas as pd
import numpy as np
from itertools import combinations

class KMapSolver:
    def __init__(self, num_vars, minterms, dont_cares, mode='SOP'):
        self.num_vars = num_vars
        self.minterms = set(minterms)
        self.dont_cares = set(dont_cares)
        self.mode = mode
        self.variables = [chr(65 + i) for i in range(num_vars)]  # A, B, C, D...
        
        # Validation
        max_val = 2**num_vars - 1
        if any(m < 0 or m > max_val for m in self.minterms):
            raise ValueError(f"Minterms must be between 0 and {max_val}")
        if any(d < 0 or d > max_val for d in self.dont_cares):
            raise ValueError(f"Don't cares must be between 0 and {max_val}")
            
        # For POS, we solve for 0s (maxterms) as if they were 1s, then invert result
        if self.mode == 'POS':
            all_terms = set(range(2**num_vars))
            # In POS, we group the 0s. The user inputs maxterms (where output is 0).
            # So if mode is POS, the 'minterms' provided are actually the 0 locations.
            # We treat them as 1s for the grouping algorithm, then format output as Product of Sums.
            self.target_terms = self.minterms
        else:
            self.target_terms = self.minterms

    def get_truth_table(self):
        rows = []
        for i in range(2**self.num_vars):
            row = {}
            # Binary representation
            bin_str = format(i, f'0{self.num_vars}b')
            for j, var in enumerate(self.variables):
                row[var] = int(bin_str[j])
            
            # Output
            if i in self.minterms:
                row['Output'] = 0 if self.mode == 'POS' else 1
            elif i in self.dont_cares:
                row['Output'] = 'X'
            else:
                row['Output'] = 1 if self.mode == 'POS' else 0
            
            row['Minterm'] = i
            rows.append(row)
        return pd.DataFrame(rows)

    def solve(self):
        # Quine-McCluskey Algorithm Implementation
        
        # 1. Group terms by number of 1s
        # We include dont_cares in the grouping process to maximize group size
        terms_to_group = self.target_terms | self.dont_cares
        if not terms_to_group:
            return "0", [], [] if self.mode == 'SOP' else "1", [], []
        
        # If all terms are present (tautology)
        if len(terms_to_group) == 2**self.num_vars:
            return "1", [], [list(terms_to_group)] if self.mode == 'SOP' else "0", [], [list(terms_to_group)]

        # Structure: groups[num_ones] = {binary_str: [minterms_covered]}
        groups = {}
        for term in terms_to_group:
            bin_str = format(term, f'0{self.num_vars}b')
            num_ones = bin_str.count('1')
            if num_ones not in groups:
                groups[num_ones] = {}
            groups[num_ones][bin_str] = [term]

        prime_implicants = set()
        
        while True:
            new_groups = {}
            marked = set()
            sorted_keys = sorted(groups.keys())
            
            for i in range(len(sorted_keys) - 1):
                k1 = sorted_keys[i]
                k2 = sorted_keys[i+1]
                
                # Optimization: k2 must be k1 + 1 for 1-bit difference check to be valid in terms of bit count
                if k2 != k1 + 1:
                    continue
                    
                for bin1, terms1 in groups[k1].items():
                    for bin2, terms2 in groups[k2].items():
                        diff = 0
                        diff_idx = -1
                        for idx in range(self.num_vars):
                            if bin1[idx] != bin2[idx]:
                                diff += 1
                                diff_idx = idx
                        
                        if diff == 1:
                            marked.add(bin1)
                            marked.add(bin2)
                            new_bin = list(bin1)
                            new_bin[diff_idx] = '-'
                            new_bin = "".join(new_bin)
                            
                            new_count = new_bin.count('1')
                            if new_count not in new_groups:
                                new_groups[new_count] = {}
                            # Merge lists of covered terms
                            new_groups[new_count][new_bin] = sorted(list(set(terms1 + terms2)))

            # Add unmarked terms to prime implicants
            for k in groups:
                for bin_str, terms in groups[k].items():
                    if bin_str not in marked:
                        prime_implicants.add((bin_str, tuple(terms)))
            
            if not new_groups:
                break
            groups = new_groups

        # 2. Select Essential Prime Implicants
        # Filter PIs to only those that cover at least one target_term (exclude PIs made purely of dont_cares)
        relevant_pis = []
        for pi_bin, covered_terms in prime_implicants:
            # Check if this PI covers any required minterms (not just dont cares)
            if any(t in self.target_terms for t in covered_terms):
                relevant_pis.append({'bin': pi_bin, 'terms': covered_terms})
        
        # Petrick's method or simple coverage for small N
        # For N<=4, a greedy approach with "Essential" check usually suffices or simple recursion.
        # Let's do a standard coverage chart approach.
        
        final_pis = []
        covered_minterms = set()
        
        # Find essential PIs
        # Map minterm -> list of PIs covering it
        mt_map = {mt: [] for mt in self.target_terms}
        for i, pi in enumerate(relevant_pis):
            for term in pi['terms']:
                if term in self.target_terms:
                    mt_map[term].append(i)
        
        # If a minterm is covered by only one PI, that PI is essential
        essential_indices = set()
        for mt, pi_indices in mt_map.items():
            if len(pi_indices) == 1:
                essential_indices.add(pi_indices[0])
        
        for idx in essential_indices:
            final_pis.append(relevant_pis[idx])
            for term in relevant_pis[idx]['terms']:
                if term in self.target_terms:
                    covered_minterms.add(term)
        
        # Cover remaining minterms
        remaining_minterms = self.target_terms - covered_minterms
        if remaining_minterms:
            # Greedy approach: pick PI that covers most remaining minterms
            # Filter remaining PIs
            potential_indices = [i for i in range(len(relevant_pis)) if i not in essential_indices]
            
            while remaining_minterms:
                best_pi_idx = -1
                max_cover = -1
                
                for idx in potential_indices:
                    # Count how many REMAINING minterms this PI covers
                    count = 0
                    for t in relevant_pis[idx]['terms']:
                        if t in remaining_minterms:
                            count += 1
                    if count > max_cover:
                        max_cover = count
                        best_pi_idx = idx
                
                if best_pi_idx != -1:
                    final_pis.append(relevant_pis[best_pi_idx])
                    for t in relevant_pis[best_pi_idx]['terms']:
                        if t in remaining_minterms:
                            remaining_minterms.remove(t)
                    potential_indices.remove(best_pi_idx)
                else:
                    # Should not happen if logic is correct
                    break
        
        # Sort PIs by size (descending) so largest groups (8, 4, 2) come first
        final_pis.sort(key=lambda x: len(x['terms']), reverse=True)
                    
        return self._format_output(final_pis)

    def _format_output(self, pis):
        # Format logic string and groups for visualization
        logic_parts = []
        groups = []
        
        for pi in pis:
            bin_str = pi['bin']
            groups.append(pi['terms'])
            
            term_str = ""
            if self.mode == 'SOP':
                # 1 is variable, 0 is complement
                for i, bit in enumerate(bin_str):
                    if bit == '1':
                        term_str += self.variables[i]
                    elif bit == '0':
                        term_str += self.variables[i] + "'"
                if term_str == "": term_str = "1"
            else: # POS
                # 0 is variable, 1 is complement, ORed together
                parts = []
                for i, bit in enumerate(bin_str):
                    if bit == '0':
                        parts.append(self.variables[i])
                    elif bit == '1':
                        parts.append(self.variables[i] + "'")
                term_str = "(" + "+".join(parts) + ")"
                if term_str == "()": term_str = "0"
            
            logic_parts.append(term_str)
            
        if not logic_parts:
            return "0" if self.mode == 'SOP' else "1", [], []

        if self.mode == 'SOP':
            equation = " + ".join(logic_parts)
        else:
            equation = "".join(logic_parts)
            
        return equation, logic_parts, groups
