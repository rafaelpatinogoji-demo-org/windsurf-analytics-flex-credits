#!/usr/bin/env python3
"""
Flex Credits by Model - Daily Breakdown
Fast parallel processing showing flex credits usage per model per day.
"""

import os
import json
import requests
import csv
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Define output directory - local to TeamFlexCredits
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

if not SERVICE_KEY:
    raise ValueError("SERVICE_KEY not found in .env file")

API_URL = "https://server.codeium.com/api/v1/Analytics"

# Model name mapping for better readability
MODEL_NAME_MAPPING = {
    "MODEL_PRIVATE_1": "Gemini 2.5 Pro (early)",
    "MODEL_PRIVATE_2": "Claude Sonnet 4.5",
    "MODEL_PRIVATE_3": "Claude Sonnet 4.5 Thinking",
    "MODEL_PRIVATE_4": "Grok 4 Code",
    "MODEL_PRIVATE_5": "GPT-5 Codex",
    "MODEL_PRIVATE_6": "GPT-5 (low reasoning)",
    "MODEL_PRIVATE_7": "GPT-5 (medium reasoning)",
    "MODEL_PRIVATE_8": "GPT-5 (high reasoning)",
    "MODEL_PRIVATE_9": "Gemini 2.5 Pro (soft-waffle)",
    "MODEL_PRIVATE_10": "GLM SWE 1.5 Alpha",
    "MODEL_PRIVATE_11": "Claude Haiku 4.5",
    # Other common model mappings
    "MODEL_CLAUDE_3_7_SONNET_20250219": "Claude 3.7 Sonnet",
    "MODEL_CLAUDE_3_7_SONNET_20250219_THINKING": "Claude 3.7 Sonnet Thinking",
    "MODEL_CLAUDE_4_SONNET": "Claude 4 Sonnet",
    "MODEL_GOOGLE_GEMINI_2_5_PRO": "Gemini 2.5 Pro",
    "MODEL_CHAT_GPT_4_1_2025_04_14": "GPT-4.1 (2025-04-14)",
    "MODEL_CHAT_GPT_4O_2024_08_06": "GPT-4o (2024-08-06)",
    "<nil>": "Unknown Model",
}


def get_friendly_model_name(model):
    """Convert model internal name to friendly display name"""
    return MODEL_NAME_MAPPING.get(model, model)


def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Please use YYYY-MM-DD format.")


def get_month_date_range(year, month):
    """Get start and end dates for a specific month"""
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def find_latest_email_mapping_file():
    """Find the latest email_api_mapping file in local output directory, then parent if exists"""
    import glob
    
    # First check local output directory
    local_pattern = os.path.join(OUTPUT_DIR, 'email_api_mapping_*.json')
    files = glob.glob(local_pattern)
    
    # If not found locally, try parent directory
    if not files:
        parent_output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        if os.path.exists(parent_output_dir):
            parent_pattern = os.path.join(parent_output_dir, 'email_api_mapping_*.json')
            files = glob.glob(parent_pattern)
    
    return sorted(files)[-1] if files else None


def read_api_keys_from_json(json_file_path):
    """Read API keys from JSON file"""
    try:
        with open(json_file_path, 'r') as json_file:
            email_api_map = json.load(json_file)
            api_key_email_map = {api_key: email for email, api_key in email_api_map.items()}
            return api_key_email_map
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return {}


