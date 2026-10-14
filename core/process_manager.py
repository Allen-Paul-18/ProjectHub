# ============================================================
# PROCESS MANAGER
# ============================================================


import shlex
from pathlib import Path
from PySide6.QtCore import QProcess


class ProcessManager:

    def __init__(self, console_callback, status_callback):

        self.console_callback = console_callback
        self.status_callback = status_callback

        self.processes = {}

    def launch(self, project):

        name = project["name"]
        project_path = Path(project["path"])

        # ----------------------------------------------------
        # CHECK PATH
        # ----------------------------------------------------

        if not project_path.exists():

            self.console_callback(
                f"\n[ERROR] Project path does not exist:\n"
                f"{project_path}\n"
            )

            self.status_callback(
                name,
                "Path missing"
            )

            return

        # ----------------------------------------------------
        # ALREADY RUNNING
        # ----------------------------------------------------

        if name in self.processes:

            process = self.processes[name]

            if process.state() != QProcess.ProcessState.NotRunning:

                self.console_callback(
                    f"[INFO] {name} is already running.\n"
                )

                return

        project_type = project.get(
            "type",
            ""
        ).lower()

        command = project.get(
            "command",
            ""
        )

        venv = project.get(
            "venv"
        )

        program = None
        arguments = []

        # ----------------------------------------------------
        # PYTHON
        # ----------------------------------------------------

        if project_type == "python":

            if venv:

                python_exe = (
                    Path(venv)
                    / "Scripts"
                    / "python.exe"
                )

                if python_exe.exists():
                    program = str(python_exe)
                else:
                    program = "python"

            else:

                program = "python"

            if command:
                arguments = shlex.split(
                    command
                )

        # ----------------------------------------------------
        # NODE
        # ----------------------------------------------------

        elif project_type == "node":

            program = "npm"

            if command.startswith("npm "):

                arguments = shlex.split(
                    command
                )[1:]

            else:

                arguments = shlex.split(
                    command
                )

        # ----------------------------------------------------
        # FLUTTER
        # ----------------------------------------------------

        elif project_type == "flutter":

            program = "flutter"

            if command.startswith("flutter "):

                arguments = shlex.split(
                    command
                )[1:]

            else:

                arguments = shlex.split(
                    command
                )

        # ----------------------------------------------------
        # OTHER
        # ----------------------------------------------------

        else:

            if not command:

                self.console_callback(
                    f"[ERROR] No launch command configured "
                    f"for {name}.\n"
                )

                return

            parts = shlex.split(
                command
            )

            program = parts[0]
            arguments = parts[1:]

        # ----------------------------------------------------
        # CREATE PROCESS
        # ----------------------------------------------------

        process = QProcess()

        process.setWorkingDirectory(
            str(project_path)
        )

        process.setProcessChannelMode(
            QProcess.ProcessChannelMode.MergedChannels
        )

        process.readyReadStandardOutput.connect(
            lambda p=process, n=name:
            self.read_output(
                p,
                n
            )
        )

        process.finished.connect(
            lambda exit_code,
                   exit_status,
                   n=name:
            self.process_finished(
                n,
                exit_code
            )
        )

        process.errorOccurred.connect(
            lambda error,
                   n=name:
            self.process_error(
                n,
                error
            )
        )

        self.processes[name] = process

        self.status_callback(
            name,
            "Starting..."
        )

        self.console_callback(
            "\n"
            + "=" * 65
            + "\n"
            f"[LAUNCH] {name}\n"
            f"Directory: {project_path}\n"
            f"Command: {program} "
            f"{' '.join(arguments)}\n"
            + "=" * 65
            + "\n"
        )

        process.start(
            program,
            arguments
        )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    def read_output(
        self,
        process,
        name
    ):

        data = process.readAllStandardOutput()

        text = bytes(data).decode(
            "utf-8",
            errors="replace"
        )

        if text:

            self.console_callback(
                f"[{name}] {text}"
            )

    # --------------------------------------------------------
    # FINISHED
    # --------------------------------------------------------

    def process_finished(
        self,
        name,
        exit_code
    ):

        self.status_callback(
            name,
            "Ready"
        )

        self.console_callback(
            f"\n[STOPPED] {name} "
            f"(exit code: {exit_code})\n"
        )

        self.processes.pop(
            name,
            None
        )

    # --------------------------------------------------------
    # ERROR
    # --------------------------------------------------------

    def process_error(
        self,
        name,
        error
    ):

        self.status_callback(
            name,
            "Error"
        )

        self.console_callback(
            f"[PROCESS ERROR] "
            f"{name}: {error}\n"
        )

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    def stop(
        self,
        project_name
    ):

        process = self.processes.get(
            project_name
        )

        if not process:
            return

        if process.state() != QProcess.ProcessState.NotRunning:

            self.console_callback(
                f"[STOP] Stopping "
                f"{project_name}...\n"
            )

            process.terminate()

            if not process.waitForFinished(
                2000
            ):

                process.kill()

        self.processes.pop(
            project_name,
            None
        )

        self.status_callback(
            project_name,
            "Ready"
        )

    # --------------------------------------------------------
    # RESTART
    # --------------------------------------------------------

    def restart(
        self,
        project
    ):

        name = project["name"]

        self.console_callback(
            f"\n[RESTART] {name}\n"
        )

        self.stop(name)

        self.launch(project)

    # --------------------------------------------------------
    # RUNNING PROCESS
    # --------------------------------------------------------

    def get_running_projects(self):
        """Return the names of projects whose processes are running."""

        running_projects = []

        for project_name, process in self.processes.items():
            if process.state() == QProcess.ProcessState.Running:
                running_projects.append(project_name)

        return running_projects
