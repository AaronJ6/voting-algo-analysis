from streamlit.components.v1 import html

def confirm(message, func):
    confirm_script = """
        <script type="text/javascript">
            window.confirm("%s") && %s();
        </script>
    """ % (message, func)
    html(confirm_script)