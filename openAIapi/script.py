response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=100,
  
    # Enter your prompt
    messages=[{"role": "user", "content": "How can I get Open AI API Key?"}]
)

print(response.choices[0].message.content)


# To obtain an OpenAI API key, follow these steps:

# 1. **Sign Up:** Go to the [OpenAI website](https://www.openai.com/) and sign up for an account if you don't already have one.

# 2. **Log In:** After creating an account, log in to the OpenAI platform.

# 3. **API Dashboard:** Navigate to the API section or the dashboard. This is often found in the user account menu or as a dedicated link on the website.

4.