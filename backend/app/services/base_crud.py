
from app.extensions import db

class BaseCRUD:

    @staticmethod
    def get_all(model):
        return model.query.all() 

    @staticmethod
    def get_by_id(model, id):
        return model.query.get(id) 
    
    @staticmethod
    def create(model, **kwargs):
        new_record = model(**kwargs) # set the model with the attributes(kwargs)
        db.session.add(new_record)  # add record
        db.session.commit()
        return new_record  # return the record 
    
    @staticmethod
    def get_all_records_by_filter(model, **kwargs):
        return model.query.filter_by(**kwargs).all() # get all rows based on the kwargs
    
    
    @staticmethod
    def get_first_record_by_filter(model, **kwargs):
        return model.query.filter_by(**kwargs).first() # get one row based on the kwargs
    
    @staticmethod
    def update(model, id, **kwargs):
        record = model.query.get(id) 
        if record:
            for key, value in kwargs.items(): # go through the kwargs as a dictionary
                if value is not None:  # ensure value is  passed 
                    setattr(record, key, value) # set the new value to its key
            db.session.commit()
            return record
        return None
    
    @staticmethod
    def delete(model, id):
        record = model.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        return False
    
