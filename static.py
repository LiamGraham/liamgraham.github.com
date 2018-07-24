TEMPLATE_DIR = "templates"


def get_template(name):
    """
    Returns the text of the HTML template having the given name.

    Arguments:
        name (str): name of template, excluding the file extension

    Returns (str): text of HTML template
    """
    with open(f"{TEMPLATE_DIR}\\{name}.html", "r") as f:
        return f.read()
