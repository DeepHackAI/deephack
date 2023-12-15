import openai
import os

openai.api_key = "OPENAI_API_KEY"

# Call ChatGPT API with prompt
def call_GPT(prompt):
    completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
    )

    # Parse results and print them out
    chat_response = completion.choices[0].message.content
    md_print(f'User: {prompt}')
    md_print(f'GPT: {chat_response}')

# Define
call_GPT(prompt="Write an essay explaining what AI is.")


# Summarization prompt

summarize_prompt="""
It is very rare for snow to fall in the U.S. state of Florida, especially in the central and southern portions of the state. With the exception of the far northern areas of the state, most of the major cities in Florida have never recorded measurable snowfall, though trace amounts have been recorded, or flurries in the air observed few times each century. According to the National Weather Service, in the Florida Keys and Key West there is no known occurrence of snow flurries since the European colonization of the region more than 300 years ago. In Miami, Fort Lauderdale, and Palm Beach there has been only one known report of snow flurries observed in the air in more than 200 years; this occurred in January 1977. In any event, Miami, Fort Lauderdale, and Palm Beach have not seen snow flurries before or since this 1977 event.

Summarize this paragraph in a single sentence:
"""

call_GPT(summarize_prompt)


# Name Parsing Instructions
instruction_prompt_example1 ="""
A user has input their first and last name into a form. We don't know in which order
their first/last name is, but we need it to be in the format 'Last, First'. Convert the following:

john doe
"""

call_GPT(instruction_prompt_example1)

# Personally Identifiable Information Removal Instructions
instruction_prompt_example2 ="""
Read the following sales email. Remove any personally identifiable information (PII),
and replace it with the appropriate placeholder. For example, replace the name "John Doe"
with "[NAME]".

Hi John,

I'm writing to you because I noticed you recently purchased a new car. I'm a salesperson
at a local dealership (Cheap Dealz), and I wanted to let you know that we have a great deal on a new
car. If you're interested, please let me know.

Thanks,

Jimmy Smith

Phone: 410-805-2345
Email: jimmysmith@cheapdealz.com
"""

call_GPT(instruction_prompt_example2)

# Essay Evaluation and Feedback Instructions
instruction_prompt_example3 ="""
Read the following excerpt from an essay and provide feedback based on the following criteria: grammar, clarity, coherence, argument quality, and use of evidence. Provide a score from 1-10 for each attribute, along with reasoning for your score.

"Despite the popular belief, there's no solid evidence supporting the idea that video games lead to violent behavior. Research on the topic is often contradictory and inconclusive. Some studies found a correlation, but correlation don't imply causation. So, it's premature to blame video games for violence in society."
"""

call_GPT(instruction_prompt_example3)

# Role Prompting
role_prompt_example4 ="""
You are a brilliant mathematician who can solve any problem in the world.
Attempt to solve the following problem:

What is (100*100)/(400*56)?
"""

call_GPT(role_prompt_example4)

# Structure Output
role_prompt_example5 ="""
In the bustling town of Emerald Hills, a diverse group of individuals made their mark. Sarah Martinez, a dedicated nurse, was known for her compassionate care at the local hospital. David Thompson, an innovative software engineer, worked tirelessly on groundbreaking projects that would revolutionize the tech industry. Meanwhile, Emily Nakamura, a talented artist and muralist, painted vibrant and thought-provoking pieces that adorned the walls of buildings and galleries alike. Lastly, Michael O'Connell, an ambitious entrepreneur, opened a unique, eco-friendly cafe that quickly became the town's favorite meeting spot. Each of these individuals contributed to the rich tapestry of the Emerald Hills community.
1. Sarah Martinez [NURSE]
2. David Thompson [SOFTWARE ENGINEER]
3. Emily Nakamura [ARTIST]
4. Michael O'Connell [ENTREPRENEUR]

At the heart of the town, Chef Oliver Hamilton has transformed the culinary scene with his farm-to-table restaurant, Green Plate. Oliver's dedication to sourcing local, organic ingredients has earned the establishment rave reviews from food critics and locals alike.

Just down the street, you'll find the Riverside Grove Library, where head librarian Elizabeth Chen has worked diligently to create a welcoming and inclusive space for all. Her efforts to expand the library's offerings and establish reading programs for children have had a significant impact on the town's literacy rates.

As you stroll through the charming town square, you'll be captivated by the beautiful murals adorning the walls. These masterpieces are the work of renowned artist, Isabella Torres, whose talent for capturing the essence of Riverside Grove has brought the town to life.

Riverside Grove's athletic achievements are also worth noting, thanks to former Olympic swimmer-turned-coach, Marcus Jenkins. Marcus has used his experience and passion to train the town's youth, leading the Riverside Grove Swim Team to several regional championships.
1. Oliver Hamilton [CHEF]
2. Elizabeth Chen [LIBRARIAN]
3. Isabella Torres [ARTIST]
4. Marcus Jenkins [COACH]

Oak Valley, a charming small town, is home to a remarkable trio of individuals whose skills and dedication have left a lasting impact on the community.

At the town's bustling farmer's market, you'll find Laura Simmons, a passionate organic farmer known for her delicious and sustainably grown produce. Her dedication to promoting healthy eating has inspired the town to embrace a more eco-conscious lifestyle.

In Oak Valley's community center, Kevin Alvarez, a skilled dance instructor, has brought the joy of movement to people of all ages. His inclusive dance classes have fostered a sense of unity and self-expression among residents, enriching the local arts scene.

Lastly, Rachel O'Connor, a tireless volunteer, dedicates her time to various charitable initiatives. Her commitment to improving the lives of others has been instrumental in creating a strong sense of community within Oak Valley.

Through their unique talents and unwavering dedication, Laura, Kevin, and Rachel have woven themselves into the fabric of Oak Valley, helping to create a vibrant and thriving small town.
"""

call_GPT(role_prompt_example5)

# Zero-shot prompting
role_prompt_example6 ="""
Add 2+2:
"""

call_GPT(role_prompt_example6)

# One-shot prompting
role_prompt_example7 ="""
Add 3+3: 6
Add 2+2:
"""

call_GPT(role_prompt_example7)

# A prompt including context, instructions, and multiple examples
combined_prompt ="""
Twitter is a social media platform where users can post short messages called "tweets".
Tweets can be positive or negative, and we would like to be able to classify tweets as
positive or negative. Here are some examples of positive and negative tweets. Make sure
to classify the last tweet correctly.

Q: Tweet: "What a beautiful day!"
Is this tweet positive or negative?

A: positive

Q: Tweet: "I hate this class"
Is this tweet positive or negative?

A: negative

Q: Tweet: "I love pockets on jeans"

A:
"""

call_GPT(combined_prompt)

# Formalizing Prompting
# Complex prompt example 1
# role, instruction, context
complex_prompt_example1 ="""
You are a doctor. Read this medical history and predict risks for the patient:

January 1, 2000: Fractured right arm playing basketball. Treated with a cast.
February 15, 2010: Diagnosed with hypertension. Prescribed lisinopril.
September 10, 2015: Developed pneumonia. Treated with antibiotics and recovered fully.
March 1, 2022: Sustained a concussion in a car accident. Admitted to the hospital and monitored for 24 hours.
"""

call_GPT(complex_prompt_example1)