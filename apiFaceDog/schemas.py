from voluptuous import Schema
from voluptuous import Required, All, Length, Range
from voluptuous.validators import Coerce

schemaUser = Schema({
    Required('name') : All(str,Length(min=1,max=30)),
    Required('email') : All(str,Length(min=1,max=30)),
    Required('password') : All(Coerce ( str ))
    
}) 
schema_Get_User = Schema({
    Required('email') : All(str, Length(min = 1))
}) 
