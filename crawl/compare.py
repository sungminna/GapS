from utils import find_diff

async def compare_and_report():
    anthropic = await find_diff('legacy/anthropic_pricing_data.md', 'dump/anthropic_pricing_data.md')
    aws_stability =await find_diff('legacy/aws_pricing_data_stability.md', 'dump/aws_pricing_data_stability.md')
    aws_titan =await find_diff('legacy/aws_pricing_data_titan.md', 'dump/aws_pricing_data_titan.md')
    azure_east =await find_diff('legacy/azure_pricing_data_east.md', 'dump/azure_pricing_data_east.md')
    azure_north =await find_diff('legacy/azure_pricing_data_north.md', 'dump/azure_pricing_data_north.md')
    gemini =await find_diff('legacy/gemini_pricing_data.md', 'dump/gemini_pricing_data.md')
    openai =await find_diff('legacy/openai_pricing_data.md', 'dump/openai_pricing_data.md')
    perplexity =await find_diff('legacy/perplexity_pricing_data.md', 'dump/perplexity_pricing_data.md')
    vertex =await find_diff('legacy/vertex_pricing_data.md', 'dump/vertex_pricing_data.md')

    print(anthropic)
    print(aws_stability)
    print(aws_titan)
    print(azure_east)
    print(azure_north)
    print(gemini)
    print(openai)
    print(perplexity)
    print(vertex)
