class Quest:
    def __init__(self, quest_id, name, description, objectives):
        self.id = quest_id
        self.name = name
        self.description = description
        self.objectives = objectives  # список цілей
        self.current_objective = 0
        self.completed = False
        self.rewards = {}  # нагороди за виконання
        
    def update_objective(self, objective_data):
        # оновлюємо прогрес поточної цілі
        if self.completed:
            return
            
        objective = self.objectives[self.current_objective]
        if (objective["type"] == objective_data["type"] and 
            objective["target"] == objective_data["target"]):
            
            # Додаємо прогрес, а не замінюємо його
            objective["progress"] += objective_data["progress"]
            objective["completed"] = objective["progress"] >= objective["required"]
            
            # перевіряємо чи завершено всі цілі
            if all(obj["completed"] for obj in self.objectives):
                self.complete_quest()
                
    def complete_quest(self):
        # завершуємо квест
        self.completed = True
        self.current_objective = len(self.objectives) - 1
        return self.rewards
        
    def get_current_objective(self):
        # повертаємо поточну ціль
        if self.completed:
            return "Quest completed!"
            
        objective = self.objectives[self.current_objective]
        progress_text = f"{objective['progress']}/{objective['required']}"
        return f"{objective['description']} ({progress_text})"

class QuestManager:
    def __init__(self):
        self.quests = {}
        self.active_quests = []
        
    def add_quest(self, quest):
        # додаємо новий квест
        self.quests[quest.id] = quest
        
    def start_quest(self, quest_id):
        # починаємо квест
        if quest_id in self.quests and quest_id not in self.active_quests:
            self.active_quests.append(quest_id)
            
    def complete_quest(self, quest_id):
        # завершуємо квест
        if quest_id in self.active_quests:
            self.active_quests.remove(quest_id)
            self.quests[quest_id].completed = True
            
    def update_quest(self, quest_id, objective_data):
        # оновлюємо прогрес квесту
        if quest_id in self.active_quests:
            self.quests[quest_id].update_objective(objective_data)
            
    def get_active_quests_info(self):
        # отримуємо інформацію про активні квести
        info = []
        for quest_id in self.active_quests:
            quest = self.quests[quest_id]
            info.append({
                "name": quest.name,
                "objective": quest.get_current_objective()
            })
        return info