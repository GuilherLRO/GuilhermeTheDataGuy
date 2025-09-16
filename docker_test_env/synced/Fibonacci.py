#!/usr/bin/env python3
"""
Fibonacci Sequence Implementation
This script provides multiple methods to calculate Fibonacci numbers.
"""

def fibonacci_recursive(n):
    """
    Calculate nth Fibonacci number using recursion.
    Time complexity: O(2^n) - inefficient for large n
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    """
    Calculate nth Fibonacci number using iteration.
    Time complexity: O(n) - efficient
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_memoized(n, memo={}):
    """
    Calculate nth Fibonacci number using memoization.
    Time complexity: O(n) - efficient with caching
    """
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


def fibonacci_sequence(n):
    """
    Generate the first n Fibonacci numbers.
    Returns a list of Fibonacci numbers.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    
    return sequence


def fibonacci_generator(n):
    """
    Generator function that yields Fibonacci numbers up to n terms.
    Memory efficient for large sequences.
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def main():
    """Main function to demonstrate different Fibonacci implementations."""
    print("Fibonacci Sequence Calculator")
    print("=" * 40)
    
    # Get user input
    try:
        n = int(input("Enter the number of Fibonacci numbers to calculate: "))
    except ValueError:
        print("Invalid input. Using default value of 10.")
        n = 10
    
    if n < 0:
        print("Please enter a non-negative number.")
        return
    
    print(f"\nFirst {n} Fibonacci numbers:")
    
    # Method 1: Generate sequence
    sequence = fibonacci_sequence(n)
    print(f"Sequence method: {sequence}")
    
    # Method 2: Using generator
    print("Generator method: ", end="")
    for i, fib in enumerate(fibonacci_generator(n)):
        print(fib, end="")
        if i < n - 1:
            print(", ", end="")
    print()
    
    # Method 3: Individual calculations
    print(f"\nIndividual calculations (using iterative method):")
    for i in range(n):
        result = fibonacci_iterative(i)
        print(f"F({i}) = {result}")
    
    # Performance comparison for larger numbers
    if n >= 20:
        print(f"\nPerformance comparison for F({n-1}):")
        
        import time
        
        # Iterative method
        start_time = time.time()
        result_iter = fibonacci_iterative(n - 1)
        iter_time = time.time() - start_time
        print(f"Iterative: F({n-1}) = {result_iter} (Time: {iter_time:.6f}s)")
        
        # Memoized method
        start_time = time.time()
        result_memo = fibonacci_memoized(n - 1)
        memo_time = time.time() - start_time
        print(f"Memoized: F({n-1}) = {result_memo} (Time: {memo_time:.6f}s)")
        
        # Recursive method (only for smaller numbers to avoid long wait)
        if n <= 30:
            start_time = time.time()
            result_rec = fibonacci_recursive(n - 1)
            rec_time = time.time() - start_time
            print(f"Recursive: F({n-1}) = {result_rec} (Time: {rec_time:.6f}s)")
        else:
            print("Recursive method skipped for large numbers (too slow)")


if __name__ == "__main__":
    main()
