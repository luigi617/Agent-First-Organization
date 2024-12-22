generate_tasks_sys_prompt = """The builder plans to create a chatbot designed to fulfill user's objectives. Given the role of the chatbot, along with any introductory information and detailed documentation (if available), your task is to identify the specific, distinct tasks that a chatbot should handle based on the user's intent. These tasks should not overlap or depend on each other and must address different aspects of the user's goals. Ensure that each task represents a unique user intent and that they can operate separately. Return the response in JSON format.

For Example:

Builder's prompt: The builder want to create a chatbot - Customer Service Assistant. The customer service assistant typically handles tasks such as answering customer inquiries, making product recommendations, assisting with orders, processing returns and exchanges, supporting billing and payments, addressing complaints, and managing customer accounts.
Builder's Information: Amazon.com is a large e-commerce platform that sells a wide variety of products, ranging from electronics to groceries.
Builder's documentations: 
https://www.amazon.com/
Holiday Deals
Disability Customer Support
Same-Day Delivery
Medical Care
Customer Service
Amazon Basics
Groceries
Prime
Buy Again
New Releases
Pharmacy
Shop By Interest
Amazon Home
Amazon Business
Subscribe & Save
Livestreams
luwanamazon's Amazon.com
Best Sellers
Household, Health & Baby Care
Sell
Gift Cards

https://www.amazon.com/bestsellers
Any Department
Amazon Devices & Accessories
Amazon Renewed
Appliances
Apps & Games
Arts, Crafts & Sewing
Audible Books & Originals
Automotive
Baby
Beauty & Personal Care
Books
Camera & Photo Products
CDs & Vinyl
Cell Phones & Accessories
Clothing, Shoes & Jewelry
Collectible Coins
Computers & Accessories
Digital Educational Resources
Digital Music
Electronics
Entertainment Collectibles
Gift Cards
Grocery & Gourmet Food
Handmade Products
Health & Household
Home & Kitchen
Industrial & Scientific
Kindle Store
Kitchen & Dining
Movies & TV
Musical Instruments
Office Products
Patio, Lawn & Garden
Pet Supplies
Software
Sports & Outdoors
Sports Collectibles
Tools & Home Improvement
Toys & Games
Unique Finds
Video Games

Reasoning Process:
Thought 1: Understand the general responsibilities of the assistant type.
Observation 1: A customer service assistant typically handles tasks such as answering customer inquiries, addressing complaints, making product recommendations, assisting with orders, processing returns and exchanges, supporting billing and payments, and managing customer accounts.

Thought 2: Based on these general tasks, identify the specific tasks relevant to this assistant, taking into account the customer's decision-making journey. Consider the typical activities customers engage in on this platform and the potential questions they might ask.
Observation 2: The customer decision-making journey includes stages like need recognition, information search, evaluating alternatives, making a purchase decision, and post-purchase behavior. On Amazon, customers log in, browse and compare products, add items to their cart, and check out. They also track orders, manage returns, and leave reviews. Therefore, the assistant would handle tasks such as product search and discovery, product inquiries, product comparison, billing and payment support, order management, and returns and exchanges.

Thought 3: Summarize the identified tasks in terms of user intent and format them into JSON.
Observation 3: Structure the output as a list of dictionaries, where each dictionary represents an intent and its corresponding task.

Answer:
```json
[
    {{
        "intent": "User want to do product search and discovery",
        "task": "Provide help in Product Search and Discovery"
    }},
    {{
        "intent": "User has product inquiry",
        "task": "Provide help in product inquiry"
    }},
    {{
        "intent": "User want to compare different products",
        "task": "Provide help in product comparison"
    }},
    {{
        "intent": "User ask for billing and payment support",
        "task": "Provide help in billing and payment support"
    }},
    {{
        "intent": "User want to manage orders",
        "task": "Provide help in order management"
    }},
    {{
        "intent": "User has request in returns and exchanges",
        "task": "Provide help in Returns and Exchanges"
    }}
]
```

Builder's prompt: The builder want to create a chatbot - {role}. {u_objective}
Builder's information: {intro}
Builder's documentations: 
{docs}
Reasoning Process:
"""


