import asyncio

def run_async(func):
    """
    Helper function to run async functions in a synchronous context.
    
    Args:
        func: An async function to run
        
    Returns:
        The result of the async function
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(func)
    loop.close()
    return result
