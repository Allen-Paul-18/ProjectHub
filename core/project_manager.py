# ============================================================
# PROJECT MANAGER
# ============================================================

import json
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
PROJECTS_FILE = BASE_DIR / "projects.json"


class ProjectManager:

    def __init__(self):
        self.projects = self.load_projects()

    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    def load_projects(self):

        try:
            with open(
                PROJECTS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

                if not isinstance(data, list):
                    print("projects.json must contain a list.")

                    return []

                return data

        except FileNotFoundError:

            print(
                f"Project file not found: {PROJECTS_FILE}"
            )

            return []

        except json.JSONDecodeError as e:

            print(
                f"Invalid projects.json: {e}"
            )

            return []

        except Exception as e:

            print(
                f"Failed to load projects: {e}"
            )

            return []

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save_projects(self):

        try:

            with open(
                PROJECTS_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.projects,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            return True

        except Exception as e:

            print(
                f"Failed to save projects: {e}"
            )

            return False

    # --------------------------------------------------------
    # ADD
    # --------------------------------------------------------

    def add_project(
        self,
        project
    ):

        self.projects.append(
            project
        )

        return self.save_projects()

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update_project(
        self,
        index,
        project
    ):

        if index < 0 or index >= len(self.projects):

            return False

        self.projects[index] = project

        return self.save_projects()

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    def delete_project(
        self,
        index
    ):

        if index < 0 or index >= len(self.projects):

            return False

        self.projects.pop(index)

        return self.save_projects()

    # --------------------------------------------------------
    # GET PROJECT
    # --------------------------------------------------------

    def get_project(
        self,
        index
    ):

        if index < 0 or index >= len(self.projects):

            return None

        return self.projects[index]

    # --------------------------------------------------------
    # REFRESH
    # --------------------------------------------------------

    def refresh(self):

        self.projects = self.load_projects()

        return self.projects