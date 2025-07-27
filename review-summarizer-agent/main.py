import argparse
import json
from review_summarizer import ReviewSummarizer
from data_handler import DataHandler


def main():
    parser = argparse.ArgumentParser(description="Review Summarizer AI Agent")
    parser.add_argument("--input", "-i", help="Input file path (JSON or CSV)")
    parser.add_argument("--output", "-o", default="summary.json", help="Output file path")
    parser.add_argument("--place", "-p", default="", help="Place name")
    parser.add_argument("--create-sample", action="store_true", help="Create sample reviews")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    summarizer = ReviewSummarizer()
    data_handler = DataHandler()

    if args.create_sample:
        data_handler.create_sample_reviews("sample_reviews.json")
        print("Sample reviews created! Run with --input sample_reviews.json")
        return

    if args.interactive:
        interactive_mode(summarizer)
        return

    if not args.input:
        print("Please provide input file with --input or use --create-sample to generate test data")
        return

    # Load reviews
    if args.input.endswith('.json'):
        data = data_handler.load_reviews_from_json(args.input)
        if data and isinstance(data, list) and 'reviews' in data[0]:
            reviews = data[0]['reviews']
            place_name = data[0].get('place_name', args.place)
        else:
            reviews = [item.get('review', str(item)) for item in data]
            place_name = args.place
    elif args.input.endswith('.csv'):
        reviews = data_handler.load_reviews_from_csv(args.input)
        place_name = args.place
    else:
        print("Unsupported file format. Use JSON or CSV.")
        return

    if not reviews:
        print("No reviews found in the input file.")
        return

    print(f"Processing {len(reviews)} reviews for: {place_name or 'Unknown Place'}")
    print("Generating summary...")

    # Generate summary
    result = summarizer.summarize_reviews(reviews, place_name)

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    # Display results
    print("\n" + "=" * 50)
    print("REVIEW SUMMARY")
    print("=" * 50)
    print(f"Place: {result['place_name']}")
    print(f"Total Reviews: {result['total_reviews']}")
    print(f"Overall Sentiment: {result['sentiment']}")
    print("\nSummary:")
    print(result['summary'])

    # Save results
    data_handler.save_summary(result, args.output)


def interactive_mode(summarizer):
    """Interactive mode for manual review input"""
    print("Interactive Review Summarizer")
    print("Enter reviews one by one. Type 'DONE' when finished.")

    reviews = []
    place_name = input("Enter place name (optional): ").strip()

    while True:
        review = input(f"\nEnter review #{len(reviews) + 1} (or 'DONE' to finish): ").strip()
        if review.upper() == 'DONE':
            break
        if review:
            reviews.append(review)

    if not reviews:
        print("No reviews entered.")
        return

    print(f"\nProcessing {len(reviews)} reviews...")
    result = summarizer.summarize_reviews(reviews, place_name)

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(result['summary'])


if __name__ == "__main__":
    main()