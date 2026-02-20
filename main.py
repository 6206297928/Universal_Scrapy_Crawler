import json
from universal.utils.chunker import ContentChunker


chunker = ContentChunker()


def process_file(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_chunks = []

    for doc in data:

        if doc["length"] < 200:
            continue

        chunks = chunker.chunk_document(
            url=doc["url"],
            title=doc["title"],
            content=doc["content"],
            domain=doc.get("domain")
        )

        all_chunks.extend(chunks)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Created {len(all_chunks)} chunks")


if __name__ == "__main__":

    process_file(
        "output.json",
        "chunks.json"
    )
