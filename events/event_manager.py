class EventManager:
    def __init__(self):
        self.listeners = {}
        
    def add_listener(self, event_type, listener):
        #додаємо слухача подій
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)
        
    def remove_listener(self, event_type, listener):
        #видаляємо слухача подій
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)
            
    def trigger_event(self, event_type, data=None):
        #викликаємо подію
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(data)
                
    #стандартні типи подій
    EVENT_PLAYER_DAMAGED = "player_damaged"
    EVENT_PLAYER_HEALED = "player_healed"
    EVENT_QUEST_STARTED = "quest_started"
    EVENT_QUEST_COMPLETED = "quest_completed"
    EVENT_ITEM_COLLECTED = "item_collected"
    EVENT_ENEMY_DEFEATED = "enemy_defeated"
    EVENT_DIALOGUE_STARTED = "dialogue_started"
    EVENT_DIALOGUE_ENDED = "dialogue_ended"