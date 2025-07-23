import re
import time

def delete_parameters(sql_query):
    """Remove parameter values from SQL query"""
    # Remove string values inside quotes
    query = re.sub(r"'[^']*'", "''", sql_query)

    # Remove numeric values after comparison operators
    query = re.sub(r'(=|>|<|>=|<=)\s*\d+', r'\1 ', query)
    return query

def is_injection(static_query, runtime_query):
    """Check if runtime query structure differs from static query"""
    static_normalized = delete_parameters(static_query)
    runtime_normalized = delete_parameters(runtime_query)

    return static_normalized != runtime_normalized

def measure_detection_time(static_query, test_query):
    """Measure time taken to detect SQL injection"""
    start_time = time.time()
    result = is_injection(static_query, test_query)
    end_time = time.time()
    return (end_time - start_time) * 1000, result  # Return time in milliseconds

def compute_time_comparison(static_query, normal_query, injected_query):
    """Compare computation time for normal vs injected queries"""
    normal_start = time.time()
    is_injection(static_query, normal_query)
    normal_end = time.time()
    normal_time = (normal_end - normal_start) * 1000  # ms
    
    injected_start = time.time()
    is_injection(static_query, injected_query)
    injected_end = time.time()
    injected_time = (injected_end - injected_start) * 1000  # ms
    
    return normal_time, injected_time
    
# Example usage
def main():
    # Example queries
    static_query = "SELECT * FROM STUDENT WHERE RNO='$rollno' AND NAME='$name';"
    normal_query = "SELECT * FROM STUDENT WHERE RNO='1001' AND NAME='AJAY';"
    injected_query = "SELECT * FROM STUDENT WHERE RNO='1' OR '1'='1'--' AND NAME='AJAY';"
    
    # Different attack types for testing
    attack_types = {
        "Tautology": "SELECT * FROM STUDENT WHERE RNO='1' OR '1'='1' AND NAME='AJAY';",
        "Union": "SELECT * FROM STUDENT WHERE RNO='1' UNION SELECT username, password FROM users--' AND NAME='AJAY';",
        "Comment": "SELECT * FROM STUDENT WHERE RNO='1'--' AND NAME='AJAY';",
        "Piggy-backed": "SELECT * FROM STUDENT WHERE RNO='1001'; DROP TABLE STUDENT;--' AND NAME='AJAY';"
    }

    # Test normal query
    print("Testing normal query...")
    print(f"Original: {normal_query}")
    print(f"Normalized: {delete_parameters(normal_query)}")
    if is_injection(static_query, normal_query):
        print("RESULT: SQL injection detected!")
    else:
        print("RESULT: No SQL injection detected.")

    print("\n" + "-" * 50 + "\n")

    # Test injected query
    print("Testing injected query...")
    print(f"Original: {injected_query}")
    print(f"Normalized: {delete_parameters(injected_query)}")
    if is_injection(static_query, injected_query):
        print("RESULT: SQL injection detected!")
    else:
        print("RESULT: No SQL injection detected.")
    
    # Detection time for different attack types
    print("\Response Time for Different Attack Types:")
    print("-----------------------------------------")
    print(f"{'Attack Type':<15} {'Detection Time (ms)':<20} {'Result':<10}")
    print("-" * 50)
    
    for attack_name, attack_query in attack_types.items():
        detection_time, result = measure_detection_time(static_query, attack_query)
        print(f"{attack_name:<15} {detection_time:<20.4f} {'Detected' if result else 'Not Detected'}")
    
    # Computation time comparison
    normal_time, injected_time = compute_time_comparison(static_query, normal_query, injected_query)
    print("\nComputation Time Comparison:")
    print("---------------------------")
    print(f"Normal query: {normal_time:.4f} ms")
    print(f"Injected query: {injected_time:.4f} ms")
