class dotdict(dict):
    def __getattribute__(self, name):
        return self[name]        