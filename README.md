# 🚀 Project Hub

**A centralized desktop dashboard for managing, launching, and monitoring development projects.**

Project Hub is a Windows desktop application built with Python and PySide6 that brings multiple development projects into one place. Instead of opening separate terminals and manually navigating between project directories, you can manage your projects through a single graphical interface.

Launch applications, monitor running processes, view console output, manage project configurations, and keep track of system resource usage from one workspace.

> **Status:** Active development

## ✨ Features

### 📁 Project Management
- Load and manage projects through a JSON configuration file.
- Display projects using organized project cards.
- Search and filter projects.
- Add, edit, and remove project configurations.
- Configure individual project commands and execution environments.

### ▶️ Process Management
- Launch projects directly from the dashboard.
- Stop and restart running projects.
- Track the running state of managed processes.
- Stream standard output and error output into an integrated console.
- Monitor running projects from a dedicated sidebar view.

### 🖥️ System Monitoring
- Display live CPU utilization.
- Monitor RAM usage and total memory.
- Show memory usage directly in the sidebar.
- Refresh system statistics periodically.

### 🧰 Developer Workspace
- Support custom launch commands for different project types.
- Configure project-specific Python virtual environments.
- Keep project configuration separate from application logic.
- Use an integrated console to inspect application output.

### 🧭 Sidebar Navigation
- Overview for project management.
- Running Projects for monitoring active processes.
- Dedicated navigation entries for developer utilities.

Some sidebar utilities are still being developed. See the roadmap below for planned functionality.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| PySide6 | Desktop GUI |
| Qt `QProcess` | Process launching and management |
| Qt `QTimer` | Periodic UI and monitoring updates |
| `psutil` | CPU, memory, and system monitoring |
| JSON | Project configuration and persistence |

## 🏗️ Project Structure

```text
ProjectHub/
├── launcher.py
├── projects.json
├── requirements.txt
│
├── core/
│   ├── process_manager.py
│   ├── project_manager.py
│   └── system_monitor.py
│
├── ui/
│   ├── main_window.py
│   ├── project_card.py
│   ├── console_panel.py
│   ├── project_editor.py
│   └── running_projects.py
│
├── assets/
├── utils/
└── README.md
```

*Note: The exact files and folders may evolve as development continues.*

### Architecture

**`launcher.py`**
- Application entry point.
- Initializes the Qt application and opens the main window.

**`core/process_manager.py`**
- Handles project process lifecycle operations.
- Launches and stops projects.
- Tracks running processes and forwards console output.

**`core/project_manager.py`**
- Loads and saves project configurations.
- Handles project creation, updates, and deletion.

**`core/system_monitor.py`**
- Collects CPU and memory statistics through `psutil`.

**`ui/main_window.py`**
- Builds the main application window.
- Coordinates navigation, project cards, system statistics, and other UI components.

**`ui/project_card.py`**
- Displays an individual project and its available actions.

**`ui/console_panel.py`**
- Displays process output in the integrated console.

**`ui/project_editor.py`**
- Provides the interface for creating and editing project configurations.

**`ui/running_projects.py`**
- Displays projects whose managed processes are currently running.

**`projects.json`**
- Stores the list of projects and their launch configurations.

## 🏗️ Architecture

The following diagram illustrates how Project Hub's application shell coordinates project management, process execution, console output, and system monitoring.

