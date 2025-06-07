# AWS-Blog_Generation_APP

Welcome to the AWS Blog Generation Application! This project leverages AWS services to create a blog generation application. The application uses Lambda functions to handle code execution, API Gateway to connect to other services, Bedrock API for blog generation, S3 Bucket for storing generated responses, and DynamoDB for storing user feedback, which is used to improve subsequent responses.
![image](https://github.com/user-attachments/assets/0ab75fdd-d1f5-4cd1-8ec0-b90986395585)


## Features

- Generate blog content using Bedrock API
- Store generated content in AWS S3 Bucket
- Collect user feedback on generated content
- Store feedback in DynamoDB
- Use feedback to improve future blog content generation

## Table of Contents

- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Architecture

1. **API Gateway**: Connects client requests to Lambda functions.
2. **Lambda Functions**: 
   - Handle blog generation requests.
   - Store generated blogs in S3.
   - Collect and store feedback in DynamoDB.
   - Use feedback to refine future responses.
3. **Bedrock API**: Generates blog content.
4. **S3 Bucket**: Stores generated blog content.
5. **DynamoDB**: Stores user feedback.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/HarshvardhanPandey2003/AWS-Blog_Generation_APP.git
    ```

2. Navigate to the project directory:
    ```sh
    cd AWS-Blog_Generation_APP
    ```

3. Set up your AWS environment by configuring your credentials.

4. Deploy the Lambda functions using AWS SAM or the Serverless Framework.

5. Set up API Gateway to route requests to your Lambda functions.

6. Create an S3 Bucket to store generated blog content.

7. Create a DynamoDB table to store user feedback.

## Usage


---

**1. The Frontend: Streamlit Interface**
The user journey begins at the Streamlit web application. Its role is simple but crucial:

* **Collect Input**: It provides a user-friendly interface with text boxes and buttons for a user to specify their blog request (e.g., topics, desired tone).
* **Initiate Request**: When the user clicks "submit," the Streamlit application packages this information into the body of an HTTP POST request and sends it to a specific URL. This URL is the endpoint provided by Amazon API Gateway.

---

**2. Amazon API Gateway: The Secure Front Door**
The HTTP request from your frontend doesn't go directly to your code. Instead, it's received by Amazon API Gateway, which acts as a managed and secure entry point for your entire backend.

* **Role and Function**: API Gateway is designed to create, publish, and secure APIs at any scale. It handles tasks like traffic management, authorization, and monitoring, allowing your Lambda functions to focus solely on their business logic.
* **Routing Logic**: This is where the separation of concerns begins. You will configure two distinct routes (or "resources") in API Gateway:

  * `POST /blogs`: This route is set up to listen for requests to create a new blog. It triggers the `generate_blog_lambda` function.
  * `POST /feedback`: This route listens for feedback submissions and triggers the `submit_feedback_lambda` function.
* **Data Transformation**: API Gateway takes the incoming HTTP request and transforms it into a JSON event object that Lambda can understand. This object contains everything about the request, including the headers, path, and the request body (the user's input).

---

**3. Lambda Function 1: The Blog Generator (`generate_blog_lambda`)**
This function is a specialized worker whose only job is to create blog posts.

* **Trigger**: It is invoked synchronously by the `POST /blogs` route in API Gateway. Synchronous invocation means API Gateway waits for this function to finish and return a response.
* **Execution Process**:

  * The Lambda function starts, receiving the event object from API Gateway.
  * It parses the `event['body']` to extract the topics, word count, and other parameters.
  * It constructs a detailed prompt and uses the AWS SDK (boto3) to call the Amazon Bedrock API.
  * Once Bedrock returns the generated text, the function performs any necessary cleaning or formatting.
  * It then calls the S3 API to save the final blog post into an S3 bucket for permanent storage.
  * Finally, it constructs a JSON response object with `statusCode: 200` and a body containing the blog content. This response is sent back to API Gateway, which then relays it to the user's browser.

---

**4. Lambda Function 2: The Feedback Collector (`submit_feedback_lambda`)**
This second function is another specialized worker, focused entirely on processing user feedback.

* **Trigger**: It is invoked synchronously by the `POST /feedback` route in API Gateway.
* **Execution Process**:

  * The function starts upon receiving the event object from the feedback submission.
  * It parses the `event['body']` to get the `blog_id`, rating, and feedback comments.
  * It connects to your DynamoDB table using the AWS SDK.
  * It executes a `PutItem` operation, saving the feedback as a new item in the table, indexed by the `blog_id` and a timestamp.
  * It returns a simple success message (e.g., `{'statusCode': 200, 'body': 'Feedback received!'}`) back to API Gateway, confirming the submission.

---

**5. The Feedback Loop: How Feedback Improves Future Responses**
Your final point describes the feedback loop, which is a critical feature. However, having the feedback Lambda directly trigger the blog generation Lambda is an **architectural anti-pattern** that creates tight coupling and complexity.

* **No Direct Invocation**: The Feedback Lambda’s job ends when it successfully writes the data to DynamoDB. It does **not** call the Blog Generation Lambda. The two functions remain completely independent.
* **Data-Driven Improvement**: The "intelligence" is added to the Blog Generation Lambda. The next time a user requests a blog on a similar topic, your `generate_blog_lambda` can be enhanced to:

  * Before calling Bedrock, perform an optional query to the DynamoDB feedback table.
  * Look for high-rated or low-rated feedback associated with the current request's topics or user ID.
  * Use this retrieved feedback to dynamically adjust the prompt sent to Bedrock. For example, it might add a line like, **"Previously, feedback indicated the tone was too formal. Please use a more conversational tone for this post."**

---




## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit your Changes (`git commit -m 'Add some YourFeature'`)
4. Push to the Branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Harshvardhan Pandey - (mailto:harshvardhanpandey2003@gmail.com)

Project Link: [https://github.com/HarshvardhanPandey2003/AWS-Blog_Generation_APP](https://github.com/HarshvardhanPandey2003/AWS-Blog_Generation_APP)

---

Thank you for using the AWS Blog Generation Application! We hope it meets your needs. If you have any questions or feedback, feel free to reach out.
