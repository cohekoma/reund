
from ollama import Client

client = Client(host="http://localhost:11434")

MODEL = "translategemma:4b"

GLOSSARY = {
    "Docker image": "Docker image",
    "API endpoint": "API endpoint",
    "race condition": "race condition",
    "dependency injection": "dependency injection",
    "thread pool": "thread pool",
}


def build_prompt(text: str, use_glossary: bool = False) -> str:
    instructions = (
        "You are a professional English (en) to Vietnamese (vi) translator. "
        "Your goal is to accurately convey the meaning and nuances of the "
        "original English text while adhering to Vietnamese grammar, "
        "vocabulary, and cultural sensitivities.\n"
        "Produce only the Vietnamese translation, without any additional "
        "explanations or commentary."
    )

    if use_glossary:
        terms = "\n".join(
            f"- {source}: {target}"
            for source, target in GLOSSARY.items()
            if source.lower() in text.lower()
        )

        if terms:
            instructions += (
                "\nPreserve these technical terms exactly as specified:\n"
                f"{terms}"
            )

    instructions += (
        "\nPlease translate the following English text into Vietnamese:"
    )
    
    return f"{instructions}\n\n\n{text}"


def translate(text: str, use_glossary: bool = False) -> str:
    response = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": build_prompt(text, use_glossary),
            }
        ],
        options={
            "temperature": 0,
        },
    )

    return response.message.content or ""


if __name__ == "__main__":
    source = """
    Dependency injection is a design pattern that helps
    reduce coupling between components.

    In Spring Boot, dependency injection is commonly
    implemented through the IoC container.

    A race condition occurs when multiple threads
    access shared resources concurrently.
    """

    print("=== BASELINE TRANSLATION ===")
    print(translate(source))

    print("\n=== WITH GLOSSARY ===")
    print(translate(source, use_glossary=True))
