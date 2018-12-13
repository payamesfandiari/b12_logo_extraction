from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from logo_extractor.db import *
import click
import json

@click.group()
@click.option('--debug/--no-debug',default=False)
@click.pass_context
def main(ctx,debug):
    ctx.obj['DEBUG'] = debug


def parse_and_load(urls):
    """
    Get the list of urls and parse them one by one.
    :param urls: A list of urls in string format
    :return: None
    """
    create_tables()
    db.connect(reuse_if_open=True)
    process = CrawlerProcess(get_project_settings())
    process.crawl('logo',urls=urls)
    process.start()
    db.close()


def return_logos():
    """
    Dumps the data stored in the DB
    :return: a list of tuples, the first element is URL and the second element is LOGO URL
    """
    db.connect(reuse_if_open=True)
    query = Logo.select()
    out = []
    for logo in query:
        out.append((logo.web_url,logo.logo_url))
    db.close()
    return out


def parse_and_return(urls):
    """
    Gets a list of urls as input. Finds the Logos and push them into DB then returns a list of tuples
    :param urls: A list of urls
    :return: a list of tuples, the first element is URL and the second element is LOGO URL
    """
    parse_and_load(urls)
    return return_logos()


@main.command()
@click.argument('f',type=click.Path(exists=True),required=True)
@click.pass_context
def get_urls(ctx,f):
    """
    Gets the file name from the user and run the parser on it.
    :param f: the input file
    """
    DEBUG = ctx.obj['DEBUG']
    if DEBUG:
        click.echo('Reading the files...')
    with open(f) as urls_file :
        temp = urls_file.readlines()
    urls = [x.split(',')[0] for x in temp]
    parse_and_load(urls)


@main.command()
@click.option('--format-json',default=False,is_flag=True)
@click.pass_context
def dump_data(ctx,format_json):
    """
    Dumps data into the terminal
    """
    DEBUG = ctx.obj['DEBUG']
    if DEBUG:
        click.echo('Reading the DB...')
    out = return_logos()
    if format_json:
        click.echo(json.dumps(out))
    else:
        click.echo(out)

@main.command()
@click.argument('f',type=click.Path(exists=True),required=True)
@click.option('--format-json',default=False,is_flag=True)
@click.pass_context
def parse_dump(ctx,f,format_json):
    """
    Find logo in urls and return the urls
    """
    DEBUG = ctx.obj['DEBUG']
    if DEBUG:
        click.echo('Parsing the URLS...')
    with open(f) as urls_file:
        temp = urls_file.readlines()
    urls = [x.split(',')[0] for x in temp]
    out = parse_and_return(urls)
    if format_json:
        click.echo(json.dumps(out))
    else:
        click.echo(out)




if __name__ == '__main__':
    main(obj={})

#
# if __name__ == '__main__':
#     """
#     This is the main entry point to the application
#
#     """
#     with open("urls.txt") as urls_file :
#         temp = urls_file.readlines()
#     urls = [x.split(',')[0] for x in temp]
#     create_tables()
#     db.connect(reuse_if_open=True)
#     process = CrawlerProcess(get_project_settings())
#     process.crawl('logo',urls=urls)
#     process.start()
#     db.close()
