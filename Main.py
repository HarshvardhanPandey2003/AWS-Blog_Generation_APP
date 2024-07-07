import boto3
import botocore.config
import json
from datetime import datetime
import re
import uuid

import re

def blog_generate_using_bedrock(topics: list, word_count: int, tone: str, target_audience: str) -> str:
    topics_str = ", ".join(topics)
    prompt = f"""Write a coherent and well-structured blog post on the following topics: {topics_str}. 
    The blog should be approximately {word_count} words long. 
    Use a {tone} tone and target the {target_audience} audience.
    Ensure smooth transitions between topics.
    
    Format the blog post as follows:
    1. Start with a title enclosed in ** (e.g., **Title**)
    2. Include an introduction
    3. Have 2-3 main sections with subheadings
    4. End with a conclusion
    
    Do not include any instructions or notes about proofreading in the final output."""

    body = {
        "prompt": prompt,
        "max_gen_len": min(2048, word_count * 4),  # Increased for longer posts
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    try:
        bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1",
                               config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))
        response = bedrock.invoke_model(body=json.dumps(body), modelId="meta.llama3-8b-instruct-v1:0")
        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        blog_details = response_data['generation']
        
        # Clean the output
        cleaned_blog = re.sub(r'\[/INST\]', '', blog_details)
        cleaned_blog = re.sub(r'Proofread for grammar and spelling errors\.', '', cleaned_blog)
        cleaned_blog = re.sub(r'\s+', ' ', cleaned_blog)
        cleaned_blog = cleaned_blog.strip()
        
        # Add proper line breaks for formatting
        cleaned_blog = re.sub(r'\*\*(.*?)\*\*', r'\n\n**\1**\n', cleaned_blog)  # Add line breaks around titles
        cleaned_blog = re.sub(r'([.!?])\s+', r'\1\n', cleaned_blog)  # Add single line break after sentences
        cleaned_blog = re.sub(r'\n{3,}', '\n\n', cleaned_blog)  # Replace multiple line breaks with double line break
        cleaned_blog = cleaned_blog.strip()
        
        return cleaned_blog
    except Exception as e:
        print(f"Error generating the blog: {e}")
        raise

def save_blog_details_s3(s3_key, s3_bucket, generate_blog):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog)
        print("Blog saved to S3")
    except Exception as e:
        print(f"Error when saving the blog to S3: {e}")

def save_feedback(blog_id, rating, feedback):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BlogFeedback')
    
    try:
        response = table.put_item(
            Item={
                'blog_id': blog_id,
                'rating': rating,
                'feedback': feedback,
                'timestamp': datetime.now().isoformat()
            }
        )
        return response
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return None

def lambda_handler(event, context):
    try:
        event_body = json.loads(event['body'])
        
        # Check if this is a feedback submission
        if 'feedback' in event_body:
            blog_id = event_body['blog_id']
            rating = event_body['rating']
            feedback = event_body['feedback']
            
            feedback_response = save_feedback(blog_id, rating, feedback)
            if feedback_response:
                return {
                    'statusCode': 200,
                    'body': json.dumps('Feedback submitted successfully')
                }
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps('Failed to submit feedback')
                }
        
        # If not feedback, proceed with blog generation
        topics = event_body['topics']
        word_count = event_body.get('word_count', 500)
        tone = event_body.get('tone', 'neutral')
        target_audience = event_body.get('target_audience', 'general')

        generate_blog = blog_generate_using_bedrock(topics, word_count, tone, target_audience)
        
        if generate_blog:
            blog_id = str(uuid.uuid4())  # Generate a unique ID for the blog
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            s3_key = f"blog-output/{blog_id}_{current_time}.txt"
            s3_bucket = 'bloggenerated'
            save_blog_details_s3(s3_key, s3_bucket, generate_blog)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Blog Generation is completed',
                    'blog_id': blog_id,
                    'blog_content': generate_blog,
                    's3_location': f"s3://{s3_bucket}/{s3_key}"
                })
            }
        else:
            print("No blog was generated")
            return {
                'statusCode': 400,
                'body': json.dumps('Failed to generate blog')
            }
    except KeyError as e:
        print(f"KeyError: {e}. Event structure: {event}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Missing required key: {str(e)}')
        }
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }