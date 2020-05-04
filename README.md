# Klippy

![Test](https://github.com/ikhurramraza/klippy/workflows/Test/badge.svg)

A command line utility that acts like a cloud clipboard.

## Installation

```bash
pip install klippy
```

## Usage

```bash
# Find help
klippy --help
klippy configure --help
klippy copy --help
klippy paste --help

# Configure namespace name and Redis credentials
# To share a single Redis server among different people
# or have multiple clipboards, use different namespaces.
klippy configure

# Copy data to the cloud clipboard (Redis database)
klippy copy file.png
klippy copy < file.txt
echo "$PATH" | klippy copy

# Paste data from the clipboard (Redis database)
klippy paste file.png
klippy paste > file.txt
klippy paste | cat
```

## Wishlist

- Introduce clipboard history

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

