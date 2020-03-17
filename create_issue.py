import asyncio
import os
import aiohttp
from gidgetlab.aiohttp import GitLabAPI

async def main():
    async with aiohttp.ClientSession() as session:
        gl = GitLabAPI(session, "andreasevers", access_token=os.getenv("GL_ACCESS_TOKEN"))
        await gl.post(
            "/projects/5724649/issues",
            data={
                "title": "We got a problem",
                "description": "Use more emoji!",
            })

loop = asyncio.get_event_loop()
loop.run_until_complete(main())