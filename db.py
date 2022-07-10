import json


class JSONDatabase:
    __db_path = 'db.json'
    __keys_list = ['name_project', 'goals', 'documents', 'skip', 'members']

    def __init__(self):
        self.update_database()

    def update_database(self):
        try:
            self.db = json.load(open(self.__db_path))
        except Exception as e:
            print('Something got wrong')
            print(e)

    def commit(self):
        json.dump(self.db, open(self.__db_path, 'w'))

    def user_exists(self, user_id):
        return True if user_id in self.db.keys() else False

    def initialize_user(self, user_id):
        self.db[user_id] = {'skip': False}

    def get_user_data(self, user_id):
        return self.db[user_id] if self.user_exists(user_id) else {}

    def clear_user_data(self, user_id):
        if self.user_exists(user_id):
            self.db.pop(user_id)
            self.commit()

    def user_data_complete(self, user_id):
        if self.user_exists(user_id) and set(self.db[user_id].keys()) == set(self.__keys_list):
            data = self.db[user_id].copy()
            self.clear_user_data(user_id)
            return data
        return {}

    def get_user_step(self, user_id):
        if not self.user_exists(user_id):
            return self.__keys_list[0]

        for step in self.__keys_list:
            if not step in self.db[user_id].keys():
                if step == 'documents' and self.db[user_id]['skip']:
                    self.db[user_id]['documents'] = []
                else: return step

            if step == 'documents' and not self.db[user_id]['skip']:
                return 'documents'

        return 'finish'

    def insert_data(self, user_id, key, value):
        if not key in self.__keys_list:
            return False

        if not self.user_exists(user_id):
            self.initialize_user(user_id)

        if key == 'documents':
            if key not in self.db[user_id].keys():
                self.db[user_id][key] = [value]
            else:
                self.db[user_id][key].append(value)
        else:
            self.db[user_id][key] = value

        self.commit()

    def __del__(self):
        self.commit()