check_best_practice_sys_prompt = """You are a userful assistance to detect if the current task needs to be further decomposed if it cannot be solved by the provided resources. Specifically, the task is positioned on a tree structure and is associated with a level. Based on the task and the current node level of the task on the tree, please output Yes if it needs to be decomposed; No otherwise meaning it is a singular task that can be handled by the resource and does not require task decomposition. Please also provide explanations for your choice. 

Here are some examples:
Task: The current task is Provide help in Product Search and Discovery. The current node level of the task is 1. 
Resources: 
MessageWorker: The worker responsible for interacting with the user with predefined responses,
RAGWorker: Answer the user's questions based on the company's internal documentations, such as the policies, FAQs, and product information,
ProductWorker: Access the company's database to retrieve information about products, such as availability, pricing, and specifications,
UserProfileWorker: Access the company's database to retrieve information about the user's preferences and history

Reasoning: This task is a high-level task that involves multiple sub-tasks such as asking for user's preference, providing product recommendations, answering questions about product or policy, and confirming user selections. Each sub-task requires different worker to complete. It will use MessageWorker to ask user's preference, then use ProductWorker to search for the product, finally make use of RAGWorker to answer user's question. So, it requires multiple interactions with the user and access to various resources. Therefore, it needs to be decomposed into smaller sub-tasks to be effectively handled by the assistant.
Answer: 
```json
{{
    "answer": "Yes"
}}
```

Task: The current task is booking a broadway show ticket. The current node level of the task is 1.
Resources:
DataBaseWorker: Access the company's database to retrieve information about ticket availability, pricing, and seating options. It will handle the booking process, which including confirming the booking details and providing relevant information. It can also handle the cancel process.
MessageWorker: The worker responsible for interacting with the user with predefined responses,
RAGWorker: Answer the user's questions based on the company's internal documentations, such as the policies, FAQs, and product information.

Reasoning: This task involves a single high-level action of booking a ticket for a broadway show. The task can be completed by accessing the database to check availability, pricing, and seating options, interacting with the user to confirm the booking details, and providing relevant information. Since it is a singular task that can be handled by the single resource without further decomposition, the answer is No.
Answer: 
```json
{{
    "answer": "No"
}}
```

Task: The current task is {task}. The current node level of the task is {level}.
Resources: {resources}
Reasoning:
"""


generate_best_practice_sys_prompt = """Given the background information about the chatbot, the task it needs to handle, and the available resources, your task is to generate a step-by-step best practice for addressing this task. Each step should represent a distinct interaction with the user, where the next step builds upon the user's response. Avoid breaking down sequences of internal worker actions within a single turn into multiple steps. Return the answer in JSON format.

For example:
Background: The builder want to create a chatbot - Customer Service Assistant. The customer service assistant typically handles tasks such as answering customer inquiries, making product recommendations, assisting with orders, processing returns and exchanges, supporting billing and payments, addressing complaints, and managing customer accounts.

Task: Provide help in Product Search and Discovery

Resources:
MessageWorker: The worker responsible for interacting with the user with predefined responses,
RAGWorker: Answer the user's questions based on the company's internal documentations, such as the policies, FAQs, and product information,
ProductWorker: Access the company's database to retrieve information about products, such as availability, pricing, and specifications,
UserProfileWorker: Access the company's database to retrieve information about the user's preferences and history.

Thought: To help users find products effectively, the assistant should first get context information about the customer from CRM, such as purchase history, demographic information, preference metadata, inquire about specific preferences or requirements (e.g., brand, features, price range) specific for the request. Second, based on the user's input, the assistant should provide personalized product recommendations. Third, the assistant should ask if there is anything not meet their goals. Finally, the assistant should confirm the user's selection, provide additional information if needed, and assist with adding the product to the cart or wish list.
Answer:
```json
[
    {{
      "step": 1,
      "task": "Retrieve the information about the customer and Inquire about specific preferences or requirements (e.g., brand, features, price range)."
    }},
    {{
      "step": 2,
      "task": "Search for the products that match user's preference and provide a curated list of products that match the user's criteria."
    }},
    {{
      "step": 3,
      "task": "Ask if the user would like to see more options or has any specific preferences."
    }},
    {{
      "step": 4,
      "task": "Confirm if the user is ready to proceed with a purchase or needs more help."
    }},
    {{
      "step": 5,
      "task": "Provide instructions for completing the purchase or next steps."
    }}
]
```

Background: The builder want to create a chatbot - {role}. {u_objective}
Task: {task}
Resources: {resources}
Thought:
"""


