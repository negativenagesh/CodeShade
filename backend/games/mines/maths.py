import math

def calculate_multiplier(bombs: int, hits: int) -> float:
    """
    Calculates the exact multiplier for Stake Mines at a given state.
    Uses nCr combinatorics based on a 0.99 RTP (House Edge 1%).
    """
    if hits == 0:
        return 1.00
    
    if hits > (25 - bombs):
        return 0.00
    
    total_safe = 25 - bombs
    total_ways = math.comb(25, hits)
    safe_ways = math.comb(total_safe, hits)
    
    if safe_ways == 0:
        return 0.00
        
    multiplier = 0.99 * (total_ways / safe_ways)
    return round(multiplier, 2)
