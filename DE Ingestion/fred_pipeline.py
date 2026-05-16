import pandas as pd
import duckdb
import requests

print("=== Fetching weather data from Open-Meteo ===")

# City coordinates
cities = {
    "London":   {"lat": 51.5074, "lon": -0.1278},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "Mumbai":   {"lat": 19.0760, "lon": 72.8777}
}

all_data = []

for city, coords in cities.items():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":  coords["lat"],
        "longitude": coords["lon"],
        "daily":     ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone":  "UTC",
        "forecast_days": 7
    }
    response = requests.get(url, params=params)
    data     = response.json()

    df_city = pd.DataFrame({
        "city":          city,
        "date":          pd.to_datetime(data["daily"]["time"]),
        "temp_max":      data["daily"]["temperature_2m_max"],
        "temp_min":      data["daily"]["temperature_2m_min"],
        "precipitation": data["daily"]["precipitation_sum"]
    })
    all_data.append(df_city)
    print(f"Fetched {len(df_city)} rows for {city}")

# Combine all cities
df = pd.concat(all_data, ignore_index=True)
print(f"\nTotal rows: {len(df)}")
print(df)

# Query with DuckDB
print("\n=== DuckDB: Hottest city each day ===")
result = duckdb.query("""
    SELECT date, city, temp_max, temp_min, precipitation
    FROM df
    ORDER BY date, temp_max DESC
""").df()

print(result)

print("\n=== DuckDB: Average temp by city this week ===")
summary = duckdb.query("""
    SELECT city,
           ROUND(AVG(temp_max), 1) AS avg_max,
           ROUND(AVG(temp_min), 1) AS avg_min,
           ROUND(SUM(precipitation), 1) AS total_rain_mm
    FROM df
    GROUP BY city
    ORDER BY avg_max DESC
""").df()

print(summary)

# Save to Parquet
print("\n=== Saving to Parquet ===")
df.to_parquet("output/weather_data.parquet", index=False)
summary.to_parquet("output/weather_summary.parquet", index=False)
print("Saved weather_data.parquet and weather_summary.parquet")