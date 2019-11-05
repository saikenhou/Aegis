from .database import CommandPermission
import discord
from discord.ext import commands


async def check_command_permission(context: commands.Context):
    """
    権限周りについて:
        DMの場合確実に有効
        CommandPermissionがなければそもそも有効化されていない
        作成されていて、かつroles、users、permissionsが空であれば誰でも使える

    :param context: commands.Context
    :return: bool
    """

    #  DMの場合
    if not context.guild:
        return True

    #  manage系、ヘルプコマンドだった場合
    if context.command.name == 'help':
        return True

    elif context.cog:
        if context.cog.qualified_name == 'ManageCog':
            return True

    p: CommandPermission = await CommandPermission.query.where(CommandPermission.id == context.guild.id) \
        .where(CommandPermission.name == context.command.name).gino.first()

    #  ない場合
    if not p:
        return False

    #  制限なしの場合
    if not p.roles and not p.users and not p.permissions:
        return True

    checks = []

    if p.roles:
        is_id_in = any(True for i in context.author.roles if str(i.id) in p.roles)

        checks.append(is_id_in)

    if p.users:
        checks.append(True if str(context.author.id) in p.users else False)

    if p.permissions:
        has_permission = any([True for value in p.permissions.split(',')
                              if discord.Permissions(int(value)).is_subset(context.author.guild_permissions)
                              ])

        checks.append(has_permission)

    return any(checks)