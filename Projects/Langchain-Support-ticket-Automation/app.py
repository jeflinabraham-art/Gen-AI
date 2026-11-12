import json
import sys
from pathlib import Path

from src.llms import create_llm
from src.workflow import build_workflow, process_ticket


# File paths relative to the project root.
INPUT_FILE = Path("src/data/support_tickets.json")
OUTPUT_FILE = Path("src/data/output/support_ticket_results.json")


def load_tickets():
    # Check whether the input file exists.
    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")

        # sys.exit(1) terminates your Python program.
        # Why 1? It conventionally indicates that the program terminated because of an error. 0 conventionally means success.
        sys.exit(1)

    # Read and parse the JSON file.
    try:
        with INPUT_FILE.open("r", encoding="utf-8") as file:
            # json.load(file) reads the JSON content from a file and converts it into Python objects (list of dictionaries).
            tickets = json.load(file)

    except json.JSONDecodeError as error:
        print(f"ERROR: Invalid JSON: {error}")
        sys.exit(1)

    # 2 checks heppen here:
    # Checks whether tickets is a Python list.
    # Checks whether the list is empty.
    if not isinstance(tickets, list) or not tickets:
        print("ERROR: The input file must contain a non-empty list.")
        sys.exit(1)

    return tickets


def save_results(results):
    # model_dump() converts a Pydantic model into a normal Python dictionary.
    # For every result in the results list, convert that result into a dictionary and collect all dictionaries into a new list.
    serializable = []
    for result in results:
        dictionary = result.model_dump()
        serializable.append(dictionary)

    # Write the results to the output JSON file.
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(serializable, file, indent=2)

    return OUTPUT_FILE


def main():
    print("=" * 40)
    print("AI SUPPORT TICKET AUTOMATION")
    print("=" * 40)

    # 1. Load tickets from the input JSON file.
    tickets = load_tickets()
    print(f"Loaded {len(tickets)} tickets.")

    # 2. Initialize the LLM and build the workflow once.
    llm = create_llm()
    workflow = build_workflow(llm)

    results = []

    # 3. Process tickets one by one.
    for ticket in tickets:
        ticket_id = ticket.get("ticket_id", "UNKNOWN")
        print(f"\nProcessing ticket: {ticket_id}")

        try:
            result = process_ticket(ticket, workflow)
            results.append(result)

        except Exception as error:
            print(f"ERROR processing {ticket_id}: {error}")
            continue

    # 4. Save successful results.
    if not results:
        print("No tickets were processed successfully.")
        sys.exit(1)

    output_path = save_results(results)

    print("\n" + "=" * 40)
    print("Processing complete!")
    print(f"Results saved to: {output_path}")
    print("=" * 40)


if __name__ == "__main__":
    main()



# Function	                 Purpose
# json.load(file)	         JSON file → Python object
# json.dump(data, file)	     Python object → JSON file
# json.loads(text)	         JSON string → Python object
# json.dumps(data)	         Python object → JSON string
