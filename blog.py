from os import listdir, path, makedirs
from shutil import rmtree
from dataclasses import dataclass
import static


# Paths for blog, blog post text, and template directories.
BLOG_DIR = "blog"
TEXT_DIR = "blog\\_text"

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
    post = static.get_template("post")

    full_name = path.splitext(text_name)[0].split("-")
    date = full_name[0:3]
    file_name = f"{'-'.join(full_name[3:])}.html"
    title, content = format_content(text)

    post = post.replace("{ POST_TITLE }", title)
    post = post.replace("{ POST_DATE }", "/".join(date))
    post = post.replace("{ POST_CONTENT }", content)

    date_path = "\\".join(date)
    post_dir = f"{BLOG_DIR}\\{date_path}"
    file_dir = f"{post_dir}\\{file_name}"
    if not path.exists(post_dir):
        makedirs(post_dir)

    with open(file_dir, "w") as f:
        f.write(post)
    return BlogPost(title, "/".join(date), content, file_dir)


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
    Creates a static HTML file for the 'Blog' page from which blog posts can be
    accessed.
    
    Arguments:
        posts (list(BlogPost)): all blog posts to be included in page   
    """
    blog = static.get_template("blog")
    post_list = ""
    # Reverse posts to descending date order (most to least recent)
    posts.reverse()

    if not posts:
        post_list = "<li>No posts</li>"
    for x in posts:
        post_list += f"<li><a href='{x.directory}'>{x.date} - {x.title}</a></li>\n"

    blog = blog.replace("{ POST_LIST }", post_list)

    with open("blog.html", "w") as f:
        f.write(blog)


def get_post_content(text_name):
    """
    Returns the content of the blog post text having the given name.

    Arguments: 
        text_name (str): name of blog post text
    
    Returns (str): content of target blog post text
    """
    with open(f"{TEXT_DIR}\\{text_name}", "r") as f:
        return f.read()


def clear_blog_directory():
    dirs = listdir(BLOG_DIR)
    exclude = [TEXT_DIR.split("\\")[-1]]
    for x in dirs:
        if x in exclude:
            continue
        rmtree(f"{BLOG_DIR}\\{x}")


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
    clear_blog_directory()
    post_names = get_text_names()
    posts = []
    for name in post_names:
        posts.append(write_post_static(name))
    write_blog_static(posts)
