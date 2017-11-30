
class Neighbor:    
    def __init__(self, is_active, last_active_time, send_count, timer):
        self.is_active = is_active
        self.last_active_time = last_active_time
        self.send_count = send_count
        self.timer = timer