def generate_email_api_mapping():
    """Generate email API mapping by fetching from UserPageAnalytics API"""
    print("\n🔄 Generating email API mapping...")
    
    # Fetch data from last 30 days
    now = datetime.now()
    start_date = now - timedelta(days=30)
    start_timestamp = start_date.strftime("%Y-%m-%dT00:00:00Z")
    end_timestamp = now.strftime("%Y-%m-%dT23:59:59Z")
    
    print(f"📡 Fetching user data from {start_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}...")
    
    url = "https://server.codeium.com/api/v1/UserPageAnalytics"
    payload = {
        "service_key": SERVICE_KEY,
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        # Show progress while making API request
        with tqdm(total=100, desc="⏳ Requesting data", bar_format='{desc}: {bar}', ncols=50) as pbar:
            response = requests.post(url, json=payload, headers=headers)
            pbar.update(50)
            response.raise_for_status()
            data = response.json()
            pbar.update(50)
        
        email_api_map = {}
        
        # Extract email-API key pairs from userTableStats
        if "userTableStats" in data and isinstance(data["userTableStats"], list):
            for user in data["userTableStats"]:
                if "email" in user and user["email"] and "apiKey" in user and user["apiKey"]:
                    email_api_map[user["email"]] = user["apiKey"]
        
        print(f"Found {len(email_api_map)} unique email-API key pairs")
        
        if email_api_map:
            # Save to local output directory
            current_date = datetime.now().strftime("%Y-%m-%d")
            output_file = os.path.join(OUTPUT_DIR, f"email_api_mapping_{current_date}.json")
            
            with open(output_file, "w") as f:
                json.dump(email_api_map, f, indent=2)
            
            print(f"✅ Saved mapping to {output_file}")
            return output_file
        else:
            print("❌ No email-API key pairs found")
            return None
            
    except Exception as e:
        print(f"❌ Error generating mapping: {e}")
        return None


def create_payload(api_key, start_date, end_date):
    """Create request payload for a specific API key"""
    return {
        "service_key": SERVICE_KEY,
        "query_requests": [
            {
                "data_source": "QUERY_DATA_SOURCE_CASCADE_DATA",
                "selections": [
                    {"field": "api_key", "name": "api_key"},
                    {"field": "date", "name": "date"},
                    {"field": "flex_credits_used", "name": "flex_credits_used"},
                    {"field": "model", "name": "model"}
                ],
                "filters": [
                    {"name": "date", "filter": "QUERY_FILTER_GE", "value": start_date},
                    {"name": "date", "filter": "QUERY_FILTER_LE", "value": end_date},
                    {"name": "api_key", "filter": "QUERY_FILTER_EQUAL", "value": api_key}
                ]
            }
        ]
    }


def fetch_data_for_api_key(api_key, start_date, end_date):
    """Fetch data for a single API key"""
    payload = create_payload(api_key, start_date, end_date)
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = []
        if "queryResults" in data and data["queryResults"]:
            for query_result in data["queryResults"]:
                if "responseItems" in query_result:
                    for response_item in query_result["responseItems"]:
                        if "item" in response_item:
                            items.append(response_item["item"])
        
        return api_key, items
    except:
        return api_key, []


def fetch_parallel(api_keys, start_date, end_date, max_workers=20):
    """Fetch data in parallel for multiple API keys"""
    all_items = []
    active_users = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_data_for_api_key, key, start_date, end_date): key 
                   for key in api_keys}
        
        # Progress bar with tqdm
        with tqdm(total=len(api_keys), desc="📊 Processing users", 
                  unit="user", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
            
            for future in as_completed(futures):
                api_key, items = future.result()
                
                if items:
                    all_items.extend(items)
                    active_users += 1
                    pbar.set_postfix({'active': active_users, 'data_points': len(all_items)})
                
                pbar.update(1)
    
    print(f"\n✅ Complete! Processed {len(api_keys)} users | Active: {active_users} | Data points: {len(all_items)}\n")
    
    return all_items


def aggregate_by_date_and_model(items):
    """Aggregate flex credits by date and model"""
    # Structure: {date: {model: flex_credits}}
    daily_model_data = defaultdict(lambda: defaultdict(float))
    
    for item in items:
        date = item.get("date", "")
        model = item.get("model", "unknown")
        
        if not date:
            continue
        
        # Only flex credits (convert from hundredths)
        flex_credits = float(item.get("flex_credits_used", 0) or 0) / 100
        
        daily_model_data[date][model] += flex_credits
    
    return daily_model_data


def format_date_for_display(date_str):
    """Format date for display"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%B %d, %Y")
    except:
        return date_str


def save_results(daily_model_data, month_name, year):
    """Save results to CSV"""
    sorted_dates = sorted(daily_model_data.keys())
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    csv_filename = os.path.join(OUTPUT_DIR, f"flex_credits_by_model_{month_name.lower()}_{year}_{current_date}.csv")
    
    # Prepare rows for CSV
    rows = []
    all_models = set()
    
    for date in sorted_dates:
        for model, flex_credits in daily_model_data[date].items():
            all_models.add(model)
            friendly_name = get_friendly_model_name(model)
            rows.append({
                'event_date': date,
                'date_formatted': format_date_for_display(date),
                'model_internal': model,
                'model_name': friendly_name,
                'flex_credits': flex_credits
            })
    
    # Sort rows by date, then by flex_credits descending
    rows.sort(key=lambda x: (x['event_date'], -x['flex_credits']))
    
    # Save to CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['event_date', 'date_formatted', 'model_internal', 'model_name', 'flex_credits'])
        writer.writeheader()
        
        for row in rows:
            writer.writerow({
                'event_date': row['event_date'],
                'date_formatted': row['date_formatted'],
                'model_internal': row['model_internal'],
                'model_name': row['model_name'],
                'flex_credits': f"{row['flex_credits']:.2f}"
            })
    
    print(f"✅ Report saved: {csv_filename}\n")
    
    # Print summary by date
    print("=" * 100)
    print(f"FLEX CREDITS BY MODEL - {month_name.upper()} {year}")
    print("=" * 100)
    
    # Calculate totals per model across all dates
    model_totals = defaultdict(float)
    grand_total = 0
    
    for date in sorted_dates:
        date_formatted = format_date_for_display(date)
        date_total = 0
        
        print(f"\n📅 {date} - {date_formatted}")
        print("-" * 100)
        
        # Sort models by flex credits descending for this date
        models_for_date = sorted(daily_model_data[date].items(), key=lambda x: -x[1])
        
        for model, flex_credits in models_for_date:
            if flex_credits > 0:  # Only show models with flex credits usage
                friendly_name = get_friendly_model_name(model)
                print(f"   {friendly_name:<60} {flex_credits:>15,.2f}")
                model_totals[model] += flex_credits
                date_total += flex_credits
        
        print(f"   {'DAILY TOTAL':<60} {date_total:>15,.2f}")
        grand_total += date_total
    
    # Print totals by model
    print("\n" + "=" * 100)
    print("TOTALS BY MODEL")
    print("=" * 100)
    
    sorted_models = sorted(model_totals.items(), key=lambda x: -x[1])
    for model, total in sorted_models:
        friendly_name = get_friendly_model_name(model)
        percentage = (total / grand_total * 100) if grand_total > 0 else 0
        print(f"{friendly_name:<60} {total:>15,.2f}  ({percentage:>5.1f}%)")
    
    print("-" * 100)
    print(f"{'GRAND TOTAL':<50} {grand_total:>15,.2f}  (100.0%)")
    print("=" * 100)
    
    # Statistics
    print(f"\n📊 Statistics:")
    print(f"   - Days with data: {len(sorted_dates)}")
    print(f"   - Total models used: {len(all_models)}")
    print(f"   - Total flex credits: {grand_total:,.2f}")
    if len(sorted_dates) > 0:
        print(f"   - Avg flex credits/day: {grand_total / len(sorted_dates):,.2f}")
    
    days_with_flex = [d for d in sorted_dates if sum(daily_model_data[d].values()) > 0]
    if days_with_flex:
        print(f"\n⚠️  Days with flex credits: {len(days_with_flex)}")
    else:
        print(f"\n✅ No flex credits used in {month_name} {year}")


def main():
    parser = argparse.ArgumentParser(
        description='Flex Credits by Model - Daily breakdown per language model',
        epilog='Examples:\n'
               '  python flex_credits_by_model.py --year 2025 --month 9\n'
               '  python flex_credits_by_model.py --year 2025 --month 9 --workers 50',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--year', type=int, help='Year (e.g., 2025)')
    parser.add_argument('--month', type=int, help='Month (1-12)')
    parser.add_argument('--start-date', type=str, help='Start date YYYY-MM-DD')
    parser.add_argument('--end-date', type=str, help='End date YYYY-MM-DD')
    parser.add_argument('--workers', type=int, default=20, help='Parallel workers (default: 20)')
    parser.add_argument('--json-file', type=str, help='Custom email mapping file')
    
    args = parser.parse_args()
    
    # Determine date range
    if args.start_date and args.end_date:
        start_date = parse_date(args.start_date)
        end_date = parse_date(args.end_date)
        month_name = datetime.strptime(start_date, "%Y-%m-%d").strftime("%B")
        year = datetime.strptime(start_date, "%Y-%m-%d").year
    elif args.year and args.month:
        if not 1 <= args.month <= 12:
            print("Error: Month must be 1-12")
            return
        start_date, end_date = get_month_date_range(args.year, args.month)
        month_name = datetime(args.year, args.month, 1).strftime("%B")
        year = args.year
    else:
        print("Using default: September 2025")
        start_date, end_date = get_month_date_range(2025, 9)
        month_name = "September"
        year = 2025
    
    print(f"\n{'='*100}")
    print(f"FLEX CREDITS BY MODEL - {month_name.upper()} {year}")
    print(f"{'='*100}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"Parallel workers: {args.workers}\n")
    
    # Load API keys
    json_file = args.json_file or find_latest_email_mapping_file()
    if not json_file:
        print("⚠️  No email_api_mapping file found")
        print("Attempting to generate one...\n")
        json_file = generate_email_api_mapping()
        if not json_file:
            print("❌ Failed to generate email_api_mapping file")
            return
    
    print(f"Loading: {json_file}")
    api_key_email_map = read_api_keys_from_json(json_file)
    api_keys = list(api_key_email_map.keys())
    
    if not api_keys:
        print("❌ No API keys found")
        return
    
    print(f"Loaded: {len(api_keys)} API keys\n")
    
    # Fetch data in parallel
    print("🚀 Starting parallel data fetch...")
    print(f"⚡ Using {args.workers} workers for maximum speed\n")
    items = fetch_parallel(api_keys, start_date, end_date, args.workers)
    
    if not items:
        print("❌ No data retrieved")
        return
    
    # Aggregate by date and model
    print("📊 Aggregating results by date and model...")
    daily_model_data = aggregate_by_date_and_model(items)
    
    if not daily_model_data:
        print("❌ No flex credits data found")
        return
    
    # Save and display results
    print("💾 Saving results to CSV...")
    save_results(daily_model_data, month_name, year)
    
    print(f"\n✨ Complete!")


if __name__ == "__main__":
    main()
