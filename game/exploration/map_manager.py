
from dataclasses import dataclass


@dataclass
class MapData:
    name: str
    background_file: str
    collision_file: str
    start_position: tuple[int, int]


class MapManager:
    def __init__(self):
        self.maps = {
            "room": MapData(
                name="room",
                background_file="ho-ru.png",
                collision_file="ho-ru_c.png",
                start_position=(210, 500),
            ),
            "hallwayR": MapData(
                name="hallwayR",
                background_file="roukaR.png",
                collision_file="roukaR_c.png",
                start_position=(40, 340),
            ),
            "hallwayL": MapData(
                name="hallwayL",
                background_file="roukaL.png",
                collision_file="roukaL_c.png",
                start_position=(40, 340),
            ),
            "syosai": MapData(
                name="syosai",
                background_file="syosai.png",
                collision_file="syosai_c.png",
                start_position=(290, 290),
            ),
        }

        # (現在のマップ名, 入口ID): 遷移先情報
        self.transitions = {
            ("room", "room_to_hallwayR"): {
                "target_map": "hallwayR",
                "spawn_position": (40, 340),
            },
            ("room", "room_to_hallwayL"): {
                "target_map": "hallwayL",
                "spawn_position": (60, 340),
            },
            ("hallwayR", "hallwayR_to_room"): {
                "target_map": "room",
                "spawn_position": (380, 440),
            },
            ("hallwayL", "hallwayL_to_room"): {
                "target_map": "room",
                "spawn_position": (60, 440),
            },
            ("hallwayL", "hallwayL_to_syosai"): {
                "target_map": "syosai",
                "spawn_position": (290, 290),
            },
            ("syosai", "syosai_to_hallwayL"): {
                "target_map": "hallwayL",
                "spawn_position": (50, 240),
            },
        }

        self.current_map_name = "syosai"

    @property
    def current_map(self) -> MapData:
        return self.maps[self.current_map_name]

    def change_map(self, map_name: str) -> MapData:
        if map_name not in self.maps:
            raise ValueError(f"存在しないマップ: {map_name}")

        self.current_map_name = map_name
        return self.current_map

    def get_transition(
        self,
        from_map: str,
        entrance_id: str,
    ) -> dict:
        """移動元マップと入口IDから遷移先情報を取得する"""
        key = (from_map, entrance_id)

        if key not in self.transitions:
            raise ValueError(f"遷移先が定義されていません: {key}")

        return self.transitions[key]
