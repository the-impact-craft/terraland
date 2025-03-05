from dataclasses import dataclass
from typing import Self

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import (
    RadioSet,
    RadioButton,
)

from terraland.domain.terraform.workspaces.entities import Workspace


class PersistentRadioButton(RadioButton):
    def toggle(self) -> Self:
        """Toggle the value of the widget.

        Returns:
            The `ToggleButton` instance.
        """
        self.value = True
        return self


class Workspaces(VerticalScroll):
    """
    Widget for managing the workspaces.
    """

    @property
    def can_focus(self) -> bool:
        """
        Indicates whether the widget can receive focus through keyboard navigation.

        Returns:
            bool: Always returns False, preventing the widget from being focusable via tabbing.
        """
        return False

    DEFAULT_CSS = """
    Workspaces > RadioSet {
        background: transparent;
        width: 100%;
        border: none;

        &:focus {
            border: none;
        }

        & > RadioButton {
            background: transparent;
            border: none;
             width: 100%;
        }
    }
    """

    WORKSPACE_RADIO_SET_ID = "workspaces_radio_set"
    workspaces: reactive[list[Workspace]] = reactive([], recompose=True)
    selected_workspace: reactive[Workspace | None] = reactive(None)

    @dataclass
    class SelectEvent(Message):
        workspace: Workspace

    def __init__(self, *args, **kwargs):
        """
        Initialize a Workspaces widget with a list of workspaces.

        Parameters:
            workspaces (list): A list of workspace names or identifiers to be displayed in the radio button set.
            *args: Variable length argument list passed to the parent VerticalScroll constructor.
            **kwargs: Arbitrary keyword arguments passed to the parent VerticalScroll constructor.

        The method stores the provided workspaces and calls the parent class constructor to set up the widget.
        """
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        """
        Compose the workspace radio buttons for selection.

        Creates a radio set with buttons for each workspace, automatically selecting
        the first workspace by default.

        Returns:
            ComposeResult: A generator yielding RadioButton widgets for each workspace.
            The first workspace's radio button is pre-selected.

        Example:
            # Generates radio buttons for ["Workspace1", "Workspace2", "Workspace3"]
            # First radio button (Workspace1) will be selected by default
        """
        with RadioSet(id=self.WORKSPACE_RADIO_SET_ID):
            for index, workspace in enumerate(self.workspaces):
                yield PersistentRadioButton(workspace.name, workspace.is_active, id=workspace.uuid)

    def watch_selected_workspace(self):
        try:
            radio_set_component: RadioSet = self.query_one(f"#{self.WORKSPACE_RADIO_SET_ID}")  # type: ignore
        except NoMatches:
            self.log.warning("component not found")
            return

        if not self.selected_workspace:
            return

        selected_workspace = [
            index for index, workspace in enumerate(self.workspaces) if workspace.name == self.selected_workspace.name
        ]
        selected_index = selected_workspace[0] if selected_workspace else None
        if selected_index is None:
            return
        radio_set_component._selected = selected_index

    def on_mount(self) -> None:
        """
        Set the border title of the widget to "Workspaces" when the widget is mounted.

        This method is called automatically when the widget is added to the application's widget tree,
        and it sets a descriptive title for the widget's border.
        """
        self.border_title = "Workspaces"
        selected_workspace = [index for index, workspace in enumerate(self.workspaces) if workspace.is_active]
        selected_index = selected_workspace[0] if selected_workspace else None

        if selected_index is None:
            return
        workspace_radio_set: RadioSet = self.query_one(f"#{self.WORKSPACE_RADIO_SET_ID}")  # type: ignore

        workspace_radio_set._selected = selected_index

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """
        Handle changes in the workspace radio set selection.

        When the radio set with the specified ID is changed, this method posts a WorkspaceChangedEvent
        with the corresponding workspace from the list of workspaces.

        Parameters:
            event (RadioSet.Changed): The event triggered by changing the radio set selection.

        Side Effects:
            Posts a WorkspaceChangedEvent with the selected workspace.

        Raises:
            IndexError: If the event index is out of range of the workspaces list.
        """
        if event.radio_set.id == self.WORKSPACE_RADIO_SET_ID:
            self.selected_workspace = self.workspaces[event.index]
            self.post_message(self.SelectEvent(self.selected_workspace))
