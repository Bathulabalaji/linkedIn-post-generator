from llm_helper import llm
from few_shot import FewShotPosts

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "5 to 10 lines"
    else:
        return "more than 10 lines"

def get_prompt(tag, length, language):
    length_str = get_length_str(length)
    fs = FewShotPosts()
    posts_examples = fs.get_posts(tag, length, language)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}

    If language is Telgish then it means it is a mix of Telugu and English. 
    If the Topic is ECET, ECET is a Englineering Common Entrance Test in Andhra Pradesh and Telangana.
    The script for the generated post should always be in English only.
    If required add emojies also for better engagement.
    '''

    if len(posts_examples)>0:
        prompt+="4) Use writing style as per the following examples."
        for i, post in enumerate(posts_examples):
            post_text = post["text"]
            prompt += f"\n\n Example {i+1} \n\n {post_text}"
            if i==1:
                break
    print(prompt)
    return prompt

def generate_post(tag, length, language):
    prompt = get_prompt(tag, length, language)    
    response = llm.invoke(prompt)
    return response.content