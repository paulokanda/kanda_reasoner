"""
In this context “scaffolding” just means a skeleton or blueprint for your package: files and class/method signatures
laid out according to your architecture, but not yet filled in with real code. It serves two purposes:

    Documentation & design
    By putting an interfaces.py in your renderer/ folder you’re explicitly declaring “here’s the contract
    that any topomap‐renderer or label‐renderer must satisfy.” That makes it easy to reason about dependencies
    (your controller depends only on an ITopoRenderer), to enforce SRP/OCP/DIP and—critically—to swap
     in different rendering implementations later without changing your controller.

    Guidance for implementation
    Rather than opening a blank file and wondering where to start, you already have:

    class ITopoRenderer(ABC):
        @abstractmethod
        def init_axes(…): …
        @abstractmethod
        def draw(…): …

    …so you know exactly what methods you need to implement.

So yes, we will actually use renderer/interfaces.py in our code:
import the abstract base classes there and have TopoRenderer inherit from ITopoRenderer.
It isn’t just commentary or “reference” in a vacuum—it’s the first step toward a clean,
SOLID-compliant implementation.

From here we’ll “fill in” each method in topomap_renderer.py and label_renderer.py to
honor that interface.


"""

