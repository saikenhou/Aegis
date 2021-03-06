from gino import Gino

db = Gino()


class CommandPermission(db.Model):
    __tablename__ = 'permission'
    number = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    id = db.Column(db.BigInteger)
    name = db.Column(db.String(100))
    roles = db.Column(db.String(2000), default='')  # 使えるroleのリスト、,で区切る
    users = db.Column(db.String(2000), default='')  # 使えるuserのリスト、,で区切る


class CommandHistory(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    user_id = db.Column(db.BigInteger)
    command = db.Column(db.String(80))
    channel_id = db.Column(db.BigInteger)
    guild_id = db.Column(db.BigInteger)
    timestamp = db.Column(db.BigInteger)


class Alias(db.Model):
    __tablename__ = 'alias'
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    user_id = db.Column(db.BigInteger)
    name = db.Column(db.String(200))
    command = db.Column(db.String(200))


class Impression(db.Model):
    __tablename__ = 'impression'
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    user_id = db.Column(db.BigInteger)
    count = db.Column(db.BigInteger)
    type = db.Column(db.String(200))
    message_id = db.Column(db.BigInteger)
    timestamp = db.Column(db.BigInteger)


class VisitMemberAnalytics(db.Model):
    __tablename__ = 'memberanalytics'
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    user_id = db.Column(db.BigInteger)
    type = db.Column(db.String(200))  # join or remove
    guild_id = db.Column(db.BigInteger)
    timestamp = db.Column(db.BigInteger)


def get(_id, name):
    return CommandPermission.query.where(CommandPermission.id == _id).where(CommandPermission.name == name).gino.first()


async def is_exist(_id, name):
    if not await get(_id, name):
        return False

    return True


async def create(_id, name):
    if await is_exist(_id, name):
        return await get(_id, name)

    return await CommandPermission.create(id=_id, name=name)


async def delete(_id, name):
    permission = await get(_id, name)
    if permission:
        await permission.delete()
        return True

    return None


async def add_role(_id, name, role_id):
    permission = await get(_id, name)
    if not permission:
        return None

    if str(role_id) in permission.roles:
        return False

    await permission.update(roles=permission.roles + f"{role_id},").apply()
    return True


async def delete_role(_id, name, role_id):
    permission = await get(_id, name)
    if not permission:
        return None

    if not str(role_id) in permission.roles:
        return False

    await permission.update(roles=permission.roles.replace(f'{role_id},', '')).apply()
    return True


async def add_user(_id, name, user_id):
    permission = await get(_id, name)
    if not permission:
        return None

    if str(user_id) in permission.users:
        return False

    await permission.update(roles=permission.users + f"{user_id},").apply()
    return True


async def delete_user(_id, name, user_id):
    permission = await get(_id, name)

    if not permission:
        return None

    if not str(user_id) in permission.users:
        return False

    await permission.update(roles=permission.roles.replace(f'{user_id},', '')).apply()
    return True
