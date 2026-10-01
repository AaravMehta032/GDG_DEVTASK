
import argparse
import json
import secrets
import string
from pathlib import Path
from urllib.parse import urlparse

BASE_URL = "https://sho.rt/"
CODE_LENGTH = 8
CODE_CHARACTERS = string.ascii_letters + string.digits


def load_records(data_file):
    if not data_file.exists():
        return []

    with data_file.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list) or any(
        not isinstance(record, dict)
        or not isinstance(record.get("url"), str)
        or not isinstance(record.get("short_url"), str)
        for record in records
    ):
        raise ValueError("The JSON file must contain a list of URL records.")

    return records


def save_records(data_file, records):
    data_file.parent.mkdir(parents=True, exist_ok=True)

    with data_file.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)
        file.write("\n")


def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def create_short_url(records):
    existing_urls = {record["short_url"] for record in records}

    while True:
        code = "".join(
            secrets.choice(CODE_CHARACTERS)
            for _ in range(CODE_LENGTH)
        )

        short_url = BASE_URL + code

        if short_url not in existing_urls:
            return short_url


def shorten_url(data_file, records):
    url = input("Enter the URL to shorten: ").strip()

    if not is_valid_url(url):
        print("Please enter a valid URL starting with http:// or https://.")
        return

    # Check whether this URL already exists
    existing = next(
        (record for record in records if record["url"] == url),
        None
    )

    if existing:
        short_url = existing["short_url"]

        # Extract only the code from the shortened URL
        code = short_url[len(BASE_URL):]

        print(f"Shortened URL: {short_url}")
        print(f"Code: {code}")
        return

    # Create a new shortened URL
    short_url = create_short_url(records)

    # Extract only the 8-character code
    code = short_url[len(BASE_URL):]

    records.append({
        "url": url,
        "short_url": short_url
    })

    save_records(data_file, records)

    print(f"Shortened URL: {short_url}")
    print(f"Code: {code}")


def show_records(records):
    if not records:
        print("No records found.")
        return

    print(json.dumps(records, indent=2))


def delete_record(data_file, records):
    print("\nDelete using:")
    print("1. Original URL")
    print("2. Shortened URL")
    print("3. Code")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        value = input("Enter the original URL: ").strip()

        matching_record = next(
            (record for record in records if record["url"] == value),
            None
        )

    elif choice == "2":
        value = input("Enter the shortened URL: ").strip()

        matching_record = next(
            (record for record in records if record["short_url"] == value),
            None
        )

    elif choice == "3":
        value = input("Enter the 8-character code: ").strip()

        short_url = BASE_URL + value

        matching_record = next(
            (
                record
                for record in records
                if record["short_url"] == short_url
            ),
            None
        )

    else:
        print("Please choose 1, 2, or 3.")
        return

    if matching_record is None:
        print("No matching record was found.")
        return

    records.remove(matching_record)
    save_records(data_file, records)

    print("Record deleted.")


def main():
    parser = argparse.ArgumentParser(
        description="A JSON-backed command-line URL shortener."
    )

    parser.add_argument(
        "--data",
        type=Path,
        default=Path(__file__).with_name("urls.json"),
        help="path to the JSON data file (default: urls.json beside this script)",
    )

    args = parser.parse_args()

    try:
        records = load_records(args.data)

    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(f"could not load {args.data}: {error}")

    while True:
        print("\nURL Shortener")
        print("1. Shorten a URL")
        print("2. Show records as JSON")
        print("3. Delete a record")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                shorten_url(args.data, records)

            elif choice == "2":
                show_records(records)

            elif choice == "3":
                delete_record(args.data, records)

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("Please choose 1, 2, 3, or 4.")

        except OSError as error:
            print(f"Could not save the JSON data: {error}")


if __name__ == "__main__":
    main()

