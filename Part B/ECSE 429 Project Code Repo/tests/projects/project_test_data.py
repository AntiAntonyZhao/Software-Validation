project_create_json = {
    "title": "sometitle",
    "completed": True,
    "active": False,  # todo this is a bug from docs
    "description": "some description",
}
project_create_bool_as_string = {
    "title": "sometitle",
    "completed": "True",
    "active": "False",
    "description": "some description",
}

project_create_xml = """\
<project>
    <active>true</active>
    <description>t enim ad minim veni</description>
    <id>1</id>
    <completed>true</completed>
    <title>incididunt ut labora</title>
</project>
"""

project_create_xml_invalid_id = """\
<project>
    <active>true</active>
    <description>t enim ad minim veni</description>
    <id>100</id>
    <completed>true</completed>
    <title>incididunt ut labora</title>
</project>
"""

project_create_xml_null_id = """\
<project>
    <active>true</active>
    <description>t enim ad minim veni</description>
    <id>null</id>
    <completed>true</completed>
    <title>incididunt ut labora</title>
</project>
"""
