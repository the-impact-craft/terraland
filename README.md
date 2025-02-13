![Command Center](https://img.shields.io/badge/terraform%20command%20center-45d298?logo=terraform&logoColor=white)
[![Maintainability](https://api.codeclimate.com/v1/badges/62ef5aeefc01a2c5521b/maintainability)](https://codeclimate.com/repos/67ab4de0fe407500a7cecccf/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/62ef5aeefc01a2c5521b/test_coverage)](https://codeclimate.com/repos/67ab4de0fe407500a7cecccf/test_coverage)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# Terry - The Visual Terraform CLI

Terry is a sleek and minimalistic CLI editor for Terraform, designed to enhance your workflow with an intuitive UI and real-time validation. Whether you're managing complex infrastructure or just getting started with Terraform, Terry provides a smooth experience right from your terminal.


![](https://github.com/the-impact-craft/terry/blob/main/media/demo1.gif)


## 🚀 Features

- 🌎 **Workspace Management**: Easily switch between different Terraform workspaces.
- 📂 **Project Explorer**: View your Terraform files and directory structure effortlessly.
- ✅ **Real-time Validation**: Execute `init`, `plan`, `apply`, `validate` and more using ui buttons or shortcut keys.
- 🖥️ **Minimalist UI**: A clean and distraction-free interface built using the Textual framework.

## 🛠 Installation

```bash
pip install terry-cli
```

## 📌 Usage

```bash
terry
```

Navigate through workspaces, view state files, and manage your Terraform infrastructure—all from a single, interactive terminal interface.

## 🎯 Shortcuts

- `Ctrl + f` - Search
- `Ctrl + Q` - Quit the app

[//]: Others to be added

## 🤝 Contributing

We welcome contributions! Feel free to open discussions to share your ideas.

## 📜 License

Terry is released under the MIT License.

---

🚀 Get started with Terry and simplify your Terraform workflow!




## Development instructions


Install requirements:

```bash
pip install -r requirements/requirements-dev.txt
```

Run in dev mode:

```bash
pip install textual-dev
cd src
export PYTHONPATH="$PYTHONPATH:$PWD" && 
textual run --dev terry/presentation/cli/app.py
```

Run tests:

```bash 
coverage run && coverage report -m
```

Open html report:

```bash
coverage html && open htmlcov/index.html
```