flowchart TD
    User((User)) -->|starts| Launcher["Application launcher<br/>launcher.py"]
    Launcher -->|opens| MainWindow["Dashboard coordinator<br/>ui/main_window.py"]

    subgraph Projects["Project Configuration"]
        ProjectManager["Project configuration manager<br/>core/project_manager.py"]
        ProjectCard["Project cards<br/>ui/project_card.py"]
        ProjectEditor["Project editor<br/>ui/project_editor.py"]
    end

    subgraph Processes["Process Operations"]
        ProcessManager["Process lifecycle manager<br/>core/process_manager.py"]
        ManagedProcesses["Launched project processes"]
        ProcessManager -->|starts and tracks| ManagedProcesses
    end

    subgraph Monitoring["Monitoring and Output"]
        RunningProjects["Running projects view<br/>ui/running_projects.py"]
        Console["Integrated console<br/>ui/console_panel.py"]
        SystemStats["System statistics view<br/>ui/system_stats.py"]
        SystemMonitor["System metrics collector<br/>core/system_monitor.py"]
        Psutil["psutil host metrics"]

        SystemStats -->|requests metrics| SystemMonitor
        SystemMonitor -->|reads metrics| Psutil
    end

    MainWindow -->|loads and updates| ProjectManager
    MainWindow -->|coordinates| ProjectCard
    MainWindow -->|opens| ProjectEditor
    MainWindow -->|launches and stops| ProcessManager
    MainWindow -->|shows| RunningProjects
    MainWindow -->|displays output| Console
    MainWindow -->|presents statistics| SystemStats

    ProjectCard -->|emits actions| MainWindow
    ProcessManager -->|forwards output| Console
    RunningProjects -->|queries and stops| ProcessManager

    classDef blue fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef amber fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef mint fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef rose fill:#ffe4e6,stroke:#e11d48,color:#881337
    classDef indigo fill:#e0e7ff,stroke:#4f46e5,color:#312e81

    class User,Launcher,MainWindow blue
    class ProjectManager,ProjectCard,ProjectEditor amber
    class ProcessManager,ManagedProcesses mint
    class RunningProjects,Console,SystemStats,SystemMonitor rose
    class Psutil indigo


## ⚙️ Installation

### Prerequisites

- Windows 10 or Windows 11
- Python 3.11 or a compatible Python version
- Git (for cloning the repository)

### 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/ProjectHub.git
cd ProjectHub
```

Replace `YOUR_USERNAME` with your GitHub username and adjust the repository name if necessary.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents script execution, activate the environment from Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install dependencies

If the repository contains `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Otherwise, install the core dependencies:

```powershell
python -m pip install PySide6 psutil
```

### 5. Launch Project Hub

```powershell
python launcher.py
```

## 📝 Configuration

Project Hub uses `projects.json` to define the projects displayed in the dashboard.

A project configuration may look like this:

```json
[
  {
    "name": "My Python Project",
    "description": "A sample Python application",
    "category": "Python",
    "icon": "🐍",
    "path": "E:/Projects/MyPythonProject",
    "type": "python",
    "command": "main.py",
    "venv": "E:/Projects/venv/.venv"
  }
]
```

### Configuration fields

| Field | Description |
|---|---|
| `name` | Project name displayed in the dashboard |
| `description` | Short project description |
| `category` | Category used to organize projects |
| `icon` | Project card icon |
| `path` | Project's root directory |
| `type` | Project type |
| `command` | Command or entry point used to launch the project |
| `venv` | Optional project-specific virtual environment |

The exact command format depends on the project's launch implementation. For example, a Streamlit application can be launched with:

```powershell
python -m streamlit run app.py
```

For projects using a virtual environment, configure the appropriate interpreter or environment path according to the command handling implemented in Project Hub.

**Important:** Use valid project paths and ensure the required dependencies are installed in the environment used by each project.

## 🧑‍💻 Development

The application is organized into separate core and UI modules to keep process management, configuration handling, monitoring, and interface code independent.

To contribute or modify the application:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the affected project-management workflows.
5. Submit a pull request.

Example:

```powershell
git checkout -b feature/my-feature
```

## 🗺️ Roadmap

Planned improvements include:

- [ ] Quick terminal access for individual projects.
- [ ] Active port monitoring with process names and PIDs.
- [ ] Stop All Projects action.
- [ ] Functional Settings page.
- [ ] Active sidebar navigation highlighting.
- [ ] Further UI polish and usability improvements.

Completed features will be checked off as they are implemented and tested.

## 🔒 Security and Configuration Notes

- Review `projects.json` before launching unfamiliar project commands.
- Avoid committing API keys, passwords, tokens, or other secrets.
- Add local environment files and virtual environments to `.gitignore`.
- Project commands execute on your machine and may have the same permissions as the user running Project Hub.

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome.

If you find a bug or have an idea for an improvement, open an issue describing the behavior and the proposed change.

## 📄 License

No license has been selected yet. Add a `LICENSE` file before publishing the project if you want to explicitly define how others may use, modify, and distribute the code.

---

**Built with Python and PySide6.**