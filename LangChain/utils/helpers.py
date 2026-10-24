import time

def print_separator(length: int = 60):
    print("=" * length)

def print_title(title: str):
    print_separator()
    print(title)
    print_separator()

def execution_time(start_time: float):
    print(f"\nExecution Time: {time.time() - start_time:.2f} seconds")

def get_response_content(response) -> None:
    content = response.content

    # Case 1: Content is already a string
    if isinstance(content, str):
        print(content)
        return None

    # Case 2: Content is a list
    if isinstance(content, str):
        print(content)
    else:
        for block in content:
            if block.get("type") == "text":
                print(block["text"])
                return None