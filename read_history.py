import json
import argparse

def load_history():
    with open("data/history.json", "r") as f:
        return json.load(f)

def print_run(run):
    print("\n=== RUN DETAILS ===")
    print("Run ID:", run.get("run_id"))
    print("Timestamp:", run.get("timestamp"))
    print("\nSelected Idea:")
    print(run["selection"]["selected_idea"])
    print("\nReasoning:")
    print(run["selection"]["reasoning"])
    print("\n--- END ---\n")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--last", action="store_true", help="Show last run")
    parser.add_argument("--first", action="store_true", help="Show first run")
    parser.add_argument("--index", type=int, help="Show run by index")
    parser.add_argument("--id", type=str, help="Show run by run_id")
    parser.add_argument("--list", action="store_true", help="List all runs")
    parser.add_argument("--summary", action="store_true", help="Show summary of selected ideas")
    parser.add_argument("--search", type=str, help="Search keyword in all runs")
    parser.add_argument("--export", type=str, help="Export a run to a separate JSON file") 
    parser.add_argument("--stats", action="store_true", help="Show statistics about all runs")
    parser.add_argument("--investments", action="store_true", help="Show all investment runs")

 

    args = parser.parse_args()
    data = load_history()
    runs = data.get("runs", [])

    if not runs:
        print("No runs found in history.")
        return

    # LIST ALL RUNS
    if args.list:
        print("\n=== ALL RUNS ===")
        for i, run in enumerate(runs):
            print(f"Index: {i} | Run ID: {run.get('run_id')} | Timestamp: {run.get('timestamp')}")
        return

    # SUMMARY
    if args.summary:
        print("\n=== SUMMARY OF SELECTED IDEAS ===")
        for i, run in enumerate(runs):
            idea = run["selection"]["selected_idea"]["title"]
            print(f"Run {i}: {idea}")
        return

    # SEARCH
    if args.search:
        keyword = args.search.lower()
        print(f"\n=== SEARCH RESULTS FOR '{keyword}' ===")
        found = False
        for i, run in enumerate(runs):
            text = json.dumps(run).lower()
            if keyword in text:
                print(f"Found in run {i} (Run ID: {run.get('run_id')})")
                found = True
        if not found:
            print("No matches found.")
        return

    # EXPORT
    if args.export:
        for run in runs:
            if run.get("run_id") == args.export:
                filename = f"export_{args.export}.json"
                with open(filename, "w") as f:
                    json.dump(run, f, indent=4)
                print(f"Run exported to {filename}")
                return
        print("Run ID not found.")
        return

    # LAST RUN
    if args.last:
        print_run(runs[-1])
        return

    # FIRST RUN
    if args.first:
        print_run(runs[0])
        return

    # RUN BY INDEX
    if args.index is not None:
        if 0 <= args.index < len(runs):
            print_run(runs[args.index])
        else:
            print("Invalid index.")
        return

    # RUN BY ID
    if args.id:
        for run in runs:
            if run.get("run_id") == args.id:
                print_run(run)
                return
        print("Run ID not found.")
        return
    
    if args.stats:
        print("\n=== RUN STATISTICS ===")
        print("Total runs:", len(runs))

    idea_counts = {}
    for run in runs:
        idea = run["selection"]["selected_idea"]["title"]
        idea_counts[idea] = idea_counts.get(idea, 0) + 1

        print("\nMost common selected ideas:")
    for idea, count in idea_counts.items():
        print(f"{idea}: {count} times")

    return
    if args.investments:
        print("\n=== ALL INVESTMENT RUNS ===")
    for i, run in enumerate(runs):
        budget = run.get("input_budget", "unknown")
        idea = run["selection"]["selected_idea"]["title"]
        print(f"Run {i}: Budget ${budget} → Selected Idea: {idea}")
    return



    print("No option selected. Use --list, --last, --first, --index, --id, --summary, --search, or --export.")

if __name__ == "__main__":
    main()
