todos_post_response = {
    "id": "3",
    "title": "Post new object",
    "doneStatus": "false",
    "description": "",
}
todos_post_response_xml = """\
<todo>
    <doneStatus>false</doneStatus>
    <description/>
    <id>3</id>
    <title>Post new object</title>
</todo>"""

todos_post_response_xml_bad = """\
<todo>
    <doneStatus>false
    <description/>
    <id>3
    <title>Post new object
</todo>"""

todos_post_data = {"title": "Post new object"}
todos_post_data_bad = {"title Post new object"}

newtitle_bad = "{title: new title}"

todos_id_tasksof_data_xml = """\
<projects>
        <active>false</active>
        <description/>
        <id>1</id>
        <completed>false</completed>
        <title>Office Work</title>
        <tasks>
            <id>2</id>
        </tasks>
        <tasks>
            <id>1</id>
        </tasks>
</projects>"""

todos_id_tasksof_data_xml_bad = """<projects><active>false</active><description/><id>1</id><completed>false</completed><title>Office 
Work</title><tasks><id>2</id></tasks><tasks><id>1</id></tasks></projects>"""
