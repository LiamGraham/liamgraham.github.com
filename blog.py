from os import listdir, path, makedirs
from shutil import rmtree
from dataclasses import dataclass

# Paths for blog, blog post text, and template directories.
BLOG_DIR = "blog"
TEXT_DIR = "blog\\_text"
TEMPLATE_DIR = "templates"


def get_text_names():
    """
    Get names of all blog post text files.

    Returns (list(str)): names of all blog post text files
    """
    text_names = listdir(TEXT_DIR)
    return text_names


def write_post_static(text_name):
    """
    Creates a static HTML file for the blog post having the given text name.

    Arguments:
        text_name: name of the blog post text file

    Returns (BlogPost): blog post object
    """
    text = get_post_content(text_name)
    static = get_template("post")

    full_name = path.splitext(text_name)[0].split("-")
    date = full_name[0:3]
    file_name = f"{'-'.join(full_name[3:])}.html"
    title, content = format_content(text)

    static = static.replace("{ POST_TITLE }", title)
    static = static.replace("{ POST_DATE }", "-".join(date))
    static = static.replace("{ POST_CONTENT }", content)

    date_path = "\\".join(date)
    post_dir = f"{BLOG_DIR}\\{date_path}"
    if not path.exists(post_dir):
        makedirs(post_dir)

    with open(f"{post_dir}\\{file_name}", "w") as f:
        f.write(static)
    return BlogPost(title, date, content, post_dir)


def format_content(text):
    """
    Returns the given text formatted for display on a webpage. Paragraph tags are
    inserted so that paragraph breaks are retained. 

    Arguments:
        text (str): text to be formatted

    Returns (str): formatted text
    """
    content = ""
    paragraph = ""
    title = ""
    lines = text.split("\n")
    title = lines.pop(0)
    for x in lines:
        line = x.strip()
        if line:
            paragraph += line
        else:
            content += f"<p>{paragraph}</p>"
            paragraph = ""
    return title, content


def write_blog_static(posts):
    """


    """
    static = get_template("blog")
    post_list = ""

    for x in posts:
        post_list += f"<li><a href='{x.directory}'>{x.date} - {x.title}</a></li>\n"
    static = static.replace("{ POST_LIST }", post_list)

    with open("blog.html", "w") as f:
        f.write(static)


def get_post_content(text_name):
    """
    Returns the content of the blog post text having the given name.

    Arguments: 
        text_name (str): name of blog post text
    
    Returns (str): content of target blog post text
    """
    with open(f"{TEXT_DIR}\\{post_name}", "r") as f:
        return f.read()


def get_template(name):
    """
    Returns the text of the HTML template having the given name.

    Arguments:
        name (str): name of template, excluding the file extension

    Returns (str): text of HTML template
    """
    with open(f"{TEMPLATE_DIR}\\{name}.html", "r") as f:
        return f.read()


@dataclass
class BlogPost:
    """
    Data class storing all blog post data.
    """
    title: str
    date: str
    content: str
    directory: str


if __name__ == "__main__":
    post_names = get_text_names()
    posts = []
    for name in post_names:
        posts.append(write_post_static(name))
    write_blog_static(posts)