# remove_duplicates_sys_prompt = """The builder plans to create a chatbot designed to fulfill user's objectives. Given the tasks and corresponding steps that the chatbot should handle, your task is to identify and remove any duplicate steps under each task that are already covered by other tasks. Ensure that each step is unique within the overall set of tasks and is not redundantly assigned. Return the response in JSON format.

# Tasks: {tasks}
# Answer:
# """

embed_builder_obj_sys_prompt = """The builder plans to create an assistant designed to provide services to users. Given the best practices for addressing a specific task and the builder's objectives, your task is to refine the steps to ensure they embed the objectives within each task. Return the answer in JSON format.

For example:
Best Practice: 
[
    {{
        "step": 1,
        "task": "Retrieve the information about the customer and Inquire about specific preferences or requirements (e.g., brand, features, price range)."
    }},
    {{
        "step": 2,
        "task": "Provide a curated list of products that match the user's criteria."
    }},
    {{
        "step": 3,
        "task": "Ask if the user would like to see more options or has any specific preferences."
    }},
    {{
        "step": 4,
        "task": "Confirm if the user is ready to proceed with a purchase or needs more help."
    }},
    {{
        "step": 5,
        "task": "Provide instructions for completing the purchase or next steps."
    }}
]
Build's objective: The customer service assistant helps in persuading customer to sign up the Prime membership.
Answer:
```json
[
    {{
        "step": 1,
        "task": "Retrieve the information about the customer from CRM and Inquire about specific preferences or requirements (e.g., brand, features, price range)."
    }},
    {{
        "step": 2,
        "task": "Provide a curated list of products that match the user's criteria."
    }},
    {{
        "step": 3,
        "task": "Ask if the user would like to see more options or has any specific preferences."
    }},
    {{
        "step": 4,
        "task": "Confirm if the user is ready to proceed with a purchase or needs more help."
    }},
    {{
        "step": 5,
        "task": "Persuade the user to sign up for the Prime membership."
    }}
]
```

Best Practice: {best_practice}
Build's objective: {b_objective}
Answer:
"""


embed_resources_sys_prompt = """The builder plans to create an assistant designed to provide services to users. Given the best practices for addressing a specific task, and the available resources, your task is to map the steps with the resources. The response should include the resources used for each step and example responses, if applicable. Return the answer in JSON format.

For example:
Best Practice: 
[
    {{
        "step": 1,
        "task": "Retrieve the information about the customer from CRM and Inquire about specific preferences or requirements (e.g., brand, features, price range)."
    }},
    {{
        "step": 2,
        "task": "Provide a curated list of products that match the user's criteria."
    }},
    {{
        "step": 3,
        "task": "Ask if the user would like to see more options or has any specific preferences."
    }},
    {{
        "step": 4,
        "task": "Confirm if the user is ready to proceed with a purchase or needs more help."
    }},
    {{
        "step": 5,
        "task": "Persuade the user to sign up for the Prime membership."
    }}
]
Resources:
{{
    "MessageWorker": "The worker responsible for interacting with the user with predefined responses",
    "RAGWorker": "Answer the user's questions based on the company's internal documentations, such as the policies, FAQs, and product information",
    "ProductWorker": "Access the company's database to retrieve information about products, such as availability, pricing, and specifications",
    "UserProfileWorker": "Access the company's database to retrieve information about the user's preferences and history"
}}
Answer:
```json
[
    {{
        "step": 1,
        "task": "Retrieve the information about the customer from CRM and Inquire about specific preferences or requirements (e.g., brand, features, price range)."
        "resource": "UserProfileWorker",
        "example_response": "Do you have some specific preferences or requirements for the product you are looking for?"
    }},
    {{
        "step": 2,
        "task": "Provide a curated list of products that match the user's criteria."
        "resource": "ProductWorker",
        "example_response": ""
    }},
    {{
        "step": 3,
        "task": "Ask if the user would like to see more options or has any specific preferences."
        "resource": "MessageWorker",
        "example_response": "Would you like to see more options or do you have any specific preferences?"
    }},
    {{
        "step": 4,
        "task": "Confirm if the user is ready to proceed with a purchase or needs more help."
        "resource": "MessageWorker",
        "example_response": "Are you ready to proceed with the purchase or do you need more help?"
    }},
    {{
        "step": 5,
        "task": "Persuade the user to sign up for the Prime membership."
        "resource": "MessageWorker",
        "example_response": "I noticed that you are a frequent shopper. Have you considered signing up for our Prime membership to enjoy exclusive benefits and discounts?"
    }}
]
```

Best Practice: {best_practice}
Resources: {resources}
Answer:
"""


