from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Set, Tuple

try:
    from aima3.agents import Environment
except Exception:
    # Fallback: permite rodar o projeto mesmo sem aima3 instalada.
    # (O grupo pode trocar por aima3 depois sem mexer no resto.)
    class Environment:  # type: ignore
        def __init__(self):
            self.things = []

        def add_thing(self, thing):
            self.things.append(thing)


Pos = Tuple[int, int]  # (row, col)


@dataclass(frozen=True)
class HospitalPercept:
    """Percepção do ambiente (pode ser expandida pelo grupo)."""

    robot_pos: Pos
    deliveries_left: frozenset[Pos]
    walls: frozenset[Pos]
    grid_size: int
    bump: bool
    delivered_now: bool


class HospitalEnvironment(Environment):


    ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT", "STAY")

    def __init__(
        self,
        grid_size: int,
        walls: Optional[Iterable[Pos]] = None,
        deliveries: Optional[Iterable[Pos]] = None,
        start: Pos = (0, 0),
        ascii_map: Optional[List[str]] = None,
    ):
        super().__init__()

        self.grid_size = int(grid_size)
        if self.grid_size <= 0:
            raise ValueError("grid_size deve ser > 0")

        self.walls: Set[Pos] = set()
        self.deliveries: Set[Pos] = set()

        if ascii_map is not None:
            self._load_from_ascii(ascii_map)
        else:
            if walls:
                self.walls = set(walls)
            if deliveries:
                self.deliveries = set(deliveries)
            self.robot_pos = start

        if self.robot_pos in self.walls:
            raise ValueError("Posição inicial do robô está em uma parede.")
        self.deliveries.discard(self.robot_pos)

        self._last_bump = False
        self._last_delivered = False

    # ---------- mapa ----------
    def _load_from_ascii(self, ascii_map: List[str]) -> None:
        """Carrega mapa NxN a partir de lista de strings.

        Caracteres aceitos: '.', '=', 'D', 'R'
        """

        if len(ascii_map) != self.grid_size:
            raise ValueError("ascii_map deve ter grid_size linhas")

        found_robot = False
        for r, line in enumerate(ascii_map):
            if len(line) != self.grid_size:
                raise ValueError("Cada linha de ascii_map deve ter grid_size colunas")
            for c, ch in enumerate(line):
                if ch == ".":
                    continue
                if ch == "=":
                    self.walls.add((r, c))
                elif ch == "D":
                    self.deliveries.add((r, c))
                elif ch == "R":
                    self.robot_pos = (r, c)
                    found_robot = True
                else:
                    raise ValueError(f"Caractere inválido no mapa: {ch!r}")

        if not found_robot:
            self.robot_pos = (0, 0)

    # ---------- helpers ----------
    def in_bounds(self, pos: Pos) -> bool:
        r, c = pos
        return 0 <= r < self.grid_size and 0 <= c < self.grid_size

    def is_free(self, pos: Pos) -> bool:
        return self.in_bounds(pos) and pos not in self.walls

    def _move(self, pos: Pos, action: str) -> Pos:
        r, c = pos
        if action == "UP":
            return (r - 1, c)
        if action == "DOWN":
            return (r + 1, c)
        if action == "LEFT":
            return (r, c - 1)
        if action == "RIGHT":
            return (r, c + 1)
        return pos

    # ---------- 1) armazenar posição do robô ----------
    def get_robot_position(self) -> Pos:
        return self.robot_pos

    # ---------- 1) executar ações ----------
    def execute_action(self, agent, action) -> None:
        action = str(action).upper()
        self._last_bump = False
        self._last_delivered = False

        if action not in self.ACTIONS:
            return

        new_pos = self._move(self.robot_pos, action)

        if action != "STAY" and not self.is_free(new_pos):
            self._last_bump = True
            return

        self.robot_pos = new_pos

        # entrega ao chegar
        if self.robot_pos in self.deliveries:
            self.deliveries.remove(self.robot_pos)
            self._last_delivered = True

    # ---------- 1) gerar percepções ----------
    def percept(self, agent) -> HospitalPercept:
        return HospitalPercept(
            robot_pos=self.robot_pos,
            deliveries_left=frozenset(self.deliveries),
            walls=frozenset(self.walls),
            grid_size=self.grid_size,
            bump=self._last_bump,
            delivered_now=self._last_delivered,
        )

    def percept_state(self):
        """Percepção no formato que o código atual do grupo usa no Problem:

        state = ((x, y), frozenset(entregas))
        """

        return (self.robot_pos, frozenset(self.deliveries))

    def export_search_state(self):
        """Alias para percept_state, mas com nome mais explícito."""

        return self.percept_state()

    # ---------- 2) render() ----------
    def render(self) -> None:
        grid = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for (r, c) in self.walls:
            if self.in_bounds((r, c)):
                grid[r][c] = "="

        for (r, c) in self.deliveries:
            if self.in_bounds((r, c)):
                grid[r][c] = "D"

        rr, cc = self.robot_pos
        grid[rr][cc] = "R"

        print("\n".join("".join(row) for row in grid))
        print(f"Pos: {self.robot_pos} | Entregas restantes: {len(self.deliveries)}")
