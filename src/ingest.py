from pathlib import Path

DOCUMENT_DIR = Path("data/documents")


def load_documents():
    documents = []

    for file_path in DOCUMENT_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        document = {
            "text": text,
            "source": file_path.name
        }

        documents.append(document)

    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(docs)