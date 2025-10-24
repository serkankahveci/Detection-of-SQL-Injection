# SQL Injection Detection by Parameter Value Removal

A Python implementation of SQL injection attack detection based on the research paper "Detection of SQL Injection Attacks by Removing the Parameter Values of SQL Query" by Katole et al. (2018).

## Overview

This tool detects SQL injection attacks by comparing the structural differences between static SQL queries and runtime SQL queries after removing parameter values. The method is lightweight, database-agnostic, and doesn't require complex parsing or machine learning algorithms.

## How It Works

The detection mechanism follows these key steps:

1. **Parameter Removal**: Extract the structural skeleton of SQL queries by removing parameter values
2. **Comparison**: Compare the normalized static query structure with the runtime query structure
3. **Detection**: Flag queries where structures differ as potential SQL injection attacks

### Example

**Static Query (Template):**
```sql
SELECT * FROM STUDENT WHERE RNO='$rollno' AND NAME='$name';
```

**Normal Runtime Query:**
```sql
SELECT * FROM STUDENT WHERE RNO='1001' AND NAME='AJAY';
```

**Malicious Runtime Query:**
```sql
SELECT * FROM STUDENT WHERE RNO='1' OR '1'='1'--' AND NAME='AJAY';
```

After parameter removal:
- **Static/Normal**: `SELECT * FROM STUDENT WHERE RNO='' AND NAME='';`
- **Malicious**: `SELECT * FROM STUDENT WHERE RNO='' OR ''=''--' AND NAME='';`

The structural difference indicates a SQL injection attack.

## Features

- **Database Agnostic**: Works with any SQL database system
- **Lightweight**: No complex parsing trees or external libraries required
- **Multiple Attack Types**: Detects various SQL injection patterns including:
  - Tautology attacks (`1=1`, `'a'='a'`)
  - Union-based attacks
  - Comment-based attacks (`--`, `/**/`)
  - Piggy-backed queries
- **Performance Monitoring**: Includes timing analysis for detection efficiency
- **High Accuracy**: Research shows 96-100% detection rates

## Installation

1. Clone this repository:
```bash
git clone https://github.com/serkankahveci/Detection-of-SQL-Injection.git
cd sql-injection-detection
```

2. No external dependencies required - uses only Python standard library

## Usage

### Basic Detection

```python
from sql_injection_detector import is_injection, delete_parameters

# Define your static query template
static_query = "SELECT * FROM STUDENT WHERE RNO='$rollno' AND NAME='$name';"

# Test a runtime query
runtime_query = "SELECT * FROM STUDENT WHERE RNO='1' OR '1'='1' AND NAME='AJAY';"

# Check for injection
if is_injection(static_query, runtime_query):
    print("SQL injection detected!")
else:
    print("Query is safe.")
```

### Performance Analysis

```python
from sql_injection_detector import measure_detection_time, compute_time_comparison

# Measure detection time
detection_time, result = measure_detection_time(static_query, test_query)
print(f"Detection completed in {detection_time:.4f} ms")

# Compare computation times
normal_time, injected_time = compute_time_comparison(static_query, normal_query, injected_query)
print(f"Normal: {normal_time:.4f} ms, Injected: {injected_time:.4f} ms")
```

### Full Example

```python
python main.py
```

This will run comprehensive tests including:
- Normal query validation
- Various attack type detection
- Performance benchmarking
- Timing analysis

## API Reference

### Core Functions

#### `delete_parameters(sql_query)`
Removes parameter values from SQL query, leaving structural skeleton.

**Parameters:**
- `sql_query` (str): The SQL query to normalize

**Returns:**
- `str`: Normalized query with parameter values removed

#### `is_injection(static_query, runtime_query)`
Determines if a runtime query contains SQL injection by comparing structures.

**Parameters:**
- `static_query` (str): The original/template SQL query
- `runtime_query` (str): The runtime query to validate

**Returns:**
- `bool`: True if injection detected, False otherwise

#### `measure_detection_time(static_query, test_query)`
Measures the time taken to detect SQL injection.

**Parameters:**
- `static_query` (str): Template query
- `test_query` (str): Query to test

**Returns:**
- `tuple`: (detection_time_ms, is_injection_result)

## Attack Types Detected

| Attack Type | Description | Example |
|-------------|-------------|---------|
| **Tautology** | Always-true conditions | `'1'='1'`, `'a'='a'` |
| **Union-based** | Combining queries with UNION | `UNION SELECT username, password FROM users` |
| **Comment** | Using SQL comments to bypass logic | `'--`, `/**/` |
| **Piggy-backed** | Multiple statements in one query | `'; DROP TABLE users;--` |

## Performance Metrics

Based on the research paper validation:

- **Detection Rate**: 96-100% across different web applications
- **Response Time**: Millisecond-level detection for various attack types
- **False Positives**: Minimal due to structural comparison approach
- **Scalability**: Suitable for real-time web application monitoring

## Advantages

1. **DBMS Independent**: Works with any SQL database
2. **No Source Code Changes**: Can be implemented as middleware
3. **Low Overhead**: Simple string processing with minimal computational cost
4. **High Accuracy**: Structural comparison reduces false positives
5. **Real-time**: Fast enough for production web applications

## Limitations

1. **Template Dependency**: Requires predefined static query templates
2. **Dynamic Query Complexity**: May need refinement for highly dynamic queries
3. **Advanced Obfuscation**: Sophisticated attacks might bypass simple parameter removal
4. **Stored Procedures**: Limited effectiveness with complex stored procedure calls

## Research Background

This implementation is based on the IEEE paper:

> Katole, R. A., Sherekar, S. S., & Thakare, V. M. (2018). "Detection of SQL Injection Attacks by Removing the Parameter Values of SQL Query." *Proceedings of the Second International Conference on Inventive Systems and Control (ICISC 2018)*, 736-741.

The research demonstrates that removing parameter values and comparing query structures provides an effective, lightweight method for SQL injection detection with high accuracy rates.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Note

This tool is designed for educational and research purposes. For production environments, consider implementing multiple layers of security including:

- Input validation and sanitization
- Parameterized queries/prepared statements
- Web Application Firewalls (WAF)
- Regular security audits
- Database access controls
