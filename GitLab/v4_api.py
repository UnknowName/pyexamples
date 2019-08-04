import aiohttp


class Gitlab(object):
    def __init__(self, server: str, token: str):
        self.server = server if server.startswith(("http://", "https://")) else "https://" + server
        self.headers = {"Private-Token": token}
        self.project = ProjectManager(self)


class BaseManager(object):
    def __init__(self, gitlab: Gitlab):
        self.headers = gitlab.headers
        self.server = gitlab.server
        self.session = aiohttp.ClientSession

    async def get(self, resource_id: int):
        url = "{}/{}/{}".format(self.server, self.path, resource_id)
        async with self.session() as session:
            async with session.get(url, headers=self.headers) as resp:
                return resp.headers, await resp.json()

    async def all(self):
        pass

    async def search(self):
        pass


class ProjectManager(BaseManager):
    resource = "project"
    path = "/api/v4/projects"
    attrs = (
        "pipeline"
    )


class Pipeline(object):
    async def get(self):
        pass

    async def all(self):
        pass


async def main():
    import os
    gitlab = Gitlab(os.getenv("GIT_SERVER"), os.getenv("GIT_TOKEN"))
    resp = await gitlab.project.get(37)
    print(resp)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())