# AWS-Blog_Generation_APP

Welcome to the AWS Blog Generation Application! This project leverages AWS services to create a blog generation application. The application uses Lambda functions to handle code execution, API Gateway to connect to other services, Bedrock API for blog generation, S3 Bucket for storing generated responses, and DynamoDB for storing user feedback, which is used to improve subsequent responses.

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

1. **Generate Blog Content**:
   - Send a request to the API Gateway endpoint to generate blog content.
   - The Lambda function will invoke the Bedrock API to generate the content.
   - The generated content will be stored in the S3 Bucket.

2. **Provide Feedback**:
   - After viewing the generated blog content, users can provide feedback.
   - The feedback will be sent to another API Gateway endpoint.
   - The Lambda function will store the feedback in DynamoDB.

3. **Refine Content Generation**:
   - Subsequent blog generation requests will incorporate user feedback stored in DynamoDB to refine and improve the content.

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
