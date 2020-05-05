# -*- coding: utf-8 -*-

import json
from xmlrpclib import Binary
from services import getAccess, dbConnect, dbBinary, loadVar
from ldap import LDAP
from settings import ldapBase, systemTypes, reservedTypes, referenceTypes, domains


class API:
    def ping(self):
        '''
        ПРОВЕРКА ДОСТУПНОСТИ СЕРВЕРА
    	    ВОЗВРАЩАЕТ:
    	    True [bool]
        '''
        return True

    def getDomains(self):
        '''
        ПОЛУЧЕНИЕ СПИСКА ДОМЕНОВ
	        ВОЗВРАЩАЕТ {json.dumps()}:
	        список имён поддерживаемых доменов (list)
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        return json.dumps(domains.keys())

    def setupDB(self, auth):
        '''
        ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        ВОЗВРАЩАЕТ:
	        True [bool]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        connection = None
        query = ''
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            adminData = '{"login":"root", "pwdHash":"30f589b7ea131c73946b7e136c9b766d:5b673242be8b0811f25f9388237ba66a", "domain":"", "privacy":9}'
            if auth[2]:
                userData = '{"login":"%s", "pwdHash":"", "domain":"%s", "privacy":9}'%(auth[0], auth[2])
            else:
                userData = '{"login":"%s", "pwdHash":"%s", "domain":"", "privacy":9}'%(auth[0], auth[1])
            secData = '{"read":[%s, "administrators", "users"], "write":[%s, "administrators"], "privacy":0}'%(1, 1)
            query = 'CREATE TABLE "{}"(id VARCHAR PRIMARY KEY, data JSONB, security JSONB); '.format('group')
            query += 'CREATE TABLE "{}"(id SERIAL PRIMARY KEY, data JSONB, security JSONB); '.format('user')
            query += "INSERT INTO \"group\"(id, data, security) VALUES ('{}', '{}', '{}'); ".format('group', '{}', secData)
            query += "INSERT INTO \"group\"(id, data, security) VALUES ('{}', '{}', '{}'); ".format('user', '{}', secData)
            query += "INSERT INTO \"group\"(id, data, security) VALUES ('{}', '{}', '{}'); ".format('security', '{}', secData)
            query += "INSERT INTO \"user\"(data, security) VALUES ('{}', '{}'); ".format(adminData, secData)
            query += "INSERT INTO \"user\"(data, security) VALUES ('{}', '{}'); ".format(userData, secData)
            query += "INSERT INTO \"group\"(id, data, security) VALUES ('{}', '{}', '{}'); ".format('administrators', '{"members":[1, 2]}', secData)
            query += "INSERT INTO \"group\"(id, data, security) VALUES ('{}', '{}', '{}'); ".format('users', '{"members":[1, 2]}', secData)
            cursor.execute(query)
            connection.commit()
        except Exception as error:
            print str(error).decode('utf8')
            raise Exception('База данных не нуждается в инициализации!')
        finally:
            if connection:
                connection.close()
        return True

    def getAuth(self, auth):
        '''
         АУТЕНТИФИКАЦИЯ ПОЛЬЗОВАТЕЛЯ
 	        АТРИБУТЫ:
 	        auth - информация для авторизации [tuple]
 		        КОРТЕЖ:
 		        login - логин [str]
 		        pwdHash - NTLM-хеш пароля [str]
 		        domain - доменное имя, при его наличии [str]
 	        ВОЗВРАЩАЕТ:
 	        True [bool]
 	        ОШИБКИ:
 	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        if getAccess(auth):
            result = True
        return result

    def addGroup(self, auth, groupIDs, groupData={}):
        '''
        СОЗДАНИЕ ГРУППЫ ПОЛЬЗОВАТЕЛЕЙ
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        groupIDs - имя группы или список имён групп [str/list]
	        groupData - данные группы [dict] {подготовленные json.dumps()}
		        КЛЮЧИ:
		        members - пользователи группы [list]
		        name (при добавлении одной группы) - отображаемое имя группы [str]
	        ВОЗВРАЩАЕТ:
	        список ID созданных групп [list]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        groupIDs = loadVar(groupIDs)
        if not isinstance(groupIDs, list):
            groupIDs = [groupIDs]
        groupData = loadVar(groupData)
        try:
            if not groupIDs:
                raise Exception('Неправильный формат "groupIDs": {}!'.format(groupIDs))
            for groupID in groupIDs:
                if (groupID in referenceTypes) or (groupID in reservedTypes):
                    try:
                        dataType = self.getType(auth, groupID)
                    except:
                        dataType = None
                    finally:
                        if not dataType:
                            raise Exception('Имя группы "{}" зарезервировано!'.format(groupID))
                if (not isinstance(groupID, unicode) and not isinstance(groupID, str)) or groupID.isdigit():
                    raise Exception('Неправильное имя группы: {}!'.format(groupID))
            if not isinstance(groupData, dict):
                raise Exception('Неправильные данные группы: {}!'.format(groupData))
            if 'name' in groupData.keys():
                if len(groupData['name']) > 1:
                    raise Exception('При создании нескольких групп разом нельзя задавать им имена!')
                try:
                    groupID = self.getGroup(auth, {'name':groupData['name']})[0][0]
                except Exception:
                    groupID = None
                finally:
                    if groupID:
                        raise Exception('Группа уже есть в системе с ID={}!'.format(groupID))
            if 'members' in groupData.keys():
                if isinstance(groupData['members'], list) and (len(groupData['members']) > 0) and isinstance(groupData['members'][0], int):
                    try:
                        self.getUser(auth, groupData['members'])
                    except Exception as error:
                        raise Exception('В "members" присутствуют несуществующие или повторяющиеся ID: {}!'.format(groupData['members']))
                else:
                    raise Exception('Неправильный список участников группы: {}!'.format(groupData['members']))
        except Exception as error:
            print str(error).decode('utf8')
            raise
        try:
            ownerID = getAccess(auth, 'group', write=True)
            secData = '{"read":[%s, "administrators", "users"], "write":[%s, "administrators"], "privacy":0}'%(ownerID, ownerID)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        connection = None
        query = ''
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            result = []
            for groupID in groupIDs:
                query = "INSERT INTO \"group\"(id, data, security) VALUES ('{}', '{}', '{}') RETURNING id".format(groupID, json.dumps(groupData), secData)
                cursor.execute(query)
                result.append(cursor.fetchone()[0])
            connection.commit()
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        return result
    
    def setGroup(self, auth, groupID, groupData):
        '''
        ИЗМЕНЕНИЕ ГРУППЫ ПОЛЬЗОВАТЕЛЕЙ
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        groupID - ID группы [str]
	        groupData - данные группы [dict] {подготовленные json.dumps()}
		        КЛЮЧИ:
		        members - пользователи группы (все старые заменяются) [list]
		        addMembers - добавление пользователей [list]
		        delMembers - удаление пользователей [list]
		        name - отображаемое имя группы [str]
	        ВОЗВРАЩАЕТ:
	        ID изменённой группы [str]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        groupID = loadVar(groupID)
        groupData = loadVar(groupData)
        try:
            if not groupData or not isinstance(groupData, dict):
                raise Exception('Неправильный формат "groupData": {}!'.format(groupData))
            name = ''
            if 'name' in groupData.keys() and groupData['name']:
                name = groupData['name']
                if (not isinstance(name, unicode) and not isinstance(name, str)) or name.isdigit():
                    raise Exception('Неправильный формат "name": {}!'.format(name))
            newMembers = []
            if 'members' in groupData.keys() and groupData['members']:
                if not isinstance(groupData['members'], list):
                    groupData['members'] = [groupData['members']]
                for entry in groupData['members']:
                    if isinstance(entry, int):
                        newMembers.append(entry)
                    elif isinstance(entry, str) and entry.isdigit():
                        newMembers.append(int(entry))
                    else:
                        raise Exception('В "members" присутствует неправильный ID: {}!'.format(entry))
                try:
                    self.getUser(auth, newMembers)
                except Exception as error:
                    raise Exception('В "members" присутствуют несуществующие или повторяющиеся ID: {}!'.format(newMembers))
            addMembers = []
            if 'addMembers' in groupData.keys() and groupData['addMembers']:
                if not isinstance(groupData['addMembers'], list):
                    groupData['addMembers'] = [groupData['addMembers']]
                for entry in groupData['addMembers']:
                    if isinstance(entry, int):
                        addMembers.append(entry)
                    elif isinstance(entry, str) and entry.isdigit():
                        addMembers.append(int(entry))
                    else:
                        raise Exception('В "addMembers" присутствует неправильный ID: {}!'.format(entry))
                try:
                    self.getUser(auth, addMembers)
                except Exception as error:
                    raise Exception('В "addMembers" присутствуют несуществующие или повторяющиеся ID: {}!'.format(addMembers))
            delMembers = []
            if 'delMembers' in groupData.keys() and groupData['delMembers']:
                if not isinstance(groupData['delMembers'], list):
                    groupData['delMembers'] = [groupData['delMembers']]
                for entry in groupData['delMembers']:
                    if isinstance(entry, int):
                        delMembers.append(entry)
                    elif isinstance(entry, str) and entry.isdigit():
                        delMembers.append(int(entry))
                    else:
                        raise Exception('В "delMembers" присутствует неправильный ID: {}!'.format(entry))
                try:
                    self.getUser(auth, delMembers)
                except Exception as error:
                    raise Exception('В "delMembers" присутствуют несуществующие или повторяющиеся ID: {}!'.format(delMembers))
        except Exception as error:
            print str(error).decode('utf8')
            raise
        try:
            getAccess(auth, 'group', dataID=groupID, write=True)
            groupData = self.getGroup(auth, groupID)[0][1]
            if not groupData:
                groupData = {}
            if not 'members' in groupData.keys():
                groupData['members'] = []
        except Exception as error:
            #print str(error).decode('utf8')
            raise
        if name:
            groupData['name'] = name
        if newMembers:
            groupData['members'] = newMembers
        if addMembers:
            groupData['members'] = list(set(groupData['members']) | set(addMembers))
        if delMembers:
            groupData['members'] = list(set(groupData['members']) - set(delMembers))
        connection = None
        query = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "UPDATE \"group\" SET data='{}' WHERE id='{}' RETURNING id".format(json.dumps(groupData), groupID)
            cursor.execute(query)
            result = cursor.fetchone()[0]
            connection.commit()
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        return result

    def getGroup(self, auth, groupFilter=[]):
        '''
        ПОЛУЧЕНИЕ ДАННЫХ ГРУППЫ ПО ID, СПИСКУ ID ИЛИ ФИЛЬТРУ.
        ФИЛЬТР ПРЕДСТАВЛЯЕТ ИЗ СЕБЯ ОДНОУРОВНЕВЫЙ СЛОВАРЬ. ВОЗВРАЩАЮТСЯ ГРУППЫ, ИМЕЮЩИЕ ТАКИЕ КЛЮЧИ С ЭТИМИ ЗНАЧЕНИЯМИ.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        groupFilter - ID, список ID или словарь с ключами [str/list/dict]
		        КЛЮЧИ:
		        members - пользователи группы [list]
		        name - отображаемое имя группы [str]
	        ВОЗВРАЩАЕТ {json.dumps()}:
	        без groupFilter - список списков [ID, data] всех групп [list]
	        при groupFilter, [dict] - список списков [ID, data] найденых групп [list]
	        при groupFilter, [list/str] - список списков [ID, data] запрошенных групп [list]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        groupFilter = loadVar(groupFilter)
        if not isinstance(groupFilter, list) and not isinstance(groupFilter, dict):
            groupFilter = [groupFilter]
        try:
            if groupFilter and isinstance(groupFilter, list):
                for groupID in groupFilter:
                    getAccess(auth, 'group', dataID=groupID)
            else:
                getAccess(auth, 'group')
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = "SELECT id,data FROM \"group\""
        if len(groupFilter) > 0:
            query += " WHERE"
            if isinstance(groupFilter, dict):
                for entry in groupFilter:
                    value = groupFilter[entry]
                    if isinstance(value, int):
                        value = [value]
                    if entry == 'name':
                        query += " LOWER(data->>'{}') LIKE LOWER('%{}%') AND".format(entry, value)
                    elif isinstance(value, list):
                        query += " (data->'{}')  @> '{}' AND".format(entry, value)
                    else:
                        query += " LOWER(data->>'{}') = LOWER('{}') AND".format(entry, value)
                query = query.rstrip(' AND')
                print 'ddd'
            else:
                for entry in groupFilter:
                    query += " id='{}' OR".format(entry)
                query = query.rstrip(' OR')
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            cursor.execute(query)
            fetch = cursor.fetchall()
            if not fetch:
                raise Exception('Группы не найдены!')
            elif isinstance(fetch[0][1], str):
                result=[]
                for entry in fetch:
                    result.append([entry[0],json.loads(entry[1])])
            else:
                result = fetch
            if isinstance(groupFilter, list) and (len(groupFilter) > 0) and (len(groupFilter) != len(result)):
                raise Exception('В поисковом запросе присутствуют несуществующие или повторяющиеся ID!')
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def delGroup(self, auth, groupIDs):
        '''
        УДАЛЕНИЕ ГРУПП
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        groupIDs - ID удаляемых групп [str/list]
	        ВОЗВРАЩАЕТ:
	        кол-во удалений >0 (int)
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        groupIDs = loadVar(groupIDs)
        if not isinstance(groupIDs, list):
            groupIDs = [groupIDs]
        try:
            if not groupIDs:
                raise Exception('Неправильный формат "groupIDs": {}!'.format(groupIDs))
            for groupID in groupIDs:
                if groupID in systemTypes:
                    raise Exception('Нельзя удалить системную группу "{}"!'.format(groupID))
                try:
                    dataType = self.getType(auth, groupID)
                except Exception:
                    dataType = None
                finally:
                    if dataType:
                        raise Exception('Группа "{}" привязана к типу!'.format(groupID))
                getAccess(auth, dataType=groupID, write=True)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "DELETE FROM \"group\" WHERE"
            for groupID in groupIDs:
                query += " id='{}' OR".format(groupID)
            query = query.rstrip(' OR')
            query += " RETURNING id"
            cursor.execute(query)
            fetch = cursor.fetchall()
            if len(fetch) > 0:
                result = len(fetch)
                for groupID in fetch:
                    groupID = [groupID[0]]
                    try:
                        security = self.getSecurity(auth, groupID)
                        security = json.loads(security)
                    except Exception as error:
                        security = {}
                    for dataType in security:
                        for entry in security[dataType]:
                            dataID = entry[0]
                            self.setSecurity(auth, {'delRead':groupID}, dataType, dataID)
            else:
                raise Exception('Ничего не было удалено.')
            connection.commit()
        except Exception as error:
            if connection:
                connection.rollback()
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def addUser(self, auth, userData, privacy=0):
        '''
        СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - имя пользователя (логин) [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        userData - данные пользователя [dict] {подготовленные json.dumps()}
		        КЛЮЧИ:
                login - имя пользователя (логин) [str]
                domain - доменное имя, при его наличии [str]
                pwdHash - NTLM-хеш пароля локального пользователя, при отсутствии domain [str]
                name - отображаемое имя пользователя [str]
                mail - электронная почта пользователя [str]
	        privacy - уровень доступа (0-9) пользователя [int]
	        ВОЗВРАЩАЕТ:
	        ID созданного пользователя [int]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        userData = loadVar(userData)
        try:
            if not userData or not isinstance(userData, dict):
                raise Exception('Неправильный формат "userData": {}!'.format(userData))
            if not 'login' in userData.keys() or not userData['login']:
                raise Exception('Необходимо задать "login" пользователя!')
            elif not isinstance(userData['login'], unicode) and not isinstance(userData['login'], str):
                raise Exception('Неправильный формат "login": {}!'.format(userData['login']))
            if not 'pwdHash' in userData.keys():
                userData['pwdHash'] = ''
            elif not isinstance(userData['pwdHash'], unicode) and not isinstance(userData['pwdHash'], str):
                raise Exception('Неправильный формат "pwdHash": {}!'.format(userData['pwdHash']))
            if not 'domain' in userData.keys() or not userData['domain']:
                userData['domain'] = ''
                if not userData['pwdHash']:
                    raise Exception('Необходимо задать "pwdHash" пользователя!')
            elif not isinstance(userData['domain'], unicode) and not isinstance(userData['domain'], str):
                raise Exception('Неправильный формат "domain": {}!'.format(userData['domain']))
            else:
                userData['pwdHash'] = ''
            if not 'name' in userData.keys():
                userData['name'] = ''
            elif not isinstance(userData['name'], unicode) and not isinstance(userData['name'], str):
                raise Exception('Неправильный формат "name": {}!'.format(userData['name']))
            if not 'mail' in userData.keys():
                userData['mail'] = ''
            elif not isinstance(userData['mail'], unicode) and not isinstance(userData['mail'], str):
                raise Exception('Неправильный формат "mail": {}!'.format(userData['mail']))
            if isinstance(privacy, int) and (0 <= privacy <= 9):
                userData['privacy'] = privacy
            else:
                raise Exception('Неправильное значение "privacy": {}!'.format(privacy))
            try:
                userID = self.getUser(auth,{'login':userData['login'], 'domain':userData['domain']})[0][0]
            except Exception:
                userID = None
            finally:
                if userID:
                    raise Exception('Пользователь уже есть в системе с ID={}!'.format(userID))
        except Exception as error:
            print str(error).decode('utf8')
            raise
        try:
            ownerID = getAccess(auth, 'user', write=True)
            secData = '{"read":[%s, "administrators", "users"], "write":[%s, "administrators"], "privacy":0}'%(ownerID, ownerID)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "INSERT INTO \"user\"(data, security) VALUES ('{}', '{}') RETURNING id".format(json.dumps(userData), secData)
            cursor.execute(query)
            result = cursor.fetchone()[0]
            connection.commit()
            self.setGroup(auth, "users", {'addMembers':result})
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        return result

    def setUser(self, auth, userID, userData):
        '''
        ИЗМЕНЕНИЕ ПОЛЬЗОВАТЕЛЯ
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        userID - ID пользователя [str]
	        userData - данные пользователя [dict] {подготовленные json.dumps()}
		        КЛЮЧИ:
                pwdHash - NTLM-хеш пароля локального пользователя, при отсутствии domain [str]
                name - отображаемое имя пользователя [str]
                mail - электронная почта пользователя [str]
	        ВОЗВРАЩАЕТ:
	        ID изменённого пользователя [int]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        userID = loadVar(userID)
        userData = loadVar(userData)
        try:
            if not userData or not isinstance(userData, dict):
                raise Exception('Неправильный формат "userData": {}!'.format(userData))
            if 'login' in userData.keys():
                    raise Exception('Изменить "login" невозможно!')
            if 'domain' in userData.keys():
                    raise Exception('Изменить "domain" невозможно!')
            name = ''
            if 'name' in userData.keys() and userData['name']:
                name = userData['name']
                if not isinstance(name, unicode) and not isinstance(name, str):
                    raise Exception('Неправильный формат "name": {}!'.format(name))
            mail = ''
            if 'mail' in userData.keys() and userData['mail']:
                mail = userData['mail']
                if not isinstance(mail, unicode) and not isinstance(mail, str):
                    raise Exception('Неправильный формат "mail": {}!'.format(mail))
            pwdHash = ''
            if 'pwdHash' in userData.keys() and userData['pwdHash']:
                pwdHash = userData['pwdHash']
                if not isinstance(pwdHash, unicode) and not isinstance(pwdHash, str):
                    raise Exception('Неправильный формат "pwdHash": {}!'.format(pwdHash))
        except Exception as error:
            print str(error).decode('utf8')
            raise
        try:
            getAccess(auth, 'user', dataID=userID, write=True)
            userData = self.getUser(auth, userID)[0][1]
            if not userData:
                raise Exception('Отсутствуют данные у пользователя с ID={}!'.format(userID))
        except Exception as error:
            print str(error).decode('utf8')
            raise
        if name:
            userData['name'] = name
        if mail:
            userData['mail'] = mail
        if pwdHash and not userData['domain']:
            userData['pwdHash'] = pwdHash
        connection = None
        query = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "UPDATE \"user\" SET data='{}' WHERE id='{}' RETURNING id".format(json.dumps(userData), userID)
            cursor.execute(query)
            result = cursor.fetchone()[0]
            connection.commit()
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        return result

    def getUser(self, auth, userFilter=[], domain=None, login=None, pwdHash=None):
        '''
        ПОЛУЧЕНИЕ ДАННЫХ ЛОКАЛЬНЫХ ИЛИ ДОМЕННЫХ ПОЛЬЗОВАТЕЛЕЙ ПО ID, СПИСКУ ID ИЛИ ФИЛЬТРУ.
        ФИЛЬТР ПРЕДСТАВЛЯЕТ ИЗ СЕБЯ ОДНОУРОВНЕВЫЙ СЛОВАРЬ. ВОЗВРАЩАЮТСЯ ГРУППЫ, ИМЕЮЩИЕ ТАКИЕ КЛЮЧИ С ЭТИМИ ЗНАЧЕНИЯМИ.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        userFilter - ID, список ID или словарь с ключами [int/str/list/dict]
		        КЛЮЧИ:
                login - имя пользователя (логин) [str]
                domain - доменное имя, при его наличии [str]
                pwdHash - NTLM-хеш пароля локального пользователя, при отсутствии domain [str]
                name - отображаемое имя пользователя [str]
                mail - электронная почта пользователя [str]
            domain - осуществлять поиск по пользователям домена [str]
            login - имя пользователя (логин) с доступом к домену, если отличное от auth [str]
            pwdHash - NTLM-хеш пароля пользователя, если отличный от auth [str]
	        ВОЗВРАЩАЕТ {json.dumps()}:
	        без userFilter - список списков [ID, data] всех пользователей [list]
	        при userFilter, [dict] - список списков [ID, data] найденых пользователей [list]
	        при userFilter, [list/int/str] - список списков [ID, data] запрошенных пользователей [list]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        userFilter = loadVar(userFilter)
        if not isinstance(userFilter, list) and not isinstance(userFilter, dict):
            userFilter = [userFilter]
        result = []
        if domain:
            if not login:
                login = auth[0]
                pwdHash = auth[1]
            ad = LDAP(login, pwdHash, domain)
            try:
                filter = '(&(sAMAccountName=*)'
                if len(userFilter) > 0:
                    if isinstance(userFilter, dict):
                        for entry in userFilter:
                            value = userFilter[entry]
                            if isinstance(value, unicode):
                                value = value.encode('utf8')
                            if entry == 'login':
                                filter += '(sAMAccountName={})'.format(value)
                            if entry == 'name':
                                filter += '(cn=*{}*)'.format(value)
                            if entry == 'mail':
                                filter += '(mail={})'.format(value)
                    else:
                        filter += '(cn=*)'
                filter += ')'
                attributes = ['sAMAccountName','cn','displayName','mail']
                base = ldapBase[domain]
            except Exception as error:
                print str(error).decode('utf8')
                raise
            connection = None
            try:
                connection = ad.connect()
                if connection.search(search_base=base, search_filter=filter.decode('utf8'), attributes=attributes):
                    i = 0
                    for entry in connection.response:
                        i += 1
                        user = {'domain':domain}
                        user['login'] = entry['attributes']['sAMAccountName']
                        user['name'] = entry['attributes']['displayName']
                        if not user['name']:
                            user['name'] = entry['attributes']['cn']
                        user['mail'] = entry['attributes']['mail']
                        result.append([i, user])
                else:
                    print filter.decode('utf8')
                    raise Exception(u'Пользователи не найдены!'.encode('cp1251'))
            except Exception as error:
                print str(error).decode('cp1251')
                raise
            finally:
                if connection:
                    connection.unbind()
        else:
            try:
                if userFilter and isinstance(userFilter, list):
                    for userID in userFilter:
                        getAccess(auth, 'user', dataID=userID)
                else:
                    getAccess(auth, 'user')
            except Exception as error:
                print str(error).decode('utf8')
                raise
            query = "SELECT id,data FROM \"user\""
            if len(userFilter) > 0:
                query += " WHERE"
                if isinstance(userFilter, dict):
                    for entry in userFilter:
                        value = userFilter[entry]
                        if entry == 'name':
                            query += " LOWER(data->>'{}') LIKE LOWER('%{}%') AND".format(entry, value)
                        elif isinstance(value, list):
                            query += " (data->'{}')  @> '{}' AND".format(entry, value)
                        else:
                            query += " LOWER(data->>'{}') = LOWER('{}') AND".format(entry, value)
                    query = query.rstrip(' AND')
                else:
                    for entry in userFilter:
                        query += " id='{}' OR".format(entry)
                    query = query.rstrip(' OR')
            connection = None
            try:
                connection = dbConnect()
                cursor = connection.cursor()
                cursor.execute(query)
                fetch = cursor.fetchall()
                if not fetch:
                    raise Exception('Пользователи не найдены!')
                elif isinstance(fetch[0][1], str):
                    result=[]
                    for entry in fetch:
                        result.append([entry[0],json.loads(entry[1])])
                else:
                    result = fetch
                if isinstance(userFilter, list) and (len(userFilter) > 0) and (len(userFilter) != len(result)):
                    raise Exception('В поисковом запросе присутствуют несуществующие или повторяющиеся ID!')
            except Exception as error:
                if query:
                    print query.decode('utf8')
                print str(error).decode('utf8')
                raise
            finally:
                if connection:
                    connection.close()
        return result

    def delUser(self, auth, userIDs):
        '''
        УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        userIDs - ID удаляемых пользователей [int/list]
	        ВОЗВРАЩАЕТ:
	        кол-во удалений >0 (int)
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        userIDs = loadVar(userIDs)
        if not isinstance(userIDs, list):
            userIDs = [userIDs]
        try:
            if not userIDs:
                raise Exception('Неправильный формат "userIDs": {}!'.format(userIDs))
            for userID in userIDs:
                if userID == getAccess(auth, 'user', dataID=userID, write=True):
                    raise Exception('Пользователю нельзя удалять самого себя!')
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "DELETE FROM \"user\" WHERE"
            for entry in userIDs:
                query += " id='{}' OR".format(entry)
            query = query.rstrip(' OR')
            query += " RETURNING id"
            cursor.execute(query)
            fetch = cursor.fetchall()
            if len(fetch) > 0:
                result = len(fetch)
                for userID in fetch:
                    userID = [userID[0]]
                    try:
                        groups = self.getGroup(auth, {'members':userID})
                    except Exception as error:
                        groups = []
                    for entry in groups:
                        self.setGroup(auth, entry[0], {'delMembers':userID})
                    try:
                        security = self.getSecurity(auth, userID)
                        security = json.loads(security)
                    except Exception as error:
                        security = {}
                    for dataType in security:
                        for entry in security[dataType]:
                            dataID = entry[0]
                            self.setSecurity(auth, {'delRead':userID}, dataType, dataID)
            else:
                raise Exception('Ничего не было удалено.')
            connection.commit()
        except Exception as error:
            if connection:
                connection.rollback()
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def setSecurity(self, auth, secData, dataType='security', dataID=None):
        '''
        ИЗМЕНЕНИЕ ИНФОРМАЦИИ О БЕЗОПАСНОСТИ ЭЛЕМЕНТА
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        secData - данные безопасности [dict] {подготовленные json.dumps()}
    		    КЛЮЧИ:
                addRead - добавление прав на чтение для групп/пользователей [list]
                delRead - удаление прав на чтение для групп/пользователей [list]
                addWrite - добавление прав на запись для групп/пользователей [list]
                delWrite - удаление прав на запись для групп/пользователей [list]
                privacy - установка уровня доступа
	        dataType - тип элемента [str] (при отсутствиии изменяются права доступа к информации о безопасности)
	        dataID - ID элемента [int/str] (при отсутствиии изменяется информация о безопасности целого типа)
	        ВОЗВРАЩАЕТ:
	        ID изменённого элемента [int/str]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        secData = loadVar(secData)
        dataType = loadVar(dataType)
        try:
            if not secData or not isinstance(secData, dict):
                raise Exception('Неправильный формат "secData": {}!'.format(secData))
            addRead = []
            if 'addRead' in secData.keys() and secData['addRead']:
                addRead = secData['addRead']
                if not isinstance(addRead, list):
                    addRead = [addRead]
                userIDs = []
                groupIDs = []
                for entry in addRead:
                    if isinstance(entry, int):
                        userIDs.append(entry)
                    elif isinstance(entry, str) and entry.isdigit():
                        userIDs.append(int(entry))
                    elif isinstance(entry, str) and entry:
                        groupIDs.append(entry)
                    else:
                        raise Exception('Неправильный формат "addRead": {}!'.format(addRead))
                try:
                    if userIDs:
                        self.getUser(auth, userIDs)
                    if groupIDs:
                        self.getGroup(auth, groupIDs)
                except Exception as error:
                    raise Exception('В "addRead" присутствуют несуществующие или повторяющиеся ID: {}!'.format(addRead))
                addRead = list(userIDs)
                addRead.extend(groupIDs)
            delRead = []
            if 'delRead' in secData.keys() and secData['delRead']:
                delRead = secData['delRead']
                if not isinstance(delRead, list):
                    delRead = [delRead]
                userIDs = []
                groupIDs = []
                for entry in delRead:
                    if isinstance(entry, int):
                        userIDs.append(entry)
                    elif isinstance(entry, str) and entry.isdigit():
                        userIDs.append(int(entry))
                    elif isinstance(entry, str) and entry:
                        groupIDs.append(entry)
                    else:
                        raise Exception('Неправильный формат "delRead": {}!'.format(delRead))
                delRead = list(userIDs)
                delRead.extend(groupIDs)
            addWrite = []
            if 'addWrite' in secData.keys() and secData['addWrite']:
                addWrite = secData['addWrite']
                if not isinstance(addWrite, list):
                    addWrite = [addWrite]
                userIDs = []
                groupIDs = []
                for entry in addWrite:
                    if isinstance(entry, int):
                        userIDs.append(entry)
                    elif isinstance(entry, str) and entry.isdigit():
                        userIDs.append(int(entry))
                    elif isinstance(entry, str) and entry:
                        groupIDs.append(entry)
                    else:
                        raise Exception('Неправильный формат "addWrite": {}!'.format(addWrite))
                try:
                    if userIDs:
                        self.getUser(auth, userIDs)
                    if groupIDs:
                        self.getGroup(auth, groupIDs)
                except Exception as error:
                    raise Exception('В "addWrite" присутствуют несуществующие или повторяющиеся ID: {}!'.format(addWrite))
                secData['addWrite'] = [userIDs].extend(groupIDs)
                addWrite = list(userIDs)
                addWrite.extend(groupIDs)
            delWrite = []
            if 'delWrite' in secData.keys() and secData['delWrite']:
                delWrite = secData['delWrite']
                if not isinstance(delWrite, list):
                    delWrite = [delWrite]
                userIDs = []
                groupIDs = []
                for entry in delWrite:
                    if isinstance(entry, int):
                        userIDs.append(entry)
                    elif isinstance(entry, str) and entry.isdigit():
                        userIDs.append(int(entry))
                    elif isinstance(entry, str) and entry:
                        groupIDs.append(entry)
                    else:
                        raise Exception('Неправильный формат "delWrite": {}!'.format(delWrite))
                delWrite = list(userIDs)
                delWrite.extend(groupIDs)
            privacy = 0
            if 'privacy' in secData.keys() and secData['privacy']:
                privacy = secData['privacy']
                if not isinstance(privacy, int) or (privacy < 0) or (privacy > 9):
                    raise Exception('Неправильный формат "privacy": {}!'.format(privacy))


####    Проверка на сохранение доступа после изменений



        except Exception as error:
            print str(error).decode('utf8')
            raise
        try:
            getAccess(auth, 'security', write=True)
            if dataID:
                getAccess(auth, dataType, dataID, write=True)
                security = self.getSecurity(auth, [], dataType, dataID)
                secData = json.loads(security)[dataType][0][1]
            else:
                getAccess(auth, dataType, write=True)
                security = self.getSecurity(auth, [], dataType)
                secData = json.loads(security)[dataType][0][1]
        except Exception as error:
            print str(error).decode('utf8')
            raise
        if privacy:
            secData['privacy'] = privacy
        if addRead:
            secData['read'] = list(set(secData['read']) | set(addRead))
        if addWrite:
            secData['write'] = list(set(secData['write']) | set(addWrite))
            secData['read'] = list(set(secData['read']) | set(addWrite))
        if delWrite:
            secData['write'] = list(set(secData['write']) - set(delWrite))
        if delRead:
            secData['read'] = list(set(secData['read']) - set(delRead))
            secData['write'] = list(set(secData['write']) - set(delRead))
        query = ""
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            if dataID:
                query += "UPDATE \"{}\" SET security='{}' WHERE id='{}' RETURNING id".format(dataType, json.dumps(secData), dataID)
            else:
                query += "UPDATE \"group\" SET security='{}' WHERE id='{}' RETURNING id".format(json.dumps(secData), dataType)
            cursor.execute(query)
            result = cursor.fetchone()[0]
            connection.commit()
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        return result

    def getSecurity(self, auth, secFilter=[], dataTypes=[], dataIDs=[]):
        '''
        ПОЛУЧЕНИЕ ИНФОРМАЦИИ О БЕЗОПАСНОСТИ ЭЛЕМЕНТА
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        secFilter - ID, список ID или словарь с ключами [int/str/list/dict]
    		    КЛЮЧИ:
                read - список групп/пользователей с правами на чтение [list]
                write - список групп/пользователей с правами на запись [list]
                privacy - уровень доступа
	        dataTypes - типы элементов [str/list] (при отсутствиии изменяются права доступа к информации о безопасности)
	        dataIDs - ID элемента [int/str/list] (при отсутствиии изменяется информация о безопасности целого типа)
	        ВОЗВРАЩАЕТ {json.dumps()}:
	        без secFilter - словарь типов со списками [ID, security] всех элементов, к которым есть доступ у текущего пользователя [dict]
	        при secFilter [dict] - словарь типов со списками [ID, security] элементов, соответствующих фильтру [dict]
	        при secFilter [list/int/str] - словарь типов со списками [ID, security] всех элементов, к которым есть доступ у заданых пользователей/групп [dict]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        secFilter = loadVar(secFilter)
        dataTypes = loadVar(dataTypes)
        if not isinstance(dataTypes, list):
            dataTypes = [dataTypes]
        dataIDs = loadVar(dataIDs)
        if not isinstance(dataIDs, list):
            dataIDs = [dataIDs]
        try:
            if len(dataTypes) > 1:
                raise Exception('Поиск по ID возможен только по одному типу данных!')
            userID = getAccess(auth, 'security')
            if dataIDs:
                for dataID in dataIDs:
                    for dataType in dataTypes:
                        getAccess(auth, dataType, dataID)
            else:
                for dataType in dataTypes:
                    getAccess(auth, dataType)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ""
        result = {}
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            if dataIDs:
                for dataID in dataIDs:
                    for dataType in dataTypes:
                        result[dataType] = []
                        if secFilter:
                            query += "SELECT '{0}' AS table_name,CAST(id AS VARCHAR),security FROM \"{0}\" WHERE id='{1}'".format(dataType, dataID)
                            query += " AND ((security->'read' @> '{0}') OR (security->'write' @> '{0}'))".format(json.dumps(secFilter))
                            query += ' UNION '
                        else:
                            query += "SELECT '{0}' AS table_name,CAST(id AS VARCHAR),security FROM \"{0}\" WHERE id='{1}'".format(dataType, dataID)
                            query += ' UNION '
                query = query.rstrip(' UNION ')
            elif dataTypes:
                for dataType in dataTypes:
                    result[dataType] = []
                    if secFilter:
                        query += "SELECT '{0}' AS table_name,CAST(id AS VARCHAR),security FROM \"group\" WHERE id='{0}'".format(dataType)
                        query += " AND ((security->'read' @> '{0}') OR (security->'write' @> '{0}'))".format(json.dumps(secFilter))
                        query += ' UNION '
                        try:
                            self.getType(auth, dataType)
                            query += "SELECT '{0}' AS table_name,CAST(id AS VARCHAR),security FROM \"{0}\" WHERE".format(dataType)
                            query += " ((security->'read' @> '{0}') OR (security->'write' @> '{0}'))".format(json.dumps(secFilter))
                            query += ' UNION '
                        except:
                            pass
                    else:
                        query += "SELECT '{0}' AS table_name,CAST(id AS VARCHAR),security FROM \"group\" WHERE id='{0}'".format(dataType)
                        query += ' UNION '
                query = query.rstrip(' UNION ')
            elif secFilter:
                dataTypes = self.getType(auth).keys()
                if isinstance(secFilter, dict):
                    if ('read' in secFilter.keys()) and secFilter['read']:
                        secFilter['read'] = json.dumps(secFilter['read'])
                    else:
                        secFilter['read'] = []
                    if ('write' in secFilter.keys()) and secFilter['write']:
                        secFilter['write'] = json.dumps(secFilter['write'])
                    else:
                        secFilter['write'] = []
                    if not ('privacy' in secFilter.keys()) or not secFilter['privacy']:
                           secFilter['privacy'] = []
                    for dataType in dataTypes:
                        result[dataType] = []
                        query += "SELECT '{0}' AS table_name,CAST(id AS VARCHAR),security FROM \"{0}\" WHERE".format(dataType)
                        if not secFilter['read'] and not secFilter['write'] and not secFilter['privacy']:
                            query += " (security->'read') @> '{0}' OR (security->'write') @> '{0}'".format(userID)
                        if secFilter['read']:
                            query += " (security->'read') @> '{0}' AND".format(secFilter['read'])
                        if secFilter['write']:
                            query += " (security->'write') @> '{0}' AND".format(secFilter['write'])
                        if secFilter['privacy']:
                            query += " (security->>'privacy') = '{0}' AND".format(secFilter['privacy'])
                        query = query.rstrip(' AND')
                        query += ' UNION '
                    query = query.rstrip(' UNION ')
                else:
                    for dataType in dataTypes:
                        result[dataType] = []
                        query += "SELECT '{0}' AS table_name,CAST(id AS VARCHAR),security FROM \"{0}\" WHERE (security->'read') @> '{1}' OR (security->'write') @> '{1}'".format(dataType, json.dumps(secFilter))
                        query += ' UNION '
                    query = query.rstrip(' UNION ')
            else:
                dataTypes = self.getType(auth).keys()
                for dataType in dataTypes:
                    result[dataType] = []
                    query += "SELECT '{0}' AS table_name,CAST(id AS VARCHAR),security FROM \"{0}\" WHERE".format(dataType)
                    query += " (security->'read') @> '{0}' OR (security->'write') @> '{0}'".format(userID)
                    query += ' UNION '
                query = query.rstrip(' UNION ')
            cursor.execute(query)
            fetch = cursor.fetchall()
            if not fetch:
                raise Exception('Не найдена информация о безопасности, соответствующая фильтру!')
            if isinstance(fetch[0][2], str):
                for entry in fetch:
                    result[entry[0]].append([(entry[1]), json.loads(entry[2])])
            else:
                for entry in fetch:
                    result[entry[0]].append([(entry[1]), entry[2]])
            # Очищаем словарь от ключей без значений
            result = dict([(key, value) for key, value in result.iteritems() if value])
        except Exception as error:
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        result = json.dumps(result)
        return result

    def addType(self, auth, dataTypes):
        '''
        СОЗДАНИЕ ТИПА ДАННЫХ
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        dataTypes - имя типа или список имён типов [str/list]
	        ВОЗВРАЩАЕТ:
	        список имён созданных типов [list]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        dataTypes = loadVar(dataTypes)
        if not isinstance(dataTypes, list):
            dataTypes = [dataTypes]
        try:
            if not dataTypes:
                raise Exception('Необходимо задать "dataTypes"!')
            else:
                for dataType in dataTypes:
                    if (not isinstance(dataType, unicode) and not isinstance(dataType, str)) or dataType.isdigit():
                        raise Exception('Неправильный формат в "dataTypes": {}!'.format(dataType))
        except Exception as error:
            print str(error).decode('utf8')
            raise
        try:
            getAccess(auth, 'group', write=True)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        groupIDs = []
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            for dataType in dataTypes:
                if dataType in referenceTypes:
                    raise Exception('Тип "{}" зарезервирован!'.format(dataType))
                query += 'CREATE TABLE "{}"'.format(dataType)
                try:
                    groupData = self.getGroup(auth, dataType)
                except Exception:
                    groupData = None
                finally:
                    if groupData:
                        raise Exception('Уже существует группа с именем добавляемого типа: {}!'.format(dataType))
                    else:
                        groupIDs.append(dataType)
                if dataType in reservedTypes:
                    query += "(id VARCHAR PRIMARY KEY, data JSONB, security JSONB); "
                    for entry in reservedTypes[dataType]:
                        query += "CREATE TABLE \"{}\"(id VARCHAR PRIMARY KEY REFERENCES {}(id), data JSONB, security JSONB); ".format(entry, dataType)
                        try:
                            groupData = self.getGroup(auth, entry)
                        except Exception:
                            groupData = None
                        finally:
                            if groupData:
                                raise Exception('Уже существует группа с именем добавляемого типа: {}!'.format(dataType))
                            else:
                                groupIDs.append(entry)
                elif dataType == 'file':
                    query += "(id SERIAL PRIMARY KEY, data BYTEA, info JSONB, security JSONB); "
                elif dataType == 'group':
                    query += "(id VARCHAR PRIMARY KEY, data JSONB, security JSONB); "
                else:
                    query += "(id SERIAL PRIMARY KEY, data JSONB, security JSONB); "
            query = query.rstrip('; ')
            cursor.execute(query)
            connection.commit()
            self.addGroup(auth, groupIDs)
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        result = groupIDs
        return result

    def getType(self, auth, dataTypes=[]):
        '''
        ИНФОРМАЦИЯ О ТИПЕ ДАННЫХ
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        dataTypes - имя типа или список имён типов [str/list]
	        ВОЗВРАЩАЕТ:
            без dataTypes - словарь из названий и формата данных всех типов [dict]
	        при dataTypes [list/int/str] - словарь из названий и формата данных заданных типов [dict]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        dataTypes = loadVar(dataTypes)
        if not isinstance(dataTypes, list):
            dataTypes = [dataTypes]
        connection = None
        query = ''
        result = {}
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            if len(dataTypes) == 0:
                cursor.execute("SELECT current_database()")
                dbName = cursor.fetchone()[0]
                query = "SELECT TABLE_NAME FROM {}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'public'".format(dbName)
                cursor.execute(query)
                dataTypes = []
                for entry in cursor.fetchall():
                    dataTypes.append(entry[0])
            for dataType in dataTypes:
####            getAccess(auth, 'group', dataType)
                query = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' AND COLUMN_NAME = 'data'".format(dataType)
                cursor.execute(query)
                fetch = cursor.fetchone()
                if fetch:
                    result[dataType] = fetch[0]
                else:
                    raise Exception('Типа "{}" не существует!'.format(dataType))
            if len(result) == 1:
                result = result.values()[0]
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def delType(self, auth, dataTypes):
        '''
        УДАЛЕНИЕ ТИПОВ ДАННЫХ
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        dataTypes - имя типа или список имён типов [str/list]
	        ВОЗВРАЩАЕТ:
	        кол-во удалений >0 (int)
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        dataTypes = loadVar(dataTypes)
        if not isinstance(dataTypes, list):
            dataTypes = [dataTypes]
        try:
            if not dataTypes:
                raise Exception('Необходимо задать "dataTypes"!')
            getAccess(auth, 'group', write=True)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        groupIDs = []
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            for dataType in dataTypes:
                groupIDs.append(dataType)
                if dataType in referenceTypes:
                    raise Exception('Тип "{}" защищён от изменения напрямую!'.format(dataType))
                if dataType in systemTypes:
                    raise Exception('Тип "{}" защищён от изменения!'.format(dataType))
                if dataType in reservedTypes:
                    for entry in reservedTypes[dataType]:
                        groupIDs.append(entry)
                        query = 'DROP TABLE "{}"; '.format(entry) + query
                query += 'DROP TABLE "{}"; '.format(dataType)
            query = query.rstrip('; ')
            cursor.execute(query)
            connection.commit()
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        try:
            result = self.delGroup(auth, groupIDs)
        except:
            result = len(groupIDs)
        return result

    def addData(self, auth, dataType, dataID=None, data={}):
        '''
        ДОБАВЛЕНИЕ ЭЛЕМЕНТА ЗАДАННОГО ТИПА С АВТОМАТИЧЕСКИМ ПОЛУЧЕНИЕМ ID, ЕСЛИ НЕ УКАЗАН КОНКРЕТНЫЙ.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        dataType - тип элемента [str]
	        dataID	- ID элемента [int/str]
	        data - данные элемента [dict/list]  {подготовленные json.dumps()}
	        ВОЗВРАЩАЕТ:
	        при пустом('') dataID, если тип позволяет, - автоинкриментный ID добавленного элемента [int]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        dataType = loadVar(dataType)
        dataID = loadVar(dataID)
        try:
            if dataType == 'file':
                raise Exception('Для работы с файлами необходимо использовать метод addFile()!')
            ownerID = getAccess(auth, dataType, write=True)
            secData = '{"read":[%s, "administrators", "users"], "write":[%s, "administrators"], "privacy":0}'%(ownerID, ownerID)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "INSERT INTO {} ".format(dataType)
            if (dataType in reservedTypes) or (dataType in referenceTypes):
                if dataID:
                    query += "(id,data,security) VALUES ('{}', '{}', '{}') RETURNING id; ".format(dataID, data, secData)
                    for entry in reservedTypes[dataType]:
                        query += "INSERT INTO {} (id,security) VALUES ('{}', '{}') RETURNING id; ".format(entry, dataID, secData)
                else:
                    raise Exception('ID типу "{}" не выдаются автоматически.'.format(dataType))
            else:
                query += "(data,security) VALUES ('{}', '{}') RETURNING id".format(data, secData)
            cursor.execute(query)
            fetch = cursor.fetchone()
            result = fetch[0]
            connection.commit()
        except Exception as error:
            if connection:
                connection.rollback()
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def setData(self, auth, dataType, dataID, data):
        '''
        ЗАМЕНА ЭЛЕМЕНТА ЗАДАННОГО ТИПА С УКАЗАННЫМ ID.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        dataType - тип элемента [str]
	        dataID	- ID элемента [int/str]
	        data - данные элемента [dict/list]  {подготовленные json.dumps()}
	        ВОЗВРАЩАЕТ:
	        кол-во изменений >0 (int)
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        dataType = loadVar(dataType)
        dataID = loadVar(dataID)
        try:
            if dataType == 'file':
                raise Exception('Для работы с файлами необходимо использовать метод addFile().')
            getAccess(auth, dataType, dataID, write=True)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "UPDATE {} SET data='{}' WHERE id='{}' RETURNING id".format(dataType, data, dataID)
            cursor.execute(query)
            result = len(cursor.fetchall())
            connection.commit()
        except Exception as error:
            if connection:
                connection.rollback()
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def getData(self, auth, dataType, dataFilter=[]):
        '''
        ПОЛУЧЕНИЕ ЭЛЕМЕНТА ЗАДАННОГО ТИПА ПО ID, СПИСКУ ID ИЛИ ФИЛЬТРУ.
        ФИЛЬТР ПРЕДСТАВЛЯЕТ ИЗ СЕБЯ ОДНОУРОВНЕВЫЙ СЛОВАРЬ. ВОЗВРАЩАЮТСЯ ЭЛЕМЕНТЫ, ИМЕЮЩИЕ ТАКИЕ КЛЮЧИ СО ЗНАЧЕНИЯМИ.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        dataType - тип элемента [str]
	        dataFilter - ID, список ID или словарь для поиска по данным о элементов [int/str/list/dict]
	        ВОЗВРАЩАЕТ {json.dumps()}:
	        при dataFilter, [dict] - список списков [ID, data] найденых записей [list]
	        при dataFilter, [dict/list пустой] - список списков [ID, data] всех записей [list]
	        при dataFilter, [list/int/str] - список списков [ID, data] запрошенных записей [list]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        dataType = loadVar(dataType)
        dataFilter = loadVar(dataFilter)
        if not isinstance(dataFilter, list) and not isinstance(dataFilter, dict):
            dataFilter = [dataFilter]
        try:
            if dataType == 'file':
                raise Exception('Для работы с файлами необходимо использовать метод getFile().')
            if dataFilter and isinstance(dataFilter, list):
                for dataID in dataFilter:
                    getAccess(auth, dataType, dataID)
            else:
                getAccess(auth, dataType)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = 'SELECT id,data FROM "{}"'.format(dataType)
            if len(dataFilter) > 0:
                query += " WHERE"
                if isinstance(dataFilter, dict):
                    for entry in dataFilter:
                        query += " data ->> '{}'='{}' AND".decode('utf8').format(entry, dataFilter[entry])
                    query = query.rstrip(' AND')
                else:
                    for entry in dataFilter:
                        query += " id='{}' OR".format(entry)
                    query = query.rstrip(' OR')
            else:
                pass
            cursor.execute(query)
            fetch = cursor.fetchall()
            if not fetch:
                raise Exception('Не найдены данные по фильтру: {}!'.format(dataFilter))
            elif isinstance(fetch[0][1], str):
                result=[]
                for entry in fetch:
                    result.append([entry[0],json.loads(entry[1])])
                result = json.dumps(result)
            else:
                result=json.dumps(fetch)
        except Exception as error:
            if connection:
                connection.rollback()
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def delData(self, auth, dataType, dataIDs):
        '''
        УДАЛЕНИЕ ЭЛЕМЕНТОВ ЗАДАННОГО ТИПА С УКАЗАННЫМИ ID.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        dataType - тип элемента [str]
	        dataIDs - ID удаляемых элементов [int/str/list]
	        ВОЗВРАЩАЕТ:
	        кол-во удалений >0 (int)
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        dataType = loadVar(dataType)
        dataIDs = loadVar(dataIDs)
        if not isinstance(dataIDs, list):
            dataIDs = [dataIDs]
        try:
            if not dataIDs:
                raise Exception('Аргумент "dataIDs" не может быть пустым!')
            for dataID in dataIDs:
                getAccess(auth, dataType, dataID, write=True)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            if dataType in reservedTypes:
                for entry in reservedTypes[dataType]:
                    query += "DELETE FROM {} WHERE".format(entry)
                    for dataID in dataIDs:
                        query += " id='{}' OR".format(dataID)
                    query = query.rstrip(' OR')
                    query += "; "
            query += "DELETE FROM {} WHERE".format(dataType)
            for dataID in dataIDs:
                query += " id='{}' OR".format(dataID)
            query = query.rstrip(' OR')
            query += " RETURNING id"
            cursor.execute(query)
            fetch = cursor.fetchall()
            if len(fetch) > 0:
                result = len(fetch)
            else:
                raise Exception('Ничего не было удалено.')
                result = False
            connection.commit()
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        return result

    def addFile(self, auth, dataType, dataID, fileData, fileInfo={}):
        '''
        ДОБАВЛЕНИЕ ФАЙЛА И ДОПОЛНИТЕЛЬНОЙ ИНФОРМАЦИИ О НЁМ.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        dataType - тип объекта, с которым связан файл [str]
	        dataID - ID объекта, с которым связан файл [int или str]
	        fileInfo - дополнительная информация о файле [dict] {подготовленный json.dumps()}
		        добавляемые сервером поля:
		        - size - размер в байтах [int];
		        - md5 - хэш-сумма MD5 [str];
		        - added - время добавления вида 2017-10-25 12:03:46.168766+03:00 [str].
		        рекомендуемые пользовательские поля:
		        - name - имя файла с расширением [str];
		        - modified - время изменения {os.stat(<ИМЯ ФАЙЛА>).st_mtime} [float];
		        - secret - уровень секретности [int];
		        - permissions - права доступа к файлу [???].
	        fileData - содержимое файла в виде xmlrpclib.Binary(<ДАННЫЕ ФАЙЛА>) [instance]
	        ВОЗВРАЩАЕТ:
	        автоинкриментный ID добавленного файла [int]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        dataType = loadVar(dataType)
        dataID = loadVar(dataID)
        fileInfo = loadVar(fileInfo)
        if not fileInfo:
            fileInfo = {}
        try:
            ownerID = getAccess(auth, 'file', write=True)
            secData = '{"read":[%s, "administrators", "users"], "write":[%s, "administrators"], "privacy":0}'%(ownerID, ownerID)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "INSERT INTO file (data,security) VALUES ({}, '{}') RETURNING id, now(), length(data), md5(data)".format(dbBinary(fileData), secData)
            cursor.execute(query)
            fetch = cursor.fetchone()
            fileID = fetch[0]
            fileInfo['dataType'] = dataType
            fileInfo['dataID'] = dataID
            fileInfo['added'] = str(fetch[1])
            fileInfo['size'] = fetch[2]
            fileInfo['md5'] = fetch[3]
            fileInfo = json.dumps(fileInfo)
            query = "UPDATE file SET info = '{}' WHERE id = '{}' RETURNING id".format(fileInfo, fileID)
            cursor.execute(query)
            result = cursor.fetchone()[0]
            connection.commit()
        except Exception as error:
            if connection:
                connection.rollback()
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def infFile(self, auth, fileFilter=[]):
        '''
        ИНФОРМАЦИЯ О ФАЙЛАХ ПО ID, СПИСКУ ID ИЛИ ФИЛЬТРУ.
        ФИЛЬТР ПРЕДСТАВЛЯЕТ ИЗ СЕБЯ ОДНОУРОВНЕВЫЙ СЛОВАРЬ. ВОЗВРАЩАЮТСЯ ЭЛЕМЕНТЫ, ИМЕЮЩИЕ ТАКИЕ КЛЮЧИ СО ЗНАЧЕНИЯМИ.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        fileFilter - ID, список ID или словарь для поиска по информации о файлах
	        ВОЗВРАЩАЕТ:
	        при fileFilter [dict] - список списков [ID, fileInfo] найденых файлов [list]
	        при fileFilter [dict/list пустой] - список списков [ID, fileInfo] всех файлов [list]
	        при fileFilter [list, int, str] - список списков [ID, fileInfo] запрошенных файлов [dict]
		        fileInfo [dict]:
		          dataType - тип объекта, с которым связан файл [str];
		          dataID - ID объекта, с которым связан файл [int или str];
		          size - размер в байтах [int];
		          md5 - хэш-сумма MD5 [str];
		          added - время добавления вида 2017-10-25 12:03:46.168766+03:00 [str];
		          другие пользовательские поля.
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        fileFilter = loadVar(fileFilter)
        if not isinstance(fileFilter, list) and not isinstance(fileFilter, dict):
            fileFilter = [fileFilter]
        try:
            if fileFilter and isinstance(fileFilter, list):
                for fileID in fileFilter:
                    getAccess(auth, 'file', dataID=fileID)
            else:
                getAccess(auth, 'file')
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "SELECT id,info FROM file"
            if len(fileFilter) > 0:
                query += " WHERE"
                if isinstance(fileFilter, dict):
                    for entry in fileFilter:
                        query += " info ->> '{}'='{}' AND".decode('utf8').format(entry, fileFilter[entry])
                    query = query.rstrip(' AND')
                else:
                    for entry in fileFilter:
                        query += " id='{}' OR".format(entry)
                    query = query.rstrip(' OR')
            else:
                pass
            cursor.execute(query)
            fetch = cursor.fetchall()
            if not fetch:
                raise Exception('Не найдено файлов по фильтру: {}!'.format(fileFilter))
                result = False
            elif isinstance(fetch[0][1], str):
                result=[]
                for entry in fetch:
                    result.append([entry[0],json.loads(entry[1])])
                result = json.dumps(result)
            else:
                result=json.dumps(fetch)
        except Exception as error:
            if connection:
                connection.rollback()
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def getFile(self, auth, fileID):
        '''
        ЗАПРС ФАЙЛА.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        fileID - ID, запрашиваемого файла [int/str]
	        ВОЗВРАЩАЕТ:
	        содержимое файла в виде xmlrpclib.Binary()
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        fileID = loadVar(fileID)
        query = ''
        connection = None
        try:
            getAccess(auth, 'file', dataID=fileID)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "SELECT data FROM file WHERE id='{}'".format(fileID)
            cursor.execute(query)
            fetch = cursor.fetchone()
            if not fetch:
                raise Exception('Файла c ID="{}" не существует!'.format(fileID))
                result = False
            elif fetch[0] is None:
                raise Exception('Файл c ID="{}" пустой!'.format(fileID))
                result = False
            else:
                result = Binary(fetch[0])
        except Exception as error:
            if connection:
                connection.rollback()
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
        return result

    def delFile(self, auth, fileIDs):
        '''
        УДАЛЕНИЕ ФАЙЛОВ.
	        АТРИБУТЫ:
	        auth - информация для авторизации [tuple]
		        КОРТЕЖ:
		        login - логин [str]
		        pwdHash - NTLM-хеш пароля [str]
		        domain - доменное имя, при его наличии [str]
	        fileIDs - ID, удаляемых файлов [int/str/list]
	        ВОЗВРАЩАЕТ:
	        количество удалённых элементов >0 [int]
	        ОШИБКИ:
	        Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
        '''
        fileIDs = loadVar(fileIDs)
        if not isinstance(fileIDs, list):
            fileIDs = [fileIDs]
        try:
            if not fileIDs:
                raise Exception('Аргумент "fileIDs" не может быть пустым!')
            for fileID in fileIDs:
                getAccess(auth, 'file', dataID=fileID, write=True)
        except Exception as error:
            print str(error).decode('utf8')
            raise
        query = ''
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            query = "DELETE FROM file WHERE"
            for entry in fileIDs:
                query += " id='{}' OR".format(entry)
            query = query.rstrip(' OR')
            query += " RETURNING id"
            cursor.execute(query)
            fetch = cursor.fetchall()
            if len(fetch) > 0:
                result = len(fetch)
            else:
                raise Exception('Ничего не было удалено.')
                result = False
            connection.commit()
        except Exception as error:
            if query:
                print query.decode('utf8')
            print str(error).decode('utf8')
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
        return result