generate_start_msg = """The builder plans to create a chatbot designed to fulfill user's objectives. Given the role of the chatbot, your task is to generate a starting message for the chatbot. Return the response in JSON format.

For Example:

Builder's prompt: The builder want to create a chatbot - Customer Service Assistant. The customer service assistant typically handles tasks such as answering customer inquiries, making product recommendations, assisting with orders, processing returns and exchanges, supporting billing and payments, addressing complaints, and managing customer accounts.
Start Message:
```json
{{
    "message": "Welcome to our Customer Service Assistant! How can I help you today?"
}}
```

Builder's prompt: The builder want to create a chatbot - {role}. {u_objective}
Start Message:
"""

generate_intent_from_task_prompt = """
The builder plans to create a chatbot designed to fulfill user's objectives. Given task name and steps of task, your task is to identify user's intent. Return the response in JSON format.

For Example:

Task name: Assist users in exploring and finding suitable Airbnb listings based on their preferences like location, date range, price, and amenities.
Task steps:
[
    "Greet the user and ask for their specific inquiry regarding purchasing or renting robots."
    "Use the RAGWorker to retrieve detailed information from the company's internal documentation about purchasing and rental options for robots.",
    "Present the retrieved information to the user, including details about pricing, terms, and conditions for both purchasing and rental options.",
    "Ask the user if they have any specific questions or need further clarification about the provided information.",
    "Based on the user's follow-up questions, use the RAGWorker again if necessary to provide additional information or clarification.",
    "Guide the user through the process of completing a transaction, if applicable, or provide contact information for further assistance if needed."
]
Answer:
```json
{{
    "message": "User seeks information about robot specifications and capabilities"
}}
```

Task name: {task_name}
Task steps:
{task_steps}
Answer:
"""



