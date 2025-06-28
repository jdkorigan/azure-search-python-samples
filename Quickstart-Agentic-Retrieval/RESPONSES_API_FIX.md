# Fix for Responses API 404 Error

## Problem
The `responses` API is a newer Azure OpenAI feature that returns a 404 error in some regions or service instances.

## Solution: Use Chat Completions API

Replace all instances of `client.responses.create()` with `client.chat.completions.create()` in your notebook.

### Before (Problematic Code):
```python
response = client.responses.create(
    model=answer_model,
    input=messages
)
wrapped = textwrap.fill(response.output_text, width=100)
```

### After (Working Code):
```python
response = client.chat.completions.create(
    model=answer_model,
    messages=messages
)
wrapped = textwrap.fill(response.choices[0].message.content, width=100)
```

## Key Changes:
1. **Method**: `client.responses.create()` → `client.chat.completions.create()`
2. **Parameter**: `input=messages` → `messages=messages`
3. **Response**: `response.output_text` → `response.choices[0].message.content`

## If You Want to Use Responses API

To use the Responses API, you need:

1. **Supported Region**: The API is only available in specific regions:
   - East US
   - West US 2
   - North Europe
   - West Europe
   - UK South
   - Australia East
   - Canada East

2. **Correct API Version**: Use `2025-03-01-preview` or later

3. **Supported Model**: Use GPT-4o, GPT-4o-mini, or other supported models

## Test Your Setup

Run the `fix_responses_api.py` script to test which API works in your environment:

```bash
python fix_responses_api.py
```

## Recommendation

Use the Chat Completions API for maximum compatibility across all Azure OpenAI regions and service instances. 