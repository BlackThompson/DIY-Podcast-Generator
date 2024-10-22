archieve_gen_podcast = """
# Context
- Please generate a podcast script based on the given content with **two hosts**.
-  [host1] should be female, [host2] should be male (You can create the name by yourself).

# Rules
- Ensure the podcast discussion about the paper is **deep and comprehensive**!!!
- Generate as many rounds of conversation as possible!
- Keep each person's turn content **short**!!!
- The language should match that of native English speakers!

# Length
- The whole content should be more than 1500 words!
"""

parsed_podcast = """
- Extract the conversation from the given podcast.
- Each person's complete statement extracted as a separate string, and save them in a list in the order they occur in the podcast. 
- You only need to save the content of the conversation, not the names of the speakers!
"""

gen_podcast = """
Generate a podcast script featuring a dialogue between two hosts based on the provided content. 

# Context
- [Host 1] is a female and [Host 2] is a male. You may create their names.
- Ensure the discussion covers the content deeply and comprehensively.
- The dialogue should have multiple rounds of conversation.

# Rules
- Keep each person's turn in the conversation **short and engaging**!!!
- Use language and expressions that match native English speakers.

# Length
- The entire script must be more than 2000 words.

# Notes
- Remember to maintain a conversational flow that feels natural and engaging for listeners.
- Ensure the content depth is balanced throughout the entire script, avoiding superficial discussion.
"""
