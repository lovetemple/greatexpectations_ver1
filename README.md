# Great Expectations Demo Project

This project demonstrates data validation using Great Expectations with a sample customer dataset.

## 📁 Project Structure

```
ge1/
├── data/
│   └── sample_customers.csv          # Sample customer data (6 records)
├── gx/                                # Great Expectations project directory
│   ├── expectations/
│   │   └── customer_validation_suite.json  # Saved expectation suite
│   ├── checkpoints/                   # Checkpoint configurations
│   ├── uncommitted/
│   │   ├── data_docs/                 # Generated HTML reports
│   │   │   └── local_site/
│   │   │       └── index.html         # Main report page
│   │   └── validations/               # Validation results
│   └── great_expectations.yml         # Main configuration
└── demo_great_expectations.py         # Complete demo script
```

## 🚀 Running the Demo

To run the comprehensive validation demo:

```bash
python demo_great_expectations.py
```

This script will:
1. Load the customer data from `data/sample_customers.csv`
2. Configure a Pandas datasource
3. Create 15 data quality expectations covering:
   - Table structure (column count, row count)
   - Customer ID validations (null checks, uniqueness, data types)
   - Email validations (null checks, format, uniqueness)
   - Signup date validations (null checks, date format)
   - Orders validations (null checks, value ranges, statistics)
   - Order value validations (null checks, value ranges)
4. Run all validations
5. Generate and open HTML reports in your browser

## ✅ Validations Implemented

### Table Structure
- Column count equals 5
- Row count between 5-1000

### Customer ID
- No null values
- All values are unique
- Data type is integer

### Email
- No null values
- Valid email format (regex)
- All emails are unique

### Signup Date
- No null values
- Date format is YYYY-MM-DD

### Orders
- No null values
- Values between 0-100
- Average between 0-10

### Average Order Value
- No null values
- Values between 0-500

## 📊 Viewing Reports

After running the demo, Data Docs (HTML reports) are automatically opened in your browser.

You can also manually open them:
```bash
open gx/uncommitted/data_docs/local_site/index.html
```

## 📝 Sample Data

The `data/sample_customers.csv` file contains 6 customer records with the following fields:
- `customer_id`: Unique customer identifier
- `email`: Customer email address
- `signup_date`: Date when customer signed up
- `orders`: Number of orders placed
- `avg_order_value`: Average value of customer's orders

## 🔧 Requirements

- Python 3.9+
- great_expectations==1.8.1
- pandas

## 📚 Learn More

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Expectation Gallery](https://greatexpectations.io/expectations/)
