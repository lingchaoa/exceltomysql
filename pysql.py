#!/usr/bin/env python
# coding:utf-8
# @Time    : 2021/2/21 12:38 下午
# @Author  : 孔令超
# @File    : pysql.py
# @Software: PyCharm

from pymysql import connect


# mysql
class MySqlDataSource(object):
    # 数据库链接
    __connection = None
    # sql执行对象
    __cursor = None

    # 初始化参数
    # 默认使用了以下数据库信息，可根据自身需求更换或者传值
    def __init__(self, database='test', host='localhost', port=3306, user='root', password='klc930816', charset='utf8'):
        self.__database = database
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__charset = charset

    # 获取数据库链接
    def __get_conn(self):
        self.__connection = connect(host=self.__host, port=self.__port,
                                    user=self.__user, password=self.__password,
                                    database=self.__database, charset=self.__charset)
        return self.__connection

    # 获取sql执行对象
    def __get_cursor(self):
        self.__cursor = self.__get_conn().cursor()
        return self.__cursor

    # 执行查询select
    def execute_query(self, sql, param):
        # 参数校验
        if sql is None and param is None:
            return None

        data_list = []
        # 执行查询
        try:
            handler = self.__get_cursor()
            handler.execute(sql, param)
            # 处理返回结果
            for content in handler.fetchall():
                data_list.append(content)
        except Exception as e:
            print('query exception:', e)
        finally:
            self.close_memory()
        return data_list

    # 执行增删改(update、insert、delete)
    def execute_modify(self, sql, param):
        # 受影响行数
        count = 0
        # 参数校验
        if sql is None or param is None:
            return count

        # 执行查询
        try:
            handler = self.__get_cursor()
            count = handler.execute(sql, param)
        except Exception as e:
            self.__connection.rollback()
            print('modify exception:', e)
        finally:
            self.__connection.commit()
            self.close_memory()
        return count

    # 释放资源
    def close_memory(self):
        if self.__cursor is not None:
            self.__cursor.close()
        if self.__connection is not None:
            self.__connection.close()


# 测试主函数（可选 只用于本地调试，使用模块调用时删除）
if __name__ == "__main__":
    # 导入uuid使得每次更新都能看到效果（可选）
    import uuid

    # 获取数据库链接
    data_base = MySqlDataSource()

    ## 1.查询
    # 执行条件查询（非条件查询将param参数设置为None即可）
    result_data = data_base.execute_query("select * from city_nation where city = %s and nation = %s", ['硅谷', '美国'])
    # 返回数据处理
    if result_data is None or len(result_data) <= 0:
        # 数据返回空输出
        print('未查询到数据')
    else:
        # 打印返回数据
        print(result_data)

    ## 2.新增
    # 返回受影响行数
    print(data_base.execute_modify("insert into city_nation values (%s,%s)",
                                   ['gpw','author']))



    ## 3.更新
    # 返回受影响行数
    print(data_base.execute_modify("update users set description = %s where name = %s",
                                   [str(uuid.uuid1()), 'Jenny']))

    ## 4.删除
    # 返回受影响行数
    print(data_base.execute_modify("delete from users where name = %s", 'gpw'))