website_example = '''<html lang="en"> <head> <title> Usage of /answers [GET] - Stack Exchange API </title> <link href="https://cdn.sstatic.net/apiv2/all.css?v=01c20169aefd" rel="stylesheet"/> <script> var parameters = {"page":"number","pagesize":"number","fromdate":"date","todate":"date","order":["desc","asc"],"min":"depends","max":"depends","sort":{"activity":"date","creation":"date","votes":"number"}}; var method = "/2.3/answers"; var filterName = "default"; </script> <script> if (state && state.charAt(0) == '#') { state = state.substring(1); } // all of these parameters are set in the ConsoleParameters section $(function () { StackExchange.api.v2.console.init( parameters, method, $('#console'), filterName, filter, dependentTypes, typeof(dontRequireSite) != 'undefined',                state, filterTypeLinks, typeof (isPostMethod) != 'undefined' ? 'POST' : 'GET', false ); }); </script> </head> <body> <div class="outside header"> <div class="inside"> <div class="logo"> <a href="/"> </a> </div> </div> </div> <div class="outside content"> <div class="inside"> <div class="mainbar"> <div class="subheader"> <h1> Usage of /answers <span class="http-method" title="expects a GET HTTP method"> GET </span> </h1> </div> <h2> Discussion </h2> <div class="indented"> <p> Returns all the undeleted answers in the system. </p> <p> The sorts accepted by this method operate on the following fields of the <a href="/docs/types/answer"> answer object </a> : <code> activity </code> is the default sort. <br/> <br/> It is possible to <a href="/docs/min-max"> create moderately complex queries </a> using <code> sort </code> , <code> min </code> , <code> max </code> , <code> fromdate </code> , and <code> todate </code> . </p> <p> This method returns a list of <a href="/docs/types/answer"> answers </a> . </p> </div> <h2 style="margin-top: 30px;"> Try It </h2> <div class="console" id="console"> <div class="console-header"> <div class="console-header-left"> <div class="site"> <div class="edit-site" title="site"> <span class="current-site"> Stack Overflow </span> <a class="show-site-editor" href="#" title="edit-site"> [edit] </a> <span class="site-param" style="display: none;"> stackoverflow </span> <span class="site-url" style="display:none;"> https://stackoverflow.com </span> </div> <div class="site-editor"> <input class="site-picker" type="text"/> </div> </div> <span class="access-token-url" style="display:none"> https://stackoverflow.com/oauth/dialog?client_id=1&amp;key=U4DMV*8nvpm3EOpvf69Rxw((&amp; </span> <span class="app-key" style="display:none"> U4DMV*8nvpm3EOpvf69Rxw(( </span> <span class="scope" style="display:none"> </span> <span class="method-type" style="display:none"> </span> <span class="req-url"> </span> </div> <div class="console-header-right"> <div class="permalink"> <a href="#"> link </a> </div> <div class="console-header-separator"> </div> <div class="filter-link"> <div class="edit-filter" title="filter"> <span class="current-filter"> default </span> filter <a class="expand-filter-popup" href="#" title="edit filter"> [edit] ▼ </a> </div> <div class="editing-filter"> <input class="manual-filter" type="text"/> filter <a class="collapse-filter-popup" href="#"> ▲ </a> </div> </div> </div> <br style="clear: both;"> </br> </div> <div class="popup-container"> <div class="permalink-popup"> <input type="text"/> </div> <div class="filter-popup"> <div class="filter-content"> <div class="filter-vis"> </div> <a class="filter-invis-link" href="#"> show [n] types not returned by /answers GET </a> <div class="filter-invis"> </div> <div class="unsafe-container"> <input class="filter-unsafe" id="filter-unsafe" name="unsafe" type="checkbox"/> <label for="filter-unsafe"> make unsafe <a href="/docs/filters" target="_blank"> (?) </a> </label> </div> </div> <div class="filter-controls"> <div class="filter-controls-left"> <a class="filter-unselect-all" href="#"> unselect all </a> </div> <div class="filter-controls-right"> <a class="filter-cancel" href="#"> cancel </a> </div> </div> </div> </div> <div class="parameters"> </div> <div class="fetched-url"> </div> <div class="run-button-container"> </div> <br style="clear: both;"> <div class="result"> <pre class="prettyprint lang-js"><code></code></pre> </div> </br> </div> </div> <div class="sidebar"> <div class="module help"> <div class="mobile-nav"> Navigation <span class="mobile-nav-arrow"> </span> </div> <div class="help-list"> </div> </div> </div> </div> <div class="bottom"> <div class="bottom-wrapper"> </div> </div> </div> <div class="outside footer"> <!-- StackOverflow.Api.V2 2024.12.6.44935 --> <div class="inside"> <p class="footer-links"> <a href="https://stackexchange.com/about"> about </a> <a href="https://stackoverflow.blog"> blog </a> <a href="https://stackexchange.com/legal/api-terms-of-use"> terms of use </a> <a href="/cdn-cgi/l/email-protection#bcc8d9ddd197ddccd5fccfc8dddfd7d9c4dfd4ddd2dbd992dfd3d1"> contact us </a> <a href="http://stackapps.com/"> feedback always welcome </a> </p> <p style="margin-bottom: 0;"> site design / logo © 2024 Stack Exchange, Inc; user contributions licensed under <a href="https://stackoverflow.com/help/licensing" rel="license"> CC BY-SA </a> </p> </div> <br style="clear: both;"/> </div> <script> $(function() { $(".mobile-nav").on("click", function() { $(".help-list").toggleClass("active"); }); }); </script> </body> </html>'''
extract_info_from_api_doc_prompt = """
Given a extracted html api documentation website, your task is to extract the api url, the description of the api, and what are its available parameters and values that the parameters can have and the format.

For Example:
Extracted html api documentation website:
""" + website_example + """
Answer:
```json
{{
    "description": "Returns all the undeleted answers in the system.",
    "parameters": "page (number): Specifies the page of results to retrieve. pagesize (number): Defines the number of results per page. fromdate (date): The start date from which to retrieve answers, given in UNIX timestamp format. todate (date): The end date up to which to retrieve answers, given in UNIX timestamp format. order (array of "desc" or "asc"): Specifies the order of results; can either be descending ("desc") or ascending ("asc"). min (depends): This parameter is used for specifying a minimum value filter for specific fields, such as votes. max (depends): This parameter is used for specifying a maximum value filter for specific fields, such as votes. sort (object): Defines the sorting criteria. The options for sorting are: activity: Sort by activity date. creation: Sort by creation date. votes: Sort by number of votes."
    "api_url": "/2.3/answers"
}}
```

Extracted html api documentation website:
"""