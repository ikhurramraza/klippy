# 📋 Klippy

A command line utility that acts like a cloud clipboard.

## 💽 Installation

```bash
pip install klippy
```

## 📖 Usage

```bash
# Configure namespace name and Redis credentials
# To share a single Redis server among different people
# or have multiple clipboards, use different namespaces.
klippy configure

# Check the configuration and the connection to the Redis server
klippy doctor

# Copy data to the cloud clipboard (Redis database)
klippy copy file.png
klippy copy < file.txt
echo "$PATH" | klippy copy

# Copy data that expires after a duration (e.g. 90s, 5m, 2h, 1d)
klippy copy --expire 1h file.png

# Paste data from the clipboard (Redis database)
klippy paste file.png
klippy paste > file.txt
klippy paste | cat

# Clear the clipboard
klippy clear
```

## 🛠️ Development

This repo ships a [DevPod](https://devpod.sh/)-compatible devcontainer that provisions
Python 3.14, a Redis sidecar (pre-configured so `klippy doctor` passes out of the box),
and the Claude CLI. Your Claude login is stored on a named volume, so you only authenticate
once even across rebuilds.

```bash
# Start the workspace without launching an IDE
devpod up . --ide none

# Drop into a shell (the venv auto-activates on login)
devpod ssh klippy
```

Inside the container, the project is at `/workspaces/klippy` with everything on `PATH`:

```bash
pytest                      # run the test suite (uses fakeredis, no Redis needed)
ruff check . && black .     # lint and format
klippy doctor               # verify the connection to the Redis sidecar
echo "hello" | klippy copy && klippy paste

claude                      # the Claude CLI, ready to use
```

Edit with vim/your editor of choice over SSH. To rebuild from scratch (auth still
persists): `devpod up . --recreate --ide none`.

## 🧞‍♂️ Wishlist

- Introduce clipboard history

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
