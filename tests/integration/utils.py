from textual.pilot import Pilot
from textual.widget import Widget

DEFAULT_SCREEN_ID = "_default"


async def focus(pilot: Pilot, widget: Widget) -> None:
    """
    Focuses the given widget within the application's interface.

    This asynchronous function ensures that the specified widget is brought
    into the visible area of the application interface, pauses briefly for
    potential visual updates, and then sets the focus to the widget. Another
    pause is applied after the focus operation for stability.

    Args:
        pilot: The controlling interface or handler responsible for managing
            the application's state and interactions.
        widget: The UI widget to be scrolled into view and focused.

    """
    widget.scroll_visible()
    await pilot.pause()
    widget.focus()
    await pilot.pause()


async def click(pilot: Pilot, widget: Widget) -> None:
    """
    Executes a sequence of actions that simulates a user clicking on a widget. The actions include
    scrolling the widget into view, hovering over it, clicking it, and introducing pauses for realistic
    interaction simulation.

    Args:
        pilot: The pilot instance controlling the simulation of user interactions. It provides methods
            such as scroll_visible, pause, hover, and click.
        widget: The target widget to be interacted with during the sequence.

    """
    widget.scroll_visible()
    await pilot.pause()
    await pilot.hover(widget)
    await pilot.click(widget)
    await pilot.pause()


async def double_click(pilot: Pilot, widget: Widget) -> None:
    """
    Performs double-click action on a given widget.

    This function scrolls the widget into the visible area, pauses,
    hovers over the widget, and performs two consecutive clicks to
    simulate a double-click event. Additional pauses are introduced
    to ensure proper event handling.

    Args:
        pilot: The driver or controller responsible for simulating
            user interactions such as scrolling, hovering, and clicking.
        widget: The target on which the double-click interaction is
            performed.

    """
    widget.scroll_visible()
    await pilot.pause()
    await pilot.hover(widget)
    await pilot.click(widget)
    await pilot.click(widget)
    await pilot.pause()


async def enter(pilot: Pilot, widget: Widget) -> None:
    """
    Simulates the process of entering a value or submitting input on a widget
    via user emulation.

    Args:
        pilot: An instance used to control and simulate user interaction.
        widget: The target widget being interacted with in the simulation.

    """
    widget.scroll_visible()
    await pilot.pause()
    widget.focus()
    await pilot.press("enter")
    await pilot.pause()
