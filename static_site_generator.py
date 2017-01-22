from jinja2 import Environment, FileSystemLoader, Markup
import json
import markdown
import os
import logging

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)


def load_json_config():
    with open('config.json') as config_list:
        articles_list = json.load(config_list, encoding='UTF-8')
    return articles_list


def markdown_filter(text):
    md = markdown.Markdown(extensions=['meta'])
    return Markup(md.convert(text))


def create_jinja_environment():
    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    env.filters['markdown'] = markdown_filter
    return env


def open_markdown_article_from_file(md_article):
    with open('articles/{0}'.format(md_article['source'])) as article_file:
        article_file = article_file.read()
        return article_file


def convert_markdown_to_html(article_file):
    html_article = markdown.markdown(article_file, output_format='html5')
    return html_article


def render_article_page(html_article, title):
    rendered_article_page = article_template.render(title=title, content=html_article)
    return rendered_article_page


def write_html_article_to_file(html_article_file, html_article_path):
    with open(html_article_path, 'a+') as article_html:
        article_html.seek(0)
        article_html.truncate()
        article_html.write(html_article_file)


def convert_articles_to_html_pages(articles):
    for md_article in articles:
        html_article_path = 'site/articles/{0}.html'.format(os.path.splitext(md_article['source'])[0])
        md_article['html'] = html_article_path
        if not os.path.exists(os.path.dirname(html_article_path)):
            os.makedirs(os.path.dirname(html_article_path))
        article_file = open_markdown_article_from_file(md_article)
        html_article = convert_markdown_to_html(article_file)
        rendered_article_page = render_article_page(html_article, md_article['title'])
        write_html_article_to_file(rendered_article_page, html_article_path)


def render_index_page(articles_list):
    with open('index.html', 'w') as index:
        index.seek(0)
        index.truncate()
        index.write(index_template.render(articles=articles_list))


if __name__ == '__main__':
    articles_list = load_json_config()
    env = create_jinja_environment()
    index_template = env.get_template('/templates/index.html')
    article_template = env.get_template('/templates/article.html')
    convert_articles_to_html_pages(articles_list['articles'])
    render_index_page(articles_list)
