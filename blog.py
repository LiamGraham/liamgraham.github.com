from os import listdir, path

BLOG_DIR = "blog"
TEXT_DIR = "blog\\_text"
TEMPLATE_DIR = "templates\\post.html"


def get_posts():
    post_names = listdir(TEXT_DIR)
    return post_names


def write_static(post_name):
    text = get_post_content(post_name)
    static = get_template()

    name = path.splitext(post_name)[0]

    content = ""
    paragraph = ""
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            content += f"<p>{paragraph}</p>"
            paragraph = ""
        else:
            paragraph += line

    static = static.replace("{POST_TITLE}", name)
    static = static.replace("{POST_DATE}", "2018-07-18")
    static = static.replace("{POST_CONTENT}", content)
    
    with open(f"{BLOG_DIR}\\{name}.html", "w") as f:
        f.write(static)


def write_list():
    pass


def get_post_content(post_name):
    with open(f"{TEXT_DIR}\\{post_name}", "r") as f:
        return f.read()


def get_template():
    with open(TEMPLATE_DIR, "r") as f:
        return f.read()


if __name__ == "__main__":
    post_names = get_posts()
    for name in post_names:
        write_static(name)
    write_list()
