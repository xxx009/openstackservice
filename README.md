##  Object Relational Tutorial
所谓ORM（Object Relational Mapping），就是建立其由Python类到数据库表的映射关系：一个Python实例(instance)对应数据库中的一行(row)。这种映射包含两层含义，一是实现对象和与之关联的的行的状态同步，二是将涉及数据库的查询操作，表达为Python类的相互关系。


##  Declaring a Mapping
当我们使用ORM的时候，其配置过程主要分为两个部分：一是描述我们要处理的数据库表的信息，二是将我们的Python类映射到这些表上。这两个过程在SQLAlchemy中是一起完成的，我们将这个过程称之为Declarative。
使用Declarative参与ORM映射的类需要被定义成为一个指定基类的子类，这个基类应当含有ORM映射中相关的类和表的信息。这样的基类我们称之为declarative base class。在我们的应用中，我们一般只需要一个这样的基类。这个基类我们可以通过declarative_base来创建


```
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```


## Create a Session

```
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
```



## Connecting
为了建立同数据库的链接，我们需要使用到create_engine


```
sql_connection = "mysql+pymysql://nova_api:b8931e5057f9478d@192.168.1.102/nova_api?charset=utf8" 
engine = create_engine(sql_connection, echo=True)
```
 

## Query
Session的query函数会返回一个Query对象。query函数可以接受多种参数类型。可以是类，或者是类的instrumented descriptor。下面的这个例子取出了所有的User记录。


```
flavors = session.query(InstanceTypes).all() 
for flavor in flavors:
     print flavor.id, flavor.name
```


## Usage in Openstack
https://github.com/openstack/nova/blob/master/nova/db/sqlalchemy/models.py

## 参考
http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#working-with-related-objects
