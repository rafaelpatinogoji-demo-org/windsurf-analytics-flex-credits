#!/usr/bin/env python3
"""
Team Monthly Credits Summary
Aggregate flex credits and prompt credits by month for a date range.
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

# Define output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

if not SERVICE_KEY:
    raise ValueError("SERVICE_KEY not found in .env file")

API_URL = "https://server.codeium.com/api/v1/Analytics"


def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Please use YYYY-MM-DD format.")


def get_month_range(year, start_month, end_month):
    """Get start and end dates for a range of months"""
    start_date = datetime(year, start_month, 1)
    
    if end_month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
    
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def find_latest_email_mapping_file():
    """Find the latest email_api_mapping file"""
    import glob
    
    local_pattern = os.path.join(OUTPUT_DIR, 'email_api_mapping_*.json')
    files = glob.glob(local_pattern)
    
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
        with tqdm(total=100, desc="⏳ Requesting data", bar_format='{desc}: {bar}', ncols=50) as pbar:
            response = requests.post(url, json=payload, headers=headers)
            pbar.update(50)
            response.raise_for_status()
            data = response.json()
            pbar.update(50)
        
        email_api_map = {}
        
        if "userTableStats" in data and isinstance(data["userTableStats"], list):
            for user in data["userTableStats"]:
                if "email" in user and user["email"] and "apiKey" in user and user["apiKey"]:
                    email_api_map[user["email"]] = user["apiKey"]
        
        print(f"Found {len(email_api_map)} unique email-API key pairs")
        
        if email_api_map:
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
                    {"field": "prompts_used", "name": "prompts_used"},
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


def safe_float(value):
    """Safely convert value to float, handling None, '<nil>', empty strings, etc."""
    if value is None or value == '' or value == '<nil>':
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def aggregate_by_month(items):
    """Aggregate items by month (YYYY-MM format)"""
    monthly_data = defaultdict(lambda: {
        "total_flex_credits": 0,
        "total_prompt_credits": 0,
        "total_credits_used": 0,
        "data_points": 0
    })
    
    for item in items:
        date = item.get("date", "")
        if not date:
            continue
        
        # Extract month (YYYY-MM) from date (YYYY-MM-DD)
        month = date[:7]
        
        flex_credits = safe_float(item.get("flex_credits_used")) / 100
        prompt_credits = safe_float(item.get("prompts_used")) / 100
        
        monthly_data[month]["total_flex_credits"] += flex_credits
        monthly_data[month]["total_prompt_credits"] += prompt_credits
        monthly_data[month]["total_credits_used"] += (flex_credits + prompt_credits)
        monthly_data[month]["data_points"] += 1
    
    return monthly_data


def format_month_for_display(month_str):
    """Format month as 'September 2025'"""
    try:
        dt = datetime.strptime(month_str + "-01", "%Y-%m-%d")
        return dt.strftime("%B %Y")
    except:
        return month_str


def save_results(monthly_data, start_date, end_date):
    """Save results to CSV"""
    sorted_months = sorted(monthly_data.keys())
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Extract period for filename
    start_month = start_date[:7]
    end_month = end_date[:7]
    period_str = f"{start_month}_to_{end_month}".replace("-", "")
    
    csv_filename = os.path.join(OUTPUT_DIR, f"team_monthly_credits_{period_str}_{current_date}.csv")
    
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'month', 'month_formatted', 'total_flex_credits', 
            'total_prompt_credits', 'total_credits_used', 'data_points'
        ])
        writer.writeheader()
        
        for month in sorted_months:
            data = monthly_data[month]
            writer.writerow({
                'month': month,
                'month_formatted': format_month_for_display(month),
                'total_flex_credits': f"{data['total_flex_credits']:.2f}",
                'total_prompt_credits': f"{data['total_prompt_credits']:.2f}",
                'total_credits_used': f"{data['total_credits_used']:.2f}",
                'data_points': data['data_points']
            })
    
    print(f"✅ Report saved: {csv_filename}\n")
    
    # Print summary table
    print("=" * 120)
    print(f"TEAM MONTHLY CREDITS SUMMARY")
    print("=" * 120)
    print(f"Period: {format_month_for_display(sorted_months[0])} to {format_month_for_display(sorted_months[-1])}")
    print("=" * 120)
    print(f"\n{'Month':<20} {'Flex Credits':>18} {'Prompt Credits':>18} {'Total Credits':>18} {'Data Points':>15}")
    print("-" * 120)
    
    grand_total_flex = 0
    grand_total_prompt = 0
    grand_total_credits = 0
    grand_total_points = 0
    
    for month in sorted_months:
        data = monthly_data[month]
        month_formatted = format_month_for_display(month)
        print(f"{month_formatted:<20} {data['total_flex_credits']:>18,.2f} {data['total_prompt_credits']:>18,.2f} {data['total_credits_used']:>18,.2f} {data['data_points']:>15,}")
        
        grand_total_flex += data['total_flex_credits']
        grand_total_prompt += data['total_prompt_credits']
        grand_total_credits += data['total_credits_used']
        grand_total_points += data['data_points']
    
    print("-" * 120)
    print(f"{'TOTAL':<20} {grand_total_flex:>18,.2f} {grand_total_prompt:>18,.2f} {grand_total_credits:>18,.2f} {grand_total_points:>15,}")
    print("=" * 120)
    
    print(f"\n📊 Statistics:")
    print(f"   - Total months with data: {len(sorted_months)}")
    print(f"   - Total flex credits: {grand_total_flex:,.2f}")
    print(f"   - Total prompt credits: {grand_total_prompt:,.2f}")
    print(f"   - Total credits used: {grand_total_credits:,.2f}")
    if len(sorted_months) > 0:
        print(f"   - Average credits per month: {grand_total_credits / len(sorted_months):,.2f}")
    
    months_with_flex = [m for m in sorted_months if monthly_data[m]['total_flex_credits'] > 0]
    if months_with_flex:
        print(f"\n⚠️  Months with flex credits: {len(months_with_flex)} of {len(sorted_months)}")
    else:
        print(f"\n✅ No flex credits used in any month")


def main():
    parser = argparse.ArgumentParser(
        description='Team Monthly Credits - Aggregate by month for date range',
        epilog='Examples:\n'
               '  python team_monthly_credits.py --year 2025 --start-month 6 --end-month 10\n'
               '  python team_monthly_credits.py --start-date 2025-06-01 --end-date 2025-10-31 --workers 50',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--year', type=int, help='Year (e.g., 2025)')
    parser.add_argument('--start-month', type=int, help='Start month (1-12)')
    parser.add_argument('--end-month', type=int, help='End month (1-12)')
    parser.add_argument('--start-date', type=str, help='Start date YYYY-MM-DD')
    parser.add_argument('--end-date', type=str, help='End date YYYY-MM-DD')
    parser.add_argument('--workers', type=int, default=20, help='Parallel workers (default: 20)')
    parser.add_argument('--json-file', type=str, help='Custom email mapping file')
    
    args = parser.parse_args()
    
    # Determine date range
    if args.start_date and args.end_date:
        start_date = parse_date(args.start_date)
        end_date = parse_date(args.end_date)
    elif args.year and args.start_month and args.end_month:
        if not (1 <= args.start_month <= 12 and 1 <= args.end_month <= 12):
            print("Error: Months must be between 1-12")
            return
        if args.start_month > args.end_month:
            print("Error: Start month must be <= end month")
            return
        start_date, end_date = get_month_range(args.year, args.start_month, args.end_month)
    else:
        print("Error: Must provide either --start-date/--end-date or --year/--start-month/--end-month")
        return
    
    print(f"\n{'='*120}")
    print(f"TEAM MONTHLY CREDITS SUMMARY")
    print(f"{'='*120}")
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
    
    # Aggregate by month
    print("📊 Aggregating results by month...")
    monthly_data = aggregate_by_month(items)
    
    if not monthly_data:
        print("❌ No data to aggregate")
        return
    
    # Save and display results
    print("💾 Saving results to CSV...")
    save_results(monthly_data, start_date, end_date)
    
    print(f"\n✨ Complete!")


if __name__ == "__main__":
    main()
