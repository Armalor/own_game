# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent
sys.path.append(__root__.__str__())
from classes import Wizard
from client import ChooseTeam, PlayGame
# ~Локальный импорт


if __name__ == "__main__":
    app = Wizard(title="Client App", steps=[ChooseTeam, PlayGame])
    app.mainloop()
