from peewee import *
from Tools import Tools

database = MySQLDatabase(**Tools.read_yaml('settings.yaml')['DATABASE'])


class FacebookAccounts(Model):
    email = CharField(constraints=[SQL("DEFAULT ' '")], primary_key=True)
    password = CharField(constraints=[SQL("DEFAULT ' '")])
    username = CharField(constraints=[SQL("DEFAULT ' '")])
    proxy_local = CharField(constraints=[SQL("DEFAULT ' '")])
    ua = CharField(constraints=[SQL("DEFAULT ' '")])
    reg_time = DateTimeField(constraints=[SQL("DEFAULT '0000-00-00 00:00:00'")])
    insert_time = DateTimeField(constraints=[SQL("DEFAULT '0000-00-00 00:00:00'")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT current_timestamp()")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    gender = CharField(constraints=[SQL("DEFAULT ' '")])
    birthday = CharField(constraints=[SQL("DEFAULT ' '")])
    cookie = CharField(constraints=[SQL("DEFAULT '[]'")])
    remark = TextField(null=True)
    secret_code = CharField()
    isused = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        database = database
        table_name = 'facebook_accounts'


# if __name__ == '__main__':
#     FacebookPosts.drop_table()
#     FacebookPosts.create_table()