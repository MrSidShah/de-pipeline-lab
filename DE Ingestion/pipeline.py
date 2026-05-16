import pandas as pd
import duckdb

# Create some sample data
data = {
    "country": ["UK", "US", "India", "UK", "US", "India"],
    "year": [2021, 2021, 2021, 2022, 2022, 2022],
    "gdp_growth": [7.4, 5.9, 8.7, 4.1, 2.1, 7.2],
    "inflation": [2.5, 4.7, 5.5, 9.1, 8.0, 6.7]
}

df = pd.DataFrame(data)

print("=== Raw Data ===")
print(df)

# Query it with DuckDB SQL
print("\n=== DuckDB Query: GDP growth > 5% ===")
result = duckdb.query("""
    SELECT country, year, gdp_growth, inflation
    FROM df
    WHERE gdp_growth > 5
    ORDER BY gdp_growth DESC
""").df()

print(result)

print("\n=== Average by Country ===")
summary = duckdb.query("""
    SELECT country,
           ROUND(AVG(gdp_growth), 2) AS avg_gdp_growth,
           ROUND(AVG(inflation), 2)  AS avg_inflation
    FROM df
    GROUP BY country
    ORDER BY avg_gdp_growth DESC
""").df()

print(summary)

print("\n=== Saving to Parquet ===")
summary.to_parquet("output/summary.parquet", index=False)
print("Saved to output/summary.parquet")