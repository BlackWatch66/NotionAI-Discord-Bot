import os

from dotenv import load_dotenv
import discord
from notionai import NotionAI, ToneEnum, TranslateLanguageEnum
from src.discordBot import DiscordClient, Sender
from src.logger import logger
from src.server import keep_alive
load_dotenv()


def run():
    client = DiscordClient()
    sender = Sender()
    notion_ai = NotionAI(os.getenv('NOTION_TOKEN'), os.getenv('NOTION_SPACE_ID'))

    @client.tree.command(name="help_me_write", description="帮我写，让AI为您写作")
    async def help_me_write(interaction: discord.Interaction, *, prompt: str, context: str, page_title: str = "", rest_content: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.help_me_write(prompt, context, page_title, rest_content)
        send_message = f"[help_me_write] prompt: {prompt} \n context: {context} \n page_title: {page_title} \n rest_content: {rest_content}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="write", description="写")
    async def write(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.write(prompt)
        send_message = f"[wirte] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)


    @client.tree.command(name="continue_write", description="继续写作，生成更多内容")
    async def continue_write(interaction: discord.Interaction, *, context: str, page_title: str = "", rest_content: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.continue_write(context, page_title, rest_content)
        send_message = f"[continue_write] context: {context} \n page_title: {page_title} \n rest_content: {rest_content}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="help_me_edit", description="帮我编辑，它将更改当前上下文")
    async def help_me_edit(interaction: discord.Interaction, *, prompt: str, context: str, page_title: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.help_me_edit(prompt, context, page_title)
        send_message = f"[help_me_edit] prompt: {prompt} \n context: {context} \n page_title: {page_title} "
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="translate", description="使用NotionAI翻译您的上下文")
    async def translate(interaction: discord.Interaction, *, language: str, context: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        send_message = f"[translate] language: {language} \n context: {context}"

        language = language.lower()
        try:
            language = TranslateLanguageEnum(language)
        except Exception:
            error_message = "❌ 错误：语言只能是：英语、韩语、中文、日语、西班牙语、俄语、法语、德语、意大利语、葡萄牙语、荷兰语、印度尼西亚语、他加禄语或越南语。"
            await sender.send_message(interaction, send_message, error_message)
        ai_response = notion_ai.translate(language, context)
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="change_tone", description="更改上下文的语气")
    async def change_tone(interaction: discord.Interaction, *, context: str, tone: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()

        send_message = f"[change_tone] context: {context} \n tone: {tone}"
        try:
            tone = ToneEnum(tone)
        except Exception:
            error_message = "❌ Error: The tone can only be: professional, casual, straightforward, confident, or friendly."
            await sender.send_message(interaction, send_message, error_message)
        ai_response = notion_ai.change_tone(context, ToneEnum(tone))
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="summarize", description="总结上下文")
    async def summarize(interaction: discord.Interaction, *, context: str, page_title: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.summarize(context, page_title)
        send_message = f"[summarize] context: {context} \n page_title: {page_title}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="improve_writing", description="改善上下文")
    async def improve_writing(interaction: discord.Interaction, *, context: str, page_title: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.improve_writing(context, page_title)
        send_message = f"[improve_writing] context: {context} \n page_title: {page_title}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="fix_spelling_grammar", description="纠正上下文中的语法错误")
    async def fix_spelling_grammar(interaction: discord.Interaction, *, context: str, page_title: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.fix_spelling_grammar(context, page_title)
        send_message = f"[fix_spelling_grammar] context: {context} \n page_title: {page_title}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="explain_this", description="上下文解释")
    async def explain_this(interaction: discord.Interaction, *, context: str, page_title: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.explain_this(context, page_title)
        send_message = f"[explain_this] context: {context} \n page_title: {page_title}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="make_longer", description="编辑文本以使上下文更长")
    async def make_longer(interaction: discord.Interaction, *, context: str, page_title: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.make_longer(context, page_title)
        send_message = f"[make_longer] context: {context} \n page_title: {page_title}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="make_shorter", description="编辑文本以使上下文更短")
    async def make_shorter(interaction: discord.Interaction, *, context: str, page_title: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.make_shorter(context, page_title)
        send_message = f"[make_shorter] context: {context} \n page_title: {page_title}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="find_action_items", description="生成行动项")
    async def find_action_items(interaction: discord.Interaction, *, context: str, page_title: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.find_action_items(context, page_title)
        send_message = f"[find_action_items] context: {context} \n page_title: {page_title}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="simplify_language", description="简化上下文")
    async def simplify_language(interaction: discord.Interaction, *, context: str, page_title: str = ""):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.simplify_language(context, page_title)
        send_message = f"[simplify_language] context: {context} \n page_title: {page_title}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="blog_post", description="生成博客文章")
    async def blog_post(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.blog_post(prompt)
        send_message = f"[blog_post] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="brainstorm_ideas", description="生成创意")
    async def brainstorm_ideas(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.brainstorm_ideas(prompt)
        send_message = f"[brainstorm_ideas] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="outline", description="生成大纲")
    async def outline(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.outline(prompt)
        send_message = f"[outline] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="social_media_post", description="生成社交媒体帖子")
    async def social_media_post(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.social_media_post(prompt)
        send_message = f"[social_media_post] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="creative_story", description="生成创意故事")
    async def creative_story(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.creative_story(prompt)
        send_message = f"[creative_story] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="poem", description="生成诗歌")
    async def poem(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.poem(prompt)
        send_message = f"[poem] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="essay", description="生成文章")
    async def essay(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.essay(prompt)
        send_message = f"[essay] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="meeting_agenda", description="生成会议议程")
    async def meeting_agenda(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.meeting_agenda(prompt)
        send_message = f"[meeting_agenda] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="press_release", description="生成新闻稿")
    async def press_release(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.press_release(prompt)
        send_message = f"[press_release] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="job_description", description="生成工作描述")
    async def job_description(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.job_description(prompt)
        send_message = f"[job_description] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="sales_email", description="生成销售电子邮件")
    async def sales_email(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.sales_email(prompt)
        send_message = f"[sales_email] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="recruiting_email", description="生成招聘电子邮件")
    async def recruiting_email(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.recruiting_email(prompt)
        send_message = f"[recruiting_email] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    @client.tree.command(name="pros_cons_list", description="生成优缺点列表")
    async def pros_cons_list(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        ai_response = notion_ai.pros_cons_list(prompt)
        send_message = f"[pros_cons_list] prompt: {prompt}"
        await sender.send_message(interaction, send_message, ai_response)

    client.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    logger.info('Server Run')
    keep_alive()
    run()
