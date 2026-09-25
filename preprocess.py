import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            posts_with_metadata = post | metadata
            enriched_posts.append(posts_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post["tags"]
        new_tags = {unified_tags[tag] for tag in current_tags}
        post["tags"]=list(new_tags)

    with open(processed_file_path, encoding="utf-8", mode="w") as otput_file:
        json.dump(enriched_posts, otput_file, indent=4)

def get_unified_tags(posts_with_metadata):

    template = '''I will give you a list of tags. You need to unifyy tags with the following requiremnts,
        1. Tags are unified and merged to create a shorter list.
            Example 1 : "JobSeekers", "Job Hunting" can all be meged into a single tag "Job Search".
            Example 2: "Motivation", "Inspiration", "Drive" can be mapped into "Motivation".
        
        2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
        3. Output should be JSON object. No preamble.
        4. Output be mapping of original tag and the unified tag.
            Example: {{"Jobseekers":"Job Search", "Job Hunting": "Job Search", "Motivation":"Motivation", "Inspiration":"Motivation"}}

        Here is the list of tags:
        {tags}
    '''
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ", ".join(unique_tags)

    pt = PromptTemplate.from_template(template)
    
    chain = pt | llm
    response = chain.invoke(input={'tags': str(unique_tags_list)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except:
        raise OutputParserException("context too big. Unable to parse jobs.")

    return res

def extract_metadata(post):
    template = '''
        You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
        1. Return a valid JSON. No preamble.
        2. JSON object should have exactly three keys: line_count, language and tags.
        3. tags is an array of text tags. Excract maximum 2 tags. 
        4. Language should be English, Telugu or Telgish (Telgish means Telugu + English)

        Here is the actual post on which you need to perform this task: {post}
    '''

    pt = PromptTemplate.from_template(template)

    chain = pt | llm
    response = chain.invoke(input={'post': post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except:
        raise OutputParserException("context too big. Unable to parse jobs.")

    return res

    # return {
    #     'line_count':post.count("\n")+1,
    #     'language':'English',
    #     'tags':["Study", "Motivation"]
    # }

if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")