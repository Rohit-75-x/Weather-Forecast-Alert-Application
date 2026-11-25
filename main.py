"""CLI entry point for the Weather Forecast & Alert Application."""

import argparse
import sys

from src.alert_engine import evaluate_alerts
from src.config import (
    AlertThresholds,
    IMAGES_DIR,
    OUTPUTS_DIR,
    REPORTS_DIR,
    ensure_output_directories,
    get_default_mode,
)
from src.data_processor import (
    parse_current_weather,
    parse_forecast_to_dataframe,
    summarize_forecast,
)
from src.report_generator import save_csv_report, save_text_report
from src.visualizer import create_weather_chart
from src.weather_fetcher import WeatherAPIError, fetch_weather_data, list_sample_cities


def print_weather_dashboard(current: dict, summary: dict, forecast_df, alert_result: dict) -> None:
    """Print a clean, readable weather and risk alert summary to the terminal."""
    print("\n" + "=" * 68)
    print(f"  WEATHER FORECAST & ALERT REPORT: {current['city'].upper()} ({current['country']})")
    print("=" * 68)
    print(f"Source        : {current['source']}")
    print(f"Timestamp     : {current['timestamp']}")
    print(f"Condition     : {current['description']}")
    print(f"Temperature   : {current['temperature_c']} °C (Feels like {current['feels_like_c']} °C)")
    print(f"Humidity      : {current['humidity_pct']} %")
    print(f"Wind Speed    : {current['wind_speed_ms']} m/s ({current['wind_speed_kmh']} km/h)")
    print(f"Air Quality   : {current['aqi_index']} / 5 ({current['aqi_label']})")

    print("\n--- Forecast Summary ---")
    print(
        f"Slots: {summary['slots_count']} | Temp: {summary['min_temp_c']}°C - {summary['max_temp_c']}°C "
        f"(Avg {summary['avg_temp_c']}°C) | Max Rain Prob: {summary['max_rain_prob_pct']}%"
    )

    if not forecast_df.empty:
        print("\n--- Upcoming Forecast Slots ---")
        display_cols = ["time_label", "temperature_c", "humidity_pct", "wind_speed_ms", "rain_prob_pct", "condition"]
        print(forecast_df[display_cols].to_string(index=False))

    print("\n--- Risk Alert Evaluation ---")
    print(f"Overall Risk Level : {alert_result['overall_risk']} ({alert_result['alert_count']} active alert(s))")
    for idx, alert in enumerate(alert_result["alerts"], start=1):
        print(f"  {idx}. [{alert['severity']}] {alert['type']}")
        print(f"     Details : {alert['message']}")
        print(f"     Advice  : {alert['advice']}")
    print("=" * 68 + "\n")


def run_pipeline(city: str, mode: str, generate_chart: bool = True) -> int:
    """Execute the complete fetch -> parse -> analyze -> alert -> visualize -> report flow."""
    ensure_output_directories()
    thresholds = AlertThresholds()

    try:
        raw_payload = fetch_weather_data(city=city, mode=mode)
    except WeatherAPIError as exc:
        print(f"\n[ERROR] {exc}")
        return 1

    current = parse_current_weather(raw_payload)
    forecast_df = parse_forecast_to_dataframe(raw_payload)
    summary = summarize_forecast(forecast_df)
    alert_result = evaluate_alerts(current, forecast_df, thresholds)

    chart_path = None
    if generate_chart:
        chart_path = create_weather_chart(city, forecast_df, alert_result, IMAGES_DIR, thresholds)

    csv_path = save_csv_report(city, forecast_df, OUTPUTS_DIR)
    report_path = save_text_report(city, current, summary, alert_result, chart_path, csv_path, REPORTS_DIR)

    print_weather_dashboard(current, summary, forecast_df, alert_result)
    print(f"[SAVED] Forecast CSV   : {csv_path}")
    if chart_path:
        print(f"[SAVED] Forecast Chart : {chart_path}")
    print(f"[SAVED] Alert Report   : {report_path}\n")
    return 0


def parse_args() -> argparse.Namespace:
    """Parse optional command-line arguments."""
    parser = argparse.ArgumentParser(description="Weather Forecast & Alert Application CLI")
    parser.add_argument("--city", type=str, help="City name (e.g., Mumbai, Delhi, Bengaluru)")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["simulation", "api"],
        default=get_default_mode(),
        help="Execution mode: 'simulation' (offline sample data) or 'api' (OpenWeatherMap)",
    )
    parser.add_argument("--no-chart", action="store_true", help="Skip generating PNG visualization chart")
    return parser.parse_args()


def main() -> int:
    """Interactive and CLI entry point."""
    args = parse_args()
    city = args.city
    mode = args.mode

    if not city:
        available = ", ".join(list_sample_cities())
        print("\n=== Weather Forecast & Alert Application ===")
        print(f"Pre-loaded simulation cities: {available} (or enter any city)")
        mode_choice = input(f"Select mode [simulation/api] (default: {mode}): ").strip().lower()
        if mode_choice in {"simulation", "api"}:
            mode = mode_choice
        city = input("Enter city name: ").strip()

    if not city:
        print("[ERROR] No city entered. Exiting.")
        return 1

    return run_pipeline(city=city, mode=mode, generate_chart=not args.no_chart)


if __name__ == "__main__":
    sys.exit(main())
