import anthropic
from django.conf import settings

PLATFORM_GUIDANCE = {
    "twitter": "under 280 characters, punchy, 1-2 relevant hashtags",
    "instagram": "engaging caption, emoji where natural, 3-5 relevant hashtags",
    "facebook": "conversational, 2-4 sentences, no more than 1 hashtag",
    "linkedin": "professional tone, no emoji, 1 relevant hashtag",
}


class ContentGenerationError(Exception):
    """Raised when the Claude API call fails; message is safe to show the client."""


def generate_product_post(product, platform, tone, extra_instructions=""):
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    system = (
        "You write short social media posts promoting products for a small business. "
        "Return only the post text, no preamble, no quotes around it."
    )
    user_content = (
        f"Product: {product.name}\n"
        f"Brand: {product.brand or 'n/a'}\n"
        f"Category: {product.category or 'n/a'}\n"
        f"Price: {product.price}\n"
        f"Description: {product.description or 'n/a'}\n\n"
        f"Platform: {platform} ({PLATFORM_GUIDANCE[platform]})\n"
        f"Tone: {tone}\n"
    )
    if extra_instructions:
        user_content += f"Extra instructions: {extra_instructions}\n"

    try:
        response = client.messages.create(
            model="claude-opus-5",
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )
    except anthropic.AuthenticationError:
        raise ContentGenerationError("AI service is misconfigured.")
    except anthropic.RateLimitError:
        raise ContentGenerationError("AI service is rate limited, try again shortly.")
    except (anthropic.APIConnectionError, anthropic.APIStatusError):
        raise ContentGenerationError("AI service is temporarily unavailable.")

    return next(b.text for b in response.content if b.type == "text")
