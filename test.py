from gridworld import GridWorld

print("TESTING LINEAR SOLVER")
print("="*60)

# Test with discount 0.95
gw = GridWorld(height=5, width=5, goal=14, danger=[2, 18, 21], 
               blocked=[6, 7, 11, 12], noise=0.0)
gw.solve_linear_system(discount_factor=0.95)
print("\nLinear Solver - Discount 0.95:")
print(gw)

# Check a specific state that should have a clear value
print(f"\nState 9 (directly above goal): {gw.get_value(9):.4f}")
print(f"Expected: around 1.56 (positive, close to goal)")

print(f"\nState 13 (left of goal): {gw.get_value(13):.4f}")
print(f"Expected: around 0.0 (goal +5 and danger -5 cancel out)")

print(f"\nState 8 (two away from goal): {gw.get_value(8):.4f}")
print(f"Expected: close to 0.0")

# Test state next to danger
print(f"\nState 17 (next to danger 18): {gw.get_value(17):.4f}")
print(f"Expected: negative (close to danger)")