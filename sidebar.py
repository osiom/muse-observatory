from nicegui import ui

class MinimalSidebar:
    def __init__(self, background: str = "black", text_color: str = "white"):
        self.background = background
        self.text_color = text_color
        self.instruction = """
        Observatory Instructions:
        
        1. Browse the cosmic content
        2. Click items to interact
        3. Use the controls to explore
        """
        self.sidebar = None  # Will store the sidebar reference
        self.is_visible = False  # Track sidebar visibility state

    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        self.is_visible = not self.is_visible
        self.sidebar.visible = self.is_visible
        ui.update()

    def render(self) -> None:
        """Render the minimal sidebar with toggle capability"""
        # Create a toggle button (position it wherever you want)
        ui.button("Toggle Sidebar", on_click=self.toggle_sidebar).classes("fixed top-2 left-2 z-50")
        
        # Create the sidebar (initially hidden)
        self.sidebar = ui.left_drawer().style(
            f"background: {self.background}; "
            f"color: {self.text_color}; "
            "padding: 1rem;"
        )
        self.sidebar.visible = False  # Start hidden
        
        with self.sidebar:
            with ui.column():
                ui.label("Instructions").classes("text-lg font-bold mb-2")
                ui.label(self.instruction).classes("whitespace-pre-line")
                # Optional close button inside the sidebar
                ui.button("Close", on_click=self.toggle_sidebar).classes("mt-4")

def create_sidebar(background: str = "black", text_color: str = "white") -> MinimalSidebar:
    """Create a minimal sidebar instance with toggle functionality"""
    return MinimalSidebar(background, text_color)