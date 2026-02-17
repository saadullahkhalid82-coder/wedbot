from services.wedding_content_ai import generate_wedding_content


def main() -> None:
    content = generate_wedding_content(
        content_type="Wedding Vows",
        tone="romantic",
        couple_names="Ayesha & Ali",
        extra_context="They met during university and value family and laughter.",
    )

    print("=== AI GENERATED WEDDING CONTENT ===\n")
    print(content)


if __name__ == "__main__":
    main()
