from __future__ import annotations

from collections import defaultdict


class ShipMount:
    def __init__(self, count: int, size: str, type_: str, mount_type):
        self.count = count
        self.size = size
        self.type_ = type_
        self.mount_type = mount_type

    @staticmethod
    def from_wiki_mount(text: str) -> ShipMount:
        clean_text = text.replace("{{ShipMounts|", "").replace("}}", "")
        parts = clean_text.split("|")

        count = int(parts[0])

        attributes = parts[1].strip().split(" ", 1)
        size = attributes[0]
        type_ = attributes[1]

        return ShipMount(count, size.upper(), type_.upper(), "Turret".upper())

    @staticmethod
    def from_game_data(data: dict) -> ShipMount:
        return ShipMount(
            count=1,
            size=data.get("size", ""),
            type_=data.get("type_", ""),
            mount_type=data.get("mount", ""),
        )

    @staticmethod  # TODO Shouldn't exist
    def consolidate_mounts(mounts: list[ShipMount]) -> list[ShipMount]:
        totals = defaultdict(int)

        for m in mounts:
            key = (m.size, m.type_, m.mount_type)
            totals[key] += m.count

        consolidated_list = []
        for (size, type_, mount_type), count in totals.items():
            new_mount = ShipMount(count, size, type_, mount_type)
            consolidated_list.append(new_mount)

        return consolidated_list

    @staticmethod # TODO works for now, but shouldn't need to exist
    def sort_mounts(mounts: list[dict]) -> list[dict]:
        def sort_key(mount):
            s = str(mount.get('size', '')).upper()
            t = str(mount.get('type_', '')).upper()
            m = str(mount.get('mount_type', '')).upper()

            return s, t, m

        return sorted(mounts, key=sort_key)

    def to_dict(self):
        return {
            "count": self.count,
            "size": self.size,
            "type_": self.type_
        }