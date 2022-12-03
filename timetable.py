
class Timetable:
    def __init__(self, data) -> None:
        self.data = data

    def get_occupancy(self, room_id, slot_id):
        return self.data[room_id, slot_id]

    def change_occupancy(self, room_id, slot_id, new_occupancy):
        self.data[room_id, slot_id] = new_occupancy
    