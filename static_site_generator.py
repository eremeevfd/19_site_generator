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


def convert_articles_to_html(articles):
    for article in articles:
        html_article_path = 'site/articles/{0}.html'.format(os.path.splitext(article['source'])[0])
        article['html'] = html_article_path
        logger.info(os.path.dirname(html_article_path))
        if not os.path.exists(os.path.dirname(html_article_path)):
            os.makedirs(os.path.dirname(html_article_path))
        logger.info(article)
        logger.info(html_article_path)
        title = article['title']
        # if not (os.path.exists(html_article_path)):
        with open('articles/{0}'.format(article['source'])) as article_file:
            article = article_file.read()
            html = markdown.markdown(article, output_format='html5')
            doc = article_template.render(title=title, content=html)
        with open(html_article_path, 'a+') as article_html:
            article_html.seek(0)
            article_html.truncate()
            article_html.write(doc)

def render_index():
    with open('index.html', 'w') as index:
        index.seek(0)
        index.truncate()
        index.write(template.render(articles=articles_list))


def convert_markdown_to_html(article_in_markdown):
    pass


if __name__ == '__main__':
    articles_list = load_json_config()
    logger.info(articles_list)
    env = Environment(loader=FileSystemLoader('.'))
    md = markdown.Markdown(extensions=['meta'])
    env.filters['markdown'] = lambda text: Markup(md.convert(text))
    template = env.get_template('/templates/index.html')
    extensions = ['markdown', 'smartypants']
    article_template = env.get_template('/templates/article.html')
    convert_articles_to_html(articles_list['articles'])
    render_index()
