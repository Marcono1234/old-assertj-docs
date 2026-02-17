import os.path
import string
import glob


def content_of(filename):
    with open("./template-data/" + filename) as file_to_read:
        return file_to_read.read()

print (" ")
print ("Generate assertj HTML files")

# stores it into a map for later substitution
template_data_map = {
    'menu': content_of('assertj-top-menu.html'),
    'head': content_of('assertj-head.html'),
    'footer': content_of('assertj-footer.html'),
    'javascript': content_of('assertj-javascript.html'),
    'assertj_core_side_menu': content_of('assertj-core-side-menu.html'),
    'assertj_swing_danger_two_robots': content_of('assertj-swing-danger-two-robots.html'),
    'assertj_swing_get_it': content_of('assertj-swing-get-it.html'),
    'assertj_swing_name': "AssertJ Swing",
    'assertj_swing_sample_with_base_test': content_of('assertj-swing-sample-with-base-test.html'),
    'assertj_swing_sample_without_base_test': content_of('assertj-swing-sample-without-base-test.html'),
    'assertj_swing_side_menu': content_of('assertj-swing-side-menu.html'),
    'assertj_news_side_menu': content_of('assertj-news-side-menu.html'),
    'assertj_guava_side_menu': content_of('assertj-guava-side-menu.html'),
    'assertj_neo4j_side_menu': content_of('assertj-neo4j-side-menu.html'),
    'assertj_db_side_menu': content_of('assertj-db-side-menu.html'),
    'assertj_jodatime_side_menu': content_of('assertj-joda-time-side-menu.html'),
    'assertj_assertions_generator_side_menu': content_of('assertj-assertions-generator-side-menu.html')
}

def new_doc_url_for_file(file_name):
    if file_name.startswith("assertj-core") or file_name.startswith("assertj-news"):
        return "https://assertj.github.io/doc/"
    if file_name.startswith("assertj-db"):
        return "https://assertj.github.io/doc/#assertj-db"
    if file_name.startswith("assertj-guava"):
        return "https://assertj.github.io/doc/#assertj-guava"
    if file_name.startswith("assertj-joda-time"):
        return "https://assertj.github.io/doc/#assertj-joda"
    if file_name.startswith("assertj-neo4j"):
        # TODO: Documentation for Neo4j is currently empty on new site
        # return "https://assertj.github.io/doc/#assertj-neo4j"
        return None
    if file_name.startswith("assertj-swing"):
        # TODO: Documentation on this old site here is more extensive; don't link to new one yet
        # return "https://assertj.github.io/doc/#assertj-swing"
        return None
    if file_name.startswith("assertj-assertions-generator"):
        # TODO: Documentation does not exist on new site yet
        return None

    # TODO: Only enable this once all documentation has been migrated to new site; see TODOs above
    # return "https://assertj.github.io/doc/"
    return None

initial_dir = os.getcwd()
templates_dir = "templates"
os.chdir(templates_dir)

for template_file_name in glob.glob("*-template.html"):
    target_file_name = '../' + template_file_name.replace('-template.html', '.html')
    print ("-- generate " + target_file_name + " from " + template_file_name)
    # open the file and read content
    template_file_path = os.path.join(os.path.dirname(__file__), template_file_name)
    with open(template_file_path) as index_template_file:
        target_file_name_content = string.Template(index_template_file.read())

    template_data_map_for_file = template_data_map.copy()
    new_doc_url = new_doc_url_for_file(template_file_name)
    # add canonical link to redirect search engines to new page, see
    # https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
    canonical_link = "" if new_doc_url is None else f'<link rel="canonical" href="{new_doc_url}" />'
    template_data_map_for_file["head"] = template_data_map_for_file["head"].replace("$canonical_link", canonical_link)

    # resolve template variables
    target_file_name_content = target_file_name_content.safe_substitute(template_data_map_for_file)

    with open(target_file_name, "w") as target_file:
        target_file.write(target_file_name_content)

os.chdir(initial_dir)
