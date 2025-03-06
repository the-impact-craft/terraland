![Command Center](https://img.shields.io/badge/terraform%20command%20center-45d298?logo=terraform&logoColor=white)
[![Maintainability](https://qlty.sh/badges/cd586ab2-d5b8-438e-ad72-48ffcb996370/maintainability.svg)](https://qlty.sh/gh/the-impact-craft/projects/terraland)
[![Test Coverage](https://api.codeclimate.com/v1/badges/62ef5aeefc01a2c5521b/test_coverage)](https://codeclimate.com/repos/67ab4de0fe407500a7cecccf/test_coverage)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# TerraLand - The Visual Terraform CLI

TerraLand is a sleek and minimalistic CLI editor for Terraform, designed to enhance your workflow with an intuitive UI and real-time validation. Whether you're managing complex infrastructure or just getting started with Terraform, TerraLand provides a smooth experience right from your terminal.

## 🚀 Features

- 🌎 **Workspace Management**: Easily switch between different Terraform workspaces.
    ![switch_workspace.gif](media/switch_workspace.gif)[](https://github.com/the-impact-craft/terraland/blob/main/media/demo1.gif)


- 📂 **Project Explorer**: View your Terraform files and directory structure effortlessly.
    ![preview_files.gif](media/preview_files.gif)


- ✅ **Real-time Validation**: Execute `init`, `plan`, `apply`, `validate` and more using ui buttons or shortcut keys.
    <p float="left">
        <img src="media/init.gif" width="49%" height="50%"/>
        <img src="media/format.gif" width="49%" height="50%"/>
    </p
  
    ![apply.gif](media/apply.gif)

- 🖥️ **Minimalist UI**: A clean and distraction-free interface built using the Textual framework.
    ![theme.gif](media/theme.gif)

## 🛠 Installation

```bash
pip install git+https://github.com/the-impact-craft/terraland.git
```

## 📌 Usage

```bash
terraland
```

Navigate through workspaces, view state files, and manage your Terraform infrastructure—all from a single, interactive terminal interface.

## 🎯 Shortcuts

- `Ctrl + f` - Search
- `Ctrl + Q` - Quit the app

[//]: Others to be added

## 🤝 Contributing

Feel free to open discussions to share your ideas.

## 📜 License

TerraLand is released under the MIT License.

---

🚀 Get started with TerraLand and simplify your Terraform workflow!


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
textual run --dev terraland/presentation/cli/app.py
```

Run tests:

```bash 
coverage run && coverage report -m
```

Open html report:

```bash
coverage html && open htmlcov/index.html